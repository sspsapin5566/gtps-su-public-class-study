import os
import sys
from PIL import Image, ImageDraw, ImageFont

def build_card_bold():
    # Full HD resolution canvas (1920 x 1080)
    w, h = 1920, 1080
    img = Image.new("RGB", (w, h), "#FFFFFF")
    draw = ImageDraw.Draw(img)

    # Use Mac bold fonts
    font_path = "/System/Library/Fonts/Hiragino Sans GB.ttc"
    if not os.path.exists(font_path):
        font_path = "/System/Library/Fonts/STHeiti Medium.ttc"
    if not os.path.exists(font_path):
        font_path = "/System/Library/Fonts/PingFang.ttc"

    # Extra Bold Font Sizes with High Contrast
    font_header = ImageFont.truetype(font_path, 46)
    font_badge = ImageFont.truetype(font_path, 28)
    font_tag = ImageFont.truetype(font_path, 26)
    font_box_title = ImageFont.truetype(font_path, 34)
    font_box_desc = ImageFont.truetype(font_path, 24)

    # 1. Top Header (Extra Bold with stroke_width=1)
    header_text = "新北市AI教育局國教輔導團學習共同體分團課例分享"
    
    draw.text((50, 36), header_text, fill="#0F172A", font=font_header, stroke_width=1, stroke_fill="#0F172A")
    
    # Header Badge [115.8] (Extra Bold)
    badge_x, badge_y = 1290, 38
    badge_w, badge_h = 124, 48
    draw.rounded_rectangle([badge_x, badge_y, badge_x + badge_w, badge_y + badge_h], radius=24, fill="#1D4ED8")
    draw.text((badge_x + 23, badge_y + 8), "115.8", fill="#FFFFFF", font=font_badge, stroke_width=1, stroke_fill="#FFFFFF")

    # 2. Pill Boxes Definition - updated exact wording
    boxes = [
        {
            "tag": "主題",
            "color": "#1D4ED8",      # Rich Dark Blue
            "border": "#2563EB",
            "title": "國小社會公開課學生4個學習小組微觀課分析",
            "desc": "蘇國瑞老師公開課，探究塭仔圳區域發展、清代新莊鐵路古地圖與地區商業發展個案之Jump學習"
        },
        {
            "tag": "工具",
            "color": "#15803D",      # Rich Dark Green
            "border": "#16A34A",
            "title": "Antigravity AI 課堂研究系統",
            "desc": "結合自動語音轉譯、精準時間軸標記、GPTimage2繪本重繪與學習共同體三階課例分析。"
        },
        {
            "tag": "痛點",
            "color": "#C2410C",      # Rich Deep Orange
            "border": "#EA580C",
            "title": "實地影帶觀課與逐字稿聽寫極為耗時",
            "desc": "實地進行 4 支影片觀課與聽寫逐字稿，每位教師在分析與紀錄上至少需要花費數天時間。"
        },
        {
            "tag": "成效",
            "color": "#7E22CE",      # Rich Deep Purple
            "border": "#9333EA",
            "title": "節省數天時間並深化專業協同學習",
            "desc": "透過 AI 自動完成影音下載、逐字稿與分析，1小時內即可完成，釋放心力進行深度專業學習。"
        },
        {
            "tag": "研發",
            "color": "#334155",      # Rich Slate Navy
            "border": "#475569",
            "title": "新北市國教輔導團學習共同體分團",
            "desc": "以研究與實踐為核心，推動社會領域課堂教學品質提升與學習共同體深度學習"
        }
    ]

    start_y = 122
    box_h = 166
    gap = 18
    box_w = 1040

    for i, b in enumerate(boxes):
        y = start_y + i * (box_h + gap)
        
        # Outer Card Container (Thick 3.5px border, crisp background)
        draw.rounded_rectangle([50, y, 50 + box_w, y + box_h], radius=18, fill="#F8FAFC", outline=b["border"], width=4)
        
        # Solid Pill Tag Badge (Extra Bold text)
        tag_x, tag_y = 70, y + 20
        tag_w, tag_h = 92, 44
        draw.rounded_rectangle([tag_x, tag_y, tag_x + tag_w, tag_y + tag_h], radius=22, fill=b["color"])
        draw.text((tag_x + 18, tag_y + 7), b["tag"], fill="#FFFFFF", font=font_tag, stroke_width=1, stroke_fill="#FFFFFF")
        
        # Box Title (Extra Bold Sharp Slate-950 with stroke_width=1 for maximum readability)
        draw.text((178, y + 22), b["title"], fill="#090D16", font=font_box_title, stroke_width=1, stroke_fill="#090D16")
        
        # Box Description (Bold Crisp Dark Text with stroke_width=0.5)
        draw.text((70, y + 86), b["desc"], fill="#1E293B", font=font_box_desc, stroke_width=0.5, stroke_fill="#1E293B")

    # 3. Right Side Illustration Assembly
    right_img_path = "output/card_right_illustration_qing.jpg"
    if os.path.exists(right_img_path):
        right_img = Image.open(right_img_path)
        
        target_w = 740
        target_h = 902
        right_img = right_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
        
        img.paste(right_img, (1125, start_y))
        
        # Rounded border frame around right illustration
        draw.rounded_rectangle([1125, start_y, 1125 + target_w, start_y + target_h], radius=18, outline="#CBD5E1", width=4)

    # Save output card
    out_png = "/Users/zhangwenbin/我的雲端硬碟/Antigravity/國泰社會學生小組分析/output/social_studies_infographic_card.png"
    img.save(out_png)
    print(f"Saved EXTRA BOLD card with updated text to {out_png}")

if __name__ == "__main__":
    build_card_bold()
