import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { QueryClientProvider } from '@tanstack/react-query';
import { queryClient } from '@/services/queryClient';
import MainLayout from '@/components/layout/MainLayout';
import HomePage from '@/pages/HomePage';
import ThreadDetailPage from '@/pages/ThreadDetailPage';
import CreateThreadPage from '@/pages/CreateThreadPage';
import NotFoundPage from '@/pages/NotFoundPage';
import { ROUTES } from '@/constants/routes';

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route element={<MainLayout />}>
            <Route path={ROUTES.HOME} element={<HomePage />} />
            <Route path={ROUTES.THREAD_DETAIL} element={<ThreadDetailPage />} />
            <Route path={ROUTES.CREATE_THREAD} element={<CreateThreadPage />} />
            <Route path={ROUTES.NOT_FOUND} element={<NotFoundPage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
