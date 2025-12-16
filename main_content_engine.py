# ============================================================
# 🤖 main_content_engine.py — Milestone 3: Integrated AI Engine
# ============================================================

from generate_content import generate_marketing_content
from optimize_content import optimize_content
from trend_analysis import fetch_trending_topics
from sentiment_analysis import analyze_sentiment
from performance_metrics import generate_performance_metrics, log_performance_metrics
from google_sheets_example import update_sheet
from slack_notify import send_slack_alert, send_performance_alert

# ============================================================
# 🧩 Main Pipeline Function
# ============================================================

def run_content_generation(topic):
    # --- Step 1: Generate Base Content ---
    print("🚀 Generating content...")
    base = generate_marketing_content(topic)
    print("✅ Base content generated:\n", base)

    # --- Step 2: Fetch Trending Topics ---
    print("\n📊 Fetching trending topics...")
    trends = fetch_trending_topics()
    print("✅ Trends fetched:", trends)

    # --- Step 3: Optimize Content ---
    print("\n✨ Optimizing content...")
    optimized = optimize_content(base, trends)
    print("✅ Optimized content:\n", optimized)

    # --- Step 4: Sentiment Analysis ---
    print("\n🧠 Analyzing sentiment of optimized content...")
    sentiment = analyze_sentiment(optimized)
    print(f"✅ Sentiment detected: {sentiment}")

    # --- Step 5: Log to Google Sheets (AI Optimization Tab) ---
    print("\n🗂️ Updating Google Sheet with content and sentiment...")
    update_sheet("AI_Optimization", [topic, base, optimized, sentiment])
    print("✅ Content + Sentiment logged successfully.")

    # --- Step 6: Simulate Performance Metrics ---
    print("\n📈 Generating simulated performance metrics...")
    metrics = generate_performance_metrics(topic)
    print("✅ Metrics generated:", metrics)

    # --- Step 7: Log Metrics to Google Sheets (Performance Tab) ---
    log_performance_metrics([
        metrics["Date"],
        metrics["Topic"],
        metrics["Views"],
        metrics["Likes"],
        metrics["Shares"]
    ])
    print("✅ Metrics logged successfully in PerformanceMetrics tab.")

    # --- Step 8: Send Slack Alerts ---
    print("\n💬 Sending Slack notifications...")
    send_slack_alert(f"✅ New optimized content generated for *{topic}* (Sentiment: {sentiment})\n\n{optimized}")
    send_performance_alert(metrics)
    print("✅ Slack alerts sent successfully!")

    print("\n🎯 Milestone 3 pipeline completed for topic:", topic)
    return optimized


# ============================================================
# 🧩 Run the Pipeline (Manual Trigger)
# ============================================================

if __name__ == "__main__":
    topic = input("📝 Enter a topic for content generation: ")
    run_content_generation(topic)
