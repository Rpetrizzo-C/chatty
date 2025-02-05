from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import json
import logging
from ..models.chat import active_rooms
from ..services.chat_service import ChatService

logger = logging.getLogger(__name__)
router = APIRouter()


@router.websocket("/ws/{room_id}/{username}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, username: str):
    logger.info(f"Connection attempt - Room ID: {room_id}")

    if room_id not in active_rooms:
        logger.warning(f"Room not found: {room_id}")
        await websocket.close(code=4000)
        return

    room = active_rooms[room_id]

    try:
        await ChatService.handle_new_participant(room, username, websocket)

        while True:
            data = await websocket.receive_text()
            message = json.loads(data)

            await ChatService.broadcast_message(
                room,
                {
                    "sender": username,
                    "message": message["content"],
                    "timestamp": message["timestamp"],
                },
            )

    except WebSocketDisconnect:
        logger.info(f"Client disconnected from room: {room_id}")
        await ChatService.handle_participant_disconnect(room, username)
