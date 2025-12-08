<script lang="ts">
	import { onMount } from "svelte";
	import TransactionForm from "$lib/components/shared/TransactionForm.svelte";
	import {
		getCategories,
		createTransaction,
		getTransactions,
	} from "$lib/services/api";
	import type { Category, Transaction } from "$lib/types"; // Assuming you have a types file

	let showModal = false;
	let categories: Category[] = [];
	let transactions: Transaction[] = [];
	let errorMessage: string | null = null;

	async function loadData() {
		try {
			categories = await getCategories();
			transactions = await getTransactions();
		} catch (error: any) {
			errorMessage = error.message;
		}
	}

	onMount(loadData);

	async function handleSave(event: CustomEvent) {
		try {
			const newTransaction = await createTransaction(event.detail);
			transactions = [...transactions, newTransaction];
			showModal = false;
			errorMessage = null;
		} catch (error: any) {
			errorMessage = `Failed to save transaction: ${error.message}`;
		}
	}
</script>

<div class="container mx-auto p-4">
	<div class="flex justify-between items-center mb-4">
		<h1 class="text-2xl font-bold">Dashboard</h1>
		<button
			on:click={() => (showModal = true)}
			class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
		>
			Add Transaction
		</button>
	</div>

	{#if errorMessage}
		<div
			class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4"
			role="alert"
		>
			<span class="block sm:inline">{errorMessage}</span>
		</div>
	{/if}

	{#if showModal}
		<TransactionForm
			{categories}
			onSave={handleSave}
			onClose={() => (showModal = false)}
		/>
	{/if}

	<!-- Transaction List Placeholder -->
	<div class="bg-white shadow rounded-lg p-4">
		<h2 class="text-xl font-semibold mb-2">Transactions</h2>
		{#if transactions.length === 0}
			<p>No transactions yet. Click "Add Transaction" to get started.</p>
		{:else}
			<ul>
				{#each transactions as transaction}
					<li>
						{transaction.date}: {transaction.description ||
							"No description"} - {transaction.amount} kr
					</li>
				{/each}
			</ul>
		{/if}
	</div>
</div>
