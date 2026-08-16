import os
from PIL import ImageFont

# Test Mac font paths for bold fonts
paths = [
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/System/Library/Fonts/Hiragino Sans GB.ttc"
]

for p in paths:
    if os.path.exists(p):
        print("Found font:", p)
        try:
            # Try index 1 or 2 for bold
            f = ImageFont.truetype(p, 30, index=2)
            print("Loaded bold index 2 for:", p)
        except Exception as e:
            print("Error loading index:", e)
