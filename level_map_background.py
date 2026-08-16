import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

def level_and_perfect_map():
    src_path = "output/qing_map_extracted.png"
    img = Image.open(src_path).convert("L") # Convert to grayscale for clean leveling
    arr = np.array(img, dtype=float)

    # Map background leveling:
    # Scale intensities so paper background (~150-220) becomes clean light parchment (#EAE5DC),
    # while dark ink lines (<100) remain sharp black ink (#222222).
    
    # Sigmoid contrast curve / linear stretch
    norm = (arr - 40) / (180 - 40)
    norm = np.clip(norm, 0.0, 1.0)
    
    # Convert back to RGB parchment tint
    paper_r = (norm * 55 + 180).astype(np.uint8) # 180..235
    paper_g = (norm * 55 + 175).astype(np.uint8) # 175..230
    paper_b = (norm * 55 + 165).astype(np.uint8) # 165..220

    rgb_arr = np.stack([paper_r, paper_g, paper_b], axis=-1)
    clean_img = Image.fromarray(rgb_arr, mode="RGB").convert("RGBA")

    draw = ImageDraw.Draw(clean_img)

    font_path = "/System/Library/Fonts/STHeiti Medium.ttc"
    if not os.path.exists(font_path):
        font_path = "/System/Library/Fonts/PingFang.ttc"

    font_medium = ImageFont.truetype(font_path, 21)
    font_he = ImageFont.truetype(font_path, 22)
    ink_color = "#1A1A1A" # Crisp dark ink

    # Target paper fill color for text replacement: sampled from leveled parchment (#EAE5DC)
    parchment_color = (230, 225, 215)

    # 1. 滬尾 (x: 345..405, y: 76..112) - Above 頭江
    draw.rectangle([342, 75, 405, 112], fill=parchment_color)
    draw.text((346, 78), "滬尾", fill=ink_color, font=font_medium)

    # 2. 淡水河 (vertical) (x: 300..342, y: 142..248) - Vertical top to bottom
    draw.rectangle([300, 142, 342, 248], fill=(205, 200, 190)) # Slightly darker river tint
    draw.text((308, 145), "淡", fill=ink_color, font=font_medium)
    draw.text((308, 178), "水", fill=ink_color, font=font_medium)
    draw.text((308, 211), "河", fill=ink_color, font=font_medium)

    # 3. 大稻埕取代枋寮大 (x: 388..465, y: 300..342)
    draw.rectangle([385, 300, 465, 342], fill=parchment_color)
    draw.text((390, 304), "大稻埕", fill=ink_color, font=font_medium)

    # 4. 海山口 (x: 288..365, y: 370..405) - Between railway and river
    draw.rectangle([288, 370, 365, 405], fill=parchment_color)
    draw.text((292, 372), "海山口", fill=ink_color, font=font_medium)

    # 5. 基隆河 的 「河」字體與基隆一樣大 (x: 520..565, y: 382..418)
    draw.rectangle([520, 382, 565, 418], fill=parchment_color)
    draw.text((525, 382), "河", fill=ink_color, font=font_he)

    # Save leveled map
    out_map_path = "output/qing_map_perfected.png"
    clean_img.save(out_map_path)
    print(f"Saved leveled perfected map to {out_map_path}")

if __name__ == "__main__":
    level_and_perfect_map()
