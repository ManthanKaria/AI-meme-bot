import requests
import os
from dotenv import load_dotenv

load_dotenv(".env")

IMGBB_API_KEY = os.getenv("IMGBB_API_KEY")


def upload_to_imgbb(image_path):
    if not IMGBB_API_KEY:
        print("❌ Error: ImgBB API key is not set.")
        return None

    if not os.path.exists(image_path):
        print(f"❌ Error: File not found at {image_path}")
        return None

    url = "https://api.imgbb.com/1/upload"
    try:
        with open(image_path, "rb") as file:
            files = {
                "image": file
            }
            payload = {
                "key": IMGBB_API_KEY
            }
            response = requests.post(url, data=payload, files=files)

        if response.status_code == 200:
            print("✅ ImgBB Response:", response.json())
            return response.json()["data"]["url"]
        else:
            print(f"❌ ImgBB upload failed. Status: {response.status_code}, Response: {response.text}")
            return None

    except Exception as e:
        print(f"❌ Exception during upload: {e}")
        return None

if __name__ == "__main__":
    image_path = "data/memes/merged/merged_Cat_memes.jpg"
    url = upload_to_imgbb(image_path)
    print("Uploaded URL:", url)

