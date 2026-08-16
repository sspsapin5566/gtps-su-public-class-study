import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def create_seamless_qing_map():
    src_path = "output/qing_map_extracted.png"
    img = Image.open(src_path).convert("RGBA")
    w, h = img.size
    
    # Paper texture source region (empty parchment area: x=100..200, y=100..200)
    paper_crop = img.crop((80, 100, 200, 220))

    # Helper function to stamp paper texture seamlessly over a bounding box
    def stamp_paper_texture(box):
        x1, y1, x2, y2 = box
        bw, bh = x2 - x1, y2 - y1
        
        # Tile paper texture to match box size
        tiled_paper = paper_crop.resize((bw, bh), Image.Resampling.BICUBIC)
        
        # Feather mask edges so patch blends 100% seamlessly into surrounding map texture
        mask = Image.new("L", (bw, bh), 255)
        mask_draw = ImageDraw.Draw(mask)
        # Soft feather edge
        for i in range(4):
            mask_draw.rectangle([i, i, bw - 1 - i, bh - 1 - i], fill=int(255 * (i + 1) / 4))
        mask = mask.filter(ImageFilter.GaussianBlur(radius=2))
        
        img.paste(tiled_paper, (x1, y1), mask)

    draw = ImageDraw.Draw(img)

    font_path = "/System/Library/Fonts/STHeiti Medium.ttc"
    if not os.path.exists(font_path):
        font_path = "/System/Library/Fonts/PingFang.ttc"

    font_medium = ImageFont.truetype(font_path, 21)
    font_large = ImageFont.truetype(font_path, 25)
    ink_color = "#151515" # Authentic dark brush ink

    # 1. 滬尾的位置在頭江的上方 (x: 350..410, y: 75..110)
    stamp_paper_texture((345, 75, 410, 110))
    draw.text((350, 78), "滬尾", fill=ink_color, font=font_medium)

    # 2. 淡水河的文字請排直的，由上而下 (x: 300..345, y: 140..250)
    stamp_paper_texture((302, 140, 345, 250))
    draw.text((310, 145), "淡", fill=ink_color, font=font_medium)
    draw.text((310, 180), "水", fill=ink_color, font=font_medium)
    draw.text((310, 215), "河", fill=ink_color, font=font_medium)

    # 3. 大稻埕取代枋寮大的三個字位置 (x: 385..465, y: 300..345)
    stamp_paper_texture((385, 300, 465, 345))
    draw.text((390, 305), "大稻埕", fill=ink_color, font=font_medium)

    # 4. 海山口的文字要移動到鐵路和河流的中間 (x: 290..365, y: 370..405)
    stamp_paper_texture((290, 370, 365, 405))
    draw.text((295, 372), "海山口", fill=ink_color, font=font_medium)

    # 5. 基隆河的河字體要跟基隆一樣大 (x: 520..565, y: 380..420)
    stamp_paper_texture((520, 380, 565, 420))
    draw.text((525, 382), "河", fill=ink_color, font=font_medium)

    # Save seamless map
    out_map_path = "output/qing_map_perfected.png"
    img.save(out_map_path)
    print(f"Saved seamlessly blended Qing map to {out_map_path}")

if __name__ == "__main__":
    create_seamless_qing_map()
