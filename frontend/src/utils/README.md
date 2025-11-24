# Utility Functions

## localStorage.ts

Safe localStorage wrapper with error handling for private browsing mode and other localStorage failures.

### Usage

```typescript
import {
  getLocalStorage,
  setLocalStorage,
  removeLocalStorage,
  clearLocalStorage,
} from './utils/localStorage';

// Get value with default
const theme = getLocalStorage('theme', 'light');

// Set value
const success = setLocalStorage('theme', 'dark');
if (!success) {
  // Handle error (e.g., show toast notification)
  showToast('Failed to save settings', 'error');
}

// Remove value
removeLocalStorage('theme');

// Clear all
clearLocalStorage();
```

### Features

- Automatic JSON serialization/deserialization
- Type-safe with TypeScript generics
- Graceful fallback when localStorage is unavailable
- Error logging for debugging
- Returns success/failure status for set operations
