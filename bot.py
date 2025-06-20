# from instagrapi import Client
# import json

# cl = Client()

# try:
#     with open("session.json", "r") as f:
#         session_data = json.load(f)
#     cl.set_settings(session_data)

#     if not cl.login_by_sessionid(session_data["authorization_data"]["sessionid"]):
#         raise Exception("Session expired. Please regenerate the session.")

#     print("✅ Logged in using session file!")

# except Exception as e:
#     print(f"❌ Error logging in: {e}")
#     exit()

# # Your bot logic here...

# from instagrapi import Client
# import json
# import os

# cl = Client()

# try:
#     # ✅ Load the full settings from session.json
#     if os.path.exists("session.json"):
#         with open("session.json", "r") as f:
#             settings = json.load(f)
#         cl.set_settings(settings)

#     # ✅ Attempt login using saved session (automatically uses sessionid)
#     cl.login("your_username", "your_password")

#     # ✅ Save session after login (fresh tokens, avoids expiration)
#     with open("session.json", "w") as f:
#         json.dump(cl.get_settings(), f)

#     print("✅ Logged in successfully using session (auto-refreshed).")

# except Exception as e:
#     print(f"❌ Login failed: {e}")
# instagram_post.py
import requests
from dotenv import load_dotenv
import os
load_dotenv(".env")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
INSTAGRAM_USER_ID=os.getenv("INSTAGRAM_USER_ID")

def create_container(image_url, caption):
    endpoint = f"https://graph.instagram.com/v22.0/{INSTAGRAM_USER_ID}/media"
    payload = {
        "image_url": image_url,
        "caption": caption,
        "access_token": ACCESS_TOKEN
    }
    res = requests.post(endpoint, data=payload)
    return res.json().get("id")

def publish_container(container_id):
    endpoint = f"https://graph.instagram.com/v22.0/{INSTAGRAM_USER_ID}/media_publish"
    payload = {
        "creation_id": container_id,
        "access_token": ACCESS_TOKEN
    }
    res = requests.post(endpoint, data=payload)
    return res.json()
