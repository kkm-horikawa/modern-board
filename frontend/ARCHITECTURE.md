# Frontend Architecture

## Overview

This document describes the architecture and design decisions for the Modern Board frontend application.

## Technology Stack

### Core Technologies

- **React 19.2**: Latest version with improved performance and new features
- **TypeScript 5.9**: Strict type checking for better code quality
- **Vite 7.1**: Fast build tool with excellent DX

### Routing

- **React Router v7**: Client-side routing with nested routes and layouts

### State Management

We use a hybrid approach for different types of state:

1. **Server State (TanStack Query)**
   - Handles all data from the API
   - Automatic caching, refetching, and synchronization
   - Reduces boilerplate for async operations

2. **Global UI State (Zustand)**
   - Lightweight state management
   - Minimal boilerplate
   - Used for UI state (sidebar, theme, etc.)

3. **Local Component State (React useState/useReducer)**
   - Component-specific state
   - Form state (managed by React Hook Form)

### Data Fetching

- **Axios**: HTTP client with interceptors for auth and error handling
- **TanStack Query**: Declarative data fetching with caching

### Form Management

- **React Hook Form**: Performant form handling with minimal re-renders
- **Zod**: Schema-based validation with TypeScript inference

### Styling

- **Tailwind CSS 4.0**: Utility-first CSS framework
- Responsive design with mobile-first approach

## Project Structure

```
src/
├── components/
│   ├── common/        # Reusable UI components
│   ├── layout/        # Layout components (Header, Footer, etc.)
│   └── features/      # Feature-specific components
├── pages/             # Page components (one per route)
├── hooks/             # Custom React hooks
├── services/          # API services and HTTP client
├── stores/            # Zustand stores for global state
├── types/             # TypeScript type definitions
├── utils/             # Utility functions
├── constants/         # Constants and configuration
└── styles/            # Global styles
```

## Design Patterns

### Component Organization

1. **Pages**: Top-level route components in `src/pages/`
2. **Layouts**: Shared layouts in `src/components/layout/`
3. **Features**: Feature-specific components in `src/components/features/`
4. **Common**: Reusable UI components in `src/components/common/`

### Data Fetching Pattern

```typescript
// Custom hook for data fetching
export function useThreads(params: UseThreadsParams) {
  return useQuery({
    queryKey: ['threads', params],
    queryFn: () => fetchThreads(params),
  });
}

// Usage in component
function ThreadList() {
  const { data, isLoading, error } = useThreads({ page: 1 });

  if (isLoading) return <Loading />;
  if (error) return <Error error={error} />;

  return <div>{/* render threads */}</div>;
}
```

### State Management Pattern

```typescript
// Zustand store
export const useUIStore = create<UIState>((set) => ({
  theme: 'light',
  setTheme: (theme) => set({ theme }),
}));

// Usage in component
function ThemeToggle() {
  const { theme, setTheme } = useUIStore();
  return <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')} />;
}
```

### Form Pattern

```typescript
// Form with React Hook Form + Zod
const schema = z.object({
  title: z.string().min(1, 'Title is required'),
  content: z.string().min(1, 'Content is required'),
});

type FormData = z.infer<typeof schema>;

function CreateThreadForm() {
  const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(schema),
  });

  const onSubmit = (data: FormData) => {
    // Submit to API
  };

  return <form onSubmit={handleSubmit(onSubmit)}>{/* form fields */}</form>;
}
```

## API Integration

### API Client Configuration

The `apiClient` in `src/services/api.ts`:
- Base URL from environment variable
- Request interceptor for adding auth tokens
- Response interceptor for error handling
- 10-second timeout

### Type Safety

All API types are defined in `src/types/api.types.ts`:
- Request/response types
- Entity types (Thread, Post, Category, User)
- Generic types (ApiResponse, PaginatedResponse, ApiError)

## Performance Optimizations

1. **Code Splitting**: Routes are loaded on demand
2. **Query Caching**: TanStack Query caches API responses (5 min stale time)
3. **Memoization**: Use React.memo, useMemo, useCallback where appropriate
4. **Virtualization**: For long lists (to be implemented with react-window)

## Error Handling

1. **API Errors**: Handled by axios interceptor
2. **Query Errors**: Handled by TanStack Query with error boundaries
3. **Form Validation**: Handled by Zod schemas

## Testing Strategy

- **Unit Tests**: Vitest for utility functions and hooks
- **Component Tests**: React Testing Library for component logic
- **Integration Tests**: Test user flows with MSW (Mock Service Worker)

## Future Enhancements

1. **shadcn/ui Integration**: Add pre-built accessible components
2. **Dark Mode**: Implement theme switching
3. **Internationalization**: Add i18n support
4. **PWA**: Add service worker for offline support
5. **Performance Monitoring**: Add analytics and error tracking
