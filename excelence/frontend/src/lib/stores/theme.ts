import { writable } from 'svelte/store';
import { browser } from '$app/environment';

export type Theme = 'light' | 'dark' | 'system';

function createThemeStore() {
    // Get initial theme from localStorage or default to 'system'
    const getInitialTheme = (): Theme => {
        if (!browser) return 'system';
        const stored = localStorage.getItem('theme') as Theme | null;
        return stored || 'system';
    };

    const { subscribe, set, update } = writable<Theme>(getInitialTheme());

    // Apply theme to document
    const applyTheme = (theme: Theme) => {
        if (!browser) return;

        const root = document.documentElement;
        
        if (theme === 'system') {
            const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
            root.classList.toggle('dark', prefersDark);
        } else {
            root.classList.toggle('dark', theme === 'dark');
        }
    };

    // Listen to system preference changes
    if (browser) {
        const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
        mediaQuery.addEventListener('change', (e) => {
            update((currentTheme) => {
                if (currentTheme === 'system') {
                    applyTheme('system');
                }
                return currentTheme;
            });
        });
    }

    return {
        subscribe,
        setTheme: (theme: Theme) => {
            if (browser) {
                localStorage.setItem('theme', theme);
                applyTheme(theme);
            }
            set(theme);
        },
        // Initialize theme on app load
        init: () => {
            const theme = getInitialTheme();
            applyTheme(theme);
        }
    };
}

export const themeStore = createThemeStore();
