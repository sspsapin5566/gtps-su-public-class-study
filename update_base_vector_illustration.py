import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def update_targeted_ink_illustration():
    base_path = "/Users/zhangwenbin/.gemini/antigravity/brain/73a5c8c4-3a1f-48b6-a788-2e684e569bc1/card_right_illustration_clean_face_1786373432672.jpg"
    img = Image.open(base_path).convert("RGBA")
    arr = np.array(img)

    # Sample exact local background colors from original vector map:
    blue_water = tuple(arr[105, 765][:3]) # Blue water (97, 164, 189)
    green_land = tuple(arr[255, 640][:3]) # Green land (132, 196, 137)

    # 1. Erase English text "Danshui" / katakana near top river (x: 740..820, y: 130..190)
    for y in range(130, 190):
        for x in range(740, 820):
            r, g, b = arr[y, x, :3]
            if r < 150 and g < 150 and b < 150:
                arr[y, x, :3] = blue_water

    # 2. Erase English text "Keelung" / katakana near right river (x: 855..940, y: 245..275)
    for y in range(245, 275):
        for x in range(855, 940):
            r, g, b = arr[y, x, :3]
            # Protect railway line dashes around y: 252..262
            if (y < 251 or y > 263) and r < 150 and g < 150 and b < 150:
                arr[y, x, :3] = blue_water

    # 3. Erase English text "Xinzhuang" near lower right (x: 870..945, y: 285..335)
    for y in range(285, 335):
        for x in range(870, 945):
            r, g, b = arr[y, x, :3]
            if r < 150 and g < 150 and b < 150:
                arr[y, x, :3] = green_land

    # 4. Erase old "尾隆" & "隆" ink strokes at top (x: 740..815, y: 88..122)
    for y in range(88, 122):
        for x in range(740, 815):
            r, g, b = arr[y, x, :3]
            if r < 150 and g < 150 and b < 150:
                arr[y, x, :3] = blue_water

    # 5. Erase old "淡水" ink strokes along river (x: 698..745, y: 125..200)
    for y in range(125, 200):
        for x in range(698, 745):
            r, g, b = arr[y, x, :3]
            if r < 150 and g < 150 and b < 150:
                arr[y, x, :3] = blue_water

    # 6. Erase old "山海" ink strokes (x: 670..735, y: 235..275) - EXCEPT railway line
    for y in range(235, 275):
        for x in range(670, 735):
            r, g, b = arr[y, x, :3]
            if (y < 251 or y > 263) and r < 150 and g < 150 and b < 150:
                arr[y, x, :3] = green_land

    # 7. Erase old "枋寮大" and "大" ink strokes (x: 745..840, y: 200..275) - EXCEPT railway line
    for y in range(200, 275):
        for x in range(745, 840):
            r, g, b = arr[y, x, :3]
            if (y < 251 or y > 263) and r < 150 and g < 150 and b < 150:
                arr[y, x, :3] = green_land

    # 8. Erase old "基隆" ink strokes (x: 855..925, y: 230..275) - EXCEPT railway line
    for y in range(230, 275):
        for x in range(855, 925):
            r, g, b = arr[y, x, :3]
            if (y < 251 or y > 263) and r < 140 and g < 140 and b < 140:
                arr[y, x, :3] = blue_water

    res_img = Image.fromarray(arr)
    draw = ImageDraw.Draw(res_img)

    font_path = "/System/Library/Fonts/STHeiti Medium.ttc"
    if not os.path.exists(font_path):
        font_path = "/System/Library/Fonts/PingFang.ttc"

    font_bold = ImageFont.truetype(font_path, 16)
    ink_color = "#1E293B" # Dark slate ink matching vector line art

    # Draw Chinese text directly onto map surface (ZERO ENGLISH TEXT & ZERO COLOR BLOCKS!)
    # 1. 滬尾
    draw.text((742, 96), "滬尾", fill=ink_color, font=font_bold)

    # 2. 淡水河 (Vertical top-to-bottom along river)
    draw.text((712, 135), "淡", fill=ink_color, font=font_bold)
    draw.text((712, 162), "水", fill=ink_color, font=font_bold)
    draw.text((712, 189), "河", fill=ink_color, font=font_bold)

    # 3. 海山口 (Placed STRICTLY BELOW RAILWAY LINE at y=268)
    draw.text((655, 268), "海山口", fill=ink_color, font=font_bold)

    # 4. 大稻埕 (Above railway line at y=230)
    draw.text((780, 230), "大稻埕", fill=ink_color, font=font_bold)

    # 5. 基隆河 (Above railway line at y=235)
    draw.text((865, 235), "基隆河", fill=ink_color, font=font_bold)

    # Save output right-side illustration
    out_illus_path = "output/card_right_illustration_qing.jpg"
    res_img.convert("RGB").save(out_illus_path)
    print(f"Saved ZERO ENGLISH TEXT illustration to {out_illus_path}")

if __name__ == "__main__":
    update_targeted_ink_illustration()
