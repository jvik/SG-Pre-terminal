<script lang="ts">
	import { onMount } from "svelte";
	import {
		categories,
		transactions,
		loadCategories,
		loadTransactions,
	} from "$lib/stores/data";

	onMount(async () => {
		await loadCategories();
		await loadTransactions();
	});
</script>

<div class="p-8">
	<div class="flex justify-between items-center mb-6">
		<h1 class="text-2xl font-bold">Spreadsheet</h1>
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
							{$categories.find(
								(c) => c.id === transaction.category_id,
							)?.name || "N/A"}
						</td>
						<td
							class="px-4 py-2 text-right"
							class:text-green-600={transaction.type === "income"}
							class:text-red-600={transaction.type === "expense"}
						>
							{transaction.type === "income"
								? "+"
								: "-"}{transaction.amount.toFixed(2)} kr
						</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
</div>
