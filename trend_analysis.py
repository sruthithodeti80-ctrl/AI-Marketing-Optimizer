# trend_analysis.py
import requests
import os

def fetch_trending_topics():
    """Fetch trending hashtags/topics from Twitter (X) using API."""
    url = "https://api.twitter.com/2/trends/place.json?id=1"
    headers = {"Authorization": f"Bearer {os.getenv('TWITTER_BEARER_TOKEN')}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        trends = [t['name'] for t in response.json()[0]['trends'][:10]]
        return trends
    else:
        print("Error fetching trends:", response.text)
        return []
