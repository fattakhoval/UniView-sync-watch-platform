import json
import time

from uuid import UUID

from fastapi.routing import APIRouter
from fastapi import WebSocket, WebSocketDisconnect

from src.manager import control_manager


ws_action_route= APIRouter()


@ws_action_route.websocket('/ws/control/{room_id}/{user_id}')
async def ws_control(room_id: UUID, user_id: UUID, websocket: WebSocket):
    websocket.user_id = str(user_id)
    await control_manager.connect(room_id, websocket)

    state = control_manager.video_state.get(room_id)

    if state and not state.get("master"):
        control_manager.video_state[room_id]["master"] = websocket.user_id

    try:

        if state:
            await websocket.send_text(json.dumps({
                "action": "sync_state",
                "state": control_manager.video_state[room_id]
            }))

        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            print(f'M: {message}')
            action = message.get('action')

            state = control_manager.video_state.get(room_id)
            master = control_manager.select_master(room_id)
            if state:
                if action in ("play", "pause"):
                    state["status"] = action
                    state["updated_at"] = time.time()

                if action == "seek" and "value" in message and master == websocket.user_id:
                    state["timestamp"] = message["value"]
                    state["updated_at"] = time.time()

                if action == 'sync' and master == websocket.user_id:
                    state["timestamp"] = message["value"]
                    state["updated_at"] = time.time()

                    control_manager.video_state[room_id] = state

                    continue

            control_manager.video_state[room_id] = state

            print(f'state: {state}')

            await control_manager.broadcast(room_id, json.dumps(message))

    except WebSocketDisconnect:
        control_manager.disconnect(room_id, websocket)
