import json
from fastapi import WebSocket, WebSocketDisconnect
import logging
from ..models.chat import ChatRoom, active_rooms

logger = logging.getLogger(__name__)


class ChatService:
    @staticmethod
    async def broadcast_message(room: ChatRoom, message: dict):
        for participant_ws in room.participants.values():
            await participant_ws.send_text(json.dumps(message))

    @staticmethod
    async def handle_participant_disconnect(room: ChatRoom, username: str):
        room.participants.pop(username)

        if not room.participants:
            logger.info(f"Room {room.id} is empty, deleting")
            del active_rooms[room.id]
        else:
            await ChatService.broadcast_message(
                room, {"system": True, "message": f"{username} has left the chat"}
            )

    @staticmethod
    async def handle_new_participant(
        room: ChatRoom, username: str, websocket: WebSocket
    ):
        await websocket.accept()
        room.participants[username] = websocket

        await ChatService.broadcast_message(
            room, {"system": True, "message": f"{username} has joined the chat"}
        )
