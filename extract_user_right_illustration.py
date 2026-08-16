import os
import numpy as np
from PIL import Image

def extract_and_replace_right_illustration():
    # 1. Load user's uploaded image media__1786463911748.png
    uploaded_path = "/Users/zhangwenbin/.gemini/antigravity/brain/73a5c8c4-3a1f-48b6-a788-2e684e569bc1/media__1786463911748.png"
    uploaded_img = Image.open(uploaded_path).convert("RGBA")
    uw, uh = uploaded_img.size

    # Crop the exact right-side illustration panel from uploaded image:
    # Based on uploaded card layout: right panel starts around x = 586/1000 * uw, y = 110/562 * uh
    # Let's inspect coordinates of right panel in media__1786463911748.png: size is 1000x562
    # Right panel rectangle: x1=586, y1=113, x2=972, y2=531
    right_panel = uploaded_img.crop((586, 112, 972, 532))

    # Save extracted right-side illustration
    right_panel_path = "output/card_right_illustration_qing.jpg"
    right_panel.convert("RGB").save(right_panel_path)
    print(f"Saved extracted right panel to {right_panel_path}")

if __name__ == "__main__":
    extract_and_replace_right_illustration()
