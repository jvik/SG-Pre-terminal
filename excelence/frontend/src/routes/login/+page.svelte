<script lang="ts">
  import { goto } from "$app/navigation";
  import { authStore } from "$lib/stores/auth";

  let email = "";
  let password = "";
  let error: string | null = null;
  let isLoading = false;
  let showSlowApiWarning = false;
  let timeoutId: ReturnType<typeof setTimeout>;

  async function handleSubmit() {
    error = null;
    isLoading = true;
    showSlowApiWarning = false;

    // Show warning after 3 seconds if still loading
    timeoutId = setTimeout(() => {
      if (isLoading) {
        showSlowApiWarning = true;
      }
    }, 3000);

    try {
      await authStore.login(email, password);
      clearTimeout(timeoutId);
      goto("/dashboard");
    } catch (err) {
      clearTimeout(timeoutId);
      error = (err as Error).message;
    } finally {
      isLoading = false;
      showSlowApiWarning = false;
    }
  }
</script>

<div class="flex items-center justify-center h-screen">
  <div class="w-full max-w-md p-8 space-y-6 bg-white rounded-lg shadow-md">
    <a href="/" class="block">
      <h1
        class="text-2xl font-bold text-center text-blue-600 hover:text-blue-700 cursor-pointer transition-colors"
      >
        Login
      </h1>
    </a>
    <form on:submit|preventDefault={handleSubmit} class="space-y-6">
      <div>
        <label for="email" class="block text-sm font-medium text-gray-700"
          >Email</label
        >
        <input
          type="email"
          id="email"
          bind:value={email}
          class="w-full px-3 py-2 mt-1 border rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
          required
        />
      </div>
      <div>
        <label for="password" class="block text-sm font-medium text-gray-700"
          >Password</label
        >
        <input
          type="password"
          id="password"
          bind:value={password}
          class="w-full px-3 py-2 mt-1 border rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
          required
        />
      </div>
      {#if error}
        <div class="flex items-start gap-3 p-4 bg-amber-50 border border-amber-200 rounded-lg">
          <svg class="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
          </svg>
          <p class="text-sm text-amber-800 flex-1">{error}</p>
        </div>
      {/if}
      {#if showSlowApiWarning}
        <div
          class="p-3 text-sm text-amber-800 bg-amber-50 border border-amber-200 rounded-md"
        >
          <p class="font-medium">⏳ Starting up backend server...</p>
          <p class="mt-1 text-xs">
            The API is hosted on Render's free tier and may take up to 30
            seconds to wake up from sleep. Please wait a moment.
          </p>
        </div>
      {/if}
      <div>
        <button
          type="submit"
          disabled={isLoading}
          class="w-full px-4 py-2 font-bold text-white bg-blue-500 rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isLoading ? "Logging in..." : "Login"}
        </button>
      </div>
    </form>
    <div class="pt-4 text-center border-t">
      <p class="text-sm text-gray-600">
        Don't have an account?
        <a
          href="/register"
          class="font-medium text-blue-600 hover:text-blue-500"
        >
          Register here
        </a>
      </p>
    </div>
  </div>
</div>
