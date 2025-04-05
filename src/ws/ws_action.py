import json
from uuid import UUID

from fastapi.routing import APIRouter
from fastapi import WebSocket, WebSocketDisconnect

from src.manager import control_manager


ws_action_route= APIRouter()


@ws_action_route.websocket('/ws/control/{room_id}')
async def ws_control(room_id: UUID, websocket: WebSocket):
    await control_manager.connect(room_id, websocket)

    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            if "action" in message:
                await control_manager.update_video_state(room_id, message)

    except WebSocketDisconnect:
        control_manager.disconnect(room_id, websocket)

