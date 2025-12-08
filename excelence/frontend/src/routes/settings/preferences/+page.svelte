<script lang="ts">
    import { themeStore } from "$lib/stores/theme";
    import type { Theme } from "$lib/stores/theme";

    function selectTheme(theme: Theme) {
        themeStore.setTheme(theme);
    }

    const themeOptions = [
        {
            value: "light" as Theme,
            label: "Light",
            description: "Default light theme",
            icon: "☀️",
        },
        {
            value: "dark" as Theme,
            label: "Dark",
            description: "Comfortable for your eyes",
            icon: "🌙",
        },
        {
            value: "system" as Theme,
            label: "System",
            description: "Follow your device's theme",
            icon: "💻",
        },
    ];
</script>

<div class="p-8">
    <div class="mb-8">
        <h1 class="text-3xl font-bold text-slate-900 dark:text-white mb-2">
            Preferences
        </h1>
        <p class="text-slate-600 dark:text-slate-400">
            Customize your app preferences
        </p>
    </div>

    <!-- Theme Section -->
    <section class="mb-8">
        <h2 class="text-xl font-bold text-slate-900 dark:text-white mb-1">
            Theme
        </h2>
        <p class="text-slate-600 dark:text-slate-400 mb-6">
            Choose how Excelence looks to you
        </p>

        <div
            class="bg-white dark:bg-slate-800 p-6 rounded-xl shadow-sm border border-slate-200 dark:border-slate-700"
        >
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                {#each themeOptions as option}
                    <button
                        class="p-4 rounded-lg border-2 text-left transition-all {$themeStore ===
                        option.value
                            ? 'border-blue-500 ring-2 ring-blue-500/50 bg-blue-50 dark:bg-blue-900/20'
                            : 'border-slate-200 dark:border-slate-700 hover:border-blue-400 dark:hover:border-blue-600'}"
                        onclick={() => selectTheme(option.value)}
                    >
                        <span
                            class="text-2xl mb-2 block {$themeStore ===
                            option.value
                                ? ''
                                : 'opacity-70'}"
                        >
                            {option.icon}
                        </span>
                        <p
                            class="font-bold text-slate-900 dark:text-white mb-1"
                        >
                            {option.label}
                        </p>
                        <p class="text-sm text-slate-600 dark:text-slate-400">
                            {option.description}
                        </p>
                    </button>
                {/each}
            </div>
        </div>
    </section>

    <!-- Future Preferences Sections -->
    <section class="mb-8">
        <h2 class="text-xl font-bold text-slate-900 dark:text-white mb-1">
            Notifications
        </h2>
        <p class="text-slate-600 dark:text-slate-400 mb-6">
            Manage your notification preferences
        </p>

        <div
            class="bg-white dark:bg-slate-800 p-6 rounded-xl shadow-sm border border-slate-200 dark:border-slate-700"
        >
            <div class="flex items-center justify-between py-3">
                <div>
                    <p class="font-medium text-slate-900 dark:text-white">
                        Email Notifications
                    </p>
                    <p class="text-sm text-slate-600 dark:text-slate-400">
                        Receive email updates about your budget
                    </p>
                </div>
                <span
                    class="text-xs font-normal text-slate-500 dark:text-slate-400 bg-slate-100 dark:bg-slate-700 px-2 py-1 rounded"
                >
                    Coming Soon
                </span>
            </div>
        </div>
    </section>

    <!-- Language Section -->
    <section class="mb-8">
        <h2 class="text-xl font-bold text-slate-900 dark:text-white mb-1">
            Language & Region
        </h2>
        <p class="text-slate-600 dark:text-slate-400 mb-6">
            Set your preferred language and currency
        </p>

        <div
            class="bg-white dark:bg-slate-800 p-6 rounded-xl shadow-sm border border-slate-200 dark:border-slate-700"
        >
            <div class="flex items-center justify-between py-3">
                <div>
                    <p class="font-medium text-slate-900 dark:text-white">
                        Language Settings
                    </p>
                    <p class="text-sm text-slate-600 dark:text-slate-400">
                        Choose your preferred language
                    </p>
                </div>
                <span
                    class="text-xs font-normal text-slate-500 dark:text-slate-400 bg-slate-100 dark:bg-slate-700 px-2 py-1 rounded"
                >
                    Coming Soon
                </span>
            </div>
        </div>
    </section>
</div>
