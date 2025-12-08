<script lang="ts">
    import { onMount } from "svelte";
    import {
        categories,
        transactions,
        loadCategories,
        loadTransactions,
    } from "$lib/stores/data";
    import { updateTransaction } from "$lib/services/api";
    import type { Transaction } from "$lib/types";

    let editingId: string | null = null;
    let editForm: {
        date: string;
        description: string;
        category_id: string;
        amount: number;
        type: "income" | "expense";
    } | null = null;

    onMount(async () => {
        await loadCategories();
        await loadTransactions();
    });

    function startEditing(transaction: Transaction) {
        editingId = transaction.id;
        editForm = {
            date: transaction.date,
            description: transaction.description || "",
            category_id: transaction.category_id,
            amount: transaction.amount,
            type: transaction.type,
        };
    }

    function cancelEditing() {
        editingId = null;
        editForm = null;
    }

    async function saveEdit(transactionId: string) {
        if (!editForm) return;

        try {
            // Prepare the update payload with proper types
            const updatePayload = {
                date: editForm.date,
                description: editForm.description || null,
                category_id: editForm.category_id,
                amount: Number(editForm.amount),
                type: editForm.type,
            };

            console.log("Sending update payload:", updatePayload);
            await updateTransaction(transactionId, updatePayload);
            await loadTransactions();
            editingId = null;
            editForm = null;
        } catch (error) {
            console.error("Full error:", error);
            const errorMsg = error?.message || JSON.stringify(error);
            alert(`Error updating transaction: ${errorMsg}`);
        }
    }
</script>

<div class="p-8">
    <div class="flex justify-between items-center mb-6">
        <h1 class="text-2xl font-bold">Spreadsheet</h1>
    </div>

    <div class="bg-white shadow-md rounded overflow-x-auto">
        <table class="min-w-full table-auto">
            <thead class="bg-gray-200">
                <tr>
                    <th class="px-4 py-2 text-left">Date</th>
                    <th class="px-4 py-2 text-left">Description</th>
                    <th class="px-4 py-2 text-left">Category</th>
                    <th class="px-4 py-2 text-left">Type</th>
                    <th class="px-4 py-2 text-right">Amount</th>
                    <th class="px-4 py-2 text-center">Actions</th>
                </tr>
            </thead>
            <tbody>
                {#each $transactions as transaction (transaction.id)}
                    {#if editingId === transaction.id && editForm}
                        <tr class="border-b bg-blue-50">
                            <td class="px-4 py-2">
                                <input
                                    type="date"
                                    bind:value={editForm.date}
                                    class="w-full px-2 py-1 border rounded"
                                />
                            </td>
                            <td class="px-4 py-2">
                                <input
                                    type="text"
                                    bind:value={editForm.description}
                                    class="w-full px-2 py-1 border rounded"
                                    placeholder="Description"
                                />
                            </td>
                            <td class="px-4 py-2">
                                <select
                                    bind:value={editForm.category_id}
                                    class="w-full px-2 py-1 border rounded"
                                >
                                    {#each $categories as category}
                                        <option value={category.id}>
                                            {category.name}
                                        </option>
                                    {/each}
                                </select>
                            </td>
                            <td class="px-4 py-2">
                                <select
                                    bind:value={editForm.type}
                                    class="w-full px-2 py-1 border rounded"
                                >
                                    <option value="income">Income</option>
                                    <option value="expense">Expense</option>
                                </select>
                            </td>
                            <td class="px-4 py-2">
                                <input
                                    type="number"
                                    step="0.01"
                                    bind:value={editForm.amount}
                                    class="w-full px-2 py-1 border rounded text-right"
                                />
                            </td>
                            <td class="px-4 py-2">
                                <div class="flex gap-2 justify-center">
                                    <button
                                        on:click={() =>
                                            saveEdit(transaction.id)}
                                        class="bg-green-500 hover:bg-green-600 text-white px-3 py-1 rounded text-sm"
                                    >
                                        Save
                                    </button>
                                    <button
                                        on:click={cancelEditing}
                                        class="bg-gray-500 hover:bg-gray-600 text-white px-3 py-1 rounded text-sm"
                                    >
                                        Cancel
                                    </button>
                                </div>
                            </td>
                        </tr>
                    {:else}
                        <tr
                            class="border-b hover:bg-gray-50 cursor-pointer"
                            on:click={() => startEditing(transaction)}
                        >
                            <td class="px-4 py-2">{transaction.date}</td>
                            <td class="px-4 py-2">
                                {transaction.description || "—"}
                            </td>
                            <td class="px-4 py-2">
                                {$categories.find(
                                    (c) => c.id === transaction.category_id,
                                )?.name || "N/A"}
                            </td>
                            <td class="px-4 py-2 capitalize">
                                {transaction.type}
                            </td>
                            <td
                                class="px-4 py-2 text-right"
                                class:text-green-600={transaction.type ===
                                    "income"}
                                class:text-red-600={transaction.type ===
                                    "expense"}
                            >
                                {transaction.type === "income"
                                    ? "+"
                                    : "-"}{transaction.amount.toFixed(2)} kr
                            </td>
                            <td class="px-4 py-2 text-center text-gray-400 text-sm">
                                Click to edit
                            </td>
                        </tr>
                    {/if}
                {/each}
            </tbody>
        </table>
    </div>
</div>
