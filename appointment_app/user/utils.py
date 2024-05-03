''' Contains utlities functions '''
import os
import secrets
from PIL import Image
from flask import current_app


def save_file(image_file):
    ''' Saves a file in the filesystem '''
    random_file_name = secrets.token_hex(8)
    file_extention = os.path.split(image_file.filename)[1]
    new_file_name = random_file_name + file_extention
    new_file_path = os.path.join(current_app.root_path, 'static/images', new_file_name)
    image = Image.open(image_file)
    image_new_size = (150, 150)
    image.thumbnail(image_new_size)
    image.save(new_file_path)
    return new_file_name
