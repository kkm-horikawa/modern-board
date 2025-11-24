import { describe, it, expect, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { ToastProvider, useToast } from './ToastContext';

function TestComponent() {
  const { showToast, toasts } = useToast();

  return (
    <div>
      <button
        type="button"
        onClick={() => showToast('Test message', 'success')}
      >
        Show Toast
      </button>
      <div data-testid="toast-count">{toasts.length}</div>
      {toasts.map((toast) => (
        <div key={toast.id} data-testid="toast">
          {toast.message} - {toast.type}
        </div>
      ))}
    </div>
  );
}

describe('ToastContext', () => {
  it('should throw error when useToast is used outside provider', () => {
    // Suppress console.error for this test
    const originalError = console.error;
    console.error = vi.fn();

    expect(() => {
      render(<TestComponent />);
    }).toThrow('useToast must be used within a ToastProvider');

    console.error = originalError;
  });

  it('should provide toast functions when wrapped in ToastProvider', () => {
    render(
      <ToastProvider>
        <TestComponent />
      </ToastProvider>,
    );

    expect(screen.getByTestId('toast-count')).toHaveTextContent('0');
  });

  it('should add toast when showToast is called', () => {
    render(
      <ToastProvider>
        <TestComponent />
      </ToastProvider>,
    );

    const button = screen.getByRole('button', { name: /show toast/i });
    button.click();

    expect(screen.getByTestId('toast-count')).toHaveTextContent('1');
    expect(screen.getByTestId('toast')).toHaveTextContent('Test message - success');
  });

  it('should auto-hide toast after duration', async () => {
    render(
      <ToastProvider>
        <TestComponent />
      </ToastProvider>,
    );

    const button = screen.getByRole('button', { name: /show toast/i });
    button.click();

    expect(screen.getByTestId('toast-count')).toHaveTextContent('1');

    // Wait for toast to disappear (default duration is 5000ms)
    await waitFor(
      () => {
        expect(screen.getByTestId('toast-count')).toHaveTextContent('0');
      },
      { timeout: 6000 },
    );
  });

  it('should support multiple toasts', () => {
    render(
      <ToastProvider>
        <TestComponent />
      </ToastProvider>,
    );

    const button = screen.getByRole('button', { name: /show toast/i });
    button.click();
    button.click();
    button.click();

    expect(screen.getByTestId('toast-count')).toHaveTextContent('3');
    expect(screen.getAllByTestId('toast')).toHaveLength(3);
  });
});
