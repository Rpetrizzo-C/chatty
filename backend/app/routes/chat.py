from fastapi import APIRouter, HTTPException
import secrets
from ..models.chat import ChatRoom, active_rooms
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/rooms/create")
async def create_room(creator_name: str, hashed_password: str, encryption_key: str):
    room_id = secrets.token_urlsafe(8)
    logger.info(f"Creating new room with ID: {room_id}")

    active_rooms[room_id] = ChatRoom(
        id=room_id,
        password=hashed_password,
        participants={},
        creator=creator_name,
        encryption_key=encryption_key,
    )

    return {"room_id": room_id}


@router.post("/rooms/verify")
async def verify_room(room_id: str, hashed_password: str):
    logger.info(f"Verifying room: {room_id}")

    if room_id not in active_rooms:
        logger.warning(f"Room not found: {room_id}")
        raise HTTPException(status_code=404, detail="Room not found")

    room = active_rooms[room_id]
    if room.password != hashed_password:
        logger.warning(f"Invalid password for room: {room_id}")
        raise HTTPException(status_code=401, detail="Invalid password")

    logger.info(f"Room {room_id} verified successfully")
    return {"valid": True, "encryption_key": room.encryption_key}
