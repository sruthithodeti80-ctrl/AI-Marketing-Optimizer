# ============================================================
# Add AB_Testing Tab Headers to Google Sheets
# ============================================================

import os
from googleapiclient.discovery import build
from google.oauth2 import service_account
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
CRED_PATH = os.getenv("GOOGLE_SHEETS_CREDENTIALS", "credentials.json")

# Authenticate
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
creds = service_account.Credentials.from_service_account_file(CRED_PATH, scopes=SCOPES)
service = build("sheets", "v4", credentials=creds)

# Define the headers for AB_Testing tab
headers = [
    "Timestamp",
    "Topic",
    "Variant ID",
    "Tone",
    "Sentiment",
    "Views",
    "Likes",
    "Shares",
    "Engagement Rate",
    "Winner"
]

# Clear and add headers to AB_Testing tab
try:
    # Clear the first row
    service.spreadsheets().values().clear(
        spreadsheetId=SHEET_ID,
        range="AB_Testing!A1:J1"
    ).execute()
    
    # Add headers
    service.spreadsheets().values().update(
        spreadsheetId=SHEET_ID,
        range="AB_Testing!A1",
        valueInputOption="RAW",
        body={"values": [headers]}
    ).execute()
    
    print("✅ AB_Testing tab headers added successfully!")
    print(f"Headers: {headers}")
except Exception as e:
    print(f"❌ Error: {e}")
