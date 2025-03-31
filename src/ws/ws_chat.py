from typing import List, Dict, Optional

from fastapi.routing import APIRouter
from fastapi import WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse

app_ws = APIRouter()

class RoomManager:

    class RoomNotExists(Exception):

        @property
        def msg(self):
            return 'Room not exists; Check id room and retry again'

    def __init__(self):
        self.rooms: Dict[str, List[Optional[WebSocket]]] = {}

    async def connect(self, room_id: str, websocket: WebSocket):
        if room_id not in self.rooms:
            raise self.RoomNotExists
        await websocket.accept()
        self.rooms[room_id].append(websocket)

    def disconnect(self, room_id: str, websocket: WebSocket):
        if room_id in self.rooms:
            self.rooms[room_id].remove(websocket)

    def get_active_connections_count(self, room_id: str):
        return len(self.rooms.get(room_id, []))

    def add_room(self, room_id):
        if room_id not in self.rooms:
            self.rooms[room_id] = []

manager = RoomManager()


@app_ws.websocket("/ws/chat/{room_id}")
async def ws_endpoint(room_id: str, websocket: WebSocket):

    try:
        await manager.connect(room_id, websocket)
    except manager.RoomNotExists as exc:
        return JSONResponse(status_code=404, content={'Error': True, 'Room ID': room_id, 'Error Info': exc.msg})

    try:
        while True:
            data = await websocket.receive_text()
            print(type(data))
            for connection in manager.rooms.get(room_id, []):
                await connection.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        manager.disconnect(room_id, websocket)
        for connection in manager.rooms.get(room_id, []):
            await connection.send_text(f"Client # left the chat")

@app_ws.get("/ws/room/{room_id}/connected-count")
async def get_connected_count(room_id: str):
    return {"count": manager.get_active_connections_count(room_id)}
