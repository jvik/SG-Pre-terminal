import { writable } from 'svelte/store';
import { getCategories, getTransactions, getSummary } from '$lib/services/api';

// --- Stores ---
export const categories = writable([]);
export const transactions = writable([]);
export const summary = writable({
	total_income: 0,
	total_expenses: 0,
	net_balance: 0
});

// --- Loading Functions ---
export const loadCategories = async () => {
	try {
		const data = await getCategories();
		categories.set(data);
	} catch (error) {
		console.error('Failed to load categories:', error);
	}
};

export const loadSummary = async () => {
	try {
		const data = await getSummary();
		summary.set(data);
	} catch (error) {
		console.error('Failed to load summary:', error);
	}
};

export const loadTransactions = async () => {
	try {
		const data = await getTransactions();
		transactions.set(data);
		// Always refresh summary when transactions change
		await loadSummary();
	} catch (error) {
		console.error('Failed to load transactions:', error);
	}
};
