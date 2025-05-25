import json
import time

from uuid import UUID

from fastapi.routing import APIRouter
from fastapi import WebSocket, WebSocketDisconnect

from src.manager import control_manager


ws_action_route= APIRouter()


@ws_action_route.websocket('/ws/control/{room_id}')
async def ws_control(room_id: UUID, websocket: WebSocket):
    await control_manager.connect(room_id, websocket)

    state = control_manager.video_state.get(room_id)

    if state and not state.get("master"):
        control_manager.video_state[room_id]["master"] = str(id(websocket))

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
            if state:
                if action in ("play", "pause"):
                    state["status"] = action
                    state["updated_at"] = time.time()

                if action == "seek" and "value" in message:
                    state["timestamp"] = message["value"]
                    state["updated_at"] = time.time()
                print(control_manager.select_master(room_id))
                if action == 'sync':
                    state["timestamp"] = message["value"]
                    state["updated_at"] = time.time()

                    control_manager.video_state[room_id] = state

                    continue

            control_manager.video_state[room_id] = state

            print(f'state: {state}')

            await control_manager.broadcast(room_id, json.dumps(message))

    except WebSocketDisconnect:
        control_manager.disconnect(room_id, websocket)

        if control_manager.video_state.get(room_id, {}).get("master") == str(id(websocket)):
            connections = control_manager.rooms.get(room_id, [])
            if connections:
                new_master = str(id(connections[0]))
                control_manager.video_state[room_id]["master"] = new_master
            else:
                control_manager.video_state[room_id]["master"] = None