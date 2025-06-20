# import requests
# import os
# import re
# from PIL import Image
# from io import BytesIO

# PEXELS_API_KEY = "9w2i2kPw4kJd6a93b04JAoMcC8ySgpxbSm9GUOmohn8VhspIWefWeT8t"
# PEXELS_SEARCH_URL = "https://api.pexels.com/v1/search"

# def sanitize_filename(name):
#     """Removes invalid characters from filename."""
#     return re.sub(r'[^a-zA-Z0-9_-]', '_', name)

# def search_pexels_image(query, download_dir="data/memes/pexels"):
#     print("🔥 Script started")
#     headers = {
#         "Authorization": PEXELS_API_KEY
#     }
#     params = {
#         "query": query,
#         "per_page": 1
#     }

#     def truncate_filename(name, max_length=100):
#         return name[:max_length].rstrip("_")

#     if not query.lower().endswith(('.jpg', '.jpeg', '.png')):
#         query += ".jpg"

#     print(f"🔍 Searching Pexels for: {query}")
#     try:
#         response = requests.get(PEXELS_SEARCH_URL, headers=headers, params=params)
#         response.raise_for_status()

#         data = response.json()
#         photos = data.get("photos")
#         if not photos:
#             print("❌ No Pexels results.")
#             return None

#         image_url = photos[0]["src"]["large"]
#         print(f"📸 Pexels Image URL: {image_url}")

#         os.makedirs(download_dir, exist_ok=True)

#         raw_filename = f"{query}"
#         filename = sanitize_filename(truncate_filename(raw_filename))
#         filepath = os.path.join(download_dir, filename)

#         img_data = requests.get(image_url).content
#         with open(filepath, 'wb') as f:
#             f.write(img_data)

#         return filepath

#     except Exception as e:
#         print(f"❌ Error fetching image from Pexels: {e}")
#         return None

# if __name__ == "__main__":
#     test_query = "nature"
#     image_path = search_pexels_image(test_query)
#     print(f"✅ Test Image Path: {image_path}")
# scrapers/pexels_scraper.py

import os
import re
import requests

# 📸 Pexels API details
PEXELS_API_KEY = "9w2i2kPw4kJd6a93b04JAoMcC8ySgpxbSm9GUOmohn8VhspIWefWeT8t"
PEXELS_SEARCH_URL = "https://api.pexels.com/v1/search"
PEXELS_DOWNLOAD_DIR = "data/memes/pexels"
os.makedirs(PEXELS_DOWNLOAD_DIR, exist_ok=True)

def sanitize_filename(name):
    """Removes invalid characters from filename."""
    return re.sub(r'[^a-zA-Z0-9_-]', '_', name)

def search_pexels_image(query):
    """
    🔍 Search and download 1 image from Pexels based on query.
    🧠 Used to fetch REACTION images.
    ✅ Returns local filepath if successful, else None.
    """
    headers = {
        "Authorization": PEXELS_API_KEY
    }
    params = {
        "query": query,
        "per_page": 1
    }

    print(f"🔍 Searching Pexels for reaction image: '{query}'")

    try:
        response = requests.get(PEXELS_SEARCH_URL, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        photos = data.get("photos")

        if not photos:
            print("❌ No results found on Pexels.")
            return None

        image_url = photos[0]["src"]["large"]
        filename = sanitize_filename(query[:100]) + ".jpg"
        filepath = os.path.join(PEXELS_DOWNLOAD_DIR, filename)

        # Download and save image
        img_data = requests.get(image_url).content
        with open(filepath, 'wb') as f:
            f.write(img_data)

        print(f"✅ Reaction image saved: {filepath}")
        return filepath

    except Exception as e:
        print(f"❌ Error fetching image from Pexels: {e}")
        return None

# 🧪 Test
if __name__ == "__main__":
    test_query = "confused face reaction"
    image_path = search_pexels_image(test_query)
    print(f"🧪 Image Path: {image_path}")
