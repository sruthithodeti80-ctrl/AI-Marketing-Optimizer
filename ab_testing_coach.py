# ============================================================
# 🧪 ab_testing_coach.py — A/B Testing & Prediction Coach
# ============================================================

import random
import pandas as pd
from datetime import datetime, timedelta
from generate_content import generate_marketing_content
from optimize_content import optimize_content
from sentiment_analysis import analyze_sentiment
from trend_analysis import fetch_trending_topics
from performance_metrics import generate_performance_metrics
from google_sheets_example import update_sheet
from slack_notify import send_slack_alert

# ============================================================
# 🔹 A/B Test Variant Generator
# ============================================================

def generate_ab_variants(topic, platform="twitter", num_variants=2):
    """
    Generate multiple content variants for A/B testing.
    Returns a list of variant dictionaries with content and metadata.
    """
    variants = []
    tones = ["engaging", "professional", "casual", "urgent", "inspirational"]
    
    print(f"🧪 Generating {num_variants} A/B test variants for '{topic}'...")
    
    for i in range(num_variants):
        tone = random.choice(tones)
        content = generate_marketing_content(topic, platform, tone)
        sentiment = analyze_sentiment(content)
        
        variant = {
            "variant_id": f"V{i+1}",
            "tone": tone,
            "content": content,
            "sentiment": sentiment,
            "platform": platform
        }
        variants.append(variant)
        print(f"✅ Variant {i+1} ({tone}): Generated")
    
    return variants


# ============================================================
# 🔹 Campaign Simulation Engine
# ============================================================

def simulate_campaign_performance(variant, days=7):
    """
    Simulate campaign performance over time with realistic patterns.
    Returns daily metrics and predictions.
    """
    base_views = random.randint(1000, 3000)
    base_engagement = random.uniform(0.05, 0.15)  # 5-15% engagement rate
    
    # Sentiment boost
    sentiment_multiplier = {
        "Positive": 1.3,
        "Neutral": 1.0,
        "Negative": 0.7
    }
    multiplier = sentiment_multiplier.get(variant["sentiment"], 1.0)
    
    daily_data = []
    for day in range(days):
        # Simulate decay and viral patterns
        decay_factor = 0.85 ** day  # Natural decay
        viral_chance = random.random()
        viral_boost = 2.5 if viral_chance > 0.9 else 1.0
        
        views = int(base_views * multiplier * decay_factor * viral_boost)
        likes = int(views * base_engagement * random.uniform(0.8, 1.2))
        shares = int(likes * random.uniform(0.2, 0.4))
        comments = int(likes * random.uniform(0.1, 0.3))
        
        daily_data.append({
            "day": day + 1,
            "views": views,
            "likes": likes,
            "shares": shares,
            "comments": comments,
            "engagement_rate": round((likes + shares + comments) / views * 100, 2)
        })
    
    return daily_data


# ============================================================
# 🔹 Predictive Recommendation Engine
# ============================================================

def predict_winner(variants_with_results):
    """
    Analyze A/B test results and predict the winning variant.
    Returns recommendations and confidence scores.
    """
    print("\n🔮 Analyzing A/B test results and generating predictions...")
    
    predictions = []
    for variant_result in variants_with_results:
        variant = variant_result["variant"]
        metrics = variant_result["total_metrics"]
        
        # Calculate composite score
        engagement_score = metrics["likes"] + (metrics["shares"] * 2) + (metrics["comments"] * 1.5)
        reach_score = metrics["views"]
        composite_score = (engagement_score * 0.6) + (reach_score * 0.4)
        
        predictions.append({
            "variant_id": variant["variant_id"],
            "tone": variant["tone"],
            "sentiment": variant["sentiment"],
            "composite_score": composite_score,
            "engagement_rate": metrics["engagement_rate"],
            "total_views": metrics["views"],
            "total_engagement": engagement_score
        })
    
    # Sort by composite score
    predictions.sort(key=lambda x: x["composite_score"], reverse=True)
    winner = predictions[0]
    
    # Calculate confidence
    if len(predictions) > 1:
        score_diff = (winner["composite_score"] - predictions[1]["composite_score"]) / winner["composite_score"]
        confidence = min(95, 50 + (score_diff * 100))
    else:
        confidence = 75
    
    recommendation = {
        "winner": winner,
        "confidence": round(confidence, 1),
        "all_variants": predictions,
        "insights": generate_insights(predictions)
    }
    
    return recommendation


# ============================================================
# 🔹 Insight Generator
# ============================================================

def generate_insights(predictions):
    """Generate actionable insights from A/B test results."""
    insights = []
    
    # Tone analysis
    tones = [p["tone"] for p in predictions]
    best_tone = predictions[0]["tone"]
    insights.append(f"✅ Best performing tone: '{best_tone}'")
    
    # Sentiment analysis
    sentiments = [p["sentiment"] for p in predictions]
    positive_count = sentiments.count("Positive")
    if positive_count > len(sentiments) / 2:
        insights.append("✅ Positive sentiment correlates with higher engagement")
    
    # Engagement patterns
    avg_engagement = sum(p["engagement_rate"] for p in predictions) / len(predictions)
    if predictions[0]["engagement_rate"] > avg_engagement * 1.2:
        insights.append(f"✅ Winner has {predictions[0]['engagement_rate']:.1f}% engagement (above average)")
    
    return insights


# ============================================================
# 🔹 Run Complete A/B Test
# ============================================================

def run_ab_test(topic, platform="twitter", num_variants=3, simulation_days=7):
    """
    Complete A/B testing pipeline with predictions and recommendations.
    """
    print(f"\n{'='*60}")
    print(f"🚀 Starting A/B Test Campaign for: {topic}")
    print(f"{'='*60}\n")
    
    # Step 1: Generate variants
    variants = generate_ab_variants(topic, platform, num_variants)
    
    # Step 2: Simulate campaign performance
    print(f"\n📊 Simulating {simulation_days}-day campaign performance...")
    variants_with_results = []
    
    for variant in variants:
        daily_metrics = simulate_campaign_performance(variant, simulation_days)
        
        # Calculate totals
        total_metrics = {
            "views": sum(d["views"] for d in daily_metrics),
            "likes": sum(d["likes"] for d in daily_metrics),
            "shares": sum(d["shares"] for d in daily_metrics),
            "comments": sum(d["comments"] for d in daily_metrics),
            "engagement_rate": round(sum(d["engagement_rate"] for d in daily_metrics) / len(daily_metrics), 2)
        }
        
        variants_with_results.append({
            "variant": variant,
            "daily_metrics": daily_metrics,
            "total_metrics": total_metrics
        })
        
        print(f"✅ {variant['variant_id']} ({variant['tone']}): {total_metrics['views']:,} views, {total_metrics['engagement_rate']}% engagement")
    
    # Step 3: Predict winner and generate recommendations
    recommendation = predict_winner(variants_with_results)
    
    # Step 4: Display results
    print(f"\n{'='*60}")
    print(f"🏆 A/B TEST RESULTS & RECOMMENDATIONS")
    print(f"{'='*60}\n")
    print(f"🥇 Winner: Variant {recommendation['winner']['variant_id']} ({recommendation['winner']['tone']})")
    print(f"📊 Confidence: {recommendation['confidence']}%")
    print(f"📈 Total Views: {recommendation['winner']['total_views']:,}")
    print(f"💬 Engagement Rate: {recommendation['winner']['engagement_rate']}%")
    print(f"\n💡 Key Insights:")
    for insight in recommendation['insights']:
        print(f"   {insight}")
    
    # Step 5: Log to Google Sheets
    print(f"\n🗂️ Logging results to Google Sheets...")
    log_ab_test_results(topic, variants_with_results, recommendation)
    
    # Step 6: Send Slack notification
    print(f"\n💬 Sending Slack notification...")
    send_ab_test_alert(topic, recommendation)
    
    print(f"\n✅ A/B Test completed successfully!\n")
    return recommendation


# ============================================================
# 🔹 Log Results to Google Sheets
# ============================================================

def log_ab_test_results(topic, variants_with_results, recommendation):
    """Log A/B test results to Google Sheets."""
    try:
        from google_sheets_example import ensure_tab_exists
        
        # Ensure AB_Testing tab exists with proper headers
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
        ensure_tab_exists("AB_Testing", headers)
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        winner = recommendation['winner']
        
        for vr in variants_with_results:
            variant = vr['variant']
            metrics = vr['total_metrics']
            is_winner = "✅" if variant['variant_id'] == winner['variant_id'] else ""
            
            row = [
                timestamp,
                topic,
                variant['variant_id'],
                variant['tone'],
                variant['sentiment'],
                metrics['views'],
                metrics['likes'],
                metrics['shares'],
                metrics['engagement_rate'],
                is_winner
            ]
            update_sheet("AB_Testing", row)
        
        print("✅ Results logged to Google Sheets")
    except Exception as e:
        print(f"⚠️ Could not log to Google Sheets: {e}")


# ============================================================
# 🔹 Send Slack Alert
# ============================================================

def send_ab_test_alert(topic, recommendation):
    """Send A/B test results via Slack."""
    try:
        winner = recommendation['winner']
        message = f"""
🧪 *A/B Test Complete: {topic}*

🏆 *Winner:* Variant {winner['variant_id']} ({winner['tone']})
📊 *Confidence:* {recommendation['confidence']}%
📈 *Views:* {winner['total_views']:,}
💬 *Engagement:* {winner['engagement_rate']}%

💡 *Key Insights:*
{chr(10).join(recommendation['insights'])}
        """
        send_slack_alert(message)
        print("✅ Slack notification sent")
    except Exception as e:
        print(f"⚠️ Could not send Slack alert: {e}")


# ============================================================
# 🔹 Main Execution
# ============================================================

if __name__ == "__main__":
    topic = input("📝 Enter campaign topic: ")
    num_variants = int(input("🔢 Number of variants to test (2-5): ") or 3)
    run_ab_test(topic, num_variants=num_variants)
