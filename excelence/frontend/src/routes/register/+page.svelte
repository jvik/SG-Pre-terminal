<script lang="ts">
  import { goto } from "$app/navigation";
  import { registerUser } from "$lib/services/api";
  import { authStore } from "$lib/stores/auth";
  import { browser } from "$app/environment";

  let email = "";
  let password = "";
  let error = "";
  let loading = false;

  async function handleSubmit() {
    error = "";
    if (password.length < 8) {
      error = "Password must be at least 8 characters long.";
      return;
    }
    const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/;
    if (!passwordRegex.test(password)) {
      error = "Password must contain at least one letter and one number.";
      return;
    }

    loading = true;
    try {
      const data = await registerUser(email, password);
      // After successful registration, log the user in automatically
      if (data.session && data.session.access_token) {
        if (browser) {
          localStorage.setItem("jwt_token", data.session.access_token);
        }
        goto("/dashboard");
      } else {
        // Registration successful but might need email confirmation
        error =
          "Registration successful! Please check your email to confirm your account, then log in.";
      }
    } catch (e: any) {
      error = e.message || "An unexpected error occurred.";
    } finally {
      loading = false;
    }
  }
</script>

<div class="flex items-center justify-center h-screen">
  <div class="w-full max-w-md p-8 space-y-6 bg-white rounded-lg shadow-md">
    <h1 class="text-2xl font-bold text-center">Register</h1>
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
        <p class="mt-1 text-xs text-gray-500">
          Password must be at least 8 characters with a letter and a number.
        </p>
      </div>
      {#if error}
        <p class="text-sm text-red-600">{error}</p>
      {/if}
      <div>
        <button
          type="submit"
          disabled={loading}
          class="w-full px-4 py-2 font-bold text-white bg-blue-500 rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {#if loading}
            Registering...
          {:else}
            Register
          {/if}
        </button>
      </div>
    </form>
  </div>
</div>
