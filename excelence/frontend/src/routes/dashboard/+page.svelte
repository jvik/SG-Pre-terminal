<script lang="ts">
	import { onMount } from "svelte";
	import TransactionForm from "$lib/components/shared/TransactionForm.svelte";
	import SpendingChart from "$lib/components/routes/dashboard/SpendingChart.svelte";
	import IncomeExpenseChart from "$lib/components/routes/dashboard/IncomeExpenseChart.svelte";
	import BalanceChart from "$lib/components/routes/dashboard/BalanceChart.svelte";
	import {
		categories,
		transactions,
		summary,
		chartData,
		loadCategories,
		loadTransactions,
	} from "$lib/stores/data";
	import { createTransaction, exportTransactions } from "$lib/services/api";
	import type { Transaction } from "$lib/types";

	let showTransactionModal = false;
	let selectedMonth = "";

	// Computed filtered transactions
	$: filteredTransactions = selectedMonth
		? $transactions.filter((t) => {
				const transactionMonth = t.date.substring(0, 7); // YYYY-MM
				return transactionMonth === selectedMonth;
		  })
		: $transactions;

	// Computed summary based on filtered transactions
	$: filteredSummary = {
		total_income: filteredTransactions
			.filter((t) => t.type === "income")
			.reduce((sum, t) => sum + t.amount, 0),
		total_expenses: filteredTransactions
			.filter((t) => t.type === "expense")
			.reduce((sum, t) => sum + t.amount, 0),
		net_balance: 0, // Will be computed below
	};
	$: filteredSummary.net_balance =
		filteredSummary.total_income - filteredSummary.total_expenses;

	// Computed chart data based on filtered transactions
	$: filteredChartData = (() => {
		const expensesByCategory = new Map();
		filteredTransactions
			.filter((t) => t.type === "expense")
			.forEach((t) => {
				const current = expensesByCategory.get(t.category_id) || 0;
				expensesByCategory.set(t.category_id, current + t.amount);
			});

		return Array.from(expensesByCategory.entries()).map(
			([categoryId, amount]) => {
				const category = $categories.find((c) => c.id === categoryId);
				return {
					category_name: category?.name || "Unknown",
					total_amount: amount,
				};
			}
		);
	})();

	// Get available months from transactions
	$: availableMonths = (() => {
		const months = new Set(
			$transactions.map((t) => t.date.substring(0, 7))
		);
		return Array.from(months).sort().reverse();
	})();

	onMount(async () => {
		await loadCategories();
		await loadTransactions(); // This will also trigger loadSummary()
	});

	async function handleSaveTransaction(data: any) {
		try {
			await createTransaction(data);
			await loadTransactions(); // Refreshes both transactions and summary
			showTransactionModal = false;
		} catch (error) {
			alert(`Error creating transaction: ${(error as Error).message}`);
		}
	}

	async function handleExport() {
		try {
			const blob = await exportTransactions();
			const url = window.URL.createObjectURL(blob);
			const a = document.createElement("a");
			a.href = url;
			a.download = "export.csv";
			document.body.appendChild(a);
			a.click();
			window.URL.revokeObjectURL(url);
			document.body.removeChild(a);
		} catch (error) {
			alert(`Error exporting data: ${(error as Error).message}`);
		}
	}
</script>

<div class="p-8 bg-gray-50 dark:bg-slate-900 min-h-screen">
	<div class="flex justify-between items-center mb-6">
		<h1 class="text-3xl font-bold text-gray-800 dark:text-white">
			Dashboard
		</h1>
		<div class="flex gap-4 items-center">
			<div class="flex items-center gap-2">
				<label
					for="month-filter"
					class="text-sm font-medium text-gray-700 dark:text-slate-300"
				>
					Month:
				</label>
				<select
					id="month-filter"
					bind:value={selectedMonth}
					class="px-3 py-2 border border-gray-300 dark:border-slate-600 rounded-md shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-slate-700 text-gray-900 dark:text-white text-sm"
				>
					<option value="">All Time</option>
					{#each availableMonths as month}
						<option value={month}>
							{new Date(month + "-01").toLocaleDateString("en-US", {
								year: "numeric",
								month: "long",
							})}
						</option>
					{/each}
				</select>
			</div>
			<button
				on:click={handleExport}
				class="bg-white dark:bg-slate-700 hover:bg-gray-100 dark:hover:bg-slate-600 text-gray-800 dark:text-white font-semibold py-2 px-4 border border-gray-400 dark:border-slate-600 rounded shadow transition-colors"
			>
				📊 Export to CSV
			</button>
			<button
				on:click={() => (showTransactionModal = true)}
				class="bg-blue-500 hover:bg-blue-700 dark:bg-blue-600 dark:hover:bg-blue-700 text-white font-bold py-2 px-4 rounded shadow transition-colors"
			>
				+ Add Transaction
			</button>
		</div>
	</div>

	<!-- Quick Stats -->
	<div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
		<div
			class="bg-gradient-to-br from-green-400 to-green-600 rounded-lg p-6 text-white shadow-lg"
		>
			<div class="flex items-center justify-between">
				<div>
					<p class="text-sm opacity-90">Total Income</p>
					<p class="text-3xl font-bold mt-2">
						{filteredSummary.total_income.toFixed(2)} kr
					</p>
				</div>
				<div class="text-5xl opacity-75">💵</div>
			</div>
		</div>

		<div
			class="bg-gradient-to-br from-red-400 to-red-600 rounded-lg p-6 text-white shadow-lg"
		>
			<div class="flex items-center justify-between">
				<div>
					<p class="text-sm opacity-90">Total Expenses</p>
					<p class="text-3xl font-bold mt-2">
						{filteredSummary.total_expenses.toFixed(2)} kr
					</p>
				</div>
				<div class="text-5xl opacity-75">💸</div>
			</div>
		</div>

		<div
			class="bg-gradient-to-br from-blue-400 to-blue-600 rounded-lg p-6 text-white shadow-lg"
		>
			<div class="flex items-center justify-between">
				<div>
					<p class="text-sm opacity-90">Net Balance</p>
					<p class="text-3xl font-bold mt-2">
						{filteredSummary.net_balance >= 0
							? "+"
							: ""}{filteredSummary.net_balance.toFixed(2)} kr
					</p>
				</div>
				<div class="text-5xl opacity-75">
					{filteredSummary.net_balance >= 0 ? "✅" : "⚠️"}
				</div>
			</div>
		</div>
	</div>

	<!-- Charts Grid -->
	<div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
		<!-- Income vs Expenses Bar Chart -->
		<div
			class="bg-white dark:bg-slate-800 shadow-lg rounded-lg p-6 border border-gray-200 dark:border-slate-700"
		>
			<h2
				class="text-xl font-bold mb-4 text-gray-800 dark:text-white flex items-center gap-2"
			>
				<span class="text-2xl">💰</span>
				Income vs Expenses
			</h2>
			<IncomeExpenseChart
				totalIncome={filteredSummary.total_income}
				totalExpenses={filteredSummary.total_expenses}
			/>
		</div>

		<!-- Spending Breakdown Pie Chart -->
		<div
			class="bg-white dark:bg-slate-800 shadow-lg rounded-lg p-6 border border-gray-200 dark:border-slate-700"
		>
			<h2
				class="text-xl font-bold mb-4 text-gray-800 dark:text-white flex items-center gap-2"
			>
				<span class="text-2xl">📈</span>
				Spending Breakdown
			</h2>
			<SpendingChart chartData={filteredChartData} />
		</div>
	</div>

	<!-- Net Balance Chart -->
	<div
		class="bg-white dark:bg-slate-800 shadow-lg rounded-lg p-6 border border-gray-200 dark:border-slate-700"
	>
		<h2
			class="text-xl font-bold mb-4 text-gray-800 dark:text-white flex items-center gap-2"
		>
			<span class="text-2xl">🏦</span>
			Net Balance
		</h2>
		<BalanceChart netBalance={filteredSummary.net_balance} />
	</div>
</div>

{#if showTransactionModal}
	<TransactionForm
		categories={$categories}
		onClose={() => (showTransactionModal = false)}
		onSave={handleSaveTransaction}
	/>
{/if}
