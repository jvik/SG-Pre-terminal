import { render, screen, waitFor, fireEvent } from '@testing-library/svelte';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import TransactionList from './TransactionList.svelte';
import userEvent from '@testing-library/user-event';

// Mock the API service
vi.mock('$lib/services/api', () => ({
  getTransactions: vi.fn(),
  getCategories: vi.fn(() => Promise.resolve({ data: [] })),
  updateTransaction: vi.fn(),
  deleteTransaction: vi.fn(),
}));

import { getTransactions, deleteTransaction } from '$lib/services/api';

const mockTransactions = [
  {
    id: '1',
    date: '2025-12-05',
    description: 'Coffee',
    amount: 5.00,
    type: 'expense',
    category_id: 'cat1',
  },
  {
    id: '2',
    date: '2025-12-04',
    description: 'Salary',
    amount: 2000.00,
    type: 'income',
    category_id: 'cat2',
  },
];


describe('TransactionList Component', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders a list of transactions on successful fetch', async () => {
    getTransactions.mockResolvedValue({ data: mockTransactions });
    render(TransactionList);

    await waitFor(() => {
      expect(screen.getByText('Coffee')).toBeInTheDocument();
      expect(screen.getByText('Salary')).toBeInTheDocument();
      expect(screen.getByText('-$5.00')).toBeInTheDocument();
      expect(screen.getByText('+$2000.00')).toBeInTheDocument();
    });
  });

  it('renders the empty state message when no transactions are returned', async () => {
    getTransactions.mockResolvedValue({ data: [] });
    render(TransactionList);

    await waitFor(() => {
      expect(screen.getByText('No transactions found. Add one to get started!')).toBeInTheDocument();
    });
  });

  it('renders an error message when the fetch fails', async () => {
    getTransactions.mockRejectedValue(new Error('Failed to fetch'));
    render(TransactionList);

    await waitFor(() => {
      expect(screen.getByText('Error: Failed to fetch')).toBeInTheDocument();
    });
  });

  it('opens delete confirmation modal when delete button is clicked', async () => {
    const user = userEvent.setup();
    getTransactions.mockResolvedValue({ data: mockTransactions });
    render(TransactionList);

    await waitFor(() => {
      expect(screen.getAllByText('Delete')[0]).toBeInTheDocument();
    });

    const deleteBtns = screen.getAllByText('Delete');
    await user.click(deleteBtns[0]);

    expect(screen.getByText('Are you sure you want to delete this transaction? This action cannot be undone.')).toBeInTheDocument();
    expect(screen.getByText('Confirm')).toBeInTheDocument();
  });

  it('calls deleteTransaction and refreshes list on confirmation', async () => {
    const user = userEvent.setup();
    getTransactions.mockResolvedValueOnce({ data: mockTransactions }); // Initial load
    deleteTransaction.mockResolvedValue({});
    getTransactions.mockResolvedValueOnce({ data: [mockTransactions[1]] }); // After delete

    render(TransactionList);

    await waitFor(() => {
      expect(screen.getByText('Coffee')).toBeInTheDocument();
    });

    // Click delete on first item
    const deleteBtns = screen.getAllByText('Delete');
    await user.click(deleteBtns[0]);

    // Click confirm
    const confirmBtn = screen.getByText('Confirm');
    await user.click(confirmBtn);

    await waitFor(() => {
      expect(deleteTransaction).toHaveBeenCalledWith('1');
      // Should verify list is refreshed, but that depends on implementation details of loadData call.
      // We mocked getTransactions a second time, so if it's called again, that's good.
      expect(getTransactions).toHaveBeenCalledTimes(2); 
    });
  });

  it('does not delete if cancel is clicked', async () => {
    const user = userEvent.setup();
    getTransactions.mockResolvedValue({ data: mockTransactions });
    render(TransactionList);

    await waitFor(() => {
      expect(screen.getByText('Coffee')).toBeInTheDocument();
    });

    // Click delete
    const deleteBtns = screen.getAllByText('Delete');
    await user.click(deleteBtns[0]);

    // Click cancel
    const cancelBtn = screen.getByText('Cancel');
    await user.click(cancelBtn);

    await waitFor(() => {
      expect(screen.queryByText('Confirm Action')).not.toBeInTheDocument();
      expect(deleteTransaction).not.toHaveBeenCalled();
    });
  });
});