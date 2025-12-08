import { writable } from 'svelte/store';
import { browser } from '$app/environment';
import api from '$lib/services/api';

const createAuthStore = () => {
  const { subscribe, set } = writable({
    isAuthenticated: browser && !!localStorage.getItem('jwt_token'),
    token: browser && localStorage.getItem('jwt_token'),
  });

  return {
    subscribe,
    login: async (email, password) => {
      const body = new URLSearchParams();
      body.append('username', email);
      body.append('password', password);

      const response = await api.post('/api/v1/auth/login', body, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });
      if (response.access_token) {
        if (browser) {
          localStorage.setItem('jwt_token', response.access_token);
        }
        set({ isAuthenticated: true, token: response.access_token });
      }
    },
    logout: () => {
      if (browser) {
        localStorage.removeItem('jwt_token');
      }
      set({ isAuthenticated: false, token: null });
    },
  };
};

export const authStore = createAuthStore();
