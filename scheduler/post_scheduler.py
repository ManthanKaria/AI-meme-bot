# import os
# import time
# import logging
# from services.instagram_bot import upload_image_to_instagram
# from services.imgbb_uploader import upload_to_imgbb
# from models.meme_generator import (
#     create_final_meme,
# )

# # Configure logging
# logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# def get_latest_images(folder):
#     images = sorted(
#         [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith((".jpg", ".png"))],
#         key=os.path.getmtime,
#         reverse=True
#     )
#     return images[0], images[1] if len(images) >= 2 else (None, None)

# def schedule_posts():
#     pexels_folder = "data/memes/pexels"

#     while True:
#         try:
#             logging.info("⚡ Starting new meme generation cycle...")

#             # Get 2 latest images
#             img1, img2 = get_latest_images(pexels_folder)
#             if not img1 or not img2:
#                 logging.warning("⚠️ Not enough images. Retrying in 5 minutes...")
#                 time.sleep(300)
#                 continue

#             # Set meme caption
#             meme_idea = "When you forget to save and your laptop crashes"
#             caption = "🔥 Made by ChatGPT | #TechMemes #DevLife"

#             # Create final meme
#             final_meme_path = create_final_meme(img1, img2, meme_idea, caption)

#             # Upload to ImgBB to get a public image URL
#             image_url = upload_to_imgbb(final_meme_path)

#             if not image_url:
#                 logging.error("❌ Failed to upload image to ImgBB.")
#                 time.sleep(300)
#                 continue

#             # Post using Instagram Graph API
#             post_success = upload_image_to_instagram(image_url, caption)

#             if post_success:
#                 logging.info(f"✅ Meme posted successfully: {final_meme_path}")
#             else:
#                 logging.error("❌ Instagram Graph API post failed.")

#             # Wait 1 hour before next post
#             time.sleep(3600)

#         except Exception as e:
#             logging.exception(f"❌ Unexpected error occurred: {e}")
#             time.sleep(300)

# if __name__ == "__main__":
#     schedule_posts()

# import os
# import time
# import shutil
# import logging
# from models.meme_generator import (
#     generate_meme_text_ai,
#     create_final_meme,
#     format_image_for_instagram,
#     add_caption_to_image,
#     upscale_image,
# )

# # Optional: trending topic selector
# # from scrapers.trend_selector import select_trending_topic

# # Configure logging
# logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# def get_latest_images(folder):
#     """Returns the two most recent image paths from the given folder."""
#     images = sorted(
#         [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith((".jpg", ".png"))],
#         key=os.path.getmtime,
#         reverse=True
#     )
#     if len(images) >= 2:
#         return images[0], images[1]
#     return None, None

# def schedule_posts():
#     """Continuously generates memes and saves them to Final Post folder instead of Instagram."""
#     pexels_folder = "data/memes/pexels"
#     final_post_folder = "data/Final Post"
#     os.makedirs(final_post_folder, exist_ok=True)

#     while True:
#         try:
#             logging.info("⚡ Starting new meme generation cycle...")

#             # Step 1: Fetch the latest two images
#             img1, img2 = get_latest_images(pexels_folder)

#             if not img1 or not img2:
#                 logging.warning("⚠️ Not enough images found in the Pexels folder. Retrying in 5 minutes...")
#                 time.sleep(300)
#                 continue

#             # Step 2: Generate meme idea (static or dynamic)
#             # meme_idea = select_trending_topic()
#             meme_idea = "When you forget to save and your laptop crashes"  # Static fallback idea
#             caption = "Made by ChatGPT 🤖"

#             # Step 3: Create the final meme
#             final_meme_path = create_final_meme(img1, img2, meme_idea, caption)

#             # Step 4: Save meme to Final Post folder
#             destination_path = os.path.join(final_post_folder, os.path.basename(final_meme_path))
#             shutil.copy(final_meme_path, destination_path)

#             logging.info(f"✅ Meme saved in Final Post folder: {destination_path}")

#             # Wait for 1 hour before generating the next meme
#             time.sleep(3600)

#         except Exception as e:
#             logging.exception(f"❌ Unexpected error occurred: {e}")
#             time.sleep(300)

# if __name__ == "__main__":
#     schedule_posts()
# import os
# import time
# import logging
# import json
# from datetime import datetime, timedelta

# # 💡 Imports from your own project
# from scrapers.reddit_scraper import get_reddit_trend_titles
# from scrapers.image_downloader import fetch_images_for_trends
# from services.instagram_bot import upload_image_to_instagram
# from services.imgbb_uploader import upload_to_imgbb
# from models.meme_generator import create_final_meme,generate_ai_caption_with_image
# # 🔧 Setup
# PEXELS_FOLDER = "data/memes/pexels"
# POSTED_MEMES_JSON = "logs/posted_memes.json"

# logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# # 🧠 Helpers
# def get_latest_images(folder):
#     images = sorted(
#         [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith((".jpg", ".png"))],
#         key=os.path.getmtime,
#         reverse=True
#     )
#     return images[0], images[1] if len(images) >= 2 else (None, None)

# def has_recently_posted(title, cooldown_days=2):
#     if not os.path.exists(POSTED_MEMES_JSON):
#         return False
#     with open(POSTED_MEMES_JSON, "r") as f:
#         posted_data = json.load(f)
#     last_post_time_str = posted_data.get(title)
#     if not last_post_time_str:
#         return False
#     last_post_time = datetime.fromisoformat(last_post_time_str)
#     return datetime.now() - last_post_time < timedelta(days=cooldown_days)

# def log_posted(title):
#     posted_data = {}
#     if os.path.exists(POSTED_MEMES_JSON):
#         with open(POSTED_MEMES_JSON, "r") as f:
#             posted_data = json.load(f)
#     posted_data[title] = datetime.now().isoformat()
#     with open(POSTED_MEMES_JSON, "w") as f:
#         json.dump(posted_data, f, indent=4)

# def get_image_dicts(titles):
#     image_dicts = []
#     for title in titles:
#         image_pairs = fetch_images_for_trends([title])  # Already returns a list of dicts with 'img1' and 'img2'

#         if not image_pairs:
#             logging.warning(f"⚠️ No valid image pairs for title: {title}")
#             continue

#         for pair in image_pairs:
#             img1_path = pair.get("img1")
#             img2_path = pair.get("img2")

#             if img1_path and img2_path and os.path.exists(img1_path) and os.path.exists(img2_path):
#                 image_dicts.append({
#                     "title": title,
#                     "img1": img1_path,
#                     "img2": img2_path
#                 })
#             else:
#                 logging.warning(f"⚠️ Image paths not found or invalid for title: {title}")

#     return image_dicts

# def schedule_posts():
#     while True:
#         try:
#             logging.info("🚀 Starting meme generation/posting cycle...")

#             trending_titles = get_reddit_trend_titles(limit=7)  # Get more than 1 for backup
#             if not trending_titles:
#                 logging.warning("⚠️ No trending titles found. Sleeping 5 mins...")
#                 time.sleep(300)
#                 continue

#             valid_titles = [title for title in trending_titles if not has_recently_posted(title)]
#             if not valid_titles:
#                 logging.info("⏭️ All trending titles already posted recently. Sleeping 1 hour...")
#                 time.sleep(3600)
#                 continue

#             image_data_list = get_image_dicts(valid_titles)
#             if not image_data_list:
#                 logging.warning("⚠️ No valid image pairs found. Sleeping 5 mins...")
#                 time.sleep(300)
#                 continue

#             for data in image_data_list:
#                 title = data["title"]
#                 img1 = data["img1"]
#                 img2 = data["img2"]

#                 logging.info(f"🎯 Working on meme for: {title}")

#                 meme_caption, full_caption = generate_ai_caption_with_image(title,image_url)
#                 if not meme_caption:
#                     logging.error("❌ Caption generation failed. Skipping...")
#                     continue

#                 meme_path = create_final_meme(img1, img2, title, caption=meme_caption)
#                 if not meme_path or not os.path.exists(meme_path):
#                     logging.error("❌ Meme creation failed or invalid path. Skipping...")
#                     continue

#                 meme_filename = os.path.basename(meme_path)

#                 image_url = upload_to_imgbb(meme_path)
#                 if not image_url:
#                     logging.error("❌ ImgBB upload failed.")
#                     continue

#                 post_success = upload_image_to_instagram(image_url, full_caption)
#                 if post_success:
#                     logging.info(f"✅ Meme posted to Instagram: {meme_filename}")
#                     log_posted(title)
#                 else:
#                     logging.error("❌ Instagram post failed.")

#                 # 💤 Optional wait before next meme
#                 logging.info("⏸️ Sleeping 3 minutes before next meme...")
#                 time.sleep(180)

#             logging.info("⏳ Cycle complete. Sleeping 1 hour...")
#             time.sleep(3600)

#         except Exception as e:
#             logging.exception(f"💥 Unhandled exception: {e}")
#             time.sleep(300)

# if __name__ == "__main__":
#     schedule_posts()
import os
import time
import shutil
import json
import logging
import boto3
from datetime import datetime, timedelta

# 🛠️ Project imports
from scrapers.reddit_scraper import get_reddit_trend_titles
from scrapers.image_downloader import fetch_images_for_trends
from services.imgbb_uploader import upload_to_imgbb
from services.instagram_bot import upload_image_to_instagram
from models.meme_generator import create_final_meme

# ⚙️ Setup
PEXELS_FOLDER = "data/memes/pexels"
FINAL_POST_FOLDER = "data/Final_Post"
POSTED_MEMES_JSON = "logs/posted_memes.json"

# S3 Configuration (⚠️ Best to load via env vars in production)
S3_BUCKET_NAME = 'ai-meme-bot-manthan'


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# 🧹 Helper Functions
def get_latest_images(folder):
    images = sorted(
        [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith((".jpg", ".png"))],
        key=os.path.getmtime,
        reverse=True
    )
    return images[:2] if len(images) >= 2 else (None, None)

def has_recently_posted(title, cooldown_days=2):
    if not os.path.exists(POSTED_MEMES_JSON):
        return False

    with open(POSTED_MEMES_JSON, "r") as f:
        posted_data = json.load(f)

    last_post_time_str = posted_data.get(title)
    if not last_post_time_str:
        return False

    last_post_time = datetime.fromisoformat(last_post_time_str)
    return datetime.now() - last_post_time < timedelta(days=cooldown_days)

def log_posted(title):
    posted_data = {}
    if os.path.exists(POSTED_MEMES_JSON):
        with open(POSTED_MEMES_JSON, "r") as f:
            posted_data = json.load(f)

    posted_data[title] = datetime.now().isoformat()

    with open(POSTED_MEMES_JSON, "w") as f:
        json.dump(posted_data, f, indent=4)

def get_image_dicts(titles):
    image_dicts = []
    for title in titles:
        image_pairs = fetch_images_for_trends([title])
        if not image_pairs:
            logging.warning(f"⚠️ No valid image pairs for title: {title}")
            continue

        for pair in image_pairs:
            img1_path = pair.get("img1")
            img2_path = pair.get("img2")
            if img1_path and img2_path and os.path.exists(img1_path) and os.path.exists(img2_path):
                image_dicts.append({
                    "title": title,
                    "img1": img1_path,
                    "img2": img2_path
                })
            else:
                logging.warning(f"⚠️ Invalid image paths for title: {title}")
    return image_dicts


def upload_file_to_s3(local_path, s3_path):
    try:
        # 👉 No need to pass access keys manually; boto3 will pick from the environment or ~/.aws/credentials
        s3_client = boto3.client('s3')
        
        s3_client.upload_file(local_path, S3_BUCKET_NAME, s3_path)
        logging.info(f"✅ Successfully uploaded to S3: {s3_path}")
        return f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{s3_path}"  # simpler URL format
    except Exception as e:
        logging.error(f"❌ Failed to upload file to S3: {e}")
        return None

# 🕒 Main Scheduler
def schedule_posts():
    while True:
        try:
            logging.info("🚀 Starting meme generation/posting cycle...")

            trending_titles = get_reddit_trend_titles(limit=1)
            if not trending_titles:
                logging.warning("⚠️ No trending titles found. Sleeping 5 mins...")
                time.sleep(300)
                continue

            valid_titles = [title for title in trending_titles if not has_recently_posted(title)]
            if not valid_titles:
                logging.info("⏭️ All trending titles already posted recently. Sleeping 1 hour...")
                time.sleep(3600)
                continue

            image_data_list = get_image_dicts(valid_titles)
            if not image_data_list:
                logging.warning("⚠️ No valid image pairs found. Sleeping 5 mins...")
                time.sleep(300)
                continue

            for data in image_data_list:
                title = data["title"]
                img1 = data["img1"]
                img2 = data["img2"]

                logging.info(f"🎯 Creating meme for: {title}")

                meme = create_final_meme(img1, img2, title)
                if not meme or not os.path.exists(meme.get("path", "")):
                    logging.error("❌ Meme creation failed or invalid path. Skipping...")
                    continue

                meme_path = meme["path"]
                caption = meme["caption"]

                # Save locally to Final Post folder
                os.makedirs(FINAL_POST_FOLDER, exist_ok=True)
                local_post_path = os.path.join(FINAL_POST_FOLDER, os.path.basename(meme_path))
                shutil.copy(meme_path, local_post_path)

                # Upload to S3
                s3_path = f"memes/{os.path.basename(local_post_path)}"
                s3_url = upload_file_to_s3(local_post_path, s3_path)

                if s3_url:
                    logging.info(f"✅ Meme uploaded to S3: {s3_url}")

                    # 🆕 Upload to Instagram using s3_url
                    success = upload_image_to_instagram(s3_url, caption)

                    if success:
                        logging.info("🎉 Successfully posted to Instagram!")
                        log_posted(title)
                    else:
                        logging.error("❌ Failed to post meme on Instagram.")

                else:
                    logging.error("❌ S3 upload failed.")

                logging.info("⏸️ Waiting 3 minutes before next meme...")
                time.sleep(180)

            logging.info("⏳ Cycle complete. Sleeping 1 hour...")
            time.sleep(3600)

        except Exception as e:
            logging.exception(f"💥 Unhandled exception: {e}")
            time.sleep(300)

if __name__ == "__main__":
    schedule_posts()




# import requests
# import logging
# import os
# import glob
# import time
# from datetime import datetime
# from dotenv import load_dotenv
# from services.imgbb_uploader import upload_to_imgbb
# import boto3

# # ================== Load environment variables ==================
# load_dotenv(".env")

# ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
# IG_USER_ID = os.getenv("IG_USER_ID")
# IMGBB_API_KEY = os.getenv("IMGBB_API_KEY")  # ImgBB API key

# GRAPH_API_BASE = "https://graph.instagram.com/v19.0"

# # ================== Configure logging ==================
# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s - %(levelname)s - %(message)s"
# )

# # ================== Utility Functions ==================

# def get_latest_image(folder_path):
#     """Get the latest JPG image from the specified folder."""
#     files = glob.glob(os.path.join(folder_path, "*.jpg"))
#     if not files:
#         logging.error(f"❌ No images found in folder: {folder_path}")
#         return None
#     latest_file = max(files, key=os.path.getctime)
#     return latest_file

# def verify_image_url(image_url):
#     """Verify if the ImgBB image URL is reachable."""
#     try:
#         response = requests.head(image_url)
#         if response.status_code == 200:
#             logging.info(f"✅ Verified ImgBB URL is reachable.")
#             return True
#         else:
#             logging.error(f"❌ ImgBB URL is not reachable. Status code: {response.status_code}")
#             return False
#     except Exception as e:
#         logging.exception(f"❌ Exception while verifying ImgBB URL: {e}")
#         return False

# def create_instagram_media_container_from_url(image_url, caption):
#     """Create media container using the ImgBB image URL."""
#     try:
#         url = f"{GRAPH_API_BASE}/{IG_USER_ID}/media"
#         logging.info(f"📤 Creating media container from ImgBB URL.")

#         data = {
#             'image_url': image_url,
#             'caption': caption,
#             'access_token': ACCESS_TOKEN
#         }

#         response = requests.post(url, data=data)
#         response_json = response.json()

#         if response.status_code == 200 and "id" in response_json:
#             container_id = response_json["id"]
#             logging.info(f"✅ Media container created. ID: {container_id}")
#             return container_id
#         else:
#             logging.error(f"❌ Failed to create media container. Response: {response_json}")
#             return None

#     except Exception as e:
#         logging.exception(f"❌ Exception while creating media container: {e}")
#         return None

# def publish_instagram_media(container_id):
#     """Publish the created media container on Instagram."""
#     try:
#         publish_url = f"{GRAPH_API_BASE}/{IG_USER_ID}/media_publish"
#         payload = {
#             "creation_id": container_id,
#             "access_token": ACCESS_TOKEN
#         }

#         logging.info("⏳ Waiting before publishing (5 seconds as per IG guidelines)...")
#         time.sleep(5)  # Respect Instagram's advice before publishing

#         response = requests.post(publish_url, data=payload)
#         response_json = response.json()

#         if response.status_code == 200 and "id" in response_json:
#             post_id = response_json["id"]
#             logging.info(f"✅ Post published successfully! Post ID: {post_id}")
#             return post_id
#         else:
#             logging.error(f"❌ Failed to publish media. Response: {response_json}")
#             return None

#     except Exception as e:
#         logging.exception(f"❌ Exception while publishing media: {e}")
#         return None

# def upload_to_s3(local_file_path, bucket_name, s3_file_name):
#     """Upload an image to AWS S3 and return the public URL."""
#     s3 = boto3.client('s3')
#     try:
#         s3.upload_file(local_file_path, bucket_name, s3_file_name)
#         region = s3.get_bucket_location(Bucket=bucket_name)['LocationConstraint']
#         if region is None:
#             region = 'ap-south-1'  # Default for N. Virginia
#         s3_url = f"https://{bucket_name}.s3.{region}.amazonaws.com/{s3_file_name}"
#         return s3_url
#     except Exception as e:
#         print("Upload failed:", e)
#         return None

# # ================== Scheduling Function ==================

# def schedule_post(folder_path, caption, scheduled_time_str):
#     """
#     Schedule an Instagram post at a specific time.
    
#     Args:
#         folder_path (str): Path to the folder containing images.
#         caption (str): Caption for the Instagram post.
#         scheduled_time_str (str): Scheduled time in format "YYYY-MM-DD HH:MM:SS".
#     """
#     try:
#         scheduled_time = datetime.strptime(scheduled_time_str, "%Y-%m-%d %H:%M:%S")
#         logging.info(f"📅 Scheduled post time: {scheduled_time}")

#         while True:
#             now = datetime.now()
#             if now >= scheduled_time:
#                 logging.info("⏰ Scheduled time reached! Uploading post...")
#                 upload_success = upload_latest_local_image(folder_path, caption)

#                 if upload_success:
#                     logging.info("✅ Post uploaded successfully.")
#                 else:
#                     logging.error("❌ Failed to upload post.")
#                 break  # Exit after posting

#             # Sleep for a short while to avoid busy waiting
#             time.sleep(10)

#     except Exception as e:
#         logging.exception(f"❌ Exception occurred during scheduling: {e}")

# # ================== Main Function ==================

# def upload_latest_local_image(folder_path, caption):
#     """Find the latest image in the folder, upload to ImgBB, verify, create container, and post."""
#     latest_image_path = get_latest_image(folder_path)
#     if not latest_image_path:
#         logging.error("❌ No image found to upload.")
#         return False

#     logging.info(f"📂 Latest image found: {latest_image_path}")

#     image_url = upload_to_imgbb(latest_image_path)
#     if not image_url:
#         logging.error("❌ Failed to upload image to ImgBB.")
#         return False

#     if not verify_image_url(image_url):
#         logging.error("❌ Uploaded ImgBB URL is not accessible. Stopping...")
#         return False

#     # Upload to S3 (optional step before posting)
#     s3_url = upload_to_s3(local_file_path=latest_image_path,
#                           bucket_name="ai-meme-bot-manthan",
#                           s3_file_name=os.path.basename(latest_image_path))
#     if not s3_url:
#         logging.error("❌ Failed to upload image to S3.")
#         return False

#     logging.info(f"✅ Image successfully uploaded to S3: {s3_url}")

#     container_id = create_instagram_media_container_from_url(s3_url, caption)
#     if not container_id:
#         logging.error("❌ Media container creation failed.")
#         return False

#     publish_id = publish_instagram_media(container_id)
#     if publish_id:
#         logging.info("✅ Image successfully published to Instagram!")
#         return True
#     else:
#         logging.error("❌ Failed to publish image to Instagram.")
#         return False

# # ================== Entry Point ==================

# if __name__ == "__main__":
#     folder_path = r"data\Final Post"  # Use double backslashes or raw string
#     caption = "Check out my latest Instagram post! 🚀"

#     # Example: Set your scheduled date and time here (24-hour format)
#     scheduled_time_str = "2025-04-26 22:30:00"  # Example: 26th April 2025, 10:30 PM

#     schedule_post(folder_path, caption, scheduled_time_str)
