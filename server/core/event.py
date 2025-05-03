from __future__ import annotations

from .participant import Participant
from .message import Message
from .transaction import Transaction
from typing import List, Dict
from services.model_manager import ModelManager


class Event:
    def __init__(self, id: str, name: str, admin: Participant):
        self.id = id
        self.name = name
        self.admin = admin
        self.participants: List[Participant] = [admin]
        self.messages: List[Message] = []
        self.transactions: List[Transaction] = []
        self.is_active: bool = True

    def add_participant(self, participant: Participant) -> Participant:
        if any(p.id == participant.id for p in self.participants):
            raise ValueError(f"Participant with name '{participant.name}' already exists.")
        self.participants.append(participant)
        return participant

    def add_message(self, message: Message, model_manager: ModelManager) -> Message:
        # Add message to log
        self.messages.append(message)

        # Run model to extract transactions
        extracted, answer = model_manager.extract_transactions(
            message=message,
            participants=self.participants
        )
        
        # Attach source message ID to each transaction and store them
        for tx in extracted:
            tx.source_message_id = message.id
            self.transactions.append(tx)

        self.messages.append(answer)
        return answer

    def end_event(self, model_manager: ModelManager) -> Dict:
        if not self.is_active:
            raise RuntimeError("Event is already finalized.")
        self.is_active = False

        settlement = model_manager.compute_settlement(self.transactions)
        return {
            "event_id": self.id,
            "event_name": self.name,
            "participants": [p.name for p in self.participants],
            "settlement": settlement
        }
