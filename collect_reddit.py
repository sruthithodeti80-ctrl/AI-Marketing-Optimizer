import os
import praw
import pandas as pd
from dotenv import load_dotenv
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

# ==============================================================
# 1️⃣ Load environment variables
# ==============================================================
load_dotenv()

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")

GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
GOOGLE_CREDENTIALS_FILE = os.getenv("GOOGLE_SHEETS_CREDENTIALS", "credentials.json")

# ==============================================================
# 2️⃣ Initialize Reddit client
# ==============================================================
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT,
)

# ==============================================================
# 3️⃣ Fetch posts from subreddit
# ==============================================================
def fetch_reddit_posts(subreddit_name="marketing", limit=50):
    print(f"📥 Fetching {limit} posts from r/{subreddit_name}...")
    subreddit = reddit.subreddit(subreddit_name)
    rows = [["platform", "post_id", "title", "score", "comments", "url"]]

    for post in subreddit.hot(limit=limit):
        rows.append([
            "Reddit",
            post.id,
            post.title,
            post.score,
            post.num_comments,
            f"https://www.reddit.com{post.permalink}"
        ])

    print(f"✅ Fetched {len(rows)-1} posts.")
    return rows

# ==============================================================
# 4️⃣ Ensure "Reddit" Sheet Exists
# ==============================================================
def ensure_reddit_sheet_exists(service):
    spreadsheet = service.spreadsheets().get(spreadsheetId=GOOGLE_SHEET_ID).execute()
    sheet_titles = [s["properties"]["title"] for s in spreadsheet.get("sheets", [])]

    if "Reddit" not in sheet_titles:
        print("🆕 'Reddit' sheet not found — creating one...")
        add_sheet_request = {
            "requests": [
                {"addSheet": {"properties": {"title": "Reddit"}}}
            ]
        }
        service.spreadsheets().batchUpdate(
            spreadsheetId=GOOGLE_SHEET_ID,
            body=add_sheet_request
        ).execute()
        print("✅ 'Reddit' sheet created successfully!")
    else:
        print("📄 'Reddit' sheet already exists — using it.")

# ==============================================================
# 5️⃣ Write data to Google Sheets
# ==============================================================
def write_to_sheets(data, sheet_range="Reddit!A1"):
    creds = Credentials.from_service_account_file(
        GOOGLE_CREDENTIALS_FILE, scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    service = build("sheets", "v4", credentials=creds)

    # ✅ Ensure the Reddit sheet exists
    ensure_reddit_sheet_exists(service)

    # 🧹 (Optional) Clear old data before writing
    service.spreadsheets().values().clear(
        spreadsheetId=GOOGLE_SHEET_ID,
        range="Reddit!A1:Z1000"
    ).execute()

    # 📝 Write new data
    service.spreadsheets().values().update(
        spreadsheetId=GOOGLE_SHEET_ID,
        range=sheet_range,
        valueInputOption="RAW",
        body={"values": data}
    ).execute()

    print(f"✅ Uploaded {len(data) - 1} Reddit rows to Google Sheets!")

# ==============================================================
# 6️⃣ Main Execution
# ==============================================================
def main():
    posts = fetch_reddit_posts("marketing", limit=50)
    if len(posts) > 1:
        write_to_sheets(posts, sheet_range="Reddit!A1")
    else:
        print("⚠️ No posts found to upload.")

if __name__ == "__main__":
    main()
