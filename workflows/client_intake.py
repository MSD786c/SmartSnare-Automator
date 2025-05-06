import os
import requests
from dotenv import load_dotenv
import urllib.parse
load_dotenv()

ZOHO_CLIENT_ID = os.getenv("ZOHO_CLIENT_ID")
ZOHO_CLIENT_SECRET = os.getenv("ZOHO_CLIENT_SECRET")
ZOHO_REFRESH_TOKEN = os.getenv("ZOHO_REFRESH_TOKEN")

def get_access_token():
    url = "https://accounts.zoho.com/oauth/v2/token"
    params = {
        "refresh_token": ZOHO_REFRESH_TOKEN,
        "client_id": ZOHO_CLIENT_ID,
        "client_secret": ZOHO_CLIENT_SECRET,
        "grant_type": "refresh_token"
    }
    response = requests.post(url, params=params)
    return response.json().get("access_token")

def find_zoho_deal_by_name(deal_name):
    import urllib.parse
    token = get_access_token()
    headers = {"Authorization": f"Zoho-oauthtoken {token}"}

    encoded_name = urllib.parse.quote(deal_name)
    search_url = f"https://www.zohoapis.com/crm/v2/Deals/search?criteria=(Deal_Name:equals:{encoded_name})"

    print("🔍 Zoho Search URL:", search_url)

    res = requests.get(search_url, headers=headers)
    print("📥 Zoho Response:", res.json())  # Debug print

    deals = res.json().get("data", [])

    if not deals:
        # Try partial match as fallback
        partial_url = f"https://www.zohoapis.com/crm/v2/Deals/search?criteria=(Deal_Name:contains:{encoded_name})"
        print("🕵️ Fallback Partial Match URL:", partial_url)

        res = requests.get(partial_url, headers=headers)
        print("📥 Fallback Response:", res.json())
        deals = res.json().get("data", [])

    return deals[0]["id"] if deals else None



def add_note_to_deal(deal_id, note):
    token = get_access_token()
    headers = {
        "Authorization": f"Zoho-oauthtoken {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "data": [{
            "Note_Title": "ContentSnare Submission Summary",
            "Note_Content": note
        }]
    }
    note_url = f"https://www.zohoapis.com/crm/v2/Deals/{deal_id}/Notes"
    response = requests.post(note_url, headers=headers, json=payload)
    return response.json()

def handle_intake_workflow(data):
    """
    Parses ContentSnare data and adds a summary note to Zoho CRM deal by Deal_Name
    """
    full_name = data.get("Full_Name")
    email = data.get("Email")
    phone = data.get("Phone")
    company = data.get("Client_Type", "Unknown")
    funding_reason = data.get("Funding_Reason", "N/A")

    summary_note = (
        f"📌 New Submission from ContentSnare:\n\n"
        f"• Name: {full_name}\n"
        f"• Email: {email}\n"
        f"• Phone: {phone}\n"
        f"• Company Type: {company}\n"
        f"• Funding Reason: {funding_reason}"
    )

    deal_id = find_zoho_deal_by_name(full_name)
    if not deal_id:
        return {"status": "failed", "reason": "No matching Zoho deal found"}

    note_response = add_note_to_deal(deal_id, summary_note)
    return {"status": "success", "note_response": note_response}
