# web/

React frontend. The UI.

## What's inside?

```
web/
├── index.html       # Entry HTML
├── vite.config.ts   # Vite settings
├── tsconfig.json    # TypeScript settings
└── src/
    ├── main.tsx         # App starts here
    ├── App.tsx          # Main component
    ├── index.css        # Global styles
    ├── components/      # Reusable UI pieces
    ├── pages/           # Full page views
    ├── services/        # API calls (talks to backend)
    └── types/           # TypeScript types
```

## Run it

```bash
npm run dev
```

Goes to: http://localhost:5173

## How to add stuff

**Add a component:**
1. Create file in `src/components/` (e.g., `ChatBox.tsx`)
2. Export your component
3. Import and use in pages or App

**Add a page:**
1. Create file in `src/pages/` (e.g., `Dashboard.tsx`)
2. Use components inside
3. Add to App routing (when you add routes)

**Call backend:**
1. Use `src/services/api.ts`
2. Example: `api.post('/chat/message', {text: 'hi'})`

Keep it simple!
