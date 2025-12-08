<script lang="ts">
	import { createCategory } from "$lib/services/api";

	export let categories: { id: string; name: string; emoji?: string }[] = [];
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
	let newCategoryEmoji = "📂";
	let formError: string | null = null;
	let isCreatingCategory = false;

	// Common emojis for quick category creation
	const commonEmojis = [
		"📂", "🍔", "🏠", "🚗", "💰", "🎮", "📱", "👕",
		"🎬", "✈️", "🏥", "📚", "🎵", "⚽", "🛒", "☕",
	];

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
		newCategoryEmoji = "📂";
		formError = null;
	}

	async function handleCreateCategory() {
		if (!newCategoryName.trim()) {
			formError = "Please enter a category name.";
			return;
		}

		try {
			isCreatingCategory = true;
			formError = null;
			const newCategory = await createCategory(newCategoryName.trim(), newCategoryEmoji);
			// Add the new category to the list
			categories = [...categories, newCategory];
			// Select the newly created category
			category_id = newCategory.id;
			// Reset and hide the input
			newCategoryName = "";
			newCategoryEmoji = "📂";
			showNewCategoryInput = false;
		} catch (error: any) {
			formError = `Failed to create category: ${error.message}`;
		} finally {
			isCreatingCategory = false;
		}
	}

	function handleSave() {
		if (!amount || amount <= 0) {
			formError = "Please enter a valid amount greater than 0.";
			return;
		}
		if (!category_id) {
			formError = "Please select a category.";
			return;
		}
		
		formError = null;
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
	class="fixed inset-0 bg-black bg-opacity-50 backdrop-blur-sm flex items-center justify-center p-4 z-50"
	on:click={onClose}
	on:keydown={(e) => e.key === "Escape" && onClose()}
	role="button"
	tabindex="0"
	aria-label="Close modal"
>
	<div
		class="bg-white dark:bg-slate-800 rounded-xl shadow-2xl w-full max-w-lg max-h-[90vh] overflow-y-auto"
		on:click|stopPropagation
		on:keydown|stopPropagation
		role="dialog"
		tabindex="-1"
	>
		<div
			class="px-6 py-5 border-b border-gray-200 dark:border-slate-700 sticky top-0 bg-white dark:bg-slate-800 z-10"
		>
			<h2 class="text-2xl font-bold text-gray-900 dark:text-white">
				{transaction ? "Edit" : "Add"} Transaction
			</h2>
		</div>

		<form
			on:submit|preventDefault={handleSave}
			data-testid="transaction-form"
			class="px-6 py-5 space-y-5"
		>
			{#if formError}
				<div
					class="bg-red-50 dark:bg-red-900/20 border-l-4 border-red-500 dark:border-red-400 p-4 rounded"
					role="alert"
				>
					<p class="text-red-700 dark:text-red-400 text-sm">
						{formError}
					</p>
				</div>
			{/if}

			<!-- Amount and Type Row -->
			<div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
				<div>
					<label
						for="amount"
						class="block text-sm font-semibold text-gray-700 dark:text-slate-300 mb-2"
					>
						Amount <span class="text-red-500">*</span>
					</label>
					<div class="relative">
						<span
							class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500 dark:text-slate-400 font-medium"
							>kr</span
						>
						<input
							type="number"
							id="amount"
							bind:value={amount}
							step="0.01"
							min="0.01"
							class="w-full pl-10 pr-4 py-3 border-2 border-gray-300 dark:border-slate-600 dark:bg-slate-700 dark:text-white rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-200 dark:focus:ring-blue-800 transition-all"
							placeholder="0.00"
							required
						/>
					</div>
				</div>

				<div>
					<label
						for="type"
						class="block text-sm font-semibold text-gray-700 dark:text-slate-300 mb-2"
					>
						Type <span class="text-red-500">*</span>
					</label>
					<select
						id="type"
						bind:value={type}
						class="w-full px-4 py-3 border-2 border-gray-300 dark:border-slate-600 dark:bg-slate-700 dark:text-white rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-200 dark:focus:ring-blue-800 transition-all appearance-none bg-white dark:bg-slate-700"
						style="background-image: url('data:image/svg+xml;charset=UTF-8,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 24 24%27 fill=%27none%27 stroke=%27currentColor%27 stroke-width=%272%27 stroke-linecap=%27round%27 stroke-linejoin=%27round%27%3e%3cpolyline points=%276 9 12 15 18 9%27%3e%3c/polyline%3e%3c/svg%3e'); background-repeat: no-repeat; background-position: right 0.7rem center; background-size: 1.5em 1.5em; padding-right: 2.5rem;"
					>
						<option value="income">💰 Income</option>
						<option value="expense">💸 Expense</option>
					</select>
				</div>
			</div>

			<!-- Date -->
			<div>
				<label
					for="date"
					class="block text-sm font-semibold text-gray-700 dark:text-slate-300 mb-2"
				>
					Date <span class="text-red-500">*</span>
				</label>
				<input
					type="date"
					id="date"
					bind:value={date}
					class="w-full px-4 py-3 border-2 border-gray-300 dark:border-slate-600 dark:bg-slate-700 dark:text-white rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-200 dark:focus:ring-blue-800 transition-all"
					required
				/>
			</div>

			<!-- Category -->
			<div>
				<label
					for="category"
					class="block text-sm font-semibold text-gray-700 dark:text-slate-300 mb-2"
				>
					Category <span class="text-red-500">*</span>
				</label>
				<select
					id="category"
					bind:value={category_id}
					class="w-full px-4 py-3 border-2 border-gray-300 dark:border-slate-600 dark:bg-slate-700 dark:text-white rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-200 dark:focus:ring-blue-800 transition-all appearance-none bg-white dark:bg-slate-700"
					style="background-image: url('data:image/svg+xml;charset=UTF-8,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 24 24%27 fill=%27none%27 stroke=%27currentColor%27 stroke-width=%272%27 stroke-linecap=%27round%27 stroke-linejoin=%27round%27%3e%3cpolyline points=%276 9 12 15 18 9%27%3e%3c/polyline%3e%3c/svg%3e'); background-repeat: no-repeat; background-position: right 0.7rem center; background-size: 1.5em 1.5em; padding-right: 2.5rem;"
					required
				>
					<option value={null} disabled>Select a category</option>
					{#each categories as category}
						<option value={category.id}>
							{category.emoji || "📂"} {category.name}
						</option>
					{/each}
				</select>

				{#if !showNewCategoryInput}
					<button
						type="button"
						on:click={() => (showNewCategoryInput = true)}
						class="mt-3 inline-flex items-center text-sm font-medium text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 transition-colors"
					>
						<svg
							class="w-4 h-4 mr-1"
							fill="none"
							stroke="currentColor"
							viewBox="0 0 24 24"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M12 6v6m0 0v6m0-6h6m-6 0H6"
							/>
						</svg>
						Create New Category
					</button>
				{:else}
					<div class="mt-3 p-4 bg-gray-50 dark:bg-slate-700/50 rounded-lg space-y-3">
						<!-- Emoji Picker -->
						<div>
							<label class="block text-xs font-semibold text-gray-700 dark:text-slate-300 mb-2">
								Icon
							</label>
							<div class="flex items-center gap-2 mb-2">
								<input
									type="text"
									bind:value={newCategoryEmoji}
									class="w-14 h-14 p-1 border-2 border-gray-300 dark:border-slate-600 dark:bg-slate-700 rounded-lg text-center text-2xl focus:border-blue-500 focus:ring-2 focus:ring-blue-200 dark:focus:ring-blue-800 transition-all"
									maxlength="2"
									placeholder="📂"
									disabled={isCreatingCategory}
								/>
								<span class="text-xs text-gray-500 dark:text-slate-400">or choose:</span>
							</div>
							<div class="grid grid-cols-8 gap-1.5">
								{#each commonEmojis as emoji}
									<button
										type="button"
										on:click={() => (newCategoryEmoji = emoji)}
										disabled={isCreatingCategory}
										class="text-xl p-1.5 rounded-md transition-all duration-150 disabled:opacity-50 {newCategoryEmoji === emoji
											? 'bg-blue-100 dark:bg-blue-900/50 ring-2 ring-blue-500 dark:ring-blue-400 scale-110'
											: 'hover:bg-gray-100 dark:hover:bg-slate-600'}"
									>
										{emoji}
									</button>
								{/each}
							</div>
						</div>

						<!-- Category Name -->
						<div>
							<label class="block text-xs font-semibold text-gray-700 dark:text-slate-300 mb-2">
								Name
							</label>
							<input
								type="text"
								bind:value={newCategoryName}
								placeholder="Category name"
								class="w-full px-4 py-2.5 border-2 border-gray-300 dark:border-slate-600 dark:bg-slate-700 dark:text-white rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-200 dark:focus:ring-blue-800 transition-all"
								disabled={isCreatingCategory}
							/>
						</div>
						<div class="flex gap-2">
							<button
								type="button"
								on:click={handleCreateCategory}
								disabled={isCreatingCategory}
								class="flex-1 inline-flex items-center justify-center bg-green-500 hover:bg-green-600 dark:bg-green-600 dark:hover:bg-green-700 text-white font-semibold py-2.5 px-4 rounded-lg shadow-sm transition-colors duration-150 disabled:opacity-50 disabled:cursor-not-allowed"
							>
								{#if isCreatingCategory}
									<svg
										class="animate-spin -ml-1 mr-2 h-4 w-4 text-white"
										xmlns="http://www.w3.org/2000/svg"
										fill="none"
										viewBox="0 0 24 24"
									>
										<circle
											class="opacity-25"
											cx="12"
											cy="12"
											r="10"
											stroke="currentColor"
											stroke-width="4"
										></circle>
										<path
											class="opacity-75"
											fill="currentColor"
											d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
										></path>
									</svg>
									Creating...
								{:else}
									Add Category
								{/if}
							</button>
							<button
								type="button"
							on:click={() => {
								showNewCategoryInput = false;
								newCategoryName = "";
								newCategoryEmoji = "📂";
								formError = null;
							}}
								disabled={isCreatingCategory}
								class="flex-1 bg-gray-200 hover:bg-gray-300 dark:bg-slate-600 dark:hover:bg-slate-500 text-gray-800 dark:text-white font-semibold py-2.5 px-4 rounded-lg transition-colors duration-150 disabled:opacity-50 disabled:cursor-not-allowed"
							>
								Cancel
							</button>
						</div>
					</div>
				{/if}
			</div>

			<!-- Description -->
			<div>
				<label
					for="description"
					class="block text-sm font-semibold text-gray-700 dark:text-slate-300 mb-2"
				>
					Description (Optional)
				</label>
				<textarea
					id="description"
					bind:value={description}
					rows="3"
					class="w-full px-4 py-3 border-2 border-gray-300 dark:border-slate-600 dark:bg-slate-700 dark:text-white rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-200 dark:focus:ring-blue-800 transition-all resize-none"
					placeholder="Add a note about this transaction..."
				></textarea>
			</div>
		</form>

		<div
			class="px-6 py-4 bg-gray-50 dark:bg-slate-700 rounded-b-xl flex flex-col sm:flex-row justify-end gap-3 sticky bottom-0"
		>
			<button
				on:click={onClose}
				type="button"
				class="w-full sm:w-auto px-5 py-2.5 text-gray-700 dark:text-slate-300 font-medium hover:bg-gray-200 dark:hover:bg-slate-600 rounded-lg transition-colors duration-150 order-2 sm:order-1"
			>
				Cancel
			</button>
			<button
				on:click={handleSave}
				type="button"
				class="w-full sm:w-auto px-5 py-2.5 bg-blue-500 hover:bg-blue-600 dark:bg-blue-600 dark:hover:bg-blue-700 text-white font-semibold rounded-lg shadow-sm transition-colors duration-150 order-1 sm:order-2"
			>
				{transaction ? "Update" : "Add"} Transaction
			</button>
		</div>
	</div>
</div>
