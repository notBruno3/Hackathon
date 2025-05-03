from typing import List
from uuid import uuid4

class Participant:
    def __init__(self, name: str, aliases: List[str] = None, role: str = "member", id : str = None):
        self.id = id
        self.name = name  # Canonical name, e.g., "Samu García"
        self.aliases = aliases or []  # e.g., ["Samu", "Sam"]
        self.role = role  # "admin" or "member"

    def is_alias(self, name: str) -> bool:
        return name.strip().lower() in {a.lower() for a in [self.name] + self.aliases}

    def __repr__(self):
        return f"Participant(name={self.name}, role={self.role})"
