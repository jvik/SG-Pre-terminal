<script lang="ts">
	import "./layout.css";
	import favicon from "$lib/assets/favicon.svg";
	import { authStore } from "$lib/stores/auth";
	import { themeStore } from "$lib/stores/theme";
	import { goto } from "$app/navigation";
	import { page } from "$app/stores";
	import { browser } from "$app/environment";
	import Sidebar from "$lib/components/layout/Sidebar.svelte";

	let { children } = $props();
	let isCollapsed = $state(false);

	$effect(() => {
		if (browser && !$authStore.isAuthenticated) {
			const publicRoutes = ["/", "/login", "/register"];
			if (!publicRoutes.includes($page.url.pathname)) {
				goto("/login");
			}
		}
	});

	// Initialize theme on mount
	$effect(() => {
		if (browser) {
			themeStore.init();
		}
	});
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

{#if $authStore.isAuthenticated}
	<Sidebar bind:isCollapsed />
	<main
		class="min-h-screen bg-slate-50 p-4 transition-all duration-300 dark:bg-slate-900"
		class:md:ml-64={!isCollapsed}
		class:md:ml-20={isCollapsed}
	>
		{@render children()}
	</main>
{:else}
	<main class="min-h-screen bg-slate-50 dark:bg-slate-900">
		{@render children()}
	</main>
{/if}
