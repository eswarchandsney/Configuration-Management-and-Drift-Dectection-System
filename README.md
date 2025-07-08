# Configuration-Management-and-Drift-Dectection-System
🛠️ Configuration Management and Drift Detection System
A system to detect and correct configuration drift across development, staging, and production environments. Built with Python and Streamlit, it offers both CLI and web-based visualization for configuration consistency checks.

🔗 Live Demo: https://configuration-management-and-drift-dectection-system.streamlit.app/

💡 Features
🔍 Detects drift across environments (dev, staging, prod)

✅ Automated and manual correction options

📊 Streamlit dashboard to review and apply fixes

📤 Export drift reports to JSON and CSV

🔁 Configuration rollback via backups

🧪 Modular, testable architecture

📁 Project Structure
perl
Copy
Edit
config-drift-system/
├── app.py                      # Streamlit frontend
├── config_drift_manager.py    # Main logic
├── configs/                   # Environment config files (YAML/JSON)
├── config_backups/            # Auto-created backups
├── requirements.txt           # Dependencies
├── README.md
🚀 How to Run Locally
Clone the repo

bash
Copy
Edit
git clone https://github.com/eswarchandsney/Configuration-Management-and-Drift-Dectection-System.git
cd Configuration-Management-and-Drift-Dectection-System
Create a virtual environment and install requirements

bash
Copy
Edit
python -m venv venv
venv\Scripts\activate  # On Windows
pip install -r requirements.txt
Run the app

bash
Copy
Edit
streamlit run app.py
🧪 Example Config Files (configs/)
dev.yaml

staging.yaml

prod.yaml

You can edit these files to simulate configuration drift and observe the app's detection and correction features.

📦 Generate requirements.txt
If missing, generate it with:

bash
Copy
Edit
pip freeze > requirements.txt
🧠 Tech Stack
Python

Streamlit

YAML / JSON

Logging & Hashing

Git & GitHub

📬 Contact
For issues or contributions, feel free to raise an Issue or submit a Pull Request.
