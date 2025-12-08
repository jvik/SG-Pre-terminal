<script lang="ts">
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	
	let error = '';
	let errorCode = '';
	let errorDescription = '';
	
	onMount(() => {
		error = $page.url.searchParams.get('error') || '';
		errorCode = $page.url.searchParams.get('error_code') || '';
		errorDescription = $page.url.searchParams.get('error_description') || '';
	});
	
	function getErrorMessage(): string {
		if (errorCode === 'otp_expired') {
			return 'Your verification link has expired. Please request a new one.';
		}
		if (error === 'access_denied') {
			return 'Access denied. Please try again.';
		}
		if (errorDescription) {
			return decodeURIComponent(errorDescription.replace(/\+/g, ' '));
		}
		return 'An authentication error occurred. Please try again.';
	}
</script>

<svelte:head>
	<title>Authentication Error - Excelence</title>
</svelte:head>

<div class="error-container">
	<div class="error-card">
		<div class="error-icon">
			<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
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
		
		<div class="actions">
			<a href="/login" class="btn-primary">Back to Login</a>
			<a href="/register" class="btn-secondary">Create New Account</a>
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
		background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
	}
	
	.error-card {
		background: white;
		border-radius: 1rem;
		padding: 3rem 2rem;
		max-width: 500px;
		width: 100%;
		box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
		text-align: center;
	}
	
	.error-icon {
		color: #ef4444;
		margin-bottom: 1.5rem;
		display: flex;
		justify-content: center;
	}
	
	h1 {
		font-size: 2rem;
		font-weight: 700;
		color: #1f2937;
		margin-bottom: 1rem;
	}
	
	.error-message {
		font-size: 1.125rem;
		color: #4b5563;
		margin-bottom: 1rem;
		line-height: 1.6;
	}
	
	.error-code {
		font-size: 0.875rem;
		color: #9ca3af;
		margin-bottom: 2rem;
		font-family: monospace;
	}
	
	.actions {
		display: flex;
		gap: 1rem;
		flex-direction: column;
	}
	
	.btn-primary,
	.btn-secondary {
		padding: 0.75rem 1.5rem;
		border-radius: 0.5rem;
		font-weight: 600;
		text-decoration: none;
		transition: all 0.2s;
		display: inline-block;
	}
	
	.btn-primary {
		background: #667eea;
		color: white;
	}
	
	.btn-primary:hover {
		background: #5568d3;
		transform: translateY(-2px);
		box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
	}
	
	.btn-secondary {
		background: #f3f4f6;
		color: #374151;
	}
	
	.btn-secondary:hover {
		background: #e5e7eb;
	}
	
	@media (min-width: 640px) {
		.actions {
			flex-direction: row;
			justify-content: center;
		}
	}
</style>
