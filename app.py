from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Import your logic handlers
from workflows.client_intake import handle_intake_workflow
from workflows.doc_checker import handle_doc_checker
#from workflows.finance_dd import handle_financial_dd

app = Flask(__name__)
def get_access_token():
    url = "https://accounts.zoho.com/oauth/v2/token"
    params = {
        "refresh_token": os.getenv("ZOHO_REFRESH_TOKEN"),
        "client_id": os.getenv("ZOHO_CLIENT_ID"),
        "client_secret": os.getenv("ZOHO_CLIENT_SECRET"),
        "grant_type": "refresh_token"
    }

    response = requests.post(url, params=params)
    data = response.json()

    if "access_token" in data:
        return data["access_token"]
    else:
        print("❌ Failed to get access token:", data)
        return None
@app.route('/webhook/contentsnare', methods=['POST'])
def contentsnare_webhook():
    data = request.json

    # Step 1: Intake
    intake_result = handle_intake_workflow(data)

    # Step 2: Document Check
    doc_status = handle_doc_checker(data)

    # Step 3: If financial docs found, run DD
    dd_result = None
    if doc_status.get("has_financials"):
        dd_result = handle_financial_dd(data)

    return jsonify({
        "intake": intake_result,
        "doc_status": doc_status,
        "dd": dd_result or "Skipped"
    }), 200


@app.route("/", methods=["GET"])
def health_check():
    return "✅ Flask is running!", 200


if __name__ == "__main__":
    app.run(port=8000)
