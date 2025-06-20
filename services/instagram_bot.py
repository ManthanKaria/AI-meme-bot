# import requests
# import logging
# import os
# from dotenv import load_dotenv

# load_dotenv(".env")

# ACCESS_TOKEN = os.getenv("INSTAGRAM_GRAPH_TOKEN")
# IMGBB_API_KEY = os.getenv("IMGBB_API_KEY")
# IG_BUSINESS_ID = "your_instagram_business_id"  # Replace with actual
# GRAPH_API_BASE = "https://graph.facebook.com/v19.0"
# ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
# IG_USER_ID = os.getenv("IG_USER_ID")
# IMGBB_API_KEY = os.getenv("IMGBB_API_KEY")

# # Test printing to verify
# print("Access Token:", ACCESS_TOKEN)
# print("Instagram User ID:", IG_USER_ID)
# print("ImgBB API Key:", IMGBB_API_KEY)
# # Function to upload image to ImgBB and get hosted URL
# def upload_to_imgbb(image_path):
#     try:
#         url = "https://api.imgbb.com/1/upload"
#         with open(image_path, "rb") as file:
#             files = {
#                 "image": file.read()
#             }
#         payload = {
#             "key": IMGBB_API_KEY,
#         }
#         response = requests.post(url, files=files, data=payload)
#         response.raise_for_status()
#         return response.json()["data"]["url"]
#     except Exception as e:
#         logging.error(f"❌ ImgBB upload failed: {e}")
#         return None

# Function to upload image to Instagram using Graph API
# def upload_image_to_instagram(image_url, caption):
#     try:
#         # Step 1: Create media container
#         create_url = f"{GRAPH_API_BASE}/{IG_BUSINESS_ID}/media"
#         payload = {
#             "image_url": image_url,
#             "caption": caption,
#             "access_token": ACCESS_TOKEN
#         }
#         res = requests.post(create_url, data=payload)
#         res_json = res.json()

#         if "id" not in res_json:
#             logging.error(f"❌ Failed to create container: {res_json}")
#             return False

#         creation_id = res_json["id"]
#         logging.info(f"✅ Created IG media container: {creation_id}")

#         # Step 2: Publish the container
#         publish_url = f"{GRAPH_API_BASE}/{IG_BUSINESS_ID}/media_publish"
#         publish_payload = {
#             "creation_id": creation_id,
#             "access_token": ACCESS_TOKEN
#         }

#         publish_res = requests.post(publish_url, data=publish_payload)
#         publish_json = publish_res.json()

#         if "id" in publish_json:
#             logging.info(f"✅ Successfully posted! Post ID: {publish_json['id']}")
#             return True
#         else:
#             logging.error(f"❌ Failed to publish media: {publish_json}")
#             return False

#     except Exception as e:
#         logging.exception(f"❌ Error during Instagram upload: {e}")
#         return False
# import requests
# import logging
# import os
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv(".env")

# # Load secrets
# ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")  # Unified naming
# IG_USER_ID = os.getenv("IG_USER_ID")
# IMGBB_API_KEY = os.getenv("IMGBB_API_KEY")

# GRAPH_API_BASE = "https://graph.instagram.com/v22.0"
# # GRAPH_API_BASE = "https://graph.facebook.com/v19.0"

# # Log to verify tokens loaded
# # if not all([ACCESS_TOKEN, IG_USER_ID, IMGBB_API_KEY]):
# #     logging.error("❌ Missing environment variables. Check .env file.")
# if not all([ACCESS_TOKEN, IG_USER_ID, IMGBB_API_KEY]):
#     raise EnvironmentError("❌ Missing essential env vars. Fix .env file.")

# # Upload image to ImgBB and return the hosted URL
# def upload_image_to_imgbb(image_path):
#     """Temporarily upload the image to imgbb and return the public URL."""
#     try:
#         imgbb_api_key = IMGBB_API_KEY  # You must register for this
#         with open(image_path, "rb") as file:
#             payload = {
#                 "key": imgbb_api_key,
#                 "image": file.read(),
#             }
#         response = requests.post("https://api.imgbb.com/1/upload", files={}, data=payload)
#         res_json = response.json()

#         if response.status_code == 200 and "data" in res_json:
#             return res_json["data"]["url"]
#         else:
#             logging.error(f"❌ Imgbb upload failed: {res_json}")
#             return None
#     except Exception as e:
#         logging.exception(f"❌ Exception during Imgbb upload: {e}")
#         return None
    
# import os
# import requests
# import logging
# from services.imgbb_uploader import upload_to_imgbb
# # Assumed these are already defined elsewhere in your project
# # from your_config import GRAPH_API_BASE, IG_USER_ID, ACCESS_TOKEN
# # from your_upload_module import upload_image_to_imgbb

# def upload_image_to_instagram_local(image_path, caption):
#     """
#     Uploads an image to Instagram using a temporary image host (e.g., ImgBB).
    
#     Parameters:
#         image_path (str): Local path to the image.
#         caption (str): Caption to be posted along with the image.
    
#     Returns:
#         bool: True if successfully posted, False otherwise.
#     """
#     if not os.path.exists(image_path):
#         logging.error(f"❌ Image file does not exist: {image_path}")
#         return False

#     print(f"📤 Uploading image from local path: {image_path}")

#     # Step 1: Upload to temporary hosting to get a public image URL
#     image_path = "data/Final Post\merged_....jpg"
#     # image_path="data\Final Post\merged_google_The_Times_today_1_formatted_HD.jpg"
#     image_url = upload_to_imgbb(image_path)
#     if not image_url:
#         logging.error("❌ Could not generate public image URL.")
#         return False

#     print(f"🌐 Public URL received: {image_url}")

#     try:
#         # Step 2: Create media container
#         create_url = f"{GRAPH_API_BASE}/{IG_USER_ID}/media"
#         create_payload = {
#             "image_url": image_url,
#             "caption": caption,
#             "access_token": ACCESS_TOKEN
#         }

#         create_response = requests.post(create_url, data=create_payload)
#         create_json = create_response.json()

#         if "id" not in create_json:
#             logging.error(f"❌ Failed to create IG media container: {create_json}")
#             return False

#         creation_id = create_json["id"]
#         logging.info(f"✅ Media container created: {creation_id}")

#         # Step 3: Publish the media
#         publish_url = f"{GRAPH_API_BASE}/{IG_USER_ID}/media_publish"
#         publish_payload = {
#             "creation_id": creation_id,
#             "access_token": ACCESS_TOKEN
#         }

#         publish_response = requests.post(publish_url, data=publish_payload)
#         publish_json = publish_response.json()

#         if "id" in publish_json:
#             logging.info(f"✅ Post published successfully! Post ID: {publish_json['id']}")
#             return True
#         else:
#             logging.error(f"❌ Media publish failed: {publish_json}")
#             return False

#     except requests.exceptions.RequestException as req_err:
#         logging.exception(f"❌ Network error during Instagram upload: {req_err}")
#     except Exception as e:
#         logging.exception(f"❌ Unexpected exception during Instagram upload: {e}")
    
#     return False





import requests
import logging
import os
import glob
import time
from dotenv import load_dotenv
from services.imgbb_uploader import upload_to_imgbb
import boto3

# ================== Load environment variables ==================
load_dotenv(".env")

creds = dict()  # dictionary to hold credentials
creds['ACCESS_TOKEN'] = os.getenv("ACCESS_TOKEN")
creds['instagram_account_id'] = os.getenv("IG_USER_ID")
creds['graph_domain'] = 'https://graph.instagram.com/'
creds['graph_version'] = 'v22.0'
creds['endpoint_base'] = creds['graph_domain'] + creds['graph_version'] + '/'
IMGBB_API_KEY = os.getenv("IMGBB_API_KEY")  # ImgBB API key

# ================== Configure logging ==================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ================== Utility Functions ==================

def get_latest_image(folder_path):
    """Get the latest JPG image from the specified folder."""
    files = glob.glob(os.path.join(folder_path, "*.jpg"))
    if not files:
        logging.error(f"❌ No images found in folder: {folder_path}")
        return None
    latest_file = max(files, key=os.path.getctime)
    return latest_file

def verify_image_url(image_url):
    """Verify if the ImgBB image URL is reachable."""
    try:
        response = requests.head(image_url)
        if response.status_code == 200:
            logging.info(f"✅ Verified ImgBB URL is reachable.")
            return True
        else:
            logging.error(f"❌ ImgBB URL is not reachable. Status code: {response.status_code}")
            return False
    except Exception as e:
        logging.exception(f"❌ Exception while verifying ImgBB URL: {e}")
        return False

def create_instagram_media_container_from_url(image_url, caption):
    """Create media container using the ImgBB image URL."""
    try:
        url = f"{creds['endpoint_base']}{creds['instagram_account_id']}/media"
        logging.info(f"📤 Creating media container from ImgBB URL.")

        data = {
            'image_url': image_url,
            'caption': caption,
            'access_token': creds['ACCESS_TOKEN']
        }

        response = requests.post(url, data=data)
        response_json = response.json()

        if response.status_code == 200 and "id" in response_json:
            container_id = response_json["id"]
            logging.info(f"✅ Media container created. ID: {container_id}")
            return container_id
        else:
            logging.error(f"❌ Failed to create media container. Response: {response_json}")
            return None

    except Exception as e:
        logging.exception(f"❌ Exception while creating media container: {e}")
        return None

def publish_instagram_media(container_id):
    """Publish the created media container on Instagram."""
    try:
        publish_url = f"{creds['endpoint_base']}{creds['instagram_account_id']}/media_publish"
        payload = {
            "creation_id": container_id,
            "access_token": creds['ACCESS_TOKEN']
        }

        logging.info("⏳ Waiting before publishing (5 seconds as per IG guidelines)...")
        time.sleep(5)  # Respect Instagram's advice before publishing

        response = requests.post(publish_url, data=payload)
        response_json = response.json()

        if response.status_code == 200 and "id" in response_json:
            post_id = response_json["id"]
            logging.info(f"✅ Post published successfully! Post ID: {post_id}")
            return post_id
        else:
            logging.error(f"❌ Failed to publish media. Response: {response_json}")
            return None

    except Exception as e:
        logging.exception(f"❌ Exception while publishing media: {e}")
        return None

def upload_to_s3(local_file_path, bucket_name, s3_file_name):
    """Upload an image to AWS S3 and return the public URL."""
    s3 = boto3.client('s3')
    try:
        s3.upload_file(local_file_path, bucket_name, s3_file_name)
        region = s3.get_bucket_location(Bucket=bucket_name)['LocationConstraint']
        if region is None:
            region = 'ap-south-1'  # Default for N. Virginia
        s3_url = f"https://{bucket_name}.s3.{region}.amazonaws.com/{s3_file_name}"
        return s3_url
    except Exception as e:
        print("Upload failed:", e)
        return None

# ================== Main Function ==================

def upload_latest_local_image(folder_path, caption):
    """Find the latest image in the folder, upload to ImgBB, verify, create container, and post."""
    latest_image_path = get_latest_image(folder_path)
    if not latest_image_path:
        logging.error("❌ No image found to upload.")
        return False

    logging.info(f"📂 Latest image found: {latest_image_path}")

    # Step 1: Upload to ImgBB
    image_url_imgbb = upload_to_imgbb(latest_image_path)
    if not image_url_imgbb:
        logging.error("❌ Failed to upload image to ImgBB.")
        return False

    # Step 2: Upload to S3
    s3_url = upload_to_s3(local_file_path=latest_image_path,
                          bucket_name="ai-meme-bot-manthan",
                          s3_file_name=os.path.basename(latest_image_path))
    if not s3_url:
        logging.error("❌ Failed to upload image to S3.")
        return False

    logging.info(f"✅ Image successfully uploaded to S3: {s3_url}")

    # Step 3: Verify ImgBB URL (keeping ImgBB as fallback or for Gemini analysis)
    if not verify_image_url(image_url_imgbb):
        logging.error("❌ Uploaded ImgBB URL is not accessible. Stopping...")
        return False

    # Step 4: Create media container using S3 URL (Instagram will use this)
    container_id = create_instagram_media_container_from_url(s3_url, caption)
    if not container_id:
        logging.error("❌ Media container creation failed.")
        return False

    # Step 5: Publish the post on Instagram
    publish_id = publish_instagram_media(container_id)
    if publish_id:
        logging.info("✅ Image successfully published to Instagram!")
        return True
    else:
        logging.error("❌ Failed to publish image to Instagram.")
        return False
# Upload image to Instagram via Graph API


def upload_image_to_instagram(image_url, caption):
    try:
        # Step 1: Create media container
        create_url = f"{creds['graph_domain']}/{creds['instagram_account_id']}/media"
        payload = {
            "image_url": image_url,
            "caption": caption,
            "access_token": creds['ACCESS_TOKEN']
        }
        res = requests.post(create_url, data=payload)
        res_json = res.json()

        if "id" not in res_json:
            logging.error(f"❌ Failed to create container: {res_json}")
            return False

        creation_id = res_json["id"]
        logging.info(f"✅ Created IG media container: {creation_id}")

        # Step 2: Publish the container
        publish_url = f"{creds['graph_domain']}/{creds['instagram_account_id']}/media_publish"
        publish_payload = {
            "creation_id": creation_id,
            "access_token": creds['ACCESS_TOKEN']
        }

        publish_res = requests.post(publish_url, data=publish_payload)
        publish_json = publish_res.json()

        if "id" in publish_json:
            logging.info(f"✅ Successfully posted! Post ID: {publish_json['id']}")
            return True
        else:
            logging.error(f"❌ Failed to publish media: {publish_json}")
            return False

    except Exception as e:
        logging.exception(f"❌ Error during Instagram upload: {e}")
        return False
# ================== Entry Point ==================

if __name__ == "__main__":
    folder_path = r"data\Final Post"  # Use double backslashes or raw string
    caption = "Check out my latest Instagram post! 🚀"

    upload_success = upload_latest_local_image(folder_path, caption)

    if upload_success:
        logging.info("✅ Script completed successfully.")
    else:
        logging.error("❌ Script failed.")
