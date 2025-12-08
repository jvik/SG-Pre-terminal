import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, fireEvent, waitFor } from '@testing-library/svelte';
import CategoriesPage from './+page.svelte';
import * as api from '$lib/services/api';

// Mock the entire api service module
vi.mock('$lib/services/api');

const mockCategories = [
	{ id: 1, name: 'Groceries' },
	{ id: 2, name: 'Salary' }
];

describe('CategoriesPage', () => {
	beforeEach(() => {
		// Reset mocks before each test
		vi.resetAllMocks();
	});

	it('renders loading state and then displays categories', async () => {
		const getCategoriesMock = vi.spyOn(api, 'getCategories').mockResolvedValue(mockCategories);

		const { getByText, findByText } = render(CategoriesPage);

		expect(getByText('Loading categories...')).toBeInTheDocument();

		// Wait for the component to finish loading and display the categories
		await findByText('Groceries');
		expect(getByText('Salary')).toBeInTheDocument();
		expect(getCategoriesMock).toHaveBeenCalledOnce();
	});

	it('handles error during category loading', async () => {
		const errorMessage = 'Failed to fetch';
		vi.spyOn(api, 'getCategories').mockRejectedValue(new Error(errorMessage));

		const { findByText } = render(CategoriesPage);

		const errorElement = await findByText(errorMessage);
		expect(errorElement).toBeInTheDocument();
	});

	it('opens a modal when "Add Category" is clicked', async () => {
		vi.spyOn(api, 'getCategories').mockResolvedValue([]);
		const { getByText, findByRole } = render(CategoriesPage);

		// Wait for loading to complete
		await waitFor(() => expect(getByText('+ Add Category')).toBeInTheDocument());

		const addButton = getByText('+ Add Category');
		await fireEvent.click(addButton);

		const modalTitle = await findByRole('heading', { name: 'Add Category' });
		expect(modalTitle).toBeInTheDocument();
	});

	it('creates a new category and refreshes the list', async () => {
		const getCategoriesMock = vi
			.spyOn(api, 'getCategories')
			.mockResolvedValueOnce([]) // Initial load
			.mockResolvedValueOnce([{ id: 3, name: 'New Category' }]); // After creation

		const createCategoryMock = vi.spyOn(api, 'createCategory').mockResolvedValue({ id: 3, name: 'New Category' });

		const { getByText, getByPlaceholderText, getByRole, findByText } = render(CategoriesPage);

		// Wait for initial load
		await waitFor(() => expect(getByText('+ Add Category')).toBeInTheDocument());

		await fireEvent.click(getByText('+ Add Category'));

		const input = getByPlaceholderText('Enter category name');
		const saveButton = getByRole('button', { name: 'Save' });

		await fireEvent.input(input, { target: { value: 'New Category' } });
		await fireEvent.click(saveButton);

		expect(createCategoryMock).toHaveBeenCalledWith('New Category');

		// Wait for the new category to appear in the list
		const newCategoryElement = await findByText('New Category');
		expect(newCategoryElement).toBeInTheDocument();
		expect(getCategoriesMock).toHaveBeenCalledTimes(2);
	});
    
    it('updates an existing category', async () => {
		vi.spyOn(api, 'getCategories').mockResolvedValue(mockCategories);
        const updateCategoryMock = vi.spyOn(api, 'updateCategory').mockResolvedValue({ id: 1, name: 'Updated Groceries' });

		const { getAllByText, getByRole, getByPlaceholderText, findByText } = render(CategoriesPage);

		// Wait for initial load
		await findByText('Groceries');

        // There are multiple "Edit" buttons, so we use getAllByText
		const editButtons = getAllByText('Edit');
		await fireEvent.click(editButtons[0]);

		const input = getByPlaceholderText('Enter category name');
		const saveButton = getByRole('button', { name: 'Save' });

		await fireEvent.input(input, { target: { value: 'Updated Groceries' } });
		await fireEvent.click(saveButton);

        expect(updateCategoryMock).toHaveBeenCalledWith(1, 'Updated Groceries');
	});

    it('deletes a category after confirmation', async () => {
        vi.spyOn(api, 'getCategories').mockResolvedValue(mockCategories);
        const deleteCategoryMock = vi.spyOn(api, 'deleteCategory').mockResolvedValue({});

        const { getAllByText, getAllByRole, findByText } = render(CategoriesPage);

        await findByText('Groceries');
        
        const deleteButtons = getAllByText('Delete');
        await fireEvent.click(deleteButtons[0]);

        const confirmModalTitle = await findByText('Confirm Deletion');
        expect(confirmModalTitle).toBeInTheDocument();

        const confirmDeleteButtons = getAllByRole('button', { name: 'Delete' });
        const confirmDeleteButton = confirmDeleteButtons[confirmDeleteButtons.length - 1];
        await fireEvent.click(confirmDeleteButton);

        expect(deleteCategoryMock).toHaveBeenCalledWith(1);
    });
});
