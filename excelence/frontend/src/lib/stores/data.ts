import { writable } from 'svelte/store';
import { getCategories, getTransactions, getSummary, getChartData } from '$lib/services/api';

// --- Stores ---
export const categories = writable([]);
export const transactions = writable([]);
export const summary = writable({
	total_income: 0,
	total_expenses: 0,
	net_balance: 0
});
export const chartData = writable([]);

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

export const loadChartData = async () => {
	try {
		const response = await getChartData();
		console.log('Chart data response:', response);
		console.log('Chart data array:', response.data);
		chartData.set(response.data || []);
	} catch (error) {
		console.error('Failed to load chart data:', error);
	}
};

export const loadTransactions = async () => {
	try {
		const data = await getTransactions();
		transactions.set(data);
		// Always refresh summary and chart data when transactions change
		await loadSummary();
		await loadChartData();
	} catch (error) {
		console.error('Failed to load transactions:', error);
	}
};
