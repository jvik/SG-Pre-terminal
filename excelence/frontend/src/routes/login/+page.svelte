<script lang="ts">
  import { goto } from "$app/navigation";
  import { authStore } from "$lib/stores/auth";

  let email = "";
  let password = "";
  let error: string | null = null;

  async function handleSubmit() {
    error = null;
    try {
      await authStore.login(email, password);
      goto("/dashboard");
    } catch (err) {
      error = (err as Error).message;
    }
  }
</script>

<div class="flex items-center justify-center h-screen">
  <div class="w-full max-w-md p-8 space-y-6 bg-white rounded-lg shadow-md">
    <h1 class="text-2xl font-bold text-center">Login</h1>
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
        <p class="text-sm text-red-600">{error}</p>
      {/if}
      <div>
        <button
          type="submit"
          class="w-full px-4 py-2 font-bold text-white bg-blue-500 rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        >
          Login
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
