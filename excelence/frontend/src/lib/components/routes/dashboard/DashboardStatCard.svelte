<script lang="ts">
  export let title: string;
  export let value: number;
  export let percentage_change: number | undefined = undefined;
</script>

<div class="bg-surface-light dark:bg-surface-dark p-6 rounded-xl shadow-sm" data-testid="stat-card-{title.toLowerCase().replace(' ', '-')}">
  <h3 class="text-text-secondary-light dark:text-text-secondary-dark text-base font-medium">{title}</h3>
  <p class="text-text-primary-light dark:text-text-primary-dark text-3xl font-bold mt-2">
    {value.toLocaleString('nb-NO', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} kr
  </p>
  {#if percentage_change !== undefined}
    <p class="text-sm mt-2" class:text-semantic-success={percentage_change >= 0} class:text-semantic-error={percentage_change < 0}>
      {percentage_change >= 0 ? '+' : ''}{percentage_change.toFixed(2)}% from last month
    </p>
  {/if}
</div>
