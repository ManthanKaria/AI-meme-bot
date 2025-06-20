# image_downloader.py

import os
import hashlib
import requests
import concurrent.futures
from bs4 import BeautifulSoup
from scrapers.pexels_scraper import search_pexels_image, sanitize_filename

IMAGE_DIR = "data/memes/"
os.makedirs(IMAGE_DIR, exist_ok=True)

def get_image_hash(image_data):
    return hashlib.md5(image_data).hexdigest()

def download_single_image(img_url, sanitized_query, count, existing_hashes, source):
    try:
        img_data = requests.get(img_url, timeout=5).content
        img_hash = get_image_hash(img_data)

        if img_hash in existing_hashes:
            print(f"⚠️ Duplicate image detected, skipping.")
            return None

        existing_hashes.add(img_hash)
        file_path = os.path.join(IMAGE_DIR, f"{source}_{sanitized_query}_{count}.jpg")

        with open(file_path, "wb") as f:
            f.write(img_data)

        print(f"✅ Saved: {file_path}")
        return {
            "path": file_path,
            "query": sanitized_query,
            "source": source
        }

    except Exception as e:
        print(f"❌ Error downloading {img_url}: {e}")
        return None

def download_images_for_trend(query, source="google", limit=1, use_pexels=False):
    sanitized_query = sanitize_filename(query)

    if use_pexels:
        print(f"🔐 Safe Mode: Fetching from Pexels for query: {query}")
        filepath = search_pexels_image(query)
        if filepath:
            return [{
                "path": filepath,
                "query": sanitized_query,
                "source": "pexels"
            }]
        return []

    # Attempt Google search
    headers = {"User-Agent": "Mozilla/5.0"}
    search_url = f"https://www.google.com/search?q={query}&tbm=isch"

    try:
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"⚠️ Google fetch failed: {e} — falling back to Pexels...")
        return download_images_for_trend(query, use_pexels=True)

    soup = BeautifulSoup(response.text, "html.parser")
    img_tags = soup.find_all("img")[1:]  # Skipping the first (Google logo)

    downloaded_images = []
    existing_hashes = set()

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = {
            executor.submit(download_single_image, img.get("src"), sanitized_query, i + 1, existing_hashes, source): i
            for i, img in enumerate(img_tags[:limit])
            if img.get("src") and img.get("src").startswith("http")
        }

        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                downloaded_images.append(result)

    if not downloaded_images:
        print("⚠️ No valid images from Google. Trying Pexels...")
        return download_images_for_trend(query, use_pexels=True)

    return downloaded_images

def extract_title_from_filename(image_path):
    try:
        filename = os.path.basename(image_path)
        name_without_ext = os.path.splitext(filename)[0]
        cleaned_title = name_without_ext.replace("_", " ").strip()
        return cleaned_title
    except Exception as e:
        print(f"⚠️ Failed to extract title: {e}")
        return "Meme"

# ✅ Public function for external calls (e.g. from trend_selector)
def fetch_images_for_trends(trend_list, limit=1):
    """
    Accepts a list of trending titles and returns image pairs (Google + Pexels) per trend.
    """
    image_pairs = []

    for trend in trend_list:
        print(f"\n🚀 Fetching images for trend: {trend}")

        # Fetch from Google
        google_images = download_images_for_trend(trend, limit=limit, source="google", use_pexels=False)
        google_img_path = google_images[0]["path"] if google_images else None

        # Fetch from Pexels
        pexels_images = download_images_for_trend(trend, limit=1, source="pexels", use_pexels=True)
        pexels_img_path = pexels_images[0]["path"] if pexels_images else None

        if google_img_path and pexels_img_path and google_img_path != pexels_img_path:
            image_pairs.append({
                "title": trend,
                "img1": google_img_path,
                "img2": pexels_img_path
            })
        else:
            print(f"⚠️ Skipping '{trend}' — insufficient unique images.")

    return image_pairs


# 🧪 Standalone test
if __name__ == "__main__":
    test_trends = ["funny Elon Musk", "AI robots", "Cat memes"]
    results = fetch_images_for_trends(test_trends)
    for r in results:
        print(f"✅ Result: {r}")
