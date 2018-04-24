from __future__ import unicode_literals
import os
from channels.asgi import get_channel_layer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "civiwiki.settings")
channel_layer = get_channel_layer()
