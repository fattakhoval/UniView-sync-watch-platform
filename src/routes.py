from src.views.auth_view import auth
from src.ws.ws_chat import ws_chat_route
from src.views.view_room import room_router
from src.ws.ws_action import ws_action_route
from src.ws.ws_share_video import ws_video_route


routers = [
    auth,
    room_router,
    ws_chat_route,
    ws_video_route,
    ws_action_route
]
