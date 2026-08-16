import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def create_native_calligraphy_map():
    src_path = "output/qing_map_extracted.png"
    img = Image.open(src_path).convert("RGBA")
    arr = np.array(img)

    # Convert map scan into a clean vintage parchment style
    # Target paper background: #DCD7CE (R:220, G:215, B:206)
    # Target ink color: #222222
    
    # We sample local paper background around each annotation box so the erased area matches surrounding paper grain perfectly!
    draw = ImageDraw.Draw(img)

    font_path = "/System/Library/Fonts/STHeiti Medium.ttc"
    if not os.path.exists(font_path):
        font_path = "/System/Library/Fonts/PingFang.ttc"

    font_text = ImageFont.truetype(font_path, 22)
    font_river_he = ImageFont.truetype(font_path, 22) # Large "河" font matching 基隆
    
    ink_color = "#1A1A1A"

    def erase_with_local_texture(x1, y1, x2, y2):
        # Sample border pixels around box to get true local paper background
        samples = []
        for x in range(max(0, x1-4), min(img.width, x2+5)):
            if y1-4 >= 0: samples.append(arr[y1-4, x][:3])
            if y2+4 < img.height: samples.append(arr[y2+4, x][:3])
        for y in range(max(0, y1-4), min(img.height, y2+5)):
            if x1-4 >= 0: samples.append(arr[y, x1-4][:3])
            if x2+4 < img.width: samples.append(arr[y, x2+4][:3])
        
        avg_col = tuple(np.mean(samples, axis=0).astype(int))
        draw.rectangle([x1, y1, x2, y2], fill=avg_col)

    # 1. 滬尾的位置在頭江的上方 (replace 尾瀧 at x: 345..400, y: 78..112)
    erase_with_local_texture(342, 76, 400, 112)
    draw.text((346, 78), "滬尾", fill=ink_color, font=font_text)

    # 2. 淡水河的文字請排直的，由上而下 (淡 水 河) (replace vertical 淡 水 at x: 302..342, y: 142..248)
    erase_with_local_texture(302, 142, 342, 248)
    draw.text((308, 145), "淡", fill=ink_color, font=font_text)
    draw.text((308, 178), "水", fill=ink_color, font=font_text)
    draw.text((308, 211), "河", fill=ink_color, font=font_text)

    # 3. 大稻埕取代枋寮大的三個字位置 (replace 埕稻大 at x: 388..465, y: 300..342)
    erase_with_local_texture(388, 300, 465, 342)
    draw.text((392, 304), "大稻埕", fill=ink_color, font=font_text)

    # 4. 海山口的文字要移動到鐵路和河流的中間 ("口山海" -> "海山口" at x: 288..365, y: 370..405)
    erase_with_local_texture(288, 370, 365, 405)
    draw.text((292, 372), "海山口", fill=ink_color, font=font_text)

    # 5. 基隆河的河字體要跟基隆一樣大 (replace small 河 at x: 520..565, y: 382..418)
    erase_with_local_texture(520, 382, 565, 418)
    draw.text((525, 382), "河", fill=ink_color, font=font_river_he)

    # Save finalized map artifact
    out_map_path = "output/qing_map_perfected.png"
    img.save(out_map_path)
    print(f"Saved native calligraphy Qing map to {out_map_path}")

if __name__ == "__main__":
    create_native_calligraphy_map()
