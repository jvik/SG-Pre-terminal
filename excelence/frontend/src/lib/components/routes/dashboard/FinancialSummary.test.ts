import { render, screen, waitFor, within } from '@testing-library/svelte';
import { describe, it, expect, vi } from 'vitest';
import FinancialSummary from './FinancialSummary.svelte';

// Mock the API service
vi.mock('$lib/services/api', () => ({
  getSummary: vi.fn(),
}));

import { getSummary } from '$lib/services/api';

describe('FinancialSummary Component', () => {
  it('renders the summary data on successful fetch', async () => {
    const mockSummary = {
      total_income: 1000,
      total_expenses: 500,
      net_balance: 500,
    };
    // @ts-ignore
    getSummary.mockResolvedValue(mockSummary);

    render(FinancialSummary, {
      total_income: mockSummary.total_income,
      total_expenses: mockSummary.total_expenses,
      net_balance: mockSummary.net_balance,
    });

    await waitFor(() => {
      const incomeCard = screen.getByTestId('stat-card-total-income');
      expect(within(incomeCard).getByText('Total Income')).toBeInTheDocument();
      expect(within(incomeCard).getByText('$1,000.00')).toBeInTheDocument();

      const expensesCard = screen.getByTestId('stat-card-total-expenses');
      expect(within(expensesCard).getByText('Total Expenses')).toBeInTheDocument();
      expect(within(expensesCard).getByText('$500.00')).toBeInTheDocument();

      const netBalanceCard = screen.getByTestId('stat-card-net-balance');
      expect(within(netBalanceCard).getByText('Net Balance')).toBeInTheDocument();
      expect(within(netBalanceCard).getByText('$500.00')).toBeInTheDocument();
    });
  });
});
