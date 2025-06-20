# # trend_selector.py

# from scrapers.google_trends import get_google_trend_titles
# from scrapers.reddit_scraper import get_reddit_trend_titles
# from scrapers.pexels_scraper import search_pexels_image
# from fuzzywuzzy import fuzz


# def match_trends(google_trends, reddit_trends, threshold=60):
#     matched = []

#     for gtrend in google_trends:
#         for rtrend in reddit_trends:
#             score = fuzz.partial_ratio(gtrend.lower(), rtrend.lower())
#             if score >= threshold:
#                 matched.append((gtrend, rtrend, score))
    
#     # Sort by match score descending
#     matched.sort(key=lambda x: x[2], reverse=True)

#     # Get unique trend titles from both sources (Google/Reddit)
#     selected = set()
#     final_trends = []
    
#     for g, r, s in matched:
#         if g not in selected and r not in selected:
#             selected.add(g)
#             selected.add(r)
#             final_trends.append(g)  # use the Google one as primary
#         if len(final_trends) == 2:
#             break

#     return final_trends


# def run_trend_selector():
#     print("📊 Fetching Google Trends...")
#     google_trends = get_google_trend_titles()

#     print("🧠 Fetching Reddit Trends...")
#     reddit_trends = get_reddit_trend_titles()

#     print("🔍 Matching trends...")
#     selected_trends = match_trends(google_trends, reddit_trends)

#     print(f"\n✅ Selected Trends: {selected_trends}\n")

#     for trend in selected_trends:
#         print(f"🖼️ Downloading copyright-safe image from Pexels for: {trend}")
#         path = search_pexels_image(trend)
#         if path:
#             print(f"✅ Saved at: {path}\n")
#         else:
#             print(f"❌ No image found for: {trend}\n")


# if __name__ == "__main__":
#     run_trend_selector()
# trend_selector.py

from scrapers.reddit_scraper import get_reddit_trend_titles

def select_trending_topic():
    titles = get_reddit_trend_titles(limit=5)
    if not titles:
        print("❌ No Reddit trends found.")
        return None
    # Just select the top one or random
    selected = titles[0]
    print(f"🎯 Selected trend: {selected}")
    return selected

if __name__ == "__main__":
    select_trending_topic()
