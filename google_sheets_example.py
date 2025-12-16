# ============================================================
# 📊 Google Sheets Integration (Milestones 1–3)
# Handles:
#   - Upload sample CSV (Milestone 1)
#   - Create 'AI_Optimization' tab for content (Milestone 2)
#   - Create 'PerformanceMetrics' tab for engagement data (Milestone 3)
# ============================================================

import os
import pandas as pd
from googleapiclient.discovery import build
from google.oauth2 import service_account
from dotenv import load_dotenv

# ============================================================
# 🔹 Load environment variables
# ============================================================
load_dotenv()

SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
CRED_PATH = os.getenv("GOOGLE_SHEETS_CREDENTIALS", "credentials.json")

print(f"Using Sheet ID: {SHEET_ID}")
print(f"Using Credentials: {CRED_PATH}")

# ============================================================
# 🔹 Authenticate Google Sheets API
# ============================================================
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
creds = service_account.Credentials.from_service_account_file(CRED_PATH, scopes=SCOPES)
service = build("sheets", "v4", credentials=creds)

# ============================================================
# 🧩 Milestone 1: Upload CSV Data to main Sheet
# ============================================================
csv_file = "sample_data.csv"
if os.path.exists(csv_file):
    df = pd.read_csv(csv_file)
    if not df.empty:
        values = [df.columns.tolist()] + df.values.tolist()
        try:
            service.spreadsheets().values().clear(
                spreadsheetId=SHEET_ID,
                range="Sheet1!A1"
            ).execute()

            service.spreadsheets().values().update(
                spreadsheetId=SHEET_ID,
                range="Sheet1!A1",
                valueInputOption="RAW",
                body={"values": values}
            ).execute()

            print(f"✅ Uploaded {len(df)} rows from sample_data.csv to Google Sheets (Sheet1).")
        except Exception as e:
            print("❌ Error uploading data:", e)
    else:
        print("⚠️ sample_data.csv is empty — no tweets to upload.")
else:
    print("⚠️ sample_data.csv not found. Skipping upload step.")

# ============================================================
# 🧩 Helper Function: Ensure a tab exists with headers
# ============================================================

def ensure_tab_exists(tab_name: str, headers: list):
    """
    Check if the given tab exists in the spreadsheet.
    If not, create it and add the specified headers.
    """
    try:
        sheet_metadata = service.spreadsheets().get(spreadsheetId=SHEET_ID).execute()
        sheet_titles = [s["properties"]["title"] for s in sheet_metadata.get("sheets", [])]

        # Create the tab if not present
        if tab_name not in sheet_titles:
            print(f"🧾 Creating new sheet tab: '{tab_name}' ...")
            requests = [{
                "addSheet": {"properties": {"title": tab_name}}
            }]
            service.spreadsheets().batchUpdate(
                spreadsheetId=SHEET_ID, body={"requests": requests}
            ).execute()

            # Add header row
            service.spreadsheets().values().update(
                spreadsheetId=SHEET_ID,
                range=f"{tab_name}!A1",
                valueInputOption="RAW",
                body={"values": [headers]}
            ).execute()

            print(f"✅ Created tab '{tab_name}' with headers: {headers}")
        else:
            print(f"✅ Tab '{tab_name}' already exists.")
    except Exception as e:
        print(f"❌ Error checking or creating tab '{tab_name}': {e}")

# ============================================================
# 🧩 Milestone 2: Append AI-generated Content
# ============================================================

def update_sheet(sheet_name: str, data_row: list):
    """
    Appends a row (Topic, Generated Content, Optimized Content, Sentiment)
    to the 'AI_Optimization' tab.
    Automatically ensures tab and headers exist.
    """
    try:
        headers = ["Topic", "Generated Content", "Optimized Content", "Sentiment"]
        ensure_tab_exists(sheet_name, headers)

        body = {"values": [data_row]}
        service.spreadsheets().values().append(
            spreadsheetId=SHEET_ID,
            range=f"{sheet_name}!A1",
            valueInputOption="RAW",
            insertDataOption="INSERT_ROWS",
            body=body
        ).execute()

        print(f"📊 Added new row to '{sheet_name}': {data_row}")

    except Exception as e:
        print(f"❌ Error appending row to '{sheet_name}': {e}")

# ============================================================
# 🧩 Milestone 3: Log Performance Metrics
# ============================================================

def log_performance_metrics(data_row: list, sheet_name="PerformanceMetrics"):
    """
    Appends a single row of metrics:
    [Date, Topic, Views, Likes, Shares]
    Creates the 'PerformanceMetrics' tab if missing.
    """
    try:
        headers = ["Date", "Topic", "Views", "Likes", "Shares"]
        ensure_tab_exists(sheet_name, headers)

        body = {"values": [data_row]}
        service.spreadsheets().values().append(
            spreadsheetId=SHEET_ID,
            range=f"{sheet_name}!A1",
            valueInputOption="RAW",
            insertDataOption="INSERT_ROWS",
            body=body
        ).execute()

        print(f"📈 Logged performance metrics to '{sheet_name}': {data_row}")

    except Exception as e:
        print(f"❌ Error logging performance metrics: {e}")
