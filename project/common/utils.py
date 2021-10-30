import os
import uuid
from django.utils.deconstruct import deconstructible
from django.db import connections


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

    return database == connections['default'].vendor
