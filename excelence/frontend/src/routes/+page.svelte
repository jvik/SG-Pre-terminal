<script lang="ts">
	import { goto } from "$app/navigation";
	import { browser } from "$app/environment";
	import { authStore } from "$lib/stores/auth";
	import LandingPage from "$lib/components/routes/landing/LandingPage.svelte";

	// Reactive redirect - runs whenever authStore changes
	$effect(() => {
		if (browser && $authStore.isAuthenticated) {
			goto("/dashboard");
		}
	});
</script>

{#if !$authStore.isAuthenticated}
	<LandingPage />
{:else}
	<!-- Loading/redirecting state -->
	<div class="min-h-screen flex items-center justify-center">
		<p class="text-gray-600 dark:text-slate-300">
			Redirecting to dashboard...
		</p>
	</div>
{/if}
