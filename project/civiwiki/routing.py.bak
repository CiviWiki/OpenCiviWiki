from channels.routing import route
from channels import include

from api import consumers

thread_routing = [
    route("websocket.connect", consumers.thread_connect, path=r"^/(?P<thread_id>[a-zA-Z0-9_]+)/$"),
    route("websocket.receive", consumers.thread_message, path=r"^/(?P<thread_id>[a-zA-Z0-9_]+)/$"),
    route("websocket.disconnect", consumers.thread_disconnect, path=r"^/(?P<thread_id>[a-zA-Z0-9_]+)/$"),
]


channel_routing = [

    include(thread_routing, path=r"^/thread"),

    route("websocket.connect", consumers.ws_connect),
    route("websocket.receive", consumers.ws_message),
    route("websocket.disconnect", consumers.ws_disconnect),
]
