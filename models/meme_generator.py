# import os
# import requests
# import textwrap
# import cv2
# import numpy as np
# from PIL import Image, ImageDraw, ImageFont
# from scrapers.trend_selector import select_trending_topic
# from config.config import GEMINI_API_URL, GEMINI_HEADERS
# import time
# import base64
# # --------------- Helper Functions ---------------
# def get_font(font_name="arial.ttf", size=24):
#     try:
#         return ImageFont.truetype(font_name, size)
#     except:
#         return ImageFont.load_default()

# def clean_caption(text):
#     import re
#     text = re.sub(r"\*\*|[*_]", "", text)
#     text = re.sub(r"^Option\s*\d+.*?:\s*", "", text, flags=re.IGNORECASE)
#     text = re.sub(r"^\s*(Hinglish|English|Sarcastic|Funny)?\s*[:\-–—]?\s*", "", text, flags=re.IGNORECASE)
#     return text.strip()

# def log_gemini_response(prompt, ai_caption):
#     log_dir = "logs"
#     os.makedirs(log_dir, exist_ok=True)
#     with open(os.path.join(log_dir, "gemini_responses.log"), "a", encoding="utf-8") as f:
#         f.write(f"\n\nPrompt: {prompt.strip()}\nResponse: {ai_caption.strip()}\n{'-' * 50}")

# # --------------- AI Caption Generator ---------------
# # def generate_ai_caption(title):
# #     prompt = f"""
# # You are a witty, sarcastic meme creator. 
# # Based on the trending meme title: "{title}", write 1 logically funny and relatable caption in Hinglish or English.
# # Avoid numbering like 'Option 1', and don't use formatting like ** or *.
# # Just write the punchline caption.
# # Then add a '#' separated list of 5-7 Instagram hashtags on a new line.
# #     """

# #     data = { "contents": [{ "parts": [{ "text": prompt.strip() }] }] }

# #     try:
# #         response = requests.post(GEMINI_API_URL, headers=GEMINI_HEADERS, json=data)

# #         if response.status_code == 429:
# #             print("❌ Gemini API quota exceeded. Waiting 30s before retrying...")
# #             time.sleep(30)  # Retry after wait
# #             return generate_ai_caption(title)

# #         elif response.status_code == 200:
# #             response_data = response.json()
# #             ai_output = response_data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "").strip()

# #             if "\n" in ai_output:
# #                 main_text, hashtags = ai_output.split("\n", 1)
# #             else:
# #                 main_text = ai_output
# #                 hashtags = "#meme #funny #relatable #trending #humor"

# #             meme_caption = clean_caption(main_text)
# #             full_caption = f"{meme_caption.strip()}\n\n{hashtags.strip()}"
# #             log_gemini_response(prompt, full_caption)
# #             return meme_caption, full_caption

# #         else:
# #             print(f"❌ Gemini API error: {response.status_code} - {response.text}")
# #             return "When Gemini naps 😂", "When Gemini naps 😂\n\n#meme #funny #fail"

# #     except Exception as e:
# #         print(f"⚠️ Exception in caption generation: {e}")
# #         return "Oops, meme forgot its punchline 😅", "Oops, meme forgot its punchline 😅\n\n#fail"

# import os
# import mimetypes
# import base64
# import requests
# import time

# # Make sure these are defined
# # GEMINI_API_URL = "..."  
# # GEMINI_HEADERS = { "Authorization": "Bearer <your-token>" }

# def get_image_base64(image_path): 
#     try:
#         image_path = image_path.replace('\\', '/')
#         if not os.path.exists(image_path):
#             print(f"[ERROR] File does not exist: {image_path}")
#             return ""

#         mime_type, _ = mimetypes.guess_type(image_path)
#         mime_type = mime_type or "application/octet-stream"

#         with open(image_path, "rb") as image_file:
#             encoded = base64.b64encode(image_file.read()).decode("utf-8").strip()
#             print(f"[DEBUG] Image successfully encoded to base64.")
#             return encoded
#     except Exception as e:
#         print(f"[ERROR] Failed to convert {image_path} to base64: {e}")
#         return ""


# def generate_ai_caption_with_image(title, image_url):
#     prompt_text = f"""
#     You are a witty, sarcastic meme creator.
#     Create a meme caption based on this image and the trending meme title: "{title}".
#     Write 1 logically funny and relatable caption in Hinglish or English.
#     Avoid numbering and formatting. Just write the punchline caption.
#     Then add a '#' separated list of 5-7 Instagram hashtags on a new line.
#     """

#     encoded_image = get_image_base64(image_url)
#     if not encoded_image:
#         print("[ERROR] Failed to encode image.")
#         return "Image error 🖼️", "Image error 🖼️\n\n#meme #error"

#     data = {
#         "contents": [
#             {
#                 "parts": [
#                     {"text": prompt_text.strip()},
#                     {
#                     "inline_data": {
#                         "mime_type": "image/jpeg",
#                         "data": encoded_image  # ONLY the base64 string here
#                     }
#                     }

#                 ]
#             }
#         ]
#     }

#     try:
#         response = requests.post(GEMINI_API_URL, headers=GEMINI_HEADERS, json=data)

#         if response.status_code == 429:
#             print("❌ Gemini API quota exceeded. Waiting 30s before retrying...")
#             time.sleep(30)
#             return generate_ai_caption_with_image(title, image_url)

#         elif response.status_code == 200:
#             response_data = response.json()
#             ai_output = response_data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "").strip()

#             if "\n" in ai_output:
#                 main_text, hashtags = ai_output.split("\n", 1)
#             else:
#                 main_text = ai_output
#                 hashtags = "#meme #funny #relatable #trending #humor"

#             meme_caption = clean_caption(main_text)
#             full_caption = f"{meme_caption.strip()}\n\n{hashtags.strip()}"
#             log_gemini_response(prompt_text, full_caption)
#             return meme_caption, full_caption

#         else:
#             print(f"❌ Gemini API error: {response.status_code} - {response.text}")
#             return "When Gemini naps 😂", "When Gemini naps 😂\n\n#meme #funny #fail"

#     except Exception as e:
#         print(f"⚠️ Exception in caption generation: {e}")
#         return "Oops, meme forgot its punchline 😅", "Oops, meme forgot its punchline 😅\n\n#fail"


    
# # --------------- Merge Images ---------------
# def merge_images(img_path1, img_path2, mode='horizontal', output_name=None):
#     MERGED_DIR = "data/memes/merged"
#     os.makedirs(MERGED_DIR, exist_ok=True)

#     try:
#         img1 = Image.open(img_path1)
#         img2 = Image.open(img_path2)

#         if mode == 'horizontal':
#             if img1.height != img2.height:
#                 img2 = img2.resize((int(img2.width * img1.height / img2.height), img1.height))
#             merged_img = Image.new('RGB', (img1.width + img2.width, img1.height))
#             merged_img.paste(img1, (0, 0))
#             merged_img.paste(img2, (img1.width, 0))
#         else:
#             if img1.width != img2.width:
#                 img2 = img2.resize((img1.width, int(img2.height * img1.width / img2.width)))
#             merged_img = Image.new('RGB', (img1.width, img1.height + img2.height))
#             merged_img.paste(img1, (0, 0))
#             merged_img.paste(img2, (0, img1.height))

#         output_name = output_name or f"merged_{os.path.basename(img_path1)}"
#         output_path = os.path.join(MERGED_DIR, output_name)
#         merged_img.save(output_path)
#         return output_path
#     except Exception as e:
#         print(f"❌ Error merging images: {e}")
#         return None

# # --------------- Add Text on Meme ---------------
# def add_meme_text(image_path, text):
#     try:
#         if not text:
#             print("⚠️ Skipping text addition: No meme text provided.")
#             return image_path

#         image = Image.open(image_path).convert("RGB")
#         width = image.width
#         font_size = max(36, width // 18)
#         font = get_font("arialbd.ttf", font_size)

#         wrapper = textwrap.TextWrapper(width=40)
#         wrapped_text = wrapper.fill(text=text)

#         dummy_img = Image.new("RGB", (width, 1000))
#         dummy_draw = ImageDraw.Draw(dummy_img)
#         text_bbox = dummy_draw.textbbox((0, 0), wrapped_text, font=font)
#         text_height = text_bbox[3] - text_bbox[1]
#         padding = 40

#         new_img = Image.new("RGB", (width, text_height + padding + image.height), "white")
#         draw = ImageDraw.Draw(new_img)
#         text_x = (width - (text_bbox[2] - text_bbox[0])) // 2
#         draw.text((text_x, padding // 2), wrapped_text, font=font, fill="black")
#         new_img.paste(image, (0, text_height + padding))

#         output_path = image_path.replace("memes", "viral_memes").replace(".jpg", ".png")
#         os.makedirs(os.path.dirname(output_path), exist_ok=True)
#         new_img.save(output_path, format="PNG", quality=100)
#         return output_path

#     except Exception as e:
#         print(f"⚠️ Error adding text: {e}")
#         return image_path

# # --------------- Resize for Instagram ---------------
# def format_image_for_instagram(image_path, caption_text, max_width=1080, padding=50, font_path="arial.ttf"):
#     try:
#         image = Image.open(image_path).convert("RGB")
        
#         # Resize image to fit width
#         aspect_ratio = image.height / image.width
#         new_width = max_width
#         new_height = int(aspect_ratio * new_width)
#         image = image.resize((new_width, new_height))

#         if not caption_text:
#             print("⚠️ No caption provided, skipping caption formatting.")
#             output_path = image_path.replace(".png", "_formatted.jpg")
#             image.save(output_path, "JPEG")
#             return output_path

#         # Setup caption
#         font_size = 40
#         font = ImageFont.truetype(font_path, font_size)
#         draw = ImageDraw.Draw(image)
        
#         # Estimate caption height
#         max_caption_width = new_width - 2 * padding
#         words = caption_text.split()
#         lines = []
#         line = ""
#         for word in words:
#             test_line = f"{line} {word}".strip()
#             w, h = draw.textbbox((0, 0), test_line, font=font)[2:]
#             if w <= max_caption_width:
#                 line = test_line
#             else:
#                 lines.append(line)
#                 line = word
#         lines.append(line)
#         caption_height = (len(lines) * (font_size + 10)) + padding
#         caption_height = min(caption_height, 400)

#         # Create final canvas
#         final_height = new_height + caption_height
#         final_image = Image.new("RGB", (new_width, final_height), (0, 0, 0))
#         final_image.paste(image, (0, 0))

#         # Draw caption
#         draw = ImageDraw.Draw(final_image)
#         y = new_height + (padding // 2)
#         for line in lines:
#             w, _ = draw.textbbox((0, 0), line, font=font)[2:]
#             x = (new_width - w) // 2
#             draw.text((x, y), line, font=font, fill="white")
#             y += font_size + 10

#         # Save
#         output_path = image_path.replace(".png", "_formatted.jpg")
#         final_image.save(output_path, "JPEG")
#         return output_path

#     except Exception as e:
#         print(f"⚠️ Error formatting image: {e}")
#         return None


# # --------------- Upscale Image ---------------
# def upscale_image(image_path, scale=2):
#     try:
#         image = cv2.imread(image_path)
#         height, width = image.shape[:2]
#         upscaled = cv2.resize(image, (width * scale, height * scale), interpolation=cv2.INTER_CUBIC)
#         sharpen_kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
#         sharpened = cv2.filter2D(upscaled, -1, sharpen_kernel)
#         output_path = image_path.replace(".jpg", "_HD.jpg").replace(".png", "_HD.jpg")
#         cv2.imwrite(output_path, sharpened, [cv2.IMWRITE_JPEG_QUALITY, 95])
#         return output_path
#     except Exception as e:
#         print(f"⚠️ Error upscaling: {e}")
#         return image_path

# # --------------- Add Instagram Caption ---------------
# def add_caption_to_image(image_path, caption_text):
#     try:
#         image = Image.open(image_path).convert("RGB")
#         draw = ImageDraw.Draw(image)

#         # Load font
#         try:
#             font = ImageFont.truetype("arial.ttf", 36)
#         except IOError:
#             font = ImageFont.load_default()

#         width, height = image.size
#         margin = 20
#         max_width = width - 2 * margin

#         # Wrap text into multiple lines
#         lines = textwrap.wrap(caption_text, width=40)
#         line_height = font.getsize('A')[1] + 10
#         text_height = line_height * len(lines)

#         # Draw semi-transparent rectangle as background
#         overlay = Image.new('RGBA', image.size, (0, 0, 0, 0))
#         overlay_draw = ImageDraw.Draw(overlay)
#         overlay_draw.rectangle(
#             [(0, height - text_height - margin), (width, height)],
#             fill=(0, 0, 0, 180)  # semi-transparent black
#         )
#         image = Image.alpha_composite(image.convert("RGBA"), overlay)

#         # Draw text with outline
#         draw = ImageDraw.Draw(image)
#         y_text = height - text_height - margin + 5
#         for line in lines:
#             text_width = font.getsize(line)[0]
#             x = (width - text_width) / 2

#             # Outline
#             draw.text((x - 1, y_text - 1), line, font=font, fill="black")
#             draw.text((x + 1, y_text - 1), line, font=font, fill="black")
#             draw.text((x - 1, y_text + 1), line, font=font, fill="black")
#             draw.text((x + 1, y_text + 1), line, font=font, fill="black")

#             # Main text
#             draw.text((x, y_text), line, font=font, fill="white")
#             y_text += line_height

#         # Save result
#         base, _ = os.path.splitext(image_path)
#         output_path = f"{base}_MEME.jpg"
#         image.convert("RGB").save(output_path, format="JPEG", quality=95)

#         return output_path

#     except Exception as e:
#         print(f"⚠️ Error adding caption: {e}")
#         return image_path

# # --------------- Meme Generator Orchestration ---------------
# def create_final_meme(img1, img2, title, image_url=None, caption=None):
#     print("🚀 Creating meme from:", img1, img2)

#     # Sanity check - file existence
#     if not os.path.exists(img1) or not os.path.exists(img2):
#         print("❌ One or both image paths are invalid.")
#         return None

#     # Step 1: Merge images
#     merged_path = merge_images(img1, img2, mode="horizontal")
#     if not merged_path or not os.path.exists(merged_path):
#         print("❌ Failed to merge images. Skipping...")
#         return None

#     # Step 2: Generate meme text from image
#     image_url = image_url or img2
#     if not image_url or not os.path.exists(image_url):
#         print(f"[ERROR] image_url is invalid or does not exist: {image_url}")
#         return None
    
#     meme_with_text = add_meme_text(merged_path, caption)
#     if meme_with_text is None:
#         print("⚠️ add_meme_text failed.")
#         return None
    
#     # Step 4: Resize + Upscale
#     final_insta_meme = format_image_for_instagram(meme_with_text, caption_text=caption)
#     if final_insta_meme is None:
#         print("⚠️ format_image_for_instagram failed.")
#         return None

#     final_hd = upscale_image(final_insta_meme)
#     if final_hd is None:
#         print("⚠️ upscale_image failed.")
#         return None

#     print(f"✅ Final Meme Ready: {final_hd}")
#     return final_hd


# # --------------- AI Text Short Meme (for overlay only) ---------------
# def generate_meme_text_ai(meme_title):
#     prompt = f"""
# You are a meme layout expert. 
# You are given this meme idea: "{meme_title}"
# Write just the exact meme text that should be displayed on the image — keep it in Hinglish or English, funny, clean, and without hashtags or numbering.
# Make sure it looks good above the image and fits well within Instagram format.
# """
#     data = {"contents": [{"parts": [{"text": prompt.strip()}]}]}
#     try:
#         response = requests.post(GEMINI_API_URL, headers=GEMINI_HEADERS, json=data)
#         if response.status_code == 200:
#             return response.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
#         else:
#             print(f"❌ Gemini API error: {response.status_code}")
#             return meme_title
#     except Exception as e:
#         print(f"⚠️ Error with Gemini: {e}")
#         return meme_title

# # ----------------- Test Run -----------------
# if __name__ == "__main__":
#     g_img = "data/memes/google_cat.jpg"
#     p_img = "data/memes/pexels_cat.jpg"
#     idea = "When your code finally runs without error"
#     caption = "Made with ChatGPT ❤️"

#     create_final_meme(g_img, p_img, idea, caption)
import os
import mimetypes
import base64
import requests
import time
import textwrap
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

# ---------- CONFIGURATION ----------
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-latest:generateContent?key=AIzaSyCABC7nUV8y-pgJGbM8KnviGrAVNX8zK5U"
GEMINI_HEADERS = {
    "Content-Type": "application/json",
}


# ---------- UTILITY FUNCTIONS ----------
def get_image_base64(image_path):
    try:
        image_path = image_path.replace('\\', '/')
        if not os.path.exists(image_path):
            print(f"[ERROR] File does not exist: {image_path}")
            return ""
        mime_type, _ = mimetypes.guess_type(image_path)
        mime_type = mime_type or "application/octet-stream"
        with open(image_path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode("utf-8").strip()
        return encoded
    except Exception as e:
        print(f"[ERROR] Failed to convert {image_path} to base64: {e}")
        return ""


def clean_caption(text):
    return text.replace("*", "").replace("**", "").strip()


def log_gemini_response(prompt, response):
    print(f"\n📜 Prompt Sent:\n{prompt}\n\n🎯 Gemini Response:\n{response}\n")


# ---------- GEMINI AI CAPTION ----------
def generate_ai_caption_with_image(title, image_path):
    prompt_text = f"""
    You are a witty, sarcastic meme creator.
    Create a meme caption based on this image and the trending meme title: "{title}".
    Write 1 logically funny and relatable caption in Hinglish or English.
    Avoid numbering and formatting. Just write the punchline caption.
    Then add a '#' separated list of 5-7 Instagram hashtags on a new line.
    """
    encoded_image = get_image_base64(image_path)
    if not encoded_image:
        return "Image error 🖼️", "Image error 🖼️\n\n#meme #error"

    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt_text.strip()},
                    {
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": encoded_image
                        }
                    }
                ]
            }
        ]
    }

    try:
        response = requests.post(GEMINI_API_URL, headers=GEMINI_HEADERS, json=data)

        if response.status_code == 429:
            print("❌ Gemini API quota exceeded. Retrying in 30s...")
            time.sleep(30)
            return generate_ai_caption_with_image(title, image_path)

        elif response.status_code == 200:
            response_data = response.json()
            ai_output = response_data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "").strip()

            if "\n" in ai_output:
                main_text, hashtags = ai_output.split("\n", 1)
            else:
                main_text = ai_output
                hashtags = "#meme #funny #relatable #trending #humor"

            meme_caption = clean_caption(main_text)
            full_caption = f"{meme_caption.strip()}\n\n{hashtags.strip()}"
            log_gemini_response(prompt_text, full_caption)
            return meme_caption, full_caption

        else:
            print(f"❌ Gemini API error: {response.status_code} - {response.text}")
            return "When Gemini naps 😂", "When Gemini naps 😂\n\n#meme #funny #fail"

    except Exception as e:
        print(f"⚠️ Exception in caption generation: {e}")
        return "Oops, meme forgot its punchline 😅", "Oops, meme forgot its punchline 😅\n\n#fail"


# ---------- IMAGE MANIPULATIONS ----------
def merge_images(img_path1, img_path2, mode='horizontal'):
    try:
        img1 = Image.open(img_path1)
        img2 = Image.open(img_path2)

        if mode == 'horizontal':
            img2 = img2.resize((int(img2.width * img1.height / img2.height), img1.height))
            merged_img = Image.new('RGB', (img1.width + img2.width, img1.height))
            merged_img.paste(img1, (0, 0))
            merged_img.paste(img2, (img1.width, 0))
        else:
            img2 = img2.resize((img1.width, int(img2.height * img1.width / img2.width)))
            merged_img = Image.new('RGB', (img1.width, img1.height + img2.height))
            merged_img.paste(img1, (0, 0))
            merged_img.paste(img2, (0, img1.height))

        output_path = f"data/memes/merged/merged_{os.path.basename(img_path1)}"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        merged_img.save(output_path)
        return output_path
    except Exception as e:
        print(f"❌ Error merging images: {e}")
        return None


def add_meme_text(image_path, text):
    try:
        image = Image.open(image_path).convert("RGB")
        width, height = image.size

        font_size = max(28, width // 25)
        font = ImageFont.truetype("arialbd.ttf", font_size)

        wrapper = textwrap.TextWrapper(width=40)
        wrapped_text = wrapper.fill(text=text)

        draw = ImageDraw.Draw(image)
        # Use multiline-compatible bbox
        text_bbox = draw.textbbox((0, 0), wrapped_text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        padding = 30
        new_img = Image.new("RGB", (width, height + text_height + padding), "black")
        new_img.paste(image, (0, 0))

        draw = ImageDraw.Draw(new_img)
        text_x = (width - text_width) // 2
        text_y = height + (padding // 2)

        draw.text((text_x, text_y), wrapped_text, font=font, fill="white")

        # Save to new path
        output_path = image_path.replace("memes", "viral_memes").replace(".jpg", ".png")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        new_img.save(output_path, format="PNG", quality=100)
        return output_path

    except Exception as e:
        print(f"[ERROR] add_meme_text failed: {e}")
        return image_path

def format_image_for_instagram(image_path, caption_text, max_width=1080, padding=50):
    try:
        image = Image.open(image_path).convert("RGB")
        aspect_ratio = image.height / image.width
        new_height = int(aspect_ratio * max_width)
        image = image.resize((max_width, new_height))

        if not caption_text:
            return image_path

        font = ImageFont.truetype("arial.ttf", 40)
        draw = ImageDraw.Draw(image)

        lines = textwrap.wrap(caption_text, width=40)
        caption_height = len(lines) * 50
        final_image = Image.new("RGB", (max_width, new_height + caption_height + padding), (0, 0, 0))
        final_image.paste(image, (0, 0))

        draw = ImageDraw.Draw(final_image)
        y = new_height + (padding // 2)
        for line in lines:
            w, _ = draw.textbbox((0, 0), line, font=font)[2:]
            x = (max_width - w) // 2
            draw.text((x, y), line, font=font, fill="white")
            y += 50

        output_path = image_path.replace(".png", "_formatted.jpg")
        final_image.save(output_path, "JPEG")
        return output_path
    except Exception as e:
        print(f"⚠️ Error formatting image: {e}")
        return None


def upscale_image(image_path, scale=2):
    try:
        image = cv2.imread(image_path)
        height, width = image.shape[:2]
        upscaled = cv2.resize(image, (width * scale, height * scale), interpolation=cv2.INTER_CUBIC)
        sharpen_kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        sharpened = cv2.filter2D(upscaled, -1, sharpen_kernel)

        output_path = image_path.replace(".jpg", "_HD.jpg").replace(".png", "_HD.jpg")
        cv2.imwrite(output_path, sharpened, [cv2.IMWRITE_JPEG_QUALITY, 95])
        return output_path
    except Exception as e:
        print(f"⚠️ Error upscaling: {e}")
        return image_path

import random
# ---------- FINAL ORCHESTRATION ----------
# import datetime
# def create_final_meme(img1, img2, title, image_url=None, caption=None):
#     print(f"🚀 Creating meme from: {img1} + {img2}")

#     if not os.path.exists(img1) or not os.path.exists(img2):
#         print("❌ One or both image paths are invalid.")
#         return None

#     merged_path = merge_images(img1, img2)
#     if not merged_path:
#         return None

#     # 🧠 AI-generated caption
#     meme_caption, full_caption = generate_ai_caption_with_image(title, merged_path)

#     # 🖊️ Overlay caption onto the meme image
#     meme_with_text = add_meme_text(merged_path, meme_caption)

#     # 📏 Format image to Instagram dimensions
#     formatted = format_image_for_instagram(meme_with_text, caption_text=meme_caption)

#     # 🔍 Optional: upscale for HD (can skip if not needed)
#     final_hd = upscale_image(formatted)

#     # 📁 Save the final meme in "data/Final Post/" folder
#     final_post_dir = "data/Final Post"
#     os.makedirs(final_post_dir, exist_ok=True)

#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     output_filename = f"meme_{timestamp}.jpg"
#     output_path = os.path.join(final_post_dir, output_filename)

#     # Save the image
#     final_hd.save(output_path)

#     print(f"✅ Final meme saved: {output_path}")

#     return {
#         "path": output_path,
#         "caption": full_caption  # Use AI generated caption + hashtags
#     }
from services.imgbb_uploader import upload_to_imgbb

import os

import os

def create_final_meme(img1, img2, title, image_url=None, caption=None):
    print(f"🚀 Creating meme from: {img1} + {img2}")

    if not os.path.exists(img1) or not os.path.exists(img2):
        print("❌ One or both image paths are invalid.")
        return None

    # Merge the images side-by-side
    merged_path = merge_images(img1, img2)
    if not merged_path:
        return None

    # Generate caption if not provided
    meme_caption, full_caption = generate_ai_caption_with_image(title, merged_path)
    selected_caption = caption if caption else meme_caption

    # ⚠️ Do NOT overlay large meme text inside the image
    # ⬇️ Instead, just format it nicely with bottom small footer-style text
    formatted = format_image_for_instagram(merged_path, selected_caption)  # Make sure this only adds small footer text

    # Optional: upscale to HD
    final_hd = upscale_image(formatted)

    print(f"✅ Final HD meme ready at: {final_hd}")

    # Upload to ImgBB for sharing
    public_url = upload_to_imgbb(final_hd)
    if not public_url:
        print("❌ Failed to upload image to ImgBB.")
        return None

    print(f"🌐 Public URL (ImgBB): {public_url}")

    return {
        "path": final_hd,
        "caption": full_caption,
        "url": public_url
    }






# Example Usage
if __name__ == "__main__":
    meme, caption = create_final_meme("data/images/img1.jpg", "data/images/img2.jpg", "When you see your crush in public")
    print("📷 Output:", meme)
    print("📝 Caption:", caption)
