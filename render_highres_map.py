import os
import fitz # PyMuPDF
from PIL import Image, ImageDraw, ImageFont

def render_high_res_map():
    pdf_path = "media__1786368825692.pdf"
    doc = fitz.open(pdf_path)
    page = doc[0]
    # Render at 4x scale (300 DPI) for super crisp quality
    pix = page.get_pixmap(matrix=fitz.Matrix(4, 4))
    high_res_path = "output/qing_map_highres.png"
    pix.save(high_res_path)
    print(f"Saved high-res map to {high_res_path}, size: {pix.width}x{pix.height}")

if __name__ == "__main__":
    render_high_res_map()
