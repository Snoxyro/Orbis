# API

This is the backend. It talks to the frontend.

## What's inside?

```
api/
├── main.py        # The app starts here
└── app/           # Your code goes here
    ├── routes/    # URLs and endpoints (calls services)
    ├── services/  # The smart stuff (AI, logic)
    └── models/    # Data shapes (used by routes & services)
```

## Flow

```
User → routes → services → response
              ↓
           models (validates data)
```

## Run it

```bash
python main.py
```

Goes to: http://localhost:8000

## How to add stuff

**Add a new endpoint:**
1. Make a file in `app/routes/` (e.g., `user.py`)
2. Copy the pattern from `routes/README.md`
3. Import it in `main.py` and add: `app.include_router(user.router)`

**Add AI logic:**
1. Make a file in `app/services/` (e.g., `rag_service.py`)
2. Write your class/functions
3. Import and use in routes

**Add data model:**
1. Make a file in `app/models/` (e.g., `user.py`)
2. Define Pydantic models
3. Use them in routes for validation

That's it. Build and go!
