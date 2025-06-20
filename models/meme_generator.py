
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
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-latest:generateContent?key=YOUR_GEMENI_API_KEY"
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
