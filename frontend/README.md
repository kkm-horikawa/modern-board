# Modern Board Frontend

A modern discussion board application built with React 19.2, TypeScript 5.9, and Vite 7.1.

## Tech Stack

- **React 19.2** - UI framework
- **TypeScript 5.9** - Type safety
- **Vite 7.1** - Build tool and dev server
- **React Router v7** - Routing
- **Zustand** - State management
- **TanStack Query (React Query)** - Data fetching and caching
- **Axios** - HTTP client
- **React Hook Form** - Form management
- **Zod** - Schema validation
- **Tailwind CSS 4.0** - Styling
- **date-fns** - Date utilities

## Project Structure

```
src/
├── components/        # Reusable components
│   ├── common/       # Generic UI components (Button, Input, etc.)
│   ├── layout/       # Layout components (Header, Footer, etc.)
│   └── features/     # Feature-specific components
├── pages/            # Page components
├── hooks/            # Custom React hooks
├── services/         # API services and clients
├── stores/           # Zustand stores
├── types/            # TypeScript type definitions
├── utils/            # Utility functions
├── constants/        # Constants and configuration
└── styles/           # Global styles
```

## Getting Started

### Prerequisites

- Node.js 18+ (recommended 20+)
- pnpm 10+ (or npm/yarn)

### Installation

1. Install dependencies:

```bash
pnpm install
```

2. Create environment file:

```bash
cp .env.example .env
```

3. Configure environment variables in `.env`:

```env
VITE_API_BASE_URL=http://localhost:8000/api
```

### Development

Start the development server:

```bash
pnpm dev
```

The app will be available at `http://localhost:5173`

### Building for Production

```bash
pnpm build
```

### Running Tests

```bash
# Run tests
pnpm test

# Run tests in watch mode
pnpm test:watch

# Run tests with coverage
pnpm test:coverage
```

### Linting and Formatting

```bash
# Check and auto-fix with Biome
pnpm lint

# Fix all issues
pnpm lint:fix

# Format code
pnpm format
```

## API Integration

The frontend is configured to communicate with the backend API. The base URL can be configured via the `VITE_API_BASE_URL` environment variable.

### API Client

The `apiClient` in `src/services/api.ts` is a pre-configured Axios instance with:
- Request/response interceptors
- Error handling
- Authentication token management
- Base URL configuration

### Data Fetching

Use TanStack Query hooks for data fetching:

```typescript
import { useThreads } from '@/hooks/useThreads';

function MyComponent() {
  const { data, isLoading, error } = useThreads({ page: 1 });
  // ...
}
```

## State Management

### Global State (Zustand)

For UI state and other global state, use Zustand stores:

```typescript
import { useUIStore } from '@/stores/uiStore';

function MyComponent() {
  const { theme, setTheme } = useUIStore();
  // ...
}
```

### Server State (TanStack Query)

For data from the API, use TanStack Query which handles caching, refetching, and synchronization automatically.

## Expanding the ESLint configuration

If you are developing a production application, we recommend updating the configuration to enable type-aware lint rules:

```js
export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...

      // Remove tseslint.configs.recommended and replace with this
      tseslint.configs.recommendedTypeChecked,
      // Alternatively, use this for stricter rules
      tseslint.configs.strictTypeChecked,
      // Optionally, add this for stylistic rules
      tseslint.configs.stylisticTypeChecked,

      // Other configs...
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])
```

You can also install [eslint-plugin-react-x](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-x) and [eslint-plugin-react-dom](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-dom) for React-specific lint rules:

```js
// eslint.config.js
import reactX from 'eslint-plugin-react-x'
import reactDom from 'eslint-plugin-react-dom'

export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...
      // Enable lint rules for React
      reactX.configs['recommended-typescript'],
      // Enable lint rules for React DOM
      reactDom.configs.recommended,
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])
```
