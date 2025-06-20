from pytrends.request import TrendReq

def get_google_trend_titles(limit=5):
    try:
        pytrends = TrendReq(hl='en-US', tz=330)
        trending_df = pytrends.trending_searches(pn='india')  # <-- ✅ This works
        if trending_df.empty:
            print("⚠️ Google Trends returned no data.")
            return []

        return trending_df[0].tolist()[:limit]
    except Exception as e:
        print(f"❌ Error fetching Google trends: {e}")
        return []

# Debug
if __name__ == "__main__":
    print("🔍 Fetching trending Google searches in India...")
    print(get_google_trend_titles())

