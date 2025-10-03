from fastapi import HTTPException, status
from app.base import *
from datetime import datetime
from PIL import Image, ExifTags
from fastapi import BackgroundTasks
from app.utils.util import get_local_time
from sqlalchemy.orm import Session
from app.utils import util
import pathlib
from io import BytesIO
import os
# import aiofiles
from pathlib import Path

DEFAULT_CHUNK_SIZE = 1024 * 1024  # 1 megabytes

def compress_image(image_data, save_path):
    """
    Save and compress an image.
    
    :param image_data: Binary data of the image.
    :param save_path: Path where the image will be saved.
    :raises Exception: If an error occurs during processing.
    """
    # Save the original image
    with open(save_path, "wb") as file_object:
        file_object.write(image_data)

    # Open and process the image
    image = Image.open(BytesIO(image_data))
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = image._getexif()
        if exif is not None:
            orientation = exif.get(orientation)
            if orientation == 3:
                image = image.rotate(180, expand=True)
            elif orientation == 6:
                image = image.rotate(270, expand=True)
            elif orientation == 8:
                image = image.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError):
        pass

    # Compress the image
    image.thumbnail((800, 600), Image.LANCZOS)
    image.save(save_path, format=image.format)


