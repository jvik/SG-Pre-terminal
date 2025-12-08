import '@testing-library/jest-dom';
import { vi } from 'vitest';

// Mock localStorage
const localStorageMock = {
    getItem: vi.fn(),
    setItem: vi.fn(),
    removeItem: vi.fn(),
    clear: vi.fn(),
};

global.localStorage = localStorageMock as any;

// Mock fetch
global.fetch = vi.fn();

// Mock $app/environment
vi.mock('$app/environment', () => ({
    browser: true,
    dev: true,
    building: false,
    version: 'test',
}));
