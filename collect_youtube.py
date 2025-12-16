import os
import requests
from dotenv import load_dotenv
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

# ==============================================================
# 1️⃣ Load environment variables
# ==============================================================
load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
GOOGLE_CREDENTIALS_FILE = os.getenv("GOOGLE_SHEETS_CREDENTIALS", "credentials.json")

# Example YouTube channel (you can replace with your target channel)
CHANNEL_ID = "UC_x5XG1OV2P6uZZ5FSM9Ttw"  # Google Developers channel

# ==============================================================
# 2️⃣ Fetch latest videos from YouTube
# ==============================================================
def fetch_videos(channel_id, max_results=5):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "key": YOUTUBE_API_KEY,
        "channelId": channel_id,
        "part": "snippet",
        "order": "date",
        "maxResults": max_results,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json().get("items", [])

def fetch_video_stats(video_id):
    url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        "key": YOUTUBE_API_KEY,
        "id": video_id,
        "part": "statistics,snippet",
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json().get("items", [])
    return data[0] if data else None

# ==============================================================
# 3️⃣ Write results to Google Sheets
# ==============================================================
def write_to_sheets(data, sheet_range="Sheet1!A1"):
    creds = Credentials.from_service_account_file(
        GOOGLE_CREDENTIALS_FILE, scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()

    body = {"values": data}
    result = (
        sheet.values()
        .append(
            spreadsheetId=GOOGLE_SHEET_ID,
            range=sheet_range,
            valueInputOption="RAW",
            insertDataOption="INSERT_ROWS",
            body=body,
        )
        .execute()
    )
    print(f"✅ Uploaded {len(data) - 1} YouTube rows to Google Sheet!")

# ==============================================================
# 4️⃣ Main Execution
# ==============================================================
def main():
    print("Fetching YouTube data...")
    videos = fetch_videos(CHANNEL_ID, max_results=10)

    rows = [["platform", "video_id", "title", "views", "likes", "comments"]]

    for v in videos:
        if "videoId" not in v["id"]:
            continue
        vid = v["id"]["videoId"]
        details = fetch_video_stats(vid)
        if not details:
            continue

        stats = details.get("statistics", {})
        snippet = details.get("snippet", {})

        rows.append([
            "YouTube",
            vid,
            snippet.get("title", "N/A"),
            stats.get("viewCount", 0),
            stats.get("likeCount", 0),
            stats.get("commentCount", 0)
        ])

    if len(rows) > 1:
        write_to_sheets(rows)
    else:
        print("⚠️ No YouTube videos found.")

if __name__ == "__main__":
    main()