import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def generate_perfect_qing_map():
    # Load extracted Qing map
    map_src = "output/qing_map_extracted.png"
    if not os.path.exists(map_src):
        # Fallback to pdf extraction if needed
        import fitz
        doc = fitz.open("media__1786368825692.pdf")
        page = doc[0]
        pix = page.get_pixmap(dpi=300)
        pix.save("output/qing_map_extracted.png")
    
    img = Image.open("output/qing_map_extracted.png").convert("RGBA")
    
    # We will also create a clean version or enhance text on this map image
    # Let's inspect map dimensions
    w, h = img.size
    print(f"Extracted Qing map dimensions: {w}x{h}")
    
if __name__ == "__main__":
    generate_perfect_qing_map()
