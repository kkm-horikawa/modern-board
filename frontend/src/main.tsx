import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import App from './App.tsx';
import ErrorBoundary from './components/common/ErrorBoundary';
import { ToastProvider } from './contexts/ToastContext';
import { ToastContainer } from './components/common/ToastContainer';

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <ErrorBoundary>
      <ToastProvider>
        <App />
        <ToastContainer />
      </ToastProvider>
    </ErrorBoundary>
  </StrictMode>,
);
