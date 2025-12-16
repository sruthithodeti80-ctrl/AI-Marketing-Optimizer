# collect_twitter.py
import snscrape.modules.twitter as sntwitter
import pandas as pd

def fetch_recent_tweets(query, total_results=30):
    print(f"🔍 Fetching {total_results} tweets for query: {query}")
    tweets = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
        if i >= total_results:
            break
        tweets.append({
            "platform": "Twitter",
            "id": tweet.id,
            "text": tweet.content,
            "created_at": tweet.date,
            "like_count": tweet.likeCount,
            "retweet_count": tweet.retweetCount,
            "reply_count": tweet.replyCount
        })
    print(f"✅ Collected {len(tweets)} tweets successfully.")
    return tweets

def save_to_csv(tweets, filename="sample_data.csv"):
    df = pd.DataFrame(tweets)
    df.to_csv(filename, index=False, encoding="utf-8")
    print(f"📁 Saved {len(df)} tweets to {filename}")

if __name__ == "__main__":
    query = "marketing lang:en since:2025-10-01 until:2025-11-03"
    tweets = fetch_recent_tweets(query, total_results=30)
    save_to_csv(tweets)
