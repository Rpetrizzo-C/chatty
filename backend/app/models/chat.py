from dataclasses import dataclass
from fastapi import WebSocket
from typing import Dict


@dataclass
class ChatRoom:
    id: str
    password: str
    participants: Dict[str, WebSocket]
    creator: str
    encryption_key: str


# Global state (in a real app, this would be a database)
active_rooms: Dict[str, ChatRoom] = {}
