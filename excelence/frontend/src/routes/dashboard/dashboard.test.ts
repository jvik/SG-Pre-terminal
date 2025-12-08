import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, fireEvent } from '@testing-library/svelte';
import Dashboard from './+page.svelte';
import * as api from '$lib/services/api';
import { writable } from 'svelte/store';

// Mock stores
vi.mock('$lib/stores/data', async () => {
  const { writable } = await import('svelte/store');
  return {
    categories: writable([{ id: 1, name: 'Food' }]),
    transactions: writable([
        { id: '1', date: '2023-01-01', description: 'Test', category_id: 1, amount: 10, type: 'expense' }
    ]),
    summary: writable({ total_income: 0, total_expenses: 10, net_balance: -10 }),
    chartData: writable([]),
    loadCategories: vi.fn(),
    loadTransactions: vi.fn(),
  };
});

// Mock API
vi.mock('$lib/services/api', () => ({
  createTransaction: vi.fn(),
  exportTransactions: vi.fn(),
}));

// Mock URL and DOM for download
global.URL.createObjectURL = vi.fn(() => 'blob:url');
global.URL.revokeObjectURL = vi.fn();

describe('Dashboard', () => {
    beforeEach(() => {
        vi.clearAllMocks();
    });

  it('renders the Export button', () => {
    const { getByText } = render(Dashboard);
    expect(getByText('Export to CSV')).toBeInTheDocument();
  });

  it('calls exportTransactions when Export button is clicked', async () => {
    // Mock successful blob response
    const mockBlob = new Blob(['csv content'], { type: 'text/csv' });
    (api.exportTransactions as any).mockResolvedValue(mockBlob);

    const { getByText } = render(Dashboard);
    const exportBtn = getByText('Export to CSV');

    await fireEvent.click(exportBtn);

    expect(api.exportTransactions).toHaveBeenCalled();
    expect(global.URL.createObjectURL).toHaveBeenCalledWith(mockBlob);
  });
});
