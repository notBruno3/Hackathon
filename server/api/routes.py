from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from uuid import uuid4
from core.participant import Participant
from core.message import Message
from core.event_manager import EventManager
from services.websocket_manager import WebSocketManager

from services.model_manager import ModelManager

router = APIRouter()
event_manager = EventManager()
model_manager = ModelManager()
ws_manager = WebSocketManager()

# --- Request Models ---
class CreateEventRequest(BaseModel):
    event_name: str
    admin_name: str
    admin_id: str

class AddMessageRequest(BaseModel):
    sender_id: str
    text: str

class AddParticipantRequest(BaseModel):
    participant_name: str

class FinalizeRequest(BaseModel):
    admin_id: str

class JoinRequest(BaseModel):
    name: str
    id: str

# --- Routes ---

############### POST REQS ##############
@router.post("/event")
def create_event(req: CreateEventRequest):
    admin = Participant(name=req.admin_name, role="admin", id=req.admin_id)
    event = event_manager.create_event(req.event_name, admin)

    # Add initial message
    initial_message = Message(sender_id="0", text="New event created! Add your expenses")
    event.messages.append(initial_message)

    return {
        "event_id": event.id,
        "admin_id": admin.id,
        "participants": [p.name for p in event.participants]
    }

@router.post("/event/{event_id}/message")
async def add_message(event_id: str, req: AddMessageRequest):
    message = Message(sender_id=req.sender_id, text=req.text)
    try:
        answer = event_manager.add_message_to_event(event_id, message, model_manager)

        import asyncio
        asyncio.create_task(ws_manager.broadcast(event_id, {
            "message": {
                "id": message.id,
                "sender_id": message.sender_id,
                "text": message.text
            }
        }))

        asyncio.create_task(ws_manager.broadcast(event_id, {
            "message": {
                "id": answer.id,
                "sender_id": answer.sender_id,
                "text": answer.text
            }
        }))


        return []
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/event/{event_id}/participant")
def add_participant(event_id: str, req: AddParticipantRequest):
    participant = Participant(req.participant_name)
    try:
        added = event_manager.add_participant_to_event(event_id, participant)
        return {
            "status": "ok",
            "participant": {
                "id": added.id,
                "name": added.name,
                "aliases": added.aliases,
                "role": added.role
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/event/{event_id}/finalize")
def finalize_event(event_id: str, req: FinalizeRequest):
    try:
        result = event_manager.finalize_event(event_id, req.admin_id, model_manager)
        return {"status": "finalized", "result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/event/{event_id}/join")
def join_event(event_id: str, req: JoinRequest):
    participant = Participant(name=req.name, id=req.id)
    try:
        added = event_manager.add_participant_to_event(event_id, participant)
        return {
            "status": "joined",
            "participant": {
                "id": added.id,
                "name": added.name,
                "aliases": added.aliases,
                "role": added.role
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

############### GET REQS ##############
@router.get("/events/{user_id}")
def get_events(user_id: str):
    return event_manager.get_events_by_user(user_id)

@router.get("/event/{event_id}")
def get_event(event_id: str):
    try:
        event = event_manager.get_event(event_id)
        return {
            "id": event.id,
            "name": event.name,
            "is_active": event.is_active,
            "admin": event.admin.name,
            "participants": event.participants,
            "message_history": event.messages
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/event/{event_id}/participants")
def get_participants(event_id: str):
    try:
        event = event_manager.get_event(event_id)
        return [
            {
                "id": p.id,
                "name": p.name,
                "aliases": p.aliases,
                "role": p.role
            }
            for p in event.participants
        ]
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get("/event/{event_id}/messages")
def get_messages(event_id: str):
    try:
        event = event_manager.get_event(event_id)
        return [
            {
                "id": m.id,
                "sender_id": m.sender_id,
                "text": m.text,
                "timestamp": m.timestamp.isoformat()
            }
            for m in event.messages
        ]
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

############### WEBSOCKET ###############

@router.websocket("/ws/{event_id}")
async def websocket_endpoint(websocket: WebSocket, event_id: str):
    await ws_manager.connect(event_id, websocket)
    try:
        while True:
            await websocket.receive_text()  # optional: keep alive
    except WebSocketDisconnect:
        ws_manager.disconnect(event_id, websocket)