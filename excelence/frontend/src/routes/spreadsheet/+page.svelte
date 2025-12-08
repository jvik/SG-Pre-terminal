<script lang="ts">
    import { onMount } from "svelte";
    import {
        categories,
        transactions,
        loadCategories,
        loadTransactions,
    } from "$lib/stores/data";
    import { updateTransaction, createTransaction } from "$lib/services/api";
    import type { Transaction } from "$lib/types";

    let editingId: string | null = null;
    let editForm: {
        date: string;
        description: string;
        category_id: string;
        amount: number;
        type: "income" | "expense";
    } | null = null;

    let isAddingNew = false;
    let newTransaction = {
        date: new Date().toISOString().split("T")[0],
        description: "",
        category_id: "",
        amount: 0,
        type: "expense" as "income" | "expense",
    };

    onMount(async () => {
        await loadCategories();
        await loadTransactions();
        // Set default category if available
        if ($categories.length > 0) {
            newTransaction.category_id = $categories[0].id;
        }
    });

    function startEditing(transaction: Transaction) {
        if (isAddingNew) return; // Don't allow editing while adding
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
            const updatePayload = {
                date: editForm.date,
                description: editForm.description || null,
                category_id: editForm.category_id,
                amount: Number(editForm.amount),
                type: editForm.type,
            };

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

    function startAddingNew() {
        isAddingNew = true;
        editingId = null;
        editForm = null;
        // Reset form with today's date
        newTransaction = {
            date: new Date().toISOString().split("T")[0],
            description: "",
            category_id: $categories.length > 0 ? $categories[0].id : "",
            amount: 0,
            type: "expense",
        };
    }

    function cancelAddingNew() {
        isAddingNew = false;
    }

    async function saveNewTransaction() {
        if (!newTransaction.category_id) {
            alert("Please select a category");
            return;
        }

        try {
            const createPayload = {
                date: newTransaction.date,
                description: newTransaction.description || null,
                category_id: newTransaction.category_id,
                amount: Number(newTransaction.amount),
                type: newTransaction.type,
            };

            await createTransaction(createPayload);
            await loadTransactions();
            isAddingNew = false;
        } catch (error) {
            console.error("Full error:", error);
            const errorMsg = error?.message || JSON.stringify(error);
            alert(`Error creating transaction: ${errorMsg}`);
        }
    }
</script>

<div class="p-8 bg-gray-50 min-h-screen">
    <div class="max-w-7xl mx-auto">
        <div class="flex justify-between items-center mb-6">
            <h1 class="text-3xl font-bold text-gray-800">Transaction Spreadsheet</h1>
            <button
                on:click={startAddingNew}
                disabled={isAddingNew}
                class="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white px-4 py-2 rounded-lg font-semibold shadow-md transition-colors flex items-center gap-2"
            >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                </svg>
                Add Transaction
            </button>
        </div>

        <div class="bg-white shadow-lg rounded-lg overflow-hidden border border-gray-200">
            <div class="overflow-x-auto">
                <table class="min-w-full divide-y divide-gray-200">
                    <thead>
                        <tr class="bg-gradient-to-r from-gray-50 to-gray-100">
                            <th class="px-6 py-4 text-left text-xs font-bold text-gray-700 uppercase tracking-wider border-r border-gray-200">
                                Date
                            </th>
                            <th class="px-6 py-4 text-left text-xs font-bold text-gray-700 uppercase tracking-wider border-r border-gray-200">
                                Description
                            </th>
                            <th class="px-6 py-4 text-left text-xs font-bold text-gray-700 uppercase tracking-wider border-r border-gray-200">
                                Category
                            </th>
                            <th class="px-6 py-4 text-left text-xs font-bold text-gray-700 uppercase tracking-wider border-r border-gray-200">
                                Type
                            </th>
                            <th class="px-6 py-4 text-right text-xs font-bold text-gray-700 uppercase tracking-wider border-r border-gray-200">
                                Amount
                            </th>
                            <th class="px-6 py-4 text-center text-xs font-bold text-gray-700 uppercase tracking-wider">
                                Actions
                            </th>
                        </tr>
                    </thead>
                    <tbody class="bg-white divide-y divide-gray-200">
                        <!-- New Transaction Row -->
                        {#if isAddingNew}
                            <tr class="bg-blue-50 border-l-4 border-l-blue-500">
                                <td class="px-6 py-3 border-r border-gray-200">
                                    <input
                                        type="date"
                                        bind:value={newTransaction.date}
                                        class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                    />
                                </td>
                                <td class="px-6 py-3 border-r border-gray-200">
                                    <input
                                        type="text"
                                        bind:value={newTransaction.description}
                                        class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                        placeholder="Enter description..."
                                    />
                                </td>
                                <td class="px-6 py-3 border-r border-gray-200">
                                    <select
                                        bind:value={newTransaction.category_id}
                                        class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                    >
                                        {#each $categories as category}
                                            <option value={category.id}>
                                                {category.emoji ? `${category.emoji} ` : ""}{category.name}
                                            </option>
                                        {/each}
                                    </select>
                                </td>
                                <td class="px-6 py-3 border-r border-gray-200">
                                    <select
                                        bind:value={newTransaction.type}
                                        class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                    >
                                        <option value="income">Income</option>
                                        <option value="expense">Expense</option>
                                    </select>
                                </td>
                                <td class="px-6 py-3 border-r border-gray-200">
                                    <input
                                        type="number"
                                        step="0.01"
                                        bind:value={newTransaction.amount}
                                        class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm text-right focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                        placeholder="0.00"
                                    />
                                </td>
                                <td class="px-6 py-3">
                                    <div class="flex gap-2 justify-center">
                                        <button
                                            on:click={saveNewTransaction}
                                            class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-md text-sm font-semibold shadow-sm transition-colors"
                                        >
                                            Save
                                        </button>
                                        <button
                                            on:click={cancelAddingNew}
                                            class="bg-gray-500 hover:bg-gray-600 text-white px-4 py-2 rounded-md text-sm font-semibold shadow-sm transition-colors"
                                        >
                                            Cancel
                                        </button>
                                    </div>
                                </td>
                            </tr>
                        {/if}

                        <!-- Existing Transactions -->
                        {#each $transactions as transaction, index (transaction.id)}
                            {#if editingId === transaction.id && editForm}
                                <tr class="bg-amber-50 border-l-4 border-l-amber-500">
                                    <td class="px-6 py-3 border-r border-gray-200">
                                        <input
                                            type="date"
                                            bind:value={editForm.date}
                                            class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-2 focus:ring-amber-500 focus:border-amber-500"
                                        />
                                    </td>
                                    <td class="px-6 py-3 border-r border-gray-200">
                                        <input
                                            type="text"
                                            bind:value={editForm.description}
                                            class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-2 focus:ring-amber-500 focus:border-amber-500"
                                            placeholder="Description"
                                        />
                                    </td>
                                    <td class="px-6 py-3 border-r border-gray-200">
                                        <select
                                            bind:value={editForm.category_id}
                                            class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-2 focus:ring-amber-500 focus:border-amber-500"
                                        >
                                            {#each $categories as category}
                                                <option value={category.id}>
                                                    {category.emoji ? `${category.emoji} ` : ""}{category.name}
                                                </option>
                                            {/each}
                                        </select>
                                    </td>
                                    <td class="px-6 py-3 border-r border-gray-200">
                                        <select
                                            bind:value={editForm.type}
                                            class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-2 focus:ring-amber-500 focus:border-amber-500"
                                        >
                                            <option value="income">Income</option>
                                            <option value="expense">Expense</option>
                                        </select>
                                    </td>
                                    <td class="px-6 py-3 border-r border-gray-200">
                                        <input
                                            type="number"
                                            step="0.01"
                                            bind:value={editForm.amount}
                                            class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm text-right focus:ring-2 focus:ring-amber-500 focus:border-amber-500"
                                        />
                                    </td>
                                    <td class="px-6 py-3">
                                        <div class="flex gap-2 justify-center">
                                            <button
                                                on:click={() => saveEdit(transaction.id)}
                                                class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-md text-sm font-semibold shadow-sm transition-colors"
                                            >
                                                Save
                                            </button>
                                            <button
                                                on:click={cancelEditing}
                                                class="bg-gray-500 hover:bg-gray-600 text-white px-4 py-2 rounded-md text-sm font-semibold shadow-sm transition-colors"
                                            >
                                                Cancel
                                            </button>
                                        </div>
                                    </td>
                                </tr>
                            {:else}
                                <tr
                                    class="hover:bg-gray-50 cursor-pointer transition-colors"
                                    class:bg-white={index % 2 === 0}
                                    class:bg-gray-50={index % 2 === 1}
                                    on:click={() => startEditing(transaction)}
                                >
                                    <td class="px-6 py-4 border-r border-gray-200 whitespace-nowrap text-sm text-gray-700 font-medium">
                                        {new Date(transaction.date).toLocaleDateString("no-NO", {
                                            year: "numeric",
                                            month: "short",
                                            day: "numeric",
                                        })}
                                    </td>
                                    <td class="px-6 py-4 border-r border-gray-200 text-sm text-gray-900">
                                        {transaction.description || "—"}
                                    </td>
                                    <td class="px-6 py-4 border-r border-gray-200 whitespace-nowrap text-sm">
                                        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                                            {#each $categories as category}
                                                {#if category.id === transaction.category_id}
                                                    {category.emoji ? `${category.emoji} ` : ""}{category.name}
                                                {/if}
                                            {/each}
                                        </span>
                                    </td>
                                    <td class="px-6 py-4 border-r border-gray-200 whitespace-nowrap text-sm">
                                        <span
                                            class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                                            class:bg-green-100={transaction.type === "income"}
                                            class:text-green-800={transaction.type === "income"}
                                            class:bg-red-100={transaction.type === "expense"}
                                            class:text-red-800={transaction.type === "expense"}
                                        >
                                            {transaction.type === "income" ? "Income" : "Expense"}
                                        </span>
                                    </td>
                                    <td
                                        class="px-6 py-4 border-r border-gray-200 whitespace-nowrap text-sm text-right font-semibold"
                                        class:text-green-600={transaction.type === "income"}
                                        class:text-red-600={transaction.type === "expense"}
                                    >
                                        {transaction.type === "income" ? "+" : "-"}{transaction.amount.toFixed(2)} kr
                                    </td>
                                    <td class="px-6 py-4 text-center text-gray-400 text-xs">
                                        <div class="flex items-center justify-center gap-1">
                                            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                                            </svg>
                                            Click to edit
                                        </div>
                                    </td>
                                </tr>
                            {/if}
                        {/each}

                        <!-- Empty state -->
                        {#if $transactions.length === 0 && !isAddingNew}
                            <tr>
                                <td colspan="6" class="px-6 py-12 text-center text-gray-500">
                                    <div class="flex flex-col items-center gap-2">
                                        <svg class="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                        </svg>
                                        <p class="text-lg font-medium">No transactions yet</p>
                                        <p class="text-sm">Click "Add Transaction" to get started</p>
                                    </div>
                                </td>
                            </tr>
                        {/if}
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Summary footer -->
        {#if $transactions.length > 0}
            <div class="mt-6 bg-gradient-to-r from-white to-gray-50 shadow-lg rounded-lg border border-gray-200 overflow-hidden">
                <div class="grid grid-cols-1 md:grid-cols-4 divide-y md:divide-y-0 md:divide-x divide-gray-200">
                    <!-- Total Transactions -->
                    <div class="p-6 flex flex-col items-center justify-center">
                        <div class="text-gray-500 text-sm font-medium mb-2 uppercase tracking-wider">Transactions</div>
                        <div class="text-3xl font-bold text-gray-800">{$transactions.length}</div>
                    </div>
                    
                    <!-- Total Income -->
                    <div class="p-6 flex flex-col items-center justify-center bg-green-50">
                        <div class="text-green-700 text-sm font-medium mb-2 uppercase tracking-wider flex items-center gap-2">
                            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                            </svg>
                            Income
                        </div>
                        <div class="text-3xl font-bold text-green-600">
                            +{$transactions
                                .filter((t) => t.type === "income")
                                .reduce((sum, t) => sum + t.amount, 0)
                                .toFixed(2)}
                        </div>
                        <div class="text-sm text-green-600 font-medium mt-1">kr</div>
                    </div>
                    
                    <!-- Total Expenses -->
                    <div class="p-6 flex flex-col items-center justify-center bg-red-50">
                        <div class="text-red-700 text-sm font-medium mb-2 uppercase tracking-wider flex items-center gap-2">
                            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 17h8m0 0V9m0 8l-8-8-4 4-6-6" />
                            </svg>
                            Expenses
                        </div>
                        <div class="text-3xl font-bold text-red-600">
                            -{$transactions
                                .filter((t) => t.type === "expense")
                                .reduce((sum, t) => sum + t.amount, 0)
                                .toFixed(2)}
                        </div>
                        <div class="text-sm text-red-600 font-medium mt-1">kr</div>
                    </div>
                    
                    <!-- Net Balance -->
                    <div class="p-6 flex flex-col items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-50">
                        <div class="text-blue-700 text-sm font-medium mb-2 uppercase tracking-wider flex items-center gap-2">
                            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                            </svg>
                            Net Balance
                        </div>
                        <div class="text-3xl font-bold text-blue-700">
                            {($transactions
                                .filter((t) => t.type === "income")
                                .reduce((sum, t) => sum + t.amount, 0) -
                                $transactions
                                    .filter((t) => t.type === "expense")
                                    .reduce((sum, t) => sum + t.amount, 0))
                                .toFixed(2)}
                        </div>
                        <div class="text-sm text-blue-700 font-medium mt-1">kr</div>
                    </div>
                </div>
            </div>
        {/if}
    </div>
</div>
