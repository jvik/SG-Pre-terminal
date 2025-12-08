<script lang="ts">
  import { onMount } from "svelte";
  import {
    getTransactions,
    getCategories,
    updateTransaction,
    deleteTransaction,
  } from "$lib/services/api";
  import TransactionForm from "$lib/components/shared/TransactionForm.svelte";
  import ConfirmationModal from "$lib/components/shared/ConfirmationModal.svelte";

  let transactions = [];
  let categories = [];
  let error = null;
  let isModalOpen = false;
  let selectedTransaction = null;

  async function loadData() {
    try {
      const transPromise = getTransactions();
      const catPromise = getCategories();
      const [transResponse, catResponse] = await Promise.all([
        transPromise,
        catPromise,
      ]);

      transactions = transResponse.data || transResponse;
      categories = catResponse.data || catResponse;
      error = null;
    } catch (err) {
      error = err.message;
      console.error("Failed to fetch data:", err);
    }
  }

  onMount(loadData);

  const openEditModal = (transaction) => {
    selectedTransaction = transaction;
    isModalOpen = true;
  };

  const handleModalClose = () => {
    isModalOpen = false;
    selectedTransaction = null;
  };

  const handleSave = async (data) => {
    if (!selectedTransaction) return; // Should only be handling updates here

    try {
      await updateTransaction(selectedTransaction.id, data);
      handleModalClose();
      await loadData(); // Re-fetch data to show updates
    } catch (err) {
      console.error("Failed to update transaction:", err);
      error = err.message; // Show error to the user
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString();
  };

  // --- Delete Handling ---
  let isDeleteModalOpen = false;
  let transactionToDelete = null;

  const openDeleteModal = (transaction) => {
    transactionToDelete = transaction;
    isDeleteModalOpen = true;
  };

  const handleDeleteClose = () => {
    isDeleteModalOpen = false;
    transactionToDelete = null;
  };

  const handleConfirmDelete = async () => {
    if (!transactionToDelete) return;
    try {
      await deleteTransaction(transactionToDelete.id);
      handleDeleteClose();
      await loadData();
    } catch (err) {
      console.error("Failed to delete transaction:", err);
      error = err.message;
    }
  };
</script>

{#if isModalOpen}
  <TransactionForm
    transaction={selectedTransaction}
    {categories}
    onSave={handleSave}
    onClose={handleModalClose}
  />
{/if}

{#if isDeleteModalOpen}
  <ConfirmationModal
    isOpen={isDeleteModalOpen}
    message="Are you sure you want to delete this transaction? This action cannot be undone."
    onConfirm={handleConfirmDelete}
    onCancel={handleDeleteClose}
  />
{/if}

<div class="bg-surface-light dark:bg-surface-dark p-6 rounded-lg shadow-md">
  <h3
    class="text-lg font-bold text-text-primary-light dark:text-text-primary-dark mb-4"
  >
    Recent Transactions
  </h3>
  {#if error}
    <p class="text-semantic-error">Error: {error}</p>
  {:else if transactions.length === 0}
    <p class="text-text-secondary-light dark:text-text-secondary-dark">
      No transactions found. Add one to get started!
    </p>
  {:else}
    <table class="w-full text-left">
      <thead>
        <tr class="border-b border-border-light dark:border-border-dark">
          <th class="p-2">Date</th>
          <th class="p-2">Description</th>
          <th class="p-2 text-right">Amount</th>
          <th class="p-2"></th>
        </tr>
      </thead>
      <tbody>
        {#each transactions as transaction}
          <tr
            class="border-b border-border-light dark:border-border-dark last:border-b-0"
          >
            <td class="p-2">{formatDate(transaction.date)}</td>
            <td class="p-2">{transaction.description || "-"}</td>
            <td
              class="p-2 text-right font-mono"
              class:text-semantic-success={transaction.type === "income"}
              class:text-semantic-error={transaction.type === "expense"}
            >
              {transaction.type === "income"
                ? "+"
                : "-"}{transaction.amount.toFixed(2)} kr
            </td>
            <td class="p-2 text-right">
              <button
                class="text-primary hover:underline mr-2"
                on:click={() => openEditModal(transaction)}>Edit</button
              >
              <button
                class="text-semantic-error hover:underline"
                on:click={() => openDeleteModal(transaction)}>Delete</button
              >
            </td>
          </tr>
        {/each}
      </tbody>
    </table>
  {/if}
</div>
