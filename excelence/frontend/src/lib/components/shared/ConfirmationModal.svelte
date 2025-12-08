<script lang="ts">
  export let isOpen: boolean;
  export let message: string;
  export let onConfirm: () => void;
  export let onCancel: () => void;
</script>

{#if isOpen}
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-surface-light dark:bg-surface-dark p-6 rounded-lg shadow-xl w-full max-w-sm">
      <h3 class="text-lg font-bold mb-4 text-text-primary-light dark:text-text-primary-dark">Confirm Action</h3>
      <p class="text-text-secondary-light dark:text-text-secondary-dark mb-6">{message}</p>
      <div class="flex justify-end gap-3">
        <button 
          on:click={onCancel}
          class="px-4 py-2 text-text-primary-light dark:text-text-primary-dark hover:bg-gray-100 dark:hover:bg-gray-700 rounded-md transition-colors"
        >
          Cancel
        </button>
        <button 
          on:click={onConfirm}
          class="px-4 py-2 bg-semantic-error text-white rounded-md hover:bg-opacity-90 transition-opacity"
        >
          Confirm
        </button>
      </div>
    </div>
  </div>
{/if}
