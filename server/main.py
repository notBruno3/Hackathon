from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class EventRequest(BaseModel):
    description: str  # e.g. "I paid €20 for pizza, Pablo €15 for drinks..."

@app.post("/split")
def split_event(event: EventRequest):
    # Placeholder logic
    return {"message": "We'll split: " + event.description}
