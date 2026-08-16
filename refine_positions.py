import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def refine_exact_positions():
    src_path = "output/qing_map_extracted.png"
    img = Image.open(src_path).convert("RGBA")
    arr = np.array(img)

    draw = ImageDraw.Draw(img)

    font_path = "/System/Library/Fonts/STHeiti Medium.ttc"
    if not os.path.exists(font_path):
        font_path = "/System/Library/Fonts/PingFang.ttc"

    font_medium = ImageFont.truetype(font_path, 21)
    font_he = ImageFont.truetype(font_path, 25) # "河" font matching 基隆
    ink_color = "#111111"

    # Helper function to inpaint a box using exact surrounding paper background
    def inpaint(x1, y1, x2, y2):
        border_pixels = []
        for x in range(max(0, x1-5), min(img.width, x2+6)):
            if y1-5 >= 0: border_pixels.append(arr[y1-5, x][:3])
            if y2+5 < img.height: border_pixels.append(arr[y2+5, x][:3])
        for y in range(max(0, y1-5), min(img.height, y2+6)):
            if x1-5 >= 0: border_pixels.append(arr[y, x1-5][:3])
            if x2+5 < img.width: border_pixels.append(arr[y, x2+5][:3])
        
        paper_pix = [p for p in border_pixels if np.mean(p) > 130]
        if not paper_pix: paper_pix = border_pixels
        mean_col = tuple(np.mean(paper_pix, axis=0).astype(int))
        
        box_w, box_h = x2 - x1, y2 - y1
        noise = np.random.randint(-2, 3, (box_h, box_w, 3))
        patch = np.clip(mean_col + noise, 0, 255).astype(np.uint8)
        patch_rgba = np.dstack([patch, np.full((box_h, box_w), 255, dtype=np.uint8)])
        img.paste(Image.fromarray(patch_rgba), (x1, y1))

    # 1. 滬尾: Above 頭江 (x: 345..405, y: 78..112)
    inpaint(345, 78, 405, 112)
    draw.text((348, 80), "滬尾", fill=ink_color, font=font_medium)

    # 2. 淡水河: Vertical 由上而下 (x: 300..340, y: 142..248)
    inpaint(300, 142, 340, 248)
    draw.text((307, 145), "淡", fill=ink_color, font=font_medium)
    draw.text((307, 178), "水", fill=ink_color, font=font_medium)
    draw.text((307, 211), "河", fill=ink_color, font=font_medium)

    # 3. 大稻埕: Replaces 「埕稻大」/「枋寮大」3 words area right above Taipei Fu (x: 382..465, y: 295..338)
    inpaint(382, 295, 465, 338)
    draw.text((387, 299), "大稻埕", fill=ink_color, font=font_medium)

    # 4. 海山口: Exactly between railway line and river, replacing old "口山海" (x: 285..362, y: 368..405)
    inpaint(285, 368, 362, 405)
    draw.text((289, 371), "海山口", fill=ink_color, font=font_medium)

    # 5. 基隆河: 「河」字體與基隆一樣大 (x: 520..565, y: 380..420)
    inpaint(520, 380, 565, 420)
    draw.text((525, 382), "河", fill=ink_color, font=font_he)

    out_map_path = "output/qing_map_perfected.png"
    img.save(out_map_path)
    print(f"Saved refined exact Qing map to {out_map_path}")

if __name__ == "__main__":
    refine_exact_positions()
