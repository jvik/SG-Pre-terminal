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
					categoryToEditId,
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
				await deleteCategory(categoryToDeleteId);
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

<div class="p-8">
	<div class="flex justify-between items-center mb-6">
		<h1 class="text-2xl font-bold">Manage Categories</h1>
		<button
			on:click={openAddModal}
			class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
		>
			+ Add Category
		</button>
	</div>

	{#if isLoading}
		<p>Loading categories...</p>
	{:else if error}
		<div
			class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative"
			role="alert"
		>
			<strong class="font-bold">Error:</strong>
			<span class="block sm:inline">{error}</span>
		</div>
	{:else}
		<div class="bg-white shadow-md rounded">
			<table class="min-w-full table-auto">
				<thead class="bg-gray-200">
					<tr>
						<th class="px-4 py-2 text-left w-16">Icon</th>
						<th class="px-4 py-2 text-left">Category Name</th>
						<th class="px-4 py-2 text-right">Actions</th>
					</tr>
				</thead>
				<tbody>
					{#each categories as category (category.id)}
						<tr class="border-b">
							<td class="px-4 py-2 text-2xl"
								>{category.emoji || "📂"}</td
							>
							<td class="px-4 py-2">{category.name}</td>
							<td class="px-4 py-2 text-right">
								<button
									on:click={() => openEditModal(category)}
									class="text-blue-500 hover:underline mr-4"
								>
									Edit
								</button>
								<button
									on:click={() =>
										openDeleteConfirm(category.id)}
									class="text-red-500 hover:underline"
								>
									Delete
								</button>
							</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
	{/if}
</div>

<!-- Add/Edit Modal -->
{#if showModal}
	<div
		class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center"
	>
		<div class="bg-white p-6 rounded-lg shadow-xl w-full max-w-md">
			<h2 class="text-xl font-bold mb-4">
				{isEditing ? "Edit" : "Add"} Category
			</h2>
			{#if modalError}
				<p class="text-red-500 text-sm mb-4">{modalError}</p>
			{/if}

			<div class="mb-4">
				<label class="block text-sm font-medium text-gray-700 mb-2"
					>Icon</label
				>
				<div class="flex items-center gap-2 mb-2">
					<input
						type="text"
						bind:value={categoryEmojiInput}
						class="w-16 p-2 border rounded text-center text-2xl"
						maxlength="2"
						placeholder="📂"
					/>
					<span class="text-sm text-gray-500">or choose:</span>
				</div>
				<div class="grid grid-cols-9 gap-2">
					{#each commonEmojis as emoji}
						<button
							type="button"
							on:click={() => (categoryEmojiInput = emoji)}
							class="text-2xl p-2 rounded hover:bg-gray-100 {categoryEmojiInput ===
							emoji
								? 'bg-blue-100'
								: ''}"
						>
							{emoji}
						</button>
					{/each}
				</div>
			</div>

			<div class="mb-4">
				<label class="block text-sm font-medium text-gray-700 mb-2"
					>Name</label
				>
				<input
					type="text"
					bind:value={categoryNameInput}
					class="w-full p-2 border rounded"
					placeholder="Enter category name"
				/>
			</div>
			<div class="flex justify-end gap-4">
				<button on:click={closeModal} class="text-gray-600"
					>Cancel</button
				>
				<button
					on:click={handleSave}
					class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
				>
					Save
				</button>
			</div>
		</div>
	</div>
{/if}

<!-- Delete Confirmation Modal -->
{#if showDeleteConfirm}
	<div
		class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center"
	>
		<div class="bg-white p-6 rounded-lg shadow-xl w-full max-w-md">
			<h2 class="text-xl font-bold mb-4">Confirm Deletion</h2>
			<p>
				Are you sure you want to delete this category? This action
				cannot be undone.
			</p>
			<p class="text-sm text-gray-600 mt-2">
				Note: Deletion will be blocked if the category is in use by any
				transactions.
			</p>
			<div class="flex justify-end gap-4 mt-6">
				<button on:click={closeDeleteConfirm} class="text-gray-600"
					>Cancel</button
				>
				<button
					on:click={confirmDelete}
					class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
				>
					Delete
				</button>
			</div>
		</div>
	</div>
{/if}
