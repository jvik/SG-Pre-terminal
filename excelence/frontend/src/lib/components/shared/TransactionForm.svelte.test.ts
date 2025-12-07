import { describe, it, expect, vi } from 'vitest';
import { render, fireEvent, screen } from '@testing-library/svelte';
import userEvent from '@testing-library/user-event';
import TransactionForm from './TransactionForm.svelte';

describe('TransactionForm', () => {
    const mockCategories = [
        { id: 'a4f2b4b0-7b6d-4b7b-8b0a-0e9f3b5a4b1e', name: 'Groceries' },
        { id: 'c2c3e1e0-7b6d-4b7b-8b0a-0e9f3b5a4b1e', name: 'Salary' }
    ];

    const mockTransaction = {
        id: 't1',
        amount: 50.00,
        type: 'expense' as const,
        date: '2025-12-01',
        description: 'Initial purchase',
        category_id: mockCategories[0].id
    };

	it('calls the onSave handler with form data on submit', async () => {
		const user = userEvent.setup();
		const onSave = vi.fn();
		render(TransactionForm, {
			props: {
				categories: mockCategories,
				onSave,
				onClose: vi.fn()
			}
		});

        // Fill out the form
        await user.type(screen.getByLabelText('Amount'), '123.45');
        await user.selectOptions(screen.getByLabelText('Type'), 'expense');
        await fireEvent.input(screen.getByLabelText('Date'), { target: { value: '2025-12-06' } });
        await user.selectOptions(screen.getByLabelText('Category'), mockCategories[0].id);
        await user.type(screen.getByLabelText('Description'), 'Test purchase');

        // Submit the form
        await fireEvent.submit(screen.getByTestId('transaction-form'));

        expect(onSave).toHaveBeenCalledWith({
            amount: 123.45,
            type: 'expense',
            date: '2025-12-06',
            description: 'Test purchase',
            category_id: mockCategories[0].id
        });
    });

	it('calls the onClose handler when cancel is clicked', async () => {
		const user = userEvent.setup();
		const onClose = vi.fn();
		render(TransactionForm, {
			props: {
				categories: mockCategories,
				onSave: vi.fn(),
				onClose
			}
		});

        await user.click(screen.getByText('Cancel'));
        expect(onClose).toHaveBeenCalled();
    });

    it('pre-fills the form when a transaction prop is provided', () => {
        render(TransactionForm, {
            props: {
				categories: mockCategories,
				transaction: mockTransaction,
				onSave: vi.fn(),
				onClose: vi.fn()
			}
        });

        expect(screen.getByLabelText('Amount').value).toBe('50');
        expect(screen.getByLabelText('Type').value).toBe('expense');
        expect(screen.getByLabelText('Date').value).toBe('2025-12-01');
        expect(screen.getByLabelText('Category').value).toBe(mockTransaction.category_id);
        expect(screen.getByLabelText('Description').value).toBe('Initial purchase');
        expect(screen.getByText('Edit Transaction')).toBeInTheDocument();
    });
});