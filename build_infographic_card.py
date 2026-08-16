import os
import sys
from PIL import Image, ImageDraw, ImageFont

def build_card():
    # 16:9 Canvas size
    width, height = 1280, 720
    img = Image.new("RGB", (width, height), "#FFFFFF")
    draw = ImageDraw.Draw(img)

    # Fonts selection
    font_paths = [
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/PingFang.ttc",
        "msjh.ttc",
        "arial.ttf"
    ]
    
    def get_font(size):
        for path in font_paths:
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
        return ImageFont.load_default()

    font_header = get_font(32)
    font_badge = get_font(20)
    font_tag = get_font(20)
    font_box_title = get_font(22)
    font_box_desc = get_font(16)

    # 1. Header Area
    draw.text((40, 35), "新北市AI教育局國教輔導團學習共同體分團課例分享", fill="#0F172A", font=font_header)
    
    # Header Badge [115.8]
    badge_x, badge_y = 860, 35
    draw.rounded_rectangle([badge_x, badge_y, badge_x + 80, badge_y + 36], radius=18, fill="#2563EB")
    draw.text((badge_x + 14, badge_y + 6), "115.8", fill="#FFFFFF", font=font_badge)

    # 2. Pill Boxes Definition
    boxes = [
        {
            "tag": "主題",
            "color": "#2563EB", # Blue
            "bg_border": "#3B82F6",
            "title": "國小社會公開課學生4個學習小組微觀課分析",
            "desc": "蘇國瑞老師公開課，探究區域發展、古地圖與商業個案之同儕互動與學習跳躍。"
        },
        {
            "tag": "工具",
            "color": "#16A34A", # Green
            "bg_border": "#22C55E",
            "title": "Antigravity AI 課堂研究系統",
            "desc": "結合自動語音轉譯、精準時間軸標記、GPTimage2繪本重繪與學習共同體三階課例分析。"
        },
        {
            "tag": "痛點",
            "color": "#EA580C", # Orange
            "bg_border": "#F97316",
            "title": "實地影帶觀課與逐字稿聽寫極為耗時",
            "desc": "實地進行 4 支影片觀課與聽寫逐字稿，每位教師在分析與紀錄上至少需要花費數天時間。"
        },
        {
            "tag": "成效",
            "color": "#9333EA", # Purple
            "bg_border": "#A855F7",
            "title": "節省數天時間並深化專業協同學習",
            "desc": "透過 AI 自動完成影音下載、逐字稿與分析，1小時內即可完成，釋放心力進行深度專業學習。"
        },
        {
            "tag": "研發",
            "color": "#475569", # Slate
            "bg_border": "#64748B",
            "title": "新北市國教輔導團學習共同體分團",
            "desc": "以研究與實踐推動社會課堂教學品質提升與學習共同體哲學深化。"
        }
    ]

    start_y = 100
    box_height = 105
    gap = 14
    box_width = 680

    for i, b in enumerate(boxes):
        y = start_y + i * (box_height + gap)
        
        # Outer Card Container (Rounded Rect with Border)
        draw.rounded_rectangle([40, y, 40 + box_width, y + box_height], radius=14, fill="#FAFAFA", outline=b["bg_border"], width=2)
        
        # Solid Pill Tag
        tag_x, tag_y = 56, y + 16
        draw.rounded_rectangle([tag_x, tag_y, tag_x + 64, tag_y + 32], radius=16, fill=b["color"])
        draw.text((tag_x + 12, tag_y + 4), b["tag"], fill="#FFFFFF", font=font_tag)
        
        # Box Title
        draw.text((134, y + 18), b["title"], fill="#0F172A", font=font_box_title)
        
        # Box Description
        draw.text((56, y + 58), b["desc"], fill="#475569", font=font_box_desc)

    # 3. Right Side Illustration Assembly
    right_img_path = "output/card_right_illustration_qing.jpg"
    if os.path.exists(right_img_path):
        right_img = Image.open(right_img_path)
        # Resize to fit right area
        target_w = 490
        target_h = 580
        right_img = right_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
        
        # Paste right illustration
        img.paste(right_img, (750, start_y))
        
        # Border around illustration container
        draw.rounded_rectangle([750, start_y, 750 + target_w, start_y + target_h], radius=16, outline="#E2E8F0", width=2)

    # Output paths
    out_png = "/Users/zhangwenbin/我的雲端硬碟/Antigravity/國泰社會學生小組分析/output/social_studies_infographic_card.png"
    img.save(out_png)
    print(f"Saved card to {out_png}")

if __name__ == "__main__":
    build_card()
