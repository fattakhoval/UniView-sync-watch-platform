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

        # state = control_manager.video_state.get(room_id)
        # if state:
        #     print(f'state: {state}')
        #     await websocket.send_text(json.dumps(state))

        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            print(message)
            if "action" in message:
                action = message["action"]

                if action == "seek" and "value" in message:
                    await control_manager.broadcast(room_id, json.dumps({
                            "action": "seek",
                            "value": message["value"]
                        }))
                # elif action == "sync_time":
                #     state = control_manager.video_state.get(room_id, {})
                #     state["current_time"] = message["current_time"]
                #
                #     if "filename" in message:
                #         state["filename"] = message["filename"]
                #
                #     await control_manager.update_video_state(room_id, state)

                else:
                    await control_manager.broadcast(room_id, json.dumps(message))

    except WebSocketDisconnect:
        control_manager.disconnect(room_id, websocket)
