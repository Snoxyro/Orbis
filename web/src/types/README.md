# types/

TypeScript types.

**Example:** `chat.ts`
```typescript
export interface Message {
  id: string
  text: string
  sender: 'user' | 'bot'
}

export interface ChatResponse {
  message: string
  agent?: string
}
```

**Used everywhere:** Import when you need type safety

Define once, use everywhere
