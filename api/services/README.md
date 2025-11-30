# services/

The brain. AI and business logic.

**Example:** `chat_service.py`
```python
class ChatService:
    def __init__(self):
        # Load your AI model here
        pass
    
    def reply(self, message: str) -> str:
        # Call OpenAI, LangChain, or your multi-agent system
        response = f"AI says: {message}"
        return response
```

**Used by:** `routes/` (they import and call this)

**Uses:** External APIs, AI models, databases
