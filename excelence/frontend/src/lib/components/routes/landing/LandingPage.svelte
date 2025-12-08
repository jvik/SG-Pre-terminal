<script lang="ts">
	import { goto } from "$app/navigation";
</script>

<div
	class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-slate-900 dark:to-slate-800"
>
	<div class="container mx-auto px-4 py-16">
		<!-- Header -->
		<div class="text-center mb-16">
			<h1
				class="text-5xl md:text-6xl font-bold text-gray-900 dark:text-white mb-4"
			>
				Welcome to <span class="text-blue-600 dark:text-blue-400"
					>Excelence</span
				>
			</h1>
			<p
				class="text-xl md:text-2xl text-gray-600 dark:text-slate-300 mb-8"
			>
				Your personal expense tracker - Simple, powerful, and free
			</p>
		</div>

		<!-- Features Grid -->
		<div class="grid md:grid-cols-3 gap-8 mb-16 max-w-6xl mx-auto">
			<div class="bg-white dark:bg-slate-800 p-6 rounded-lg shadow-lg">
				<div class="text-4xl mb-4">📊</div>
				<h3
					class="text-xl font-semibold text-gray-900 dark:text-white mb-2"
				>
					Track Your Spending
				</h3>
				<p class="text-gray-600 dark:text-slate-300">
					Monitor your income and expenses with intuitive charts and
					visualizations
				</p>
			</div>

			<div class="bg-white dark:bg-slate-800 p-6 rounded-lg shadow-lg">
				<div class="text-4xl mb-4">🎯</div>
				<h3
					class="text-xl font-semibold text-gray-900 dark:text-white mb-2"
				>
					Organize by Category
				</h3>
				<p class="text-gray-600 dark:text-slate-300">
					Create custom categories to organize your transactions your
					way
				</p>
			</div>

			<div class="bg-white dark:bg-slate-800 p-6 rounded-lg shadow-lg">
				<div class="text-4xl mb-4">💾</div>
				<h3
					class="text-xl font-semibold text-gray-900 dark:text-white mb-2"
				>
					Export Your Data
				</h3>
				<p class="text-gray-600 dark:text-slate-300">
					Download your financial data anytime in CSV format for
					analysis
				</p>
			</div>
		</div>

		<!-- CTA Section -->
		<div class="text-center max-w-2xl mx-auto">
			<div class="bg-white dark:bg-slate-800 p-8 rounded-xl shadow-xl">
				<h2
					class="text-3xl font-bold text-gray-900 dark:text-white mb-4"
				>
					Ready to take control of your finances?
				</h2>
				<p class="text-lg text-gray-600 dark:text-slate-300 mb-8">
					Join thousands of users who are already managing their
					budgets with Excelence
				</p>

				<div class="flex flex-col sm:flex-row gap-4 justify-center">
					<button
						on:click={() => goto("/register")}
						class="bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 text-white font-bold py-3 px-8 rounded-lg text-lg shadow-lg transition-colors"
					>
						Get Started Free
					</button>
					<button
						on:click={() => goto("/login")}
						class="bg-white hover:bg-gray-50 dark:bg-slate-700 dark:hover:bg-slate-600 text-gray-800 dark:text-white font-semibold py-3 px-8 rounded-lg text-lg border-2 border-gray-300 dark:border-slate-600 shadow-lg transition-colors"
					>
						Sign In
					</button>
				</div>

				<p class="mt-6 text-sm text-gray-500 dark:text-slate-400">
					No credit card required • Free forever • Your data stays
					private
				</p>
			</div>
		</div>
	</div>
</div>
