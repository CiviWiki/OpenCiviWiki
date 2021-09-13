import os
import uuid
from django.utils.deconstruct import deconstructible


@deconstructible
class PathAndRename(object):
    def __init__(self, sub_path):
        self.sub_path = sub_path

    def __call__(self, instance, filename):
        extension = filename.split(".")[-1]
        new_filename = str(uuid.uuid4())
        filename = "{}.{}".format(new_filename, extension)
        return os.path.join(self.sub_path, filename)
