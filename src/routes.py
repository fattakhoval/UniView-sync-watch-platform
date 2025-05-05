from src.views.auth_view import auth
from src.views.event_view import event_view
from src.ws.ws_chat import ws_chat_route
from src.views.room_view import room_router
from src.ws.ws_action import ws_action_route
from src.ws.ws_video import ws_video_route
from src.views.video_view import video_router
from src.views.message_view import message_router
from src.views.friend_view import friend_view


routers = [
    auth,
    room_router,
    video_router,
    friend_view,
    event_view,
    message_router,
    ws_chat_route,
    ws_video_route,
    ws_action_route
]
