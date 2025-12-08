<script lang="ts">
  import { goto } from "$app/navigation";
  import { registerUser } from "$lib/services/api";
  import { authStore } from "$lib/stores/auth";
  import { browser } from "$app/environment";

  let email = "";
  let password = "";
  let error = "";
  let success = "";
  let loading = false;

  async function handleSubmit() {
    error = "";
    success = "";
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
        success = "Registration successful! Redirecting to dashboard...";
        loading = false;
        setTimeout(() => {
          goto("/dashboard");
        }, 2000);
      } else if (data.user) {
        // Registration successful but needs email confirmation
        success =
          "Registration successful! We've sent a verification email to your inbox. Please verify your email before logging in.";
        loading = false;
      } else {
        error = "Registration failed. Please try again.";
        loading = false;
      }
    } catch (e: any) {
      error = e.message || "An unexpected error occurred.";
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
        <div
          class="flex items-start gap-3 p-4 bg-amber-50 border border-amber-200 rounded-lg"
        >
          <svg
            class="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5"
            fill="currentColor"
            viewBox="0 0 20 20"
          >
            <path
              fill-rule="evenodd"
              d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z"
              clip-rule="evenodd"
            />
          </svg>
          <p class="text-sm text-amber-800 flex-1">{error}</p>
        </div>
      {/if}
      {#if success}
        <div
          class="flex items-start gap-3 p-4 bg-green-50 border border-green-200 rounded-lg"
        >
          <svg
            class="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5"
            fill="currentColor"
            viewBox="0 0 20 20"
          >
            <path
              fill-rule="evenodd"
              d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
              clip-rule="evenodd"
            />
          </svg>
          <div class="flex-1">
            <p class="text-sm text-green-800">{success}</p>
            <a
              href="/login"
              class="mt-3 inline-block text-sm font-medium text-blue-600 hover:text-blue-700 underline"
            >
              Go to Login
            </a>
          </div>
        </div>
      {/if}
      <div>
        <button
          type="submit"
          disabled={loading || success !== ""}
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
    <div class="pt-4 text-center border-t">
      <p class="text-sm text-gray-600">
        Already have an account?
        <a
          href="/login"
          class="font-medium text-blue-600 hover:text-blue-500"
        >
          Login here
        </a>
      </p>
    </div>
  </div>
</div>
