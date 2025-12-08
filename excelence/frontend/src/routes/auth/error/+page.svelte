<script lang="ts">
    import { page } from "$app/stores";
    import { onMount } from "svelte";
    import { authStore } from "$lib/stores/auth";

    let error = $state("");
    let errorCode = $state("");
    let errorDescription = $state("");
    let email = $state("");
    let isResending = $state(false);
    let resendSuccess = $state(false);
    let resendError = $state("");

    onMount(() => {
        error = $page.url.searchParams.get("error") || "";
        errorCode = $page.url.searchParams.get("error_code") || "";
        errorDescription =
            $page.url.searchParams.get("error_description") || "";
    });

    function getErrorMessage(): string {
        if (errorCode === "otp_expired") {
            return "Your verification link has expired. Please request a new one.";
        }
        if (error === "access_denied") {
            return "Access denied. Please try again.";
        }
        if (errorDescription) {
            return decodeURIComponent(errorDescription.replace(/\+/g, " "));
        }
        return "An authentication error occurred. Please try again.";
    }

    function isExpiredVerification(): boolean {
        return errorCode === "otp_expired" || 
               (error === "access_denied" && errorDescription?.includes("expired"));
    }

    async function handleResendVerification() {
        if (!email) {
            resendError = "Please enter your email address";
            return;
        }

        resendError = "";
        resendSuccess = false;
        isResending = true;

        try {
            await authStore.resendVerification(email);
            resendSuccess = true;
        } catch (err) {
            resendError = (err as Error).message;
        } finally {
            isResending = false;
        }
    }
</script>

<svelte:head>
    <title>Authentication Error - Excelence</title>
</svelte:head>

<div class="error-container">
    <div class="error-card">
        <div class="error-icon">
            <svg
                xmlns="http://www.w3.org/2000/svg"
                width="64"
                height="64"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
            >
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="15" y1="9" x2="9" y2="15"></line>
                <line x1="9" y1="9" x2="15" y2="15"></line>
            </svg>
        </div>

        <h1>Authentication Error</h1>

        <p class="error-message">
            {getErrorMessage()}
        </p>

        {#if errorCode}
            <p class="error-code">Error Code: {errorCode}</p>
        {/if}

        {#if isExpiredVerification() && !resendSuccess}
            <div class="resend-section">
                <p class="resend-prompt">Enter your email to receive a new verification link:</p>
                <input
                    type="email"
                    bind:value={email}
                    placeholder="your@email.com"
                    class="email-input"
                    disabled={isResending}
                />
                {#if resendError}
                    <p class="error-text">{resendError}</p>
                {/if}
                <button
                    onclick={handleResendVerification}
                    disabled={isResending}
                    class="btn-resend"
                >
                    {isResending ? "Sending..." : "Resend Verification Email"}
                </button>
            </div>
        {/if}

        {#if resendSuccess}
            <div class="success-message">
                ✓ Verification email sent! Please check your inbox.
            </div>
        {/if}

        <div class="actions">
            <a href="/login" class="btn-primary">Back to Login</a>
            {#if !isExpiredVerification()}
                <a href="/register" class="btn-secondary">Create New Account</a>
            {/if}
        </div>
    </div>
</div>

<style>
    .error-container {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
        padding: 1rem;
        background: linear-gradient(to bottom right, rgb(241 245 249), rgb(226 232 240));
    }

    :global(.dark) .error-container {
        background: linear-gradient(to bottom right, rgb(15 23 42), rgb(30 41 59));
    }

    .error-card {
        background: white;
        border-radius: 1rem;
        padding: 3rem 2rem;
        max-width: 500px;
        width: 100%;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
        text-align: center;
    }

    :global(.dark) .error-card {
        background: rgb(30 41 59);
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
    }

    .error-icon {
        color: rgb(239 68 68);
        margin-bottom: 1.5rem;
        display: flex;
        justify-content: center;
    }

    h1 {
        font-size: 2rem;
        font-weight: 700;
        color: rgb(15 23 42);
        margin-bottom: 1rem;
    }

    :global(.dark) h1 {
        color: rgb(241 245 249);
    }

    .error-message {
        font-size: 1.125rem;
        color: rgb(71 85 105);
        margin-bottom: 1rem;
        line-height: 1.6;
    }

    :global(.dark) .error-message {
        color: rgb(203 213 225);
    }

    .error-code {
        font-size: 0.875rem;
        color: rgb(148 163 184);
        margin-bottom: 2rem;
        font-family: monospace;
    }

    .resend-section {
        margin: 2rem 0;
        padding: 1.5rem;
        background: rgb(241 245 249);
        border-radius: 0.5rem;
    }

    :global(.dark) .resend-section {
        background: rgb(15 23 42);
    }

    .resend-prompt {
        font-size: 0.875rem;
        color: rgb(71 85 105);
        margin-bottom: 1rem;
    }

    :global(.dark) .resend-prompt {
        color: rgb(203 213 225);
    }

    .email-input {
        width: 100%;
        padding: 0.75rem;
        border: 1px solid rgb(203 213 225);
        border-radius: 0.5rem;
        font-size: 1rem;
        margin-bottom: 1rem;
        transition: border-color 0.2s;
    }

    :global(.dark) .email-input {
        background: rgb(30 41 59);
        border-color: rgb(71 85 105);
        color: rgb(241 245 249);
    }

    .email-input:focus {
        outline: none;
        border-color: rgb(59 130 246);
    }

    .email-input:disabled {
        opacity: 0.6;
        cursor: not-allowed;
    }

    .error-text {
        color: rgb(239 68 68);
        font-size: 0.875rem;
        margin-bottom: 0.5rem;
    }

    .success-message {
        background: rgb(220 252 231);
        color: rgb(22 101 52);
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1.5rem;
        font-weight: 500;
    }

    :global(.dark) .success-message {
        background: rgb(20 83 45);
        color: rgb(187 247 208);
    }

    .actions {
        display: flex;
        gap: 1rem;
        flex-direction: column;
    }

    .btn-primary,
    .btn-secondary,
    .btn-resend {
        padding: 0.75rem 1.5rem;
        border-radius: 0.5rem;
        font-weight: 600;
        text-decoration: none;
        transition: all 0.2s;
        display: inline-block;
        border: none;
        cursor: pointer;
        font-size: 1rem;
    }

    .btn-primary {
        background: rgb(59 130 246);
        color: white;
    }

    .btn-primary:hover {
        background: rgb(37 99 235);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
    }

    .btn-secondary {
        background: rgb(241 245 249);
        color: rgb(51 65 85);
    }

    :global(.dark) .btn-secondary {
        background: rgb(51 65 85);
        color: rgb(241 245 249);
    }

    .btn-secondary:hover {
        background: rgb(226 232 240);
    }

    :global(.dark) .btn-secondary:hover {
        background: rgb(71 85 105);
    }

    .btn-resend {
        width: 100%;
        background: rgb(59 130 246);
        color: white;
    }

    .btn-resend:hover:not(:disabled) {
        background: rgb(37 99 235);
    }

    .btn-resend:disabled {
        opacity: 0.6;
        cursor: not-allowed;
    }

    @media (min-width: 640px) {
        .actions {
            flex-direction: row;
            justify-content: center;
        }
    }
</style>
