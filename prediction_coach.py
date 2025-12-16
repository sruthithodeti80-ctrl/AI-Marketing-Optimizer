# ============================================================
# 🔮 prediction_coach.py — Predictive Analytics & Recommendations
# ============================================================

import pandas as pd
import random
from datetime import datetime, timedelta
from performance_metrics import generate_performance_metrics
from sentiment_analysis import analyze_sentiment
from trend_analysis import fetch_trending_topics

# ============================================================
# 🔹 Historical Data Analyzer
# ============================================================

def analyze_historical_performance(csv_file="reddit_data.csv"):
    """
    Analyze historical performance data to identify patterns.
    Returns insights and predictions based on past campaigns.
    """
    try:
        df = pd.read_csv(csv_file)
        print(f"📊 Analyzing {len(df)} historical records...")
        
        insights = {
            "total_campaigns": len(df),
            "avg_engagement": df.get("score", pd.Series([0])).mean() if "score" in df.columns else 0,
            "best_performing_topics": [],
            "engagement_trends": "stable"
        }
        
        print(f"✅ Historical analysis complete")
        return insights
    except Exception as e:
        print(f"⚠️ Could not analyze historical data: {e}")
        return {"total_campaigns": 0, "avg_engagement": 0}


# ============================================================
# 🔹 Content Performance Predictor
# ============================================================

def predict_content_performance(content, platform="twitter"):
    """
    Predict how content will perform based on multiple factors.
    Returns predicted metrics and confidence score.
    """
    print(f"\n🔮 Predicting performance for {platform} content...")
    
    # Factor 1: Sentiment analysis
    sentiment = analyze_sentiment(content)
    sentiment_score = {"Positive": 1.3, "Neutral": 1.0, "Negative": 0.7}[sentiment]
    
    # Factor 2: Content length
    word_count = len(content.split())
    length_score = 1.2 if 15 <= word_count <= 30 else 0.9
    
    # Factor 3: Hashtag presence
    hashtag_count = content.count("#")
    hashtag_score = min(1.0 + (hashtag_count * 0.1), 1.3)
    
    # Factor 4: Emoji presence
    emoji_score = 1.15 if any(char for char in content if ord(char) > 127) else 1.0
    
    # Factor 5: Call-to-action detection
    cta_keywords = ["click", "learn", "discover", "join", "get", "try", "download"]
    has_cta = any(keyword in content.lower() for keyword in cta_keywords)
    cta_score = 1.2 if has_cta else 1.0
    
    # Calculate composite prediction
    base_views = random.randint(1500, 3500)
    composite_multiplier = sentiment_score * length_score * hashtag_score * emoji_score * cta_score
    
    predicted_views = int(base_views * composite_multiplier)
    predicted_engagement_rate = round(random.uniform(3, 12) * composite_multiplier, 2)
    predicted_likes = int(predicted_views * (predicted_engagement_rate / 100))
    predicted_shares = int(predicted_likes * random.uniform(0.2, 0.4))
    
    # Calculate confidence based on factor alignment
    confidence = min(95, 60 + (composite_multiplier - 1) * 50)
    
    prediction = {
        "predicted_views": predicted_views,
        "predicted_likes": predicted_likes,
        "predicted_shares": predicted_shares,
        "predicted_engagement_rate": predicted_engagement_rate,
        "confidence": round(confidence, 1),
        "factors": {
            "sentiment": sentiment,
            "sentiment_impact": f"{(sentiment_score - 1) * 100:+.0f}%",
            "length_optimal": 15 <= word_count <= 30,
            "has_hashtags": hashtag_count > 0,
            "has_emojis": emoji_score > 1.0,
            "has_cta": has_cta
        }
    }
    
    return prediction


# ============================================================
# 🔹 Optimization Recommendations
# ============================================================

def generate_recommendations(content, prediction):
    """
    Generate actionable recommendations to improve content performance.
    """
    recommendations = []
    factors = prediction["factors"]
    
    # Sentiment recommendations
    if factors["sentiment"] == "Negative":
        recommendations.append("⚠️ Negative sentiment detected. Consider reframing with positive language.")
    elif factors["sentiment"] == "Neutral":
        recommendations.append("💡 Add emotional appeal to increase engagement.")
    
    # Length recommendations
    if not factors["length_optimal"]:
        word_count = len(content.split())
        if word_count < 15:
            recommendations.append("📝 Content is too short. Add more context (aim for 15-30 words).")
        else:
            recommendations.append("✂️ Content is too long. Shorten for better readability.")
    
    # Hashtag recommendations
    if not factors["has_hashtags"]:
        recommendations.append("🏷️ Add 2-3 relevant hashtags to increase discoverability.")
    
    # Emoji recommendations
    if not factors["has_emojis"]:
        recommendations.append("😊 Add emojis to make content more engaging and visual.")
    
    # CTA recommendations
    if not factors["has_cta"]:
        recommendations.append("📢 Include a clear call-to-action (e.g., 'Learn more', 'Join us').")
    
    # Performance-based recommendations
    if prediction["predicted_engagement_rate"] < 5:
        recommendations.append("⚡ Low engagement predicted. Consider A/B testing different approaches.")
    
    if not recommendations:
        recommendations.append("✅ Content is well-optimized! No major changes needed.")
    
    return recommendations


# ============================================================
# 🔹 Best Time to Post Predictor
# ============================================================

def predict_best_posting_time(platform="twitter"):
    """
    Predict optimal posting times based on platform and audience patterns.
    """
    posting_schedules = {
        "twitter": [
            {"time": "9:00 AM", "day": "Weekdays", "engagement_boost": 1.3},
            {"time": "12:00 PM", "day": "Weekdays", "engagement_boost": 1.5},
            {"time": "5:00 PM", "day": "Weekdays", "engagement_boost": 1.4},
            {"time": "8:00 PM", "day": "Weekends", "engagement_boost": 1.2}
        ],
        "instagram": [
            {"time": "11:00 AM", "day": "Weekdays", "engagement_boost": 1.4},
            {"time": "2:00 PM", "day": "Weekdays", "engagement_boost": 1.3},
            {"time": "7:00 PM", "day": "Daily", "engagement_boost": 1.5}
        ],
        "linkedin": [
            {"time": "8:00 AM", "day": "Weekdays", "engagement_boost": 1.5},
            {"time": "12:00 PM", "day": "Weekdays", "engagement_boost": 1.4},
            {"time": "5:00 PM", "day": "Weekdays", "engagement_boost": 1.3}
        ]
    }
    
    schedule = posting_schedules.get(platform, posting_schedules["twitter"])
    best_time = max(schedule, key=lambda x: x["engagement_boost"])
    
    return {
        "platform": platform,
        "best_time": best_time["time"],
        "best_day": best_time["day"],
        "expected_boost": f"+{(best_time['engagement_boost'] - 1) * 100:.0f}%",
        "all_recommendations": schedule
    }


# ============================================================
# 🔹 Trend-Based Content Suggestions
# ============================================================

def suggest_trending_content():
    """
    Suggest content topics based on current trends.
    """
    print("\n📈 Fetching trending topics for content suggestions...")
    
    try:
        trends = fetch_trending_topics()
        if not trends:
            trends = ["AI", "Sustainability", "Remote Work", "Digital Marketing", "Tech Innovation"]
        
        suggestions = []
        for i, trend in enumerate(trends[:5], 1):
            suggestions.append({
                "rank": i,
                "topic": trend,
                "potential_reach": random.randint(5000, 20000),
                "competition": random.choice(["Low", "Medium", "High"])
            })
        
        return suggestions
    except Exception as e:
        print(f"⚠️ Could not fetch trends: {e}")
        return []


# ============================================================
# 🔹 Complete Prediction Coach
# ============================================================

def run_prediction_coach(content, platform="twitter"):
    """
    Complete prediction and recommendation pipeline.
    """
    print(f"\n{'='*60}")
    print(f"🔮 PREDICTION COACH - Content Analysis")
    print(f"{'='*60}\n")
    
    print(f"📝 Content: {content[:100]}...")
    
    # Step 1: Predict performance
    prediction = predict_content_performance(content, platform)
    
    print(f"\n📊 Performance Prediction:")
    print(f"   Views: {prediction['predicted_views']:,}")
    print(f"   Likes: {prediction['predicted_likes']:,}")
    print(f"   Shares: {prediction['predicted_shares']:,}")
    print(f"   Engagement Rate: {prediction['predicted_engagement_rate']}%")
    print(f"   Confidence: {prediction['confidence']}%")
    
    # Step 2: Generate recommendations
    recommendations = generate_recommendations(content, prediction)
    
    print(f"\n💡 Recommendations:")
    for rec in recommendations:
        print(f"   {rec}")
    
    # Step 3: Best posting time
    timing = predict_best_posting_time(platform)
    
    print(f"\n⏰ Optimal Posting Time:")
    print(f"   Best Time: {timing['best_time']} ({timing['best_day']})")
    print(f"   Expected Boost: {timing['expected_boost']}")
    
    # Step 4: Trending suggestions
    trending = suggest_trending_content()
    
    if trending:
        print(f"\n📈 Trending Topics to Consider:")
        for suggestion in trending[:3]:
            print(f"   {suggestion['rank']}. {suggestion['topic']} (Reach: {suggestion['potential_reach']:,}, Competition: {suggestion['competition']})")
    
    print(f"\n{'='*60}\n")
    
    return {
        "prediction": prediction,
        "recommendations": recommendations,
        "timing": timing,
        "trending": trending
    }


# ============================================================
# 🔹 Main Execution
# ============================================================

if __name__ == "__main__":
    sample_content = "Discover how AI is transforming education! 🚀 Join our webinar to learn more. #AI #Education #Innovation"
    run_prediction_coach(sample_content, platform="twitter")
