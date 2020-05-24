from PIL import Image
from io import BytesIO
from resizeimage import resizeimage
import os
from pathlib import Path
from flask import current_app

# Define Globals
path_prefix="/home/eskimotv"
img_suffix="/static/img"
app_prefix="/app/app"
cover_image_path="/cover-images"
img_path=f"{path_prefix}{app_prefix}{img_suffix}"

def save_cover_image(img,article_slug):
   response = requests.get(imgURL)
   img = Image.open(BytesIO(response.content))
   new_height = int(img.height * (max_width / img.width))
   img = img.resize((max_width,new_height))
   img = resizeimage.resize_crop(img,[1920,900])
   img.save(imgPath + imgName,optimize=True,quality=60)
   img = img.resize((480,225))
   img.save(thumbs_path + imgName,optimize=True,quality=60)
   return img_suffix + imgName
