from channels.routing import route
from my.consumers import ws_connect, ws_disconnect, ws_receive

channel_routing = [
    route("websocket.connect", ws_connect, path=r"^/chat-(?P<room_pk>[0-9_]+)/$"),
    route('websocket.receive', ws_receive, path=r"^/chat-(?P<room_pk>[0-9_]+)/$"),
    route("websocket.disconnect", ws_disconnect, path=r"^/chat-(?P<room_pk>[0-9_]+)/$"),
]
