import os

# 🔹 AI APIs (Free & Unlimited)
HUGGING_FACE_API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base"
HUGGING_FACE_HEADERS = {"Authorization": f"Bearer {os.getenv('HUGGING_FACE_KEY')}"}

GEMINI_API_KEY = "Your_Gemeni_API"
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-latest:generateContent?key=Your_Gemeni_API"
GEMINI_HEADERS = {
    "Content-Type": "application/json",
}
# 🔹 Pexel APIs (Free & Unlimited images)
PEXELS_API_KEY = "YOUR_PIXEL_API"
PEXELS_SEARCH_URL = "https://api.pexels.com/v1/search"

# 🔹 Paths
MEME_DIR = "data/memes/"
VIRAL_MEME_DIR = "data/viral_memes/"

