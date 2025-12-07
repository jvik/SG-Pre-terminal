<script lang="ts">
  import DashboardStatCard from "./DashboardStatCard.svelte";

  export let total_income: number;
  export let total_expenses: number;
  export let net_balance: number;
</script>

<div class="grid grid-cols-1 md:grid-cols-3 gap-6">
  <DashboardStatCard title="Total Income" value={total_income} />
  <DashboardStatCard title="Total Expenses" value={total_expenses} />
  <DashboardStatCard title="Net Balance" value={net_balance} />
</div>
