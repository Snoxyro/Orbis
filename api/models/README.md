# models/

Data shapes. What your data looks like.

**Example:** `chat.py`
```python
from pydantic import BaseModel

class ChatMessage(BaseModel):
    text: str
    user_id: str = "anonymous"

class ChatResponse(BaseModel):
    response: str
    agent: str = "default"
```

**Used by:**
- `routes/` - validates incoming requests
- `services/` - type hints and structure

Pydantic auto-checks your data. No bad data gets through!
