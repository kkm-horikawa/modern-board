/**
 * Example component demonstrating toast notification usage
 * This file serves as documentation and can be used for testing
 */

import { useToast } from '../../contexts/ToastContext';
import {
  getLocalStorage,
  setLocalStorage,
} from '../../utils/localStorage';

export function ExampleToastUsage() {
  const { showToast } = useToast();

  const handleSuccess = () => {
    showToast('Operation completed successfully!', 'success');
  };

  const handleError = () => {
    showToast('An error occurred. Please try again.', 'error');
  };

  const handleWarning = () => {
    showToast('This action cannot be undone.', 'warning');
  };

  const handleInfo = () => {
    showToast('New features are available!', 'info');
  };

  const handleSaveSettings = () => {
    const success = setLocalStorage('userSettings', {
      theme: 'dark',
      notifications: true,
    });

    if (success) {
      showToast('Settings saved successfully!', 'success');
    } else {
      showToast('Failed to save settings. Storage may be unavailable.', 'error');
    }
  };

  const handleLoadSettings = () => {
    const settings = getLocalStorage('userSettings', null);

    if (settings) {
      showToast(`Settings loaded: ${JSON.stringify(settings)}`, 'info');
    } else {
      showToast('No saved settings found.', 'warning');
    }
  };

  return (
    <div className="p-8 max-w-2xl mx-auto">
      <h2 className="text-2xl font-bold mb-6">Toast Notification Examples</h2>

      <div className="space-y-4">
        <div>
          <h3 className="text-lg font-semibold mb-2">Basic Toast Types</h3>
          <div className="flex gap-2 flex-wrap">
            <button
              type="button"
              onClick={handleSuccess}
              className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
            >
              Success Toast
            </button>
            <button
              type="button"
              onClick={handleError}
              className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
            >
              Error Toast
            </button>
            <button
              type="button"
              onClick={handleWarning}
              className="px-4 py-2 bg-yellow-500 text-white rounded hover:bg-yellow-600"
            >
              Warning Toast
            </button>
            <button
              type="button"
              onClick={handleInfo}
              className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
            >
              Info Toast
            </button>
          </div>
        </div>

        <div>
          <h3 className="text-lg font-semibold mb-2">
            LocalStorage with Toast Integration
          </h3>
          <div className="flex gap-2">
            <button
              type="button"
              onClick={handleSaveSettings}
              className="px-4 py-2 bg-purple-500 text-white rounded hover:bg-purple-600"
            >
              Save Settings
            </button>
            <button
              type="button"
              onClick={handleLoadSettings}
              className="px-4 py-2 bg-indigo-500 text-white rounded hover:bg-indigo-600"
            >
              Load Settings
            </button>
          </div>
        </div>
      </div>

      <div className="mt-8 p-4 bg-gray-100 rounded">
        <h3 className="font-semibold mb-2">Usage Example:</h3>
        <pre className="text-sm overflow-x-auto">
          {`import { useToast } from './contexts/ToastContext';

function MyComponent() {
  const { showToast } = useToast();

  const handleAction = () => {
    try {
      // Your action here
      showToast('Success!', 'success');
    } catch (error) {
      showToast('Error occurred', 'error');
    }
  };

  return <button onClick={handleAction}>Do Action</button>;
}`}
        </pre>
      </div>
    </div>
  );
}
