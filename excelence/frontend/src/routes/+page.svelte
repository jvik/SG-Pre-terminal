<script lang="ts">
	import { goto } from "$app/navigation";
	import { browser } from "$app/environment";
	import { onMount } from "svelte";
	import { authStore } from "$lib/stores/auth";
	import LandingPage from "$lib/components/routes/landing/LandingPage.svelte";

	let verificationMessage = $state("");
	let isProcessingVerification = $state(false);
	let isHandlingCallback = $state(false);

	onMount(() => {
		// Check for email verification callback (Supabase redirects with hash)
		if (browser && window.location.hash) {
			isHandlingCallback = true;
			const hashParams = new URLSearchParams(
				window.location.hash.substring(1),
			);

			// Check for errors first
			const error = hashParams.get("error");
			const errorCode = hashParams.get("error_code");
			const errorDescription = hashParams.get("error_description");

			if (error) {
				// Redirect to error page with error details as query params
				const errorParams = new URLSearchParams();
				errorParams.set("error", error);
				if (errorCode) errorParams.set("error_code", errorCode);
				if (errorDescription)
					errorParams.set("error_description", errorDescription);

				goto(`/auth/error?${errorParams.toString()}`);
				return;
			}

			// Check for successful verification
			const accessToken = hashParams.get("access_token");
			const type = hashParams.get("type");

			if (accessToken && type === "signup") {
				isProcessingVerification = true;
				verificationMessage =
					"Email verified successfully! Redirecting to login...";

				// Clear the hash from URL
				window.history.replaceState(null, "", window.location.pathname);

				// Redirect to login page after a short delay
				setTimeout(() => {
					goto("/login?verified=true");
				}, 2000);
			}
		}
	});

	// Reactive redirect - runs whenever authStore changes
	$effect(() => {
		if (
			browser &&
			$authStore.isAuthenticated &&
			!isProcessingVerification &&
			!isHandlingCallback
		) {
			goto("/dashboard");
		}
	});
</script>

{#if isProcessingVerification}
	<div class="min-h-screen flex items-center justify-center bg-gray-50">
		<div class="max-w-md p-8 bg-white rounded-lg shadow-md text-center">
			<svg
				class="w-16 h-16 mx-auto text-green-500 mb-4"
				fill="currentColor"
				viewBox="0 0 20 20"
			>
				<path
					fill-rule="evenodd"
					d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
					clip-rule="evenodd"
				/>
			</svg>
			<h2 class="text-2xl font-bold text-gray-900 mb-2">
				Email Verified!
			</h2>
			<p class="text-gray-600">{verificationMessage}</p>
		</div>
	</div>
{:else if !$authStore.isAuthenticated}
	<LandingPage />
{:else}
	<!-- Loading/redirecting state -->
	<div class="min-h-screen flex items-center justify-center">
		<p class="text-gray-600 dark:text-slate-300">
			Redirecting to dashboard...
		</p>
	</div>
{/if}
