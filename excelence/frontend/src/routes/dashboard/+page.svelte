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

	let showTransactionModal = false;

	onMount(async () => {
		await loadCategories();
		await loadTransactions(); // This will also trigger loadSummary()
	});

	async function handleSaveTransaction(event) {
		try {
			await createTransaction(event.detail);
			await loadTransactions(); // Refreshes both transactions and summary
			showTransactionModal = false;
		} catch (error) {
			alert(`Error creating transaction: ${error.message}`);
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
			alert(`Error exporting data: ${error.message}`);
		}
	}
</script>

<div class="p-8 bg-gray-50 min-h-screen">
	<div class="flex justify-between items-center mb-6">
		<h1 class="text-3xl font-bold text-gray-800">Dashboard</h1>
		<div class="flex gap-4">
			<button
				on:click={handleExport}
				class="bg-white hover:bg-gray-100 text-gray-800 font-semibold py-2 px-4 border border-gray-400 rounded shadow transition-colors"
			>
				📊 Export to CSV
			</button>
			<button
				on:click={() => (showTransactionModal = true)}
				class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded shadow transition-colors"
			>
				+ Add Transaction
			</button>
		</div>
	</div>

	<!-- Quick Stats -->
	<div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
		<div class="bg-gradient-to-br from-green-400 to-green-600 rounded-lg p-6 text-white shadow-lg">
			<div class="flex items-center justify-between">
				<div>
					<p class="text-sm opacity-90">Total Income</p>
					<p class="text-3xl font-bold mt-2">{$summary.total_income.toFixed(2)} kr</p>
				</div>
				<div class="text-5xl opacity-75">💵</div>
			</div>
		</div>

		<div class="bg-gradient-to-br from-red-400 to-red-600 rounded-lg p-6 text-white shadow-lg">
			<div class="flex items-center justify-between">
				<div>
					<p class="text-sm opacity-90">Total Expenses</p>
					<p class="text-3xl font-bold mt-2">{$summary.total_expenses.toFixed(2)} kr</p>
				</div>
				<div class="text-5xl opacity-75">💸</div>
			</div>
		</div>

		<div class="bg-gradient-to-br from-blue-400 to-blue-600 rounded-lg p-6 text-white shadow-lg">
			<div class="flex items-center justify-between">
				<div>
					<p class="text-sm opacity-90">Net Balance</p>
					<p class="text-3xl font-bold mt-2">
						{$summary.net_balance >= 0 ? '+' : ''}{$summary.net_balance.toFixed(2)} kr
					</p>
				</div>
				<div class="text-5xl opacity-75">
					{$summary.net_balance >= 0 ? '✅' : '⚠️'}
				</div>
			</div>
		</div>
	</div>

	<!-- Charts Grid -->
	<div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
		<!-- Income vs Expenses Bar Chart -->
		<div class="bg-white shadow-lg rounded-lg p-6">
			<h2 class="text-xl font-bold mb-4 text-gray-800 flex items-center gap-2">
				<span class="text-2xl">💰</span>
				Income vs Expenses
			</h2>
			<IncomeExpenseChart 
				totalIncome={$summary.total_income} 
				totalExpenses={$summary.total_expenses} 
			/>
		</div>

		<!-- Spending Breakdown Pie Chart -->
		<div class="bg-white shadow-lg rounded-lg p-6">
			<h2 class="text-xl font-bold mb-4 text-gray-800 flex items-center gap-2">
				<span class="text-2xl">📈</span>
				Spending Breakdown
			</h2>
			<SpendingChart chartData={$chartData} />
		</div>
	</div>

	<!-- Net Balance Chart -->
	<div class="bg-white shadow-lg rounded-lg p-6">
		<h2 class="text-xl font-bold mb-4 text-gray-800 flex items-center gap-2">
			<span class="text-2xl">🏦</span>
			Net Balance
		</h2>
		<BalanceChart netBalance={$summary.net_balance} />
	</div>
</div>

{#if showTransactionModal}
	<TransactionForm
		categories={$categories}
		onClose={() => (showTransactionModal = false)}
		onSave={handleSaveTransaction}
	/>
{/if}
