from PIL import Image
from resizeimage import resizeimage
import os
from pathlib import Path
from flask import current_app

# Define Globals
max_width=1920
static_directory="/static/"
cover_image_path="img/cover-images/"
static_file_path=f"{current_app.root_path}{static_directory}"

def save_cover_image(img,article_slug):
    img_name = f"{article_slug}-cover-image.jpg"
    new_height = int(img.height * (max_width / img.width))
    img = img.resize((max_width,new_height))
    img = resizeimage.resize_crop(img,[1920,900])
    img = img.convert("RGB")
    img.save(f"{static_file_path}{cover_image_path}{img_name}",optimize=True,quality=65)
    return f"{cover_image_path}{img_name}"

def delete_image(img_path):
    path_to_file_to_delete = f"{static_file_path}{img_path}"
    try:
        if os.path.exists(path_to_file_to_delete):
            os.remove(path_to_file_to_delete)
    except Exception as err:
        print(err)
