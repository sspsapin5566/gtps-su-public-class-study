import os
import glob
from PIL import Image

brain_dir = "/Users/zhangwenbin/.gemini/antigravity/brain/73a5c8c4-3a1f-48b6-a788-2e684e569bc1"
files = glob.glob(os.path.join(brain_dir, "**/*.*"), recursive=True)
files.sort(key=os.path.getmtime, reverse=True)

print("Recent files in brain dir:")
for f in files[:15]:
    print(f, os.path.getmtime(f))
