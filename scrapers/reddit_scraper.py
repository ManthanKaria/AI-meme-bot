# reddit_scraper.py
import requests

HEADERS = {"User-Agent": "Mozilla/5.0"}
REDDIT_POPULAR_URL = "https://www.reddit.com/r/popular.json"

def get_reddit_trend_titles(limit=5):
    try:
        response = requests.get(REDDIT_POPULAR_URL, headers=HEADERS)
        if response.status_code != 200:
            print(f"❌ Failed to fetch Reddit: {response.status_code}")
            return []

        data = response.json()
        posts = data.get("data", {}).get("children", [])
        titles = [
            post["data"]["title"]
            for post in posts
            if len(post["data"]["title"]) < 100
        ]
        return titles[:limit]
    except Exception as e:
        print(f"❌ Error fetching Reddit trends: {e}")
        return []

# Debug
if __name__ == "__main__":
    print(get_reddit_trend_titles())
