import os
import cv2

def merge_trend_and_reaction(google_img_path, pexels_img_path):
    bg = cv2.imread(google_img_path)
    reaction = cv2.imread(pexels_img_path)

    if bg is None or reaction is None:
        raise Exception("Image not found for merging.")

    # Resize reaction to match width of background
    reaction = cv2.resize(reaction, (bg.shape[1], int(bg.shape[0] * 0.3)))

    merged = cv2.vconcat([bg, reaction])

    save_path = os.path.join("generated_memes", os.path.basename(google_img_path))
    os.makedirs("generated_memes", exist_ok=True)
    cv2.imwrite(save_path, merged)
    return save_path
