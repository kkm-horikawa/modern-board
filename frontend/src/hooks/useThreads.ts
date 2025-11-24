import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/services/api';
import type { Thread, PaginatedResponse } from '@/types/api.types';

interface UseThreadsParams {
  page?: number;
  pageSize?: number;
  categoryId?: string;
}

export function useThreads({ page = 1, pageSize = 20, categoryId }: UseThreadsParams = {}) {
  return useQuery({
    queryKey: ['threads', { page, pageSize, categoryId }],
    queryFn: async () => {
      const params = new URLSearchParams({
        page: String(page),
        page_size: String(pageSize),
        ...(categoryId && { category_id: categoryId }),
      });

      const response = await apiClient.get<PaginatedResponse<Thread>>(
        `/threads?${params}`
      );
      return response.data;
    },
  });
}
