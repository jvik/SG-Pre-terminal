<script lang="ts">
	import { onMount } from 'svelte';
	import TransactionForm from '$lib/components/shared/TransactionForm.svelte';
	import FinancialSummary from '$lib/components/routes/dashboard/FinancialSummary.svelte';
	import {
		categories,
		transactions,
		summary,
		loadCategories,
		loadTransactions
	} from '$lib/stores/data';
	import { createTransaction } from '$lib/services/api';

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
</script>

<div class="p-8">
	<div class="flex justify-between items-center mb-6">
		<h1 class="text-2xl font-bold">Dashboard</h1>
		<button
			on:click={() => (showTransactionModal = true)}
			class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
		>
			+ Add Transaction
		</button>
	</div>

	<div class="mb-6">
		<FinancialSummary {...$summary} />
	</div>

	<div class="bg-white shadow-md rounded">
		<table class="min-w-full table-auto">
			<thead class="bg-gray-200">
				<tr>
					<th class="px-4 py-2 text-left">Date</th>
					<th class="px-4 py-2 text-left">Description</th>
					<th class="px-4 py-2 text-left">Category</th>
					<th class="px-4 py-2 text-right">Amount</th>
				</tr>
			</thead>
			<tbody>
				{#each $transactions as transaction (transaction.id)}
					<tr class="border-b">
						<td class="px-4 py-2">{transaction.date}</td>
						<td class="px-4 py-2">{transaction.description}</td>
						<td class="px-4 py-2">
							{$categories.find((c) => c.id === transaction.category_id)?.name || 'N/A'}
						</td>
						<td
							class="px-4 py-2 text-right"
							class:text-green-600={transaction.type === 'income'}
							class:text-red-600={transaction.type === 'expense'}
						>
							{transaction.type === 'income' ? '+' : '-'}${transaction.amount.toFixed(2)}
						</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
</div>

{#if showTransactionModal}
	<TransactionForm
		categories={$categories}
		on:close={() => (showTransactionModal = false)}
		on:save={handleSaveTransaction}
	/>
{/if}