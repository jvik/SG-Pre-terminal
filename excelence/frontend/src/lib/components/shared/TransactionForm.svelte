<script lang="ts">
	import { createCategory } from "$lib/services/api";

	export let categories: { id: string; name: string }[] = [];
	export let transaction: any = null; // If passed, component is in edit mode
	export let onSave: (data: any) => void;
	export let onClose: () => void;

	let amount: number | null = null;
	let type: "income" | "expense" = "expense";
	let date = new Date().toISOString().split("T")[0];
	let description = "";
	let category_id: string | null = null;
	let showNewCategoryInput = false;
	let newCategoryName = "";

	$: {
		if (transaction) {
			amount = transaction.amount;
			type = transaction.type;
			date = new Date(transaction.date).toISOString().split("T")[0];
			description = transaction.description;
			category_id = transaction.category_id;
		} else {
			// Reset form for "add" mode
			amount = null;
			type = "expense";
			date = new Date().toISOString().split("T")[0];
			description = "";
			category_id = null;
		}
		// Hide new category input when switching transactions
		showNewCategoryInput = false;
		newCategoryName = "";
	}

	async function handleCreateCategory() {
		if (!newCategoryName.trim()) {
			alert("Please enter a category name.");
			return;
		}

		try {
			const newCategory = await createCategory(newCategoryName.trim());
			// Add the new category to the list
			categories = [...categories, newCategory];
			// Select the newly created category
			category_id = newCategory.id;
			// Reset and hide the input
			newCategoryName = "";
			showNewCategoryInput = false;
		} catch (error: any) {
			alert(`Failed to create category: ${error.message}`);
		}
	}

	function handleSave() {
		if (!amount || !category_id) {
			// Basic validation
			alert("Amount and category are required.");
			return;
		}
		const data = {
			amount: Number(amount),
			type,
			date,
			description,
			category_id,
		};
		onSave(data);
	}
</script>

<div
	class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center"
>
	<div class="bg-white p-6 rounded-lg shadow-xl w-full max-w-md">
		<h2 class="text-xl font-bold mb-4">
			{transaction ? "Edit" : "Add"} Transaction
		</h2>
		<form
			on:submit|preventDefault={handleSave}
			data-testid="transaction-form"
		>
			<div class="mb-4">
				<label
					for="amount"
					class="block text-sm font-medium text-gray-700"
					>Amount</label
				>
				<input
					type="number"
					id="amount"
					bind:value={amount}
					class="mt-1 block w-full p-2 border rounded"
					required
				/>
			</div>
			<div class="mb-4">
				<label
					for="type"
					class="block text-sm font-medium text-gray-700">Type</label
				>
				<select
					id="type"
					bind:value={type}
					class="mt-1 block w-full p-2 border rounded"
				>
					<option value="expense">Expense</option>
					<option value="income">Income</option>
				</select>
			</div>
			<div class="mb-4">
				<label
					for="date"
					class="block text-sm font-medium text-gray-700">Date</label
				>
				<input
					type="date"
					id="date"
					bind:value={date}
					class="mt-1 block w-full p-2 border rounded"
					required
				/>
			</div>
			<div class="mb-4">
				<label
					for="category"
					class="block text-sm font-medium text-gray-700"
					>Category</label
				>
				<select
					id="category"
					bind:value={category_id}
					class="mt-1 block w-full p-2 border rounded"
					required
				>
					<option value={null} disabled>Select a category</option>
					{#each categories as category}
						<option value={category.id}>{category.name}</option>
					{/each}
				</select>
				{#if !showNewCategoryInput}
					<button
						type="button"
						on:click={() => (showNewCategoryInput = true)}
						class="mt-2 text-sm text-blue-600 hover:text-blue-800"
					>
						+ Create New Category
					</button>
				{:else}
					<div class="mt-2 flex gap-2">
						<input
							type="text"
							bind:value={newCategoryName}
							placeholder="New category name"
							class="flex-1 p-2 border rounded text-sm"
						/>
						<button
							type="button"
							on:click={handleCreateCategory}
							class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-3 rounded text-sm"
						>
							Add
						</button>
						<button
							type="button"
							on:click={() => {
								showNewCategoryInput = false;
								newCategoryName = "";
							}}
							class="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-3 rounded text-sm"
						>
							Cancel
						</button>
					</div>
				{/if}
			</div>
			<div class="mb-4">
				<label
					for="description"
					class="block text-sm font-medium text-gray-700"
					>Description</label
				>
				<input
					type="text"
					id="description"
					bind:value={description}
					class="mt-1 block w-full p-2 border rounded"
				/>
			</div>
			<div class="flex justify-end gap-4">
				<button type="button" on:click={onClose} class="text-gray-600"
					>Cancel</button
				>
				<button
					type="submit"
					class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
				>
					Save
				</button>
			</div>
		</form>
	</div>
</div>
