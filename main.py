import os
from services.instagram_bot import InstagramBot
from scrapers.reddit_scraper import fetch_reddit_memes
from scrapers.google_trends import get_trending, download_trending_images, extract_title_from_filename
from scrapers.pexels_scraper import search_pexels_image
from models.meme_generator import generate_meme

def main():
    print("🚀 Starting Meme Bot Automation...\n")

    # 1. Initialize Instagram Bot
    bot = InstagramBot()

    # 2. Try fetching memes from Reddit
    memes = fetch_reddit_memes()
    if memes:
        print("🎯 Using memes from Reddit")
        selected_meme = memes[0]
        title = selected_meme["title"]
        image_path = selected_meme["image"]
        caption_options = selected_meme.get("caption_options")
    else:
        print("🔍 No Reddit memes found. Using Google Trends...")

        # 3. Get Google trending topics
        trends = get_trending()
        if not trends:
            print("❌ No Google trends found. Exiting.")
            return

        # 4. Try getting an image from Pexels
        top_trend = trends[0]
        image_path = search_pexels_image(top_trend)

        if image_path:
            print(f"📸 Image downloaded from **Pexels** for trend: {top_trend}")
            image_source = "Pexels"
        else:
            print("⚠️ Pexels image not found. Falling back to Google Image search...")
            downloaded_images = download_trending_images(top_trend, limit=1)

            if not downloaded_images:
                print("❌ No images found for the top trend. Exiting.")
                return

            image_path = downloaded_images[0]
            image_source = "Google Images"

        title = extract_title_from_filename(image_path)
        caption_options = None

    print(f"\n🖼️ Meme Selected: {title}")
    print(f"📷 Image Source: {image_source if 'image_source' in locals() else 'Reddit'}")

    # 5. Generate meme with caption & overlay
    meme_path, final_caption = generate_meme(image_path, caption_options)
    if meme_path is None or final_caption is None:
        print("❌ Meme generation failed. Exiting.")
        return

    print(f"\n📝 Final Caption:\n{final_caption}")

    # 6. Post to Instagram
    bot.post_meme(meme_path, final_caption)

    # 7. Logout
    bot.logout()
    print("\n✅ Meme posted successfully!")

if __name__ == "__main__":
    main()
