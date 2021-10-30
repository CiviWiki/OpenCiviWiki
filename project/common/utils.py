import os
import uuid
import requests
import PIL
from django.utils.deconstruct import deconstructible
from django.db import connections
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.core.exceptions import BadRequest


@deconstructible
class PathAndRename:
    """Return a uuid4 file name with extension"""

    def __init__(self, sub_path):
        self.sub_path = sub_path

    def __call__(self, instance, filename):
        extension = filename.split(".")[-1]
        new_filename = str(uuid.uuid4())
        filename = f"{new_filename}.{extension}"
        return os.path.join(self.sub_path, filename)


def check_database(database):
    """Get the name of database engine running currently"""

    return database == connections["default"].vendor


def check_image_with_pil(image_file):
    """This function uses the PIL library to make sure the image format is supported"""
    try:
        PIL.Image.open(image_file)
    except IOError:
        return False
    return True


def save_image_from_url(model, url):
    """Get image from the URL and save it for `image` field of the model"""

    response = requests.get(url)
    if response.status_code != 200:
        raise BadRequest("Invalid request: Image not found!")

    img_temp = NamedTemporaryFile(delete=True)
    img_temp.write(response.content)
    img_temp.flush()
    img_file = File(img_temp)
    if check_image_with_pil(img_file):
        model.image.save("image.jpg", File(img_temp), save=True)
