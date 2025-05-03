from __future__ import annotations

from .participant import Participant
from .message import Message
from .transaction import Transaction
from .event import Event
from typing import Dict, List
from services.model_manager import ModelManager
from uuid import uuid4

class EventManager:
    def __init__(self):
        self.events: Dict[str, Event] = {}

    def create_event(self, name: str, admin: Participant) -> Event:
        event_id = str(uuid4())
        event = Event(id=event_id, name=name, admin=admin)
        self.events[event_id] = event
        return event

    def get_event(self, event_id: str) -> Event:
        if event_id not in self.events:
            raise ValueError(f"Event with ID '{event_id}' not found")
        return self.events[event_id]
    
    def get_events_by_user(self, user_id: str) -> List[Event]:
        return [
            event
            for event in self.events.values()
            if any(p.id == user_id for p in event.participants)
        ]

    def add_message_to_event(self, event_id: str, message: Message, model_manager: ModelManager) -> Message:
        event = self.get_event(event_id)
        if not event.is_active:
            raise RuntimeError("Cannot add messages to a closed event")
        return event.add_message(message, model_manager)
    
    def add_participant_to_event(self, event_id: str, participant) -> Participant:
        event = self.get_event(event_id)
        if not event.is_active:
            raise RuntimeError("Cannot add participants to a closed event")
        return event.add_participant(participant)

    def finalize_event(self, event_id: str, admin_id: str, model_manager: ModelManager) -> Dict:
        event = self.get_event(event_id)
        if event.admin.id != admin_id:
            raise PermissionError("Only the event admin can finalize the event")
        return event.end_event(model_manager)
