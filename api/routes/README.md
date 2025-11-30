# routes/

API endpoints. What users hit.

**Example:** `chat.py`
```python
from fastapi import APIRouter
from app.services.chat_service import ChatService
from app.models.chat import ChatMessage

router = APIRouter()
chat_service = ChatService()

@router.post("/message")
async def send_message(msg: ChatMessage):
    reply = chat_service.reply(msg.text)
    return {"response": reply}
```

**Connects:**
- Uses `models/` for data shapes
- Calls `services/` to do work
- Returns JSON to frontend
