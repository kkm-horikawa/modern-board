/**
 * Safe localStorage wrapper with error handling
 * Handles cases where localStorage is unavailable (e.g., private browsing mode)
 */

/**
 * Check if localStorage is available
 */
function isLocalStorageAvailable(): boolean {
  try {
    const test = '__localStorage_test__';
    localStorage.setItem(test, test);
    localStorage.removeItem(test);
    return true;
  } catch {
    return false;
  }
}

/**
 * Safely get an item from localStorage
 * @param key - The key to retrieve
 * @param defaultValue - Default value if key doesn't exist or error occurs
 * @returns The stored value or default value
 */
export function getLocalStorage<T>(key: string, defaultValue: T): T {
  if (!isLocalStorageAvailable()) {
    console.warn('localStorage is not available, using default value');
    return defaultValue;
  }

  try {
    const item = localStorage.getItem(key);
    if (item === null) {
      return defaultValue;
    }
    return JSON.parse(item) as T;
  } catch (error) {
    console.error(`Error reading from localStorage (key: ${key}):`, error);
    return defaultValue;
  }
}

/**
 * Safely set an item in localStorage
 * @param key - The key to set
 * @param value - The value to store
 * @returns true if successful, false otherwise
 */
export function setLocalStorage<T>(key: string, value: T): boolean {
  if (!isLocalStorageAvailable()) {
    console.warn('localStorage is not available, cannot save data');
    return false;
  }

  try {
    localStorage.setItem(key, JSON.stringify(value));
    return true;
  } catch (error) {
    console.error(`Error writing to localStorage (key: ${key}):`, error);
    return false;
  }
}

/**
 * Safely remove an item from localStorage
 * @param key - The key to remove
 * @returns true if successful, false otherwise
 */
export function removeLocalStorage(key: string): boolean {
  if (!isLocalStorageAvailable()) {
    console.warn('localStorage is not available');
    return false;
  }

  try {
    localStorage.removeItem(key);
    return true;
  } catch (error) {
    console.error(`Error removing from localStorage (key: ${key}):`, error);
    return false;
  }
}

/**
 * Safely clear all items from localStorage
 * @returns true if successful, false otherwise
 */
export function clearLocalStorage(): boolean {
  if (!isLocalStorageAvailable()) {
    console.warn('localStorage is not available');
    return false;
  }

  try {
    localStorage.clear();
    return true;
  } catch (error) {
    console.error('Error clearing localStorage:', error);
    return false;
  }
}
