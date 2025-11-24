// Common API response types

export interface ApiResponse<T> {
  data: T;
  message?: string;
  success: boolean;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  pageSize: number;
  totalPages: number;
}

export interface ApiError {
  message: string;
  code?: string;
  details?: unknown;
}

// Thread types
export interface Thread {
  id: string;
  title: string;
  content: string;
  categoryId: string;
  authorId: string;
  createdAt: string;
  updatedAt: string;
  postsCount: number;
  isPinned: boolean;
  isLocked: boolean;
}

export interface CreateThreadInput {
  title: string;
  content: string;
  categoryId: string;
}

export interface UpdateThreadInput {
  title?: string;
  content?: string;
  isPinned?: boolean;
  isLocked?: boolean;
}

// Post types
export interface Post {
  id: string;
  threadId: string;
  content: string;
  authorId: string;
  createdAt: string;
  updatedAt: string;
}

export interface CreatePostInput {
  threadId: string;
  content: string;
}

export interface UpdatePostInput {
  content: string;
}

// Category types
export interface Category {
  id: string;
  name: string;
  description?: string;
  threadsCount: number;
  createdAt: string;
}

// User types (basic)
export interface User {
  id: string;
  username: string;
  email?: string;
  createdAt: string;
}
