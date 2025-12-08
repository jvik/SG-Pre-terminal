<script lang="ts">
    import { goto } from "$app/navigation";

    const settingsSections = [
        {
            title: "Categories",
            description: "Manage your transaction categories",
            icon: "📂",
            href: "/settings/categories",
        },
        {
            title: "Profile",
            description: "Update your profile information",
            icon: "👤",
            href: "/settings/profile",
            disabled: true,
        },
        {
            title: "Preferences",
            description: "Customize your app preferences",
            icon: "⚙️",
            href: "/settings/preferences",
        },
        {
            title: "Security",
            description: "Change password and security settings",
            icon: "🔒",
            href: "/settings/security",
            disabled: true,
        },
    ];

    function navigateTo(href: string, disabled: boolean) {
        if (!disabled) {
            goto(href);
        }
    }
</script>

<div class="p-8">
    <h1 class="text-3xl font-bold text-slate-900 dark:text-white mb-2">
        Settings
    </h1>
    <p class="text-slate-600 dark:text-slate-400 mb-8">
        Manage your account settings and preferences
    </p>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        {#each settingsSections as section}
            <button
                class="group relative bg-white dark:bg-slate-800 rounded-lg shadow-sm border border-slate-200 dark:border-slate-700 p-6 text-left transition-all duration-200 {section.disabled
                    ? 'opacity-60 cursor-not-allowed'
                    : 'hover:shadow-md hover:border-slate-300 dark:hover:border-slate-600 cursor-pointer'}"
                onclick={() =>
                    navigateTo(section.href, section.disabled || false)}
                disabled={section.disabled}
            >
                <div class="flex items-center gap-4">
                    <div class="text-3xl">{section.icon}</div>
                    <div class="flex-1">
                        <h2
                            class="text-xl font-semibold text-slate-900 dark:text-white mb-1 flex items-center gap-2"
                        >
                            {section.title}
                            {#if section.disabled}
                                <span
                                    class="text-xs font-normal text-slate-500 dark:text-slate-400 bg-slate-100 dark:bg-slate-700 px-2 py-1 rounded"
                                >
                                    Coming Soon
                                </span>
                            {/if}
                        </h2>
                        <p class="text-slate-600 dark:text-slate-400">
                            {section.description}
                        </p>
                    </div>
                    {#if !section.disabled}
                        <svg
                            class="w-6 h-6 text-slate-400 group-hover:text-slate-600 dark:group-hover:text-slate-300 transition-colors"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                        >
                            <path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                stroke-width="2"
                                d="M9 5l7 7-7 7"
                            />
                        </svg>
                    {/if}
                </div>
            </button>
        {/each}
    </div>
</div>
