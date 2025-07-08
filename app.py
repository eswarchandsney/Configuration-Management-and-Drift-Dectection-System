import streamlit as st
import json
import os
from config_drift_manager import ConfigDriftManager

CONFIG_PATHS = {
    "development": "./configs/dev.yaml",
    "staging": "./configs/staging.yaml",
    "production": "./configs/prod.yaml"
}

st.title("⚙️ Configuration Drift Dashboard")

if st.button("Run Drift Detection"):
    manager = ConfigDriftManager(CONFIG_PATHS)
    result = manager.run()

    st.success("Drift detection completed.")
    st.json(result)

    if result["drifts_detected"]:
        for drift in result["drifts_detected"]:
            st.subheader(f"Drift in {drift['environment']}")
            for diff in drift["differences"]:
                st.markdown(f"- **{diff['path']}**: {diff['issue']}")
                if "reference_value" in diff:
                    st.text(f"  Reference: {diff['reference_value']}")
                if "target_value" in diff:
                    st.text(f"  Target: {diff['target_value']}")
    else:
        st.info("✅ No configuration drift detected.")

if os.path.exists("drift_report.json"):
    with open("drift_report.json") as f:
        drift_data = json.load(f)
    st.sidebar.download_button("📥 Download Report (JSON)", json.dumps(drift_data, indent=2), file_name="drift_report.json")
