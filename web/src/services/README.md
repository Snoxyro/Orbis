# services/

Talk to the backend.

**Example:** Using `api.ts`
```tsx
import api from '../services/api'

const response = await api.post('/chat/message', {
  text: 'Hello!'
})
```

**Contains:**
- `api.ts` - HTTP calls to backend
- Add more services as needed (e.g., `auth.ts`, `storage.ts`)

Keep API logic separate from UI
