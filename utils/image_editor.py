# from PIL import Image, ImageDraw, ImageFont
# import textwrap
# import os

# def add_caption_to_image(image_path, caption, font_path="arial.ttf", font_size=28, margin=40):
#     """Adds wrapped caption text at the bottom of the image."""
#     try:
#         # Load image
#         image = Image.open(image_path)
#         draw = ImageDraw.Draw(image)
#         width, height = image.size

#         # Load font
#         font = ImageFont.truetype(font_path, font_size)

#         # Wrap text
#         max_chars_per_line = width // (font_size // 2)  # Adjust wrapping based on image width
#         lines = textwrap.wrap(caption, width=max_chars_per_line)

#         # Calculate total height for all caption lines
#         total_text_height = len(lines) * (font_size + 10)

#         # Create new image with extra space at the bottom
#         new_height = height + total_text_height + margin
#         new_image = Image.new("RGB", (width, new_height), (0, 0, 0))  # black background
#         new_image.paste(image, (0, 0))

#         # Re-initialize drawing context on new image
#         draw = ImageDraw.Draw(new_image)

#         y_text = height + (margin // 2)

#         # Draw each line of the caption
#         for line in lines:
#             text_width, text_height = draw.textsize(line, font=font)
#             x_text = (width - text_width) // 2
#             draw.text((x_text, y_text), line, font=font, fill="white")
#             y_text += font_size + 10

#         # Save updated image
#         new_path = image_path.replace(".jpg", "_captioned.jpg")
#         new_image.save(new_path)

#         return new_path

#     except Exception as e:
#         print(f"❌ Failed to add caption: {e}")
#         return image_path
from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

def add_caption_to_image(image_path, caption, font_path="arial.ttf", font_size=28, margin=40):
    """
    Adds a caption to the bottom of an image with proper text wrapping and spacing.
    Returns the path of the new image with caption.
    """
    try:
        # Load original image
        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)
        width, height = image.size

        # Load font
        font = ImageFont.truetype(font_path, font_size)

        # Calculate wrapping
        max_chars_per_line = width // (font_size // 2)
        lines = textwrap.wrap(caption, width=max_chars_per_line)

        # Calculate text height
        total_text_height = len(lines) * (font_size + 10)
        new_height = height + total_text_height + margin

        # Create new image with extra space
        new_image = Image.new("RGB", (width, new_height), (0, 0, 0))  # black background
        new_image.paste(image, (0, 0))

        draw = ImageDraw.Draw(new_image)
        y_text = height + (margin // 2)

        for line in lines:
            text_width, text_height = draw.textsize(line, font=font)
            x_text = (width - text_width) // 2
            draw.text((x_text, y_text), line, font=font, fill="white")
            y_text += font_size + 10

        # Save and return
        new_path = image_path.replace(".jpg", "_captioned.jpg")
        new_image.save(new_path)

        print(f"🖼️ Captioned image saved to: {new_path}")
        return new_path

    except Exception as e:
        print(f"❌ Failed to add caption to {image_path}: {e}")
        return image_path
