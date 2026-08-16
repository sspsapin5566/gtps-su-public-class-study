import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def composite_perfect_qing_illustration():
    bg_path = "/Users/zhangwenbin/.gemini/antigravity/brain/73a5c8c4-3a1f-48b6-a788-2e684e569bc1/card_right_illustration_1786285400703.jpg"
    qing_path = "output/qing_map_perfected.png"

    bg_img = Image.open(bg_path).convert("RGBA")
    qing_img = Image.open(qing_path).convert("RGBA")

    bg_arr = np.array(bg_img)

    # 1. Whiteboard Screen Display Area: x [462..968], y [78..382]
    wb_x1, wb_y1, wb_x2, wb_y2 = 462, 78, 968, 382
    wb_w, wb_h = wb_x2 - wb_x1, wb_y2 - wb_y1

    qing_wb = qing_img.resize((wb_w, wb_h), Image.Resampling.LANCZOS)
    qing_wb_arr = np.array(qing_wb)

    # 2. Erase ALL old background whiteboard elements completely (x: 445..980, y: 70..400) to pure white wall (#FFFFFF)
    canvas_arr = bg_arr.copy()
    canvas_arr[70:400, 445:980] = [255, 255, 255, 255]

    # Paste perfected Qing map onto whiteboard screen
    canvas_arr[wb_y1:wb_y2, wb_x1:wb_x2] = qing_wb_arr

    # Restore ORIGINAL kids' hair, skin, faces, and clothes 100% over map and wall!
    fg_mask = np.zeros((bg_img.height, bg_img.width), dtype=bool)
    for y in range(70, 410):
        for x in range(440, 980):
            r, g, b, a = bg_arr[y, x]
            is_hair = (r < 100 and g < 100 and b < 100)
            is_skin = (r > 165 and g > 105 and b > 85 and r > g and g > b - 20)
            is_blue_shirt = (b > 110 and b > r + 10)
            is_teacher_blue = (b > 110 and r < 100)

            if is_hair or is_skin or is_blue_shirt or is_teacher_blue:
                fg_mask[y, x] = True

    canvas_arr[fg_mask] = bg_arr[fg_mask]

    res_img = Image.fromarray(canvas_arr)
    draw_res = ImageDraw.Draw(res_img)

    # Draw whiteboard outer bezel frame AFTER erasing background so old board lines NEVER bleed through!
    draw_res.rounded_rectangle([460, 75, 970, 385], radius=6, outline="#334155", width=3)
    draw_res.rounded_rectangle([461, 76, 969, 384], radius=5, outline="#94A3B8", width=1)

    # 3. Desk Map Area (Center table: x 298 to 685, y 612 to 752)
    desk_x1, desk_y1, desk_x2, desk_y2 = 298, 612, 685, 752
    desk_w, desk_h = desk_x2 - desk_x1, desk_y2 - desk_y1

    qing_desk = qing_img.resize((desk_w, desk_h), Image.Resampling.LANCZOS)
    
    quad_dst = (
        25, 0,                      # Top Left
        0, desk_h,                  # Bottom Left
        desk_w, desk_h,             # Bottom Right
        desk_w - 25, 0              # Top Right
    )
    
    qing_desk_warped = qing_desk.transform(
        (desk_w, desk_h),
        Image.QUAD,
        quad_dst,
        resample=Image.Resampling.BICUBIC
    )

    res_img.paste(qing_desk_warped, (desk_x1, desk_y1), qing_desk_warped)

    # Outline around desk map sheet
    draw_res.polygon([
        (desk_x1 + 25, desk_y1),
        (desk_x2 - 25, desk_y1),
        (desk_x2, desk_y2),
        (desk_x1, desk_y2)
    ], outline="#334155", width=2)

    # Save composited right-side illustration
    out_illus_path = "output/card_right_illustration_qing.jpg"
    res_img.convert("RGB").save(out_illus_path)
    print(f"Saved PERFECT PRISTINE Qing map illustration to {out_illus_path}")

if __name__ == "__main__":
    composite_perfect_qing_illustration()
