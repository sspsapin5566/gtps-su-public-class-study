import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def high_contrast_map_edit():
    src_path = "output/qing_map_extracted.png"
    img = Image.open(src_path).convert("RGBA")
    arr = np.array(img)

    draw = ImageDraw.Draw(img)

    font_path = "/System/Library/Fonts/STHeiti Medium.ttc"
    if not os.path.exists(font_path):
        font_path = "/System/Library/Fonts/PingFang.ttc"

    # Crisp font matching original map size
    font_large = ImageFont.truetype(font_path, 26)
    font_medium = ImageFont.truetype(font_path, 21)
    font_river_he = ImageFont.truetype(font_path, 26) # Large "河" matching 基隆

    ink_color = "#111111"

    # In-painting texture blending: for each bounding box, sample exact surrounding ink-free paper pixels
    def inpaint_box(box):
        x1, y1, x2, y2 = box
        # Sample border pixels that are paper background (> 140 intensity)
        border_pixels = []
        for x in range(max(0, x1-6), min(img.width, x2+7)):
            if y1-5 >= 0: border_pixels.append(arr[y1-5, x][:3])
            if y2+5 < img.height: border_pixels.append(arr[y2+5, x][:3])
        for y in range(max(0, y1-6), min(img.height, y2+7)):
            if x1-5 >= 0: border_pixels.append(arr[y, x1-5][:3])
            if x2+5 < img.width: border_pixels.append(arr[y, x2+5][:3])
        
        # Filter for paper background pixels
        paper_pix = [p for p in border_pixels if np.mean(p) > 130]
        if not paper_pix:
            paper_pix = border_pixels
            
        mean_col = tuple(np.mean(paper_pix, axis=0).astype(int))
        
        # Add subtle noise matching paper grain
        box_w, box_h = x2 - x1, y2 - y1
        noise = np.random.randint(-3, 4, (box_h, box_w, 3))
        patch = np.clip(mean_col + noise, 0, 255).astype(np.uint8)
        patch_rgba = np.dstack([patch, np.full((box_h, box_w), 255, dtype=np.uint8)])
        
        patch_img = Image.fromarray(patch_rgba)
        img.paste(patch_img, (x1, y1))

    # 1. 滬尾的位置在頭江的上方 (replace 尾瀧 at x: 340..402, y: 75..112)
    inpaint_box([340, 75, 402, 112])
    draw.text((345, 78), "滬尾", fill=ink_color, font=font_medium)

    # 2. 淡水河的文字請排直的，由上而下 (淡 水 河) (replace vertical 淡 水 at x: 300..342, y: 142..248)
    inpaint_box([300, 142, 342, 248])
    draw.text((308, 145), "淡", fill=ink_color, font=font_medium)
    draw.text((308, 178), "水", fill=ink_color, font=font_medium)
    draw.text((308, 211), "河", fill=ink_color, font=font_medium)

    # 3. 大稻埕取代枋寮大的三個字位置 (replace 埕稻大 at x: 388..465, y: 300..342)
    inpaint_box([388, 300, 465, 342])
    draw.text((392, 304), "大稻埕", fill=ink_color, font=font_medium)

    # 4. 海山口的文字要移動到鐵路和河流的中間 ("口山海" -> "海山口" at x: 288..365, y: 370..405)
    inpaint_box([288, 370, 365, 405])
    draw.text((292, 372), "海山口", fill=ink_color, font=font_medium)

    # 5. 基隆河的河字體要跟基隆一樣大 (replace small 河 at x: 520..565, y: 380..420)
    inpaint_box([520, 380, 565, 420])
    draw.text((525, 382), "河", fill=ink_color, font=font_river_he)

    out_map_path = "output/qing_map_perfected.png"
    img.save(out_map_path)
    print(f"Saved high-contrast inpainted Qing map to {out_map_path}")

if __name__ == "__main__":
    high_contrast_map_edit()
