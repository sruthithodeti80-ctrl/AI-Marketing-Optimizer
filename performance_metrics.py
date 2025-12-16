# ============================================================
# 📊 performance_metrics.py — Milestone 3 (Fixed)
# ============================================================

import random
from datetime import datetime
from google_sheets_example import log_performance_metrics as write_to_sheet

# ============================================================
# 🔹 Step 1: Generate Simulated Metrics
# ============================================================

def generate_performance_metrics(topic):
    """
    Simulate engagement metrics for the generated content.
    Returns a dictionary with engagement data.
    """
    metrics = {
        "Topic": topic,
        "Views": random.randint(1000, 5000),
        "Likes": random.randint(100, 1000),
        "Shares": random.randint(50, 500),
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    return metrics


# ============================================================
# 🔹 Step 2: Log Metrics to Google Sheet
# ============================================================

def log_performance_metrics(data_row):
    """
    Logs performance metrics (Date, Topic, Views, Likes, Shares)
    into the 'PerformanceMetrics' tab in Google Sheets.
    """
    try:
        write_to_sheet(data_row)  # ✅ call the sheet logger, not itself
        print(f"✅ Logged metrics successfully: {data_row}")
    except Exception as e:
        print(f"❌ Error while logging performance metrics: {e}")


# ============================================================
# 🔹 Step 3: Direct Test (Optional)
# ============================================================

if __name__ == "__main__":
    print("🧪 Testing performance metrics generation...")
    topic = "AI Education Reform"
    metrics = generate_performance_metrics(topic)
    print("✅ Generated metrics:", metrics)
    print("🗂️ Logging metrics to Google Sheet...")
    log_performance_metrics([
        metrics["Date"],
        metrics["Topic"],
        metrics["Views"],
        metrics["Likes"],
        metrics["Shares"]
    ])
