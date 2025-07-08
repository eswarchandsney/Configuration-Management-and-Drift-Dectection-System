import yaml
import json
import os
import hashlib
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ConfigScanner:
    def __init__(self, config_paths: Dict[str, str]):
        self.config_paths = config_paths
        self.configs: Dict[str, Dict] = {}

    def load_config(self, env: str) -> Optional[Dict]:
        try:
            path = self.config_paths.get(env)
            if not path or not os.path.exists(path):
                logger.error(f"Config file not found for {env}: {path}")
                return None

            with open(path, 'r') as f:
                if path.endswith('.yaml') or path.endswith('.yml'):
                    config = yaml.safe_load(f)
                elif path.endswith('.json'):
                    config = json.load(f)
                else:
                    logger.error(f"Unsupported file format for {env}: {path}")
                    return None

            self.configs[env] = config
            logger.info(f"Successfully loaded config for {env}")
            return config
        except Exception as e:
            logger.error(f"Error loading config for {env}: {str(e)}")
            return None

    def scan_all(self) -> Dict[str, Dict]:
        for env in self.config_paths:
            self.load_config(env)
        return self.configs


class DriftDetector:
    def __init__(self, reference_env: str = "production"):
        self.reference_env = reference_env

    def generate_config_hash(self, config: Dict) -> str:
        config_str = json.dumps(config, sort_keys=True)
        return hashlib.sha256(config_str.encode()).hexdigest()

    def detect_drift(self, configs: Dict[str, Dict]) -> List[Dict]:
        reference_config = configs.get(self.reference_env)
        drifts = []
        if not reference_config:
            logger.error(f"Reference configuration '{self.reference_env}' not found.")
            return []

        for env, config in configs.items():
            if env == self.reference_env:
                continue

            diff = self._compare_configs(reference_config, config)
            if diff:
                drifts.append({
                    "environment": env,
                    "differences": diff,
                    "hash_mismatch": self.generate_config_hash(reference_config) != self.generate_config_hash(config)
                })
                logger.info(f"Drift detected in {env}")

        return drifts

    def _compare_configs(self, ref_config: Dict, target_config: Dict) -> List[Dict]:
        differences = []

        def compare_dicts(ref: Dict, target: Dict, path: str = ""):
            for key in set(ref.keys()) | set(target.keys()):
                new_path = f"{path}.{key}" if path else key

                if key not in ref:
                    differences.append({"path": new_path, "issue": "missing_in_reference", "value": target[key]})
                elif key not in target:
                    differences.append({"path": new_path, "issue": "missing_in_target", "value": ref[key]})
                elif isinstance(ref[key], dict) and isinstance(target[key], dict):
                    compare_dicts(ref[key], target[key], new_path)
                elif ref[key] != target[key]:
                    differences.append({
                        "path": new_path,
                        "issue": "value_mismatch",
                        "reference_value": ref[key],
                        "target_value": target[key]
                    })

        compare_dicts(ref_config, target_config)
        return differences


class ConfigDriftManager:
    def __init__(self, config_paths: Dict[str, str]):
        self.scanner = ConfigScanner(config_paths)
        self.detector = DriftDetector()
        self.config_paths = config_paths

    def run(self) -> Dict[str, Any]:
        result = {
            "status": "success",
            "scanned_configs": 0,
            "drifts_detected": []
        }

        configs = self.scanner.scan_all()
        result["scanned_configs"] = len(configs)

        drifts = self.detector.detect_drift(configs)
        result["drifts_detected"] = drifts

        with open("drift_report.json", "w") as jf:
            json.dump(result, jf, indent=2)

        return result


if __name__ == "__main__":
    config_paths = {
        "development": "./configs/dev.yaml",
        "staging": "./configs/staging.yaml",
        "production": "./configs/prod.yaml"
    }

    manager = ConfigDriftManager(config_paths)
    output = manager.run()
    print(json.dumps(output, indent=2))
