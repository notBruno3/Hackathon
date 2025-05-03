from datetime import datetime
from uuid import uuid4

class Message:
    def __init__(self, sender_id: str, text: str):
        self.id = str(uuid4())
        self.sender_id = sender_id  # references a Participant
        self.text = text

    def __repr__(self):
        return f"Message(from={self.sender_id}, text='{self.text[:20]}...')"
