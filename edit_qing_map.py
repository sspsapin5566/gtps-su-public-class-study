import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def create_perfected_qing_map():
    src_path = "output/qing_map_extracted.png"
    img = Image.open(src_path).convert("RGBA")
    
    # 1. Convert map to grayscale / clean parchment texture
    # The map background is warm light gray/creamy paper texture (~RGB 220, 215, 210)
    arr = np.array(img)
    
    draw = ImageDraw.Draw(img)

    # Use Chinese font matching brush calligraphy / Traditional Chinese ink style
    font_path = "/System/Library/Fonts/STHeiti Medium.ttc"
    if not os.path.exists(font_path):
        font_path = "/System/Library/Fonts/PingFang.ttc"

    font_large = ImageFont.truetype(font_path, 26)
    font_medium = ImageFont.truetype(font_path, 22)
    font_small = ImageFont.truetype(font_path, 18)

    ink_color = "#1E1E1E" # Ink black matching original map calligraphy

    # Helper function: blend in patch using surrounding paper texture median color
    def patch_region(box):
        x1, y1, x2, y2 = box
        # Sample border pixels around box to get true local paper background
        border_pixels = []
        for x in range(x1-5, x2+5):
            if 0 <= x < img.width:
                if 0 <= y1-5 < img.height: border_pixels.append(arr[y1-5, x][:3])
                if 0 <= y2+5 < img.height: border_pixels.append(arr[y2+5, x][:3])
        for y in range(y1-5, y2+5):
            if 0 <= y < img.height:
                if 0 <= x1-5 < img.width: border_pixels.append(arr[y, x1-5][:3])
                if 0 <= x2+5 < img.width: border_pixels.append(arr[y, x2+5][:3])
        
        median_color = tuple(np.median(border_pixels, axis=0).astype(int))
        draw.rectangle([x1, y1, x2, y2], fill=median_color)

    # 1. 滬尾的位置在頭江的上方
    # Erase old "尾瀧" (x: 340..395, y: 75..110)
    patch_region([340, 75, 395, 110])
    draw.text((345, 78), "滬尾", fill=ink_color, font=font_medium)

    # 2. 淡水河的文字請排直的，由上而下 (淡 水 河)
    # Erase old vertical "淡 水" (x: 300..340, y: 140..250)
    patch_region([300, 140, 340, 250])
    draw.text((308, 145), "淡", fill=ink_color, font=font_medium)
    draw.text((308, 180), "水", fill=ink_color, font=font_medium)
    draw.text((308, 215), "河", fill=ink_color, font=font_medium)

    # 3. 大稻埕取代枋寮大的三個字位置 (實際上是取代原圖上的「埕稻大」/「大稻埕」, at x:385..460, y:300..340)
    # Erase old "埕稻大" at x:385..460, y:300..345
    patch_region([385, 300, 465, 345])
    draw.text((390, 305), "大稻埕", fill=ink_color, font=font_medium)

    # 4. 海山口的文字要移動到鐵路和河流的中間 ("口山海" -> "海山口")
    # Erase old "口山海" at x:295..360, y:370..405
    patch_region([295, 370, 360, 405])
    # Place "海山口" right between railway and river (x: 295, y: 372)
    draw.text((295, 372), "海山口", fill=ink_color, font=font_medium)

    # 5. 基隆河的河字體要跟基隆一樣大
    # Erase old small "河" and katakana (x: 520..565, y: 385..420)
    patch_region([520, 385, 565, 420])
    draw.text((525, 385), "河", fill=ink_color, font=font_medium)

    # Save perfected map
    out_map_path = "output/qing_map_perfected.png"
    img.save(out_map_path)
    print(f"Saved seamlessly perfected Qing Dynasty map to {out_map_path}")

if __name__ == "__main__":
    create_perfected_qing_map()
