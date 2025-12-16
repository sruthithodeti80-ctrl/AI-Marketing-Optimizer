# ============================================================
# 💬 Slack Notification Module (Milestones 1–3)
# ============================================================

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

# ============================================================
# 🧩 Basic Slack Alert (Used for new content notifications)
# ============================================================

def send_slack_alert(message: str):
    """
    Sends a simple text alert to the configured Slack channel.
    """
    if not SLACK_WEBHOOK_URL:
        print("❌ Slack webhook URL not found in environment.")
        return

    payload = {"text": message}
    response = requests.post(SLACK_WEBHOOK_URL, json=payload)

    if response.status_code == 200:
        print("✅ Sent Slack alert successfully.")
    else:
        print(f"❌ Failed to send Slack message: {response.text}")


# ============================================================
# 🧩 Milestone 3: Send Performance Metrics Report
# ============================================================

def send_performance_alert(metrics: dict):
    """
    Sends a formatted performance summary to Slack.
    Example input:
        {
            "Topic": "AI Marketing",
            "Views": 3200,
            "Likes": 420,
            "Shares": 120,
            "Date": "2025-11-11 15:00"
        }
    """

    if not SLACK_WEBHOOK_URL:
        print("❌ Slack webhook URL missing.")
        return

    # Format the Slack message nicely
    message = (
        f"📊 *Performance Report*\n"
        f"• *Topic:* {metrics.get('Topic', 'N/A')}\n"
        f"• *Views:* {metrics.get('Views', 0)} 👀\n"
        f"• *Likes:* {metrics.get('Likes', 0)} ❤️\n"
        f"• *Shares:* {metrics.get('Shares', 0)} 🔁\n"
        f"• *Generated On:* {metrics.get('Date', '')}"
    )

    payload = {"text": message}
    response = requests.post(SLACK_WEBHOOK_URL, json=payload)

    if response.status_code == 200:
        print("✅ Sent Slack performance alert successfully.")
    else:
        print(f"❌ Failed to send performance Slack message: {response.text}")


# ============================================================
# 🧩 Optional: Rich Slack Block Message (Bonus - Advanced Format)
# ============================================================

def send_block_message(title: str, content: str):
    """
    Sends a rich-formatted Slack message using block kit (optional).
    You can use this to send structured updates later.
    """
    if not SLACK_WEBHOOK_URL:
        print("❌ Slack webhook URL not found.")
        return

    payload = {
        "blocks": [
            {"type": "header", "text": {"type": "plain_text", "text": f"📢 {title}"}},
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": content}
            },
            {"type": "divider"}
        ]
    }

    response = requests.post(SLACK_WEBHOOK_URL, json=payload)

    if response.status_code == 200:
        print("✅ Sent block message successfully.")
    else:
        print(f"❌ Failed to send block message: {response.text}")


# ============================================================
# 🧩 Test Run
# ============================================================

if __name__ == "__main__":
    # 1️⃣ Simple test alert
    send_slack_alert("🚀 Test message from AI Marketing Optimizer Slack Bot!")

    # 2️⃣ Performance report test
    test_metrics = {
        "Topic": "AI-powered Marketing",
        "Views": 4500,
        "Likes": 820,
        "Shares": 300,
        "Date": "2025-11-11 15:45:00"
    }
    send_performance_alert(test_metrics)
