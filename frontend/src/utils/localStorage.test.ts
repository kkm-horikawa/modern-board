import { describe, it, expect, beforeEach, vi } from 'vitest';
import {
  getLocalStorage,
  setLocalStorage,
  removeLocalStorage,
  clearLocalStorage,
} from './localStorage';

describe('localStorage utilities', () => {
  beforeEach(() => {
    localStorage.clear();
    vi.clearAllMocks();
  });

  describe('getLocalStorage', () => {
    it('should return default value when key does not exist', () => {
      const result = getLocalStorage('nonexistent', 'default');
      expect(result).toBe('default');
    });

    it('should return stored value when key exists', () => {
      localStorage.setItem('key', JSON.stringify('value'));
      const result = getLocalStorage('key', 'default');
      expect(result).toBe('value');
    });

    it('should handle complex objects', () => {
      const obj = { name: 'test', count: 42 };
      localStorage.setItem('key', JSON.stringify(obj));
      const result = getLocalStorage('key', {});
      expect(result).toEqual(obj);
    });

    it('should return default value on parse error', () => {
      localStorage.setItem('key', 'invalid json');
      const result = getLocalStorage('key', 'default');
      expect(result).toBe('default');
    });

    it('should return default value when localStorage is unavailable', () => {
      const setItemSpy = vi.spyOn(Storage.prototype, 'setItem');
      setItemSpy.mockImplementation(() => {
        throw new Error('QuotaExceededError');
      });

      const result = getLocalStorage('key', 'default');
      expect(result).toBe('default');

      setItemSpy.mockRestore();
    });
  });

  describe('setLocalStorage', () => {
    it('should store value successfully', () => {
      const result = setLocalStorage('key', 'value');
      expect(result).toBe(true);
      expect(localStorage.getItem('key')).toBe(JSON.stringify('value'));
    });

    it('should store complex objects', () => {
      const obj = { name: 'test', count: 42 };
      const result = setLocalStorage('key', obj);
      expect(result).toBe(true);
      expect(JSON.parse(localStorage.getItem('key')!)).toEqual(obj);
    });

    it('should return false on storage error', () => {
      const setItemSpy = vi.spyOn(Storage.prototype, 'setItem');
      setItemSpy.mockImplementation(() => {
        throw new Error('QuotaExceededError');
      });

      const result = setLocalStorage('key', 'value');
      expect(result).toBe(false);

      setItemSpy.mockRestore();
    });
  });

  describe('removeLocalStorage', () => {
    it('should remove existing key', () => {
      localStorage.setItem('key', 'value');
      const result = removeLocalStorage('key');
      expect(result).toBe(true);
      expect(localStorage.getItem('key')).toBeNull();
    });

    it('should return true even if key does not exist', () => {
      const result = removeLocalStorage('nonexistent');
      expect(result).toBe(true);
    });

    it('should return false on error', () => {
      const removeItemSpy = vi.spyOn(Storage.prototype, 'removeItem');
      removeItemSpy.mockImplementation(() => {
        throw new Error('Error');
      });

      const result = removeLocalStorage('key');
      expect(result).toBe(false);

      removeItemSpy.mockRestore();
    });
  });

  describe('clearLocalStorage', () => {
    it('should clear all items', () => {
      localStorage.setItem('key1', 'value1');
      localStorage.setItem('key2', 'value2');

      const result = clearLocalStorage();
      expect(result).toBe(true);
      expect(localStorage.length).toBe(0);
    });

    it('should return false on error', () => {
      const clearSpy = vi.spyOn(Storage.prototype, 'clear');
      clearSpy.mockImplementation(() => {
        throw new Error('Error');
      });

      const result = clearLocalStorage();
      expect(result).toBe(false);

      clearSpy.mockRestore();
    });
  });
});
