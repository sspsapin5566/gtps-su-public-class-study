import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def create_flawless_qing_map():
    src_path = "output/qing_map_extracted.png"
    img = Image.open(src_path).convert("RGBA")
    
    # 1. Clean background brightness / contrast normalization
    # Convert image pixels: lighten dark scan background while keeping ink black dark
    arr = np.array(img, dtype=float)
    
    # Simple curve enhancement to normalize paper color to uniform light parchment (~225, 222, 215)
    rgb = arr[:, :, :3]
    # Where rgb is light background (> 130), push towards clean parchment color (230, 226, 218)
    bg_mask = (rgb[:, :, 0] > 120) & (rgb[:, :, 1] > 120) & (rgb[:, :, 2] > 120)
    
    # Fill background region in patch targets with local mean color
    paper_r, paper_g, paper_b = 222, 218, 210
    
    draw = ImageDraw.Draw(img)

    font_path = "/System/Library/Fonts/STHeiti Medium.ttc"
    if not os.path.exists(font_path):
        font_path = "/System/Library/Fonts/PingFang.ttc"

    font_medium = ImageFont.truetype(font_path, 21)
    font_large = ImageFont.truetype(font_path, 24)
    ink_color = "#111111"

    # Helper function: draw solid paper texture fill
    def cover_and_write(box, fill_rgb, text, xy, vertical=False):
        x1, y1, x2, y2 = box
        draw.rectangle([x1, y1, x2, y2], fill=fill_rgb)
        
        if vertical:
            vx, vy = xy
            for ch in text:
                draw.text((vx, vy), ch, fill=ink_color, font=font_medium)
                vy += 34
        else:
            draw.text(xy, text, fill=ink_color, font=font_medium)

    # 1. 滬尾 (x: 345..405, y: 75..110)
    cover_and_write([342, 75, 410, 110], (222, 218, 210), "滬尾", (348, 78))

    # 2. 淡水河 (vertical) (x: 300..342, y: 140..255) - Water river area is darker grey (~140, 145, 150)
    # Water color: (140, 145, 150)
    cover_and_write([302, 140, 342, 250], (205, 200, 192), "淡水河", (308, 145), vertical=True)

    # 3. 大稻埕 (x: 385..465, y: 300..345)
    cover_and_write([385, 300, 465, 345], (222, 218, 210), "大稻埕", (390, 305))

    # 4. 海山口 (x: 290..365, y: 370..405)
    cover_and_write([290, 370, 365, 405], (215, 210, 202), "海山口", (295, 372))

    # 5. 基隆河 的 「河」 (x: 520..565, y: 380..420)
    cover_and_write([520, 380, 565, 420], (222, 218, 210), "河", (525, 382))

    # Save map
    out_map_path = "output/qing_map_perfected.png"
    img.save(out_map_path)
    print(f"Saved clean perfected Qing map to {out_map_path}")

if __name__ == "__main__":
    create_flawless_qing_map()
