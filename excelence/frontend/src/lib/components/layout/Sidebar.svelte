<script lang="ts">
	import { page } from "$app/stores";
	import { authStore } from "$lib/stores/auth";
	import { goto } from "$app/navigation";

	// Derived state for the current path
	let currentPath = $derived($page.url.pathname);

	// Sidebar visibility state (mobile)
	let isOpen = $state(false);
	// Sidebar collapsed state (desktop) - bindable for parent component
	let { isCollapsed = $bindable(false) } = $props();

	const links = [
		{
			href: "/dashboard",
			label: "Dashboard",
			icon: `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />`,
		},
		{
			href: "/spreadsheet",
			label: "Spreadsheet",
			icon: `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17V7m0 10a2 2 0 01-2 2H5a2 2 0 01-2-2V7a2 2 0 012-2h2a2 2 0 012 2m0 10a2 2 0 002 2h2a2 2 0 002-2M9 7a2 2 0 012-2h2a2 2 0 012 2m0 10V7m0 10a2 2 0 002 2h2a2 2 0 002-2V7a2 2 0 00-2-2h-2a2 2 0 00-2 2" />`,
		},
		{
			href: "/settings",
			label: "Settings",
			icon: `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />`,
		},
	];

	function logout() {
		authStore.logout();
		goto("/login");
	}

	function toggle() {
		isOpen = !isOpen;
	}

	function toggleCollapse() {
		isCollapsed = !isCollapsed;
	}

	// Close sidebar when navigating
	$effect(() => {
		// dependency on currentPath triggers this
		if (currentPath) {
			isOpen = false;
		}
	});
</script>

<!-- Hamburger Button (Mobile Only) -->
<button
	class="fixed top-2 left-2 z-50 rounded-lg bg-white p-2 text-slate-600 focus:ring-2 focus:ring-slate-200 focus:outline-none dark:bg-slate-800 dark:text-slate-400 dark:focus:ring-slate-700 md:hidden"
	onclick={toggle}
	aria-controls="sidebar"
	aria-expanded={isOpen}
>
	<span class="sr-only">Open sidebar</span>
	<svg
		class="h-6 w-6"
		fill="currentColor"
		viewBox="0 0 20 20"
		xmlns="http://www.w3.org/2000/svg"
	>
		<path
			clip-rule="evenodd"
			fill-rule="evenodd"
			d="M2 4.75A.75.75 0 012.75 4h14.5a.75.75 0 010 1.5H2.75A.75.75 0 012 4.75zm0 5A.75.75 0 012.75 9h14.5a.75.75 0 010 1.5H2.75A.75.75 0 012 9.75zm0 5A.75.75 0 012.75 14h14.5a.75.75 0 010 1.5H2.75A.75.75 0 012 14.75z"
		></path>
	</svg>
</button>

<aside
	id="sidebar"
	class="fixed top-0 left-0 z-40 h-screen border-r border-slate-200 bg-white transition-all duration-300 md:translate-x-0 dark:border-slate-700 dark:bg-slate-800"
	class:w-64={!isCollapsed}
	class:w-20={isCollapsed}
	class:translate-x-0={isOpen}
	class:-translate-x-full={!isOpen}
	aria-label="Sidebar"
>
	<div class="h-full overflow-y-auto px-3 py-4 flex flex-col">
		<div class="mb-6 px-4 flex items-center justify-between">
			{#if !isCollapsed}
				<span
					class="self-center text-xl font-black whitespace-nowrap text-slate-800 dark:text-white"
				>
					Excelence
				</span>
			{:else}
				<span
					class="self-center text-xl font-black text-slate-800 dark:text-white"
				>
					E
				</span>
			{/if}
			<!-- Desktop Collapse Toggle -->
			<button
				onclick={toggleCollapse}
				class="hidden md:block p-1.5 rounded-lg text-slate-600 hover:bg-slate-100 dark:text-slate-400 dark:hover:bg-slate-700 transition-colors"
				aria-label={isCollapsed ? "Expand sidebar" : "Collapse sidebar"}
			>
				<svg
					class="w-5 h-5 transition-transform duration-300"
					class:rotate-180={isCollapsed}
					fill="none"
					stroke="currentColor"
					viewBox="0 0 24 24"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M11 19l-7-7 7-7m8 14l-7-7 7-7"
					/>
				</svg>
			</button>
		</div>
		<ul class="space-y-2 font-medium flex-1">
			{#each links as link}
				{@const isActive =
					currentPath === link.href ||
					(link.href !== "/" && currentPath.startsWith(link.href))}
				<li>
					<a
						href={link.href}
						class="group flex items-center rounded-lg p-2 transition-colors duration-200"
						class:justify-center={isCollapsed}
						class:bg-blue-50={isActive}
						class:text-blue-600={isActive}
						class:text-slate-600={!isActive}
						class:hover:bg-blue-50={!isActive}
						class:hover:text-blue-600={!isActive}
						class:dark:text-slate-200={!isActive}
						class:dark:hover:bg-slate-700={!isActive}
						title={isCollapsed ? link.label : ""}
					>
						<svg
							class="w-6 h-6"
							class:flex-shrink-0={!isCollapsed}
							fill="none"
							stroke="currentColor"
							viewBox="0 0 24 24"
						>
							{@html link.icon}
						</svg>
						{#if !isCollapsed}
							<span class="ms-3">{link.label}</span>
						{/if}
					</a>
				</li>
			{/each}
		</ul>
		<div class="px-3 mt-auto">
			<button
				onclick={logout}
				class="w-full flex items-center justify-center gap-2 rounded-lg p-2 bg-red-50 text-red-600 hover:bg-red-100 dark:bg-red-900/20 dark:text-red-400 dark:hover:bg-red-900/30 transition-colors duration-200 font-medium"
				title={isCollapsed ? "Logg ut" : ""}
			>
				<svg
					class="w-5 h-5"
					fill="none"
					stroke="currentColor"
					viewBox="0 0 24 24"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
					/>
				</svg>
				{#if !isCollapsed}
					<span class="ms-1">Logg ut</span>
				{/if}
			</button>
		</div>
	</div>
</aside>

<!-- Overlay for mobile -->
{#if isOpen}
	<div
		class="fixed inset-0 z-30 bg-slate-900/50 md:hidden"
		onclick={toggle}
		role="presentation"
	></div>
{/if}
