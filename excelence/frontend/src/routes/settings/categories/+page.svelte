<script lang="ts">
	import { onMount } from "svelte";
	import {
		getCategories,
		createCategory,
		updateCategory,
		deleteCategory,
	} from "$lib/services/api";

	let categories: { id: number; name: string; emoji?: string }[] = [];
	let isLoading = true;
	let error: string | null = null;

	// Modal state
	let showModal = false;
	let isEditing = false;
	let categoryToEditId: number | null = null;
	let categoryNameInput = "";
	let categoryEmojiInput = "📂";
	let modalError: string | null = null;

	// Common emojis for categories
	const commonEmojis = [
		"📂",
		"🍔",
		"🏠",
		"🚗",
		"💰",
		"🎮",
		"📱",
		"👕",
		"🎬",
		"✈️",
		"🏥",
		"📚",
		"🎵",
		"⚽",
		"🛒",
		"☕",
		"🎁",
		"💼",
	];

	// Delete confirmation state
	let showDeleteConfirm = false;
	let categoryToDeleteId: number | null = null;

	onMount(async () => {
		await loadCategories();
	});

	async function loadCategories() {
		try {
			isLoading = true;
			error = null;
			const fetchedCategories = await getCategories();
			categories = fetchedCategories;
		} catch (e: any) {
			error = e.message;
		} finally {
			isLoading = false;
		}
	}

	function openAddModal() {
		isEditing = false;
		categoryToEditId = null;
		categoryNameInput = "";
		categoryEmojiInput = "📂";
		modalError = null;
		showModal = true;
	}

	function openEditModal(category: {
		id: number;
		name: string;
		emoji?: string;
	}) {
		isEditing = true;
		categoryToEditId = category.id;
		categoryNameInput = category.name;
		categoryEmojiInput = category.emoji || "📂";
		modalError = null;
		showModal = true;
	}

	function closeModal() {
		showModal = false;
	}

	async function handleSave() {
		if (!categoryNameInput.trim()) {
			modalError = "Category name cannot be empty.";
			return;
		}

		// Check for duplicate names (case-insensitive)
		const normalizedName = categoryNameInput.trim().toLowerCase();
		const isDuplicate = categories.some(
			(cat) =>
				cat.name.toLowerCase() === normalizedName &&
				cat.id !== categoryToEditId,
		);

		if (isDuplicate) {
			modalError = "A category with this name already exists.";
			return;
		}

		try {
			modalError = null;
			if (isEditing && categoryToEditId !== null) {
				await updateCategory(
					String(categoryToEditId),
					categoryNameInput,
					categoryEmojiInput,
				);
			} else {
				await createCategory(categoryNameInput, categoryEmojiInput);
			}
			await loadCategories(); // Refresh list
			closeModal();
		} catch (e: any) {
			modalError = e.message;
		}
	}

	function openDeleteConfirm(id: number) {
		categoryToDeleteId = id;
		showDeleteConfirm = true;
	}

	async function confirmDelete() {
		if (categoryToDeleteId !== null) {
			try {
				await deleteCategory(String(categoryToDeleteId));
				await loadCategories(); // Refresh list
			} catch (e: any) {
				error = e.message; // Show error on the main page
			} finally {
				closeDeleteConfirm();
			}
		}
	}

	function closeDeleteConfirm() {
		showDeleteConfirm = false;
		categoryToDeleteId = null;
	}
</script>

<div class="min-h-screen bg-gray-50 dark:bg-slate-900">
	<div class="max-w-6xl mx-auto p-8">
		<div class="mb-8">
			<h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-2">
				Categories
			</h1>
			<p class="text-gray-600 dark:text-slate-400">
				Organize your transactions with custom categories
			</p>
		</div>

		<div class="mb-6 flex justify-end">
			<button
				on:click={openAddModal}
				class="inline-flex items-center bg-blue-500 hover:bg-blue-600 dark:bg-blue-600 dark:hover:bg-blue-700 text-white font-semibold py-2.5 px-5 rounded-lg shadow-sm transition-colors duration-150"
			>
				<svg
					class="w-5 h-5 mr-2"
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
				Add Category
			</button>
		</div>

		{#if isLoading}
			<div
				class="bg-white dark:bg-slate-800 shadow-lg rounded-lg p-12 text-center"
			>
				<div
					class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mb-4"
				></div>
				<p class="text-gray-600 dark:text-slate-400">
					Loading categories...
				</p>
			</div>
		{:else if error}
			<div
				class="bg-red-50 dark:bg-red-900/20 border-l-4 border-red-500 dark:border-red-400 text-red-700 dark:text-red-400 p-6 rounded-lg shadow-sm"
				role="alert"
			>
				<div class="flex items-start">
					<svg
						class="w-6 h-6 mr-3 flex-shrink-0"
						fill="currentColor"
						viewBox="0 0 20 20"
					>
						<path
							fill-rule="evenodd"
							d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
							clip-rule="evenodd"
						/>
					</svg>
					<div>
						<h3 class="font-semibold mb-1">Error</h3>
						<p>{error}</p>
					</div>
				</div>
			</div>
		{:else}
			<div
				class="bg-white dark:bg-slate-800 shadow-lg rounded-lg overflow-hidden border border-gray-200 dark:border-slate-700"
			>
				{#if categories.length === 0}
					<div
						class="p-8 text-center text-gray-500 dark:text-slate-400"
					>
						<p class="text-lg">No categories yet</p>
						<p class="text-sm mt-2">
							Click "Add Category" to create your first category
						</p>
					</div>
				{:else}
					<table class="min-w-full">
						<thead>
							<tr
								class="bg-gray-50 dark:bg-slate-700 border-b border-gray-200 dark:border-slate-600"
							>
								<th
									class="px-6 py-4 text-left text-xs font-semibold text-gray-600 dark:text-slate-300 uppercase tracking-wider w-20"
									>Icon</th
								>
								<th
									class="px-6 py-4 text-left text-xs font-semibold text-gray-600 dark:text-slate-300 uppercase tracking-wider"
									>Category Name</th
								>
								<th
									class="px-6 py-4 text-right text-xs font-semibold text-gray-600 dark:text-slate-300 uppercase tracking-wider w-48"
									>Actions</th
								>
							</tr>
						</thead>
						<tbody
							class="divide-y divide-gray-200 dark:divide-slate-700"
						>
							{#each categories as category (category.id)}
								<tr
									class="hover:bg-gray-50 dark:hover:bg-slate-700/50 transition-colors duration-150"
								>
									<td class="px-6 py-4">
										<span class="text-3xl"
											>{category.emoji || "📂"}</span
										>
									</td>
									<td class="px-6 py-4">
										<span
											class="text-gray-900 dark:text-white font-medium"
											>{category.name}</span
										>
									</td>
									<td class="px-6 py-4 text-right">
										<div class="flex justify-end gap-2">
											<button
												on:click={() =>
													openEditModal(category)}
												class="inline-flex items-center px-3 py-1.5 text-sm font-medium text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 hover:bg-blue-50 dark:hover:bg-blue-900/30 rounded-md transition-colors duration-150"
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
														d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
													/>
												</svg>
												Edit
											</button>
											<button
												on:click={() =>
													openDeleteConfirm(
														category.id,
													)}
												class="inline-flex items-center px-3 py-1.5 text-sm font-medium text-red-600 dark:text-red-400 hover:text-red-800 dark:hover:text-red-300 hover:bg-red-50 dark:hover:bg-red-900/30 rounded-md transition-colors duration-150"
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
														d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
													/>
												</svg>
												Delete
											</button>
										</div>
									</td>
								</tr>
							{/each}
						</tbody>
					</table>
				{/if}
			</div>
		{/if}
	</div>
</div>

<!-- Add/Edit Modal -->
{#if showModal}
	<div
		class="fixed inset-0 bg-black bg-opacity-50 backdrop-blur-sm flex items-center justify-center p-4 z-50"
		on:click={closeModal}
		on:keydown={(e) => e.key === "Escape" && closeModal()}
		role="button"
		tabindex="0"
		aria-label="Close modal"
	>
		<div
			class="bg-white dark:bg-slate-800 rounded-xl shadow-2xl w-full max-w-md"
			on:click|stopPropagation
			on:keydown|stopPropagation
			role="dialog"
			tabindex="-1"
		>
			<div
				class="px-6 py-5 border-b border-gray-200 dark:border-slate-700"
			>
				<h2 class="text-2xl font-bold text-gray-900 dark:text-white">
					{isEditing ? "Edit" : "Add"} Category
				</h2>
			</div>

			<div class="px-6 py-5 space-y-5">
				{#if modalError}
					<div
						class="bg-red-50 dark:bg-red-900/20 border-l-4 border-red-500 dark:border-red-400 p-4 rounded"
					>
						<p class="text-red-700 dark:text-red-400 text-sm">
							{modalError}
						</p>
					</div>
				{/if}

				<div>
					<label
						for="category-emoji"
						class="block text-sm font-semibold text-gray-700 dark:text-slate-300 mb-3"
						>Icon</label
					>
					<div class="flex items-center gap-3 mb-3">
						<input
							id="category-emoji"
							type="text"
							bind:value={categoryEmojiInput}
							class="w-20 h-20 p-2 border-2 border-gray-300 dark:border-slate-600 dark:bg-slate-700 rounded-lg text-center text-4xl focus:border-blue-500 focus:ring-2 focus:ring-blue-200 dark:focus:ring-blue-800 transition-all"
							maxlength="2"
							placeholder="📂"
						/>
						<span class="text-sm text-gray-500 dark:text-slate-400"
							>or choose from popular icons:</span
						>
					</div>
					<div class="grid grid-cols-9 gap-2">
						{#each commonEmojis as emoji}
							<button
								type="button"
								on:click={() => (categoryEmojiInput = emoji)}
								class="text-2xl p-2 rounded-lg transition-all duration-150 {categoryEmojiInput ===
								emoji
									? 'bg-blue-100 dark:bg-blue-900/50 ring-2 ring-blue-500 dark:ring-blue-400 scale-110'
									: 'hover:bg-gray-100 dark:hover:bg-slate-700'}"
							>
								{emoji}
							</button>
						{/each}
					</div>
				</div>

				<div>
					<label
						for="category-name"
						class="block text-sm font-semibold text-gray-700 dark:text-slate-300 mb-2"
						>Category Name</label
					>
					<input
						id="category-name"
						type="text"
						bind:value={categoryNameInput}
						class="w-full px-4 py-3 border-2 border-gray-300 dark:border-slate-600 dark:bg-slate-700 dark:text-white rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-200 dark:focus:ring-blue-800 transition-all"
						placeholder="Enter category name"
					/>
				</div>
			</div>

			<div
				class="px-6 py-4 bg-gray-50 dark:bg-slate-700 rounded-b-xl flex justify-end gap-3"
			>
				<button
					on:click={closeModal}
					class="px-5 py-2.5 text-gray-700 dark:text-slate-300 font-medium hover:bg-gray-200 dark:hover:bg-slate-600 rounded-lg transition-colors duration-150"
				>
					Cancel
				</button>
				<button
					on:click={handleSave}
					class="px-5 py-2.5 bg-blue-500 hover:bg-blue-600 dark:bg-blue-600 dark:hover:bg-blue-700 text-white font-semibold rounded-lg shadow-sm transition-colors duration-150"
				>
					Save Category
				</button>
			</div>
		</div>
	</div>
{/if}

<!-- Delete Confirmation Modal -->
{#if showDeleteConfirm}
	<div
		class="fixed inset-0 bg-black bg-opacity-50 backdrop-blur-sm flex items-center justify-center p-4 z-50"
		on:click={closeDeleteConfirm}
		on:keydown={(e) => e.key === "Escape" && closeDeleteConfirm()}
		role="button"
		tabindex="0"
		aria-label="Close modal"
	>
		<div
			class="bg-white dark:bg-slate-800 rounded-xl shadow-2xl w-full max-w-md"
			on:click|stopPropagation
			on:keydown|stopPropagation
			role="dialog"
			tabindex="-1"
		>
			<div
				class="px-6 py-5 border-b border-gray-200 dark:border-slate-700"
			>
				<div class="flex items-center">
					<div class="flex-shrink-0">
						<svg
							class="h-8 w-8 text-red-500 dark:text-red-400"
							fill="none"
							stroke="currentColor"
							viewBox="0 0 24 24"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
							/>
						</svg>
					</div>
					<h2
						class="ml-3 text-2xl font-bold text-gray-900 dark:text-white"
					>
						Confirm Deletion
					</h2>
				</div>
			</div>

			<div class="px-6 py-5">
				<p class="text-gray-700 dark:text-slate-300">
					Are you sure you want to delete this category? This action
					cannot be undone.
				</p>
				<div
					class="mt-3 bg-yellow-50 dark:bg-yellow-900/20 border-l-4 border-yellow-400 dark:border-yellow-500 p-4 rounded"
				>
					<p class="text-sm text-yellow-700 dark:text-yellow-400">
						<strong>Note:</strong> Deletion will be blocked if the category
						is in use by any transactions.
					</p>
				</div>
			</div>

			<div
				class="px-6 py-4 bg-gray-50 dark:bg-slate-700 rounded-b-xl flex justify-end gap-3"
			>
				<button
					on:click={closeDeleteConfirm}
					class="px-5 py-2.5 text-gray-700 dark:text-slate-300 font-medium hover:bg-gray-200 dark:hover:bg-slate-600 rounded-lg transition-colors duration-150"
				>
					Cancel
				</button>
				<button
					on:click={confirmDelete}
					class="px-5 py-2.5 bg-red-500 hover:bg-red-600 dark:bg-red-600 dark:hover:bg-red-700 text-white font-semibold rounded-lg shadow-sm transition-colors duration-150"
				>
					Delete Category
				</button>
			</div>
		</div>
	</div>
{/if}
