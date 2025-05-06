# SmartSnare-Automator
An intelligent Flask-based automation system that connects ContentSnare webhooks to a complete CRM workflow—handling client intake, document validation, financial due diligence, reminders, internal alerts, and LP assignment using AI. Built for Zoho CRM.

file structure layout:
/hfs_flask_app/
├── app.py
├── .env
├── requirements.txt
├── /workflows/
│   ├── client_intake.py
│   ├── doc_checker.py
│   ├── finance_dd.py
│   ├── internal_notification.py
│   ├── reminders.py
│   └── lp_assignment.py
