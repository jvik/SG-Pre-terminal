<script lang="ts">
	import { onMount } from "svelte";
	import Chart from "chart.js/auto";

	export let chartData: { category_name: string; total_amount: number }[] =
		[];

	let canvas: HTMLCanvasElement;
	let chart: Chart;

	$: if (chart && chartData) {
		chart.data = formatData(chartData);
		chart.update();
	}

	function formatData(rawData: typeof chartData) {
		const colorPalette = [
			"#FF6B6B",
			"#4ECDC4",
			"#45B7D1",
			"#FFA07A",
			"#98D8C8",
			"#F7DC6F",
			"#BB8FCE",
			"#85C1E2",
			"#F8B739",
			"#52B788",
			"#E63946",
			"#457B9D",
		];

		const total = rawData.reduce((sum, d) => sum + d.total_amount, 0);

		return {
			labels: rawData.map((d) => d.category_name),
			datasets: [
				{
					data: rawData.map((d) => d.total_amount),
					backgroundColor: colorPalette.slice(0, rawData.length),
					borderWidth: 2,
					borderColor: "#ffffff",
					hoverOffset: 8,
					hoverBorderColor: "#ffffff",
					hoverBorderWidth: 3,
				},
			],
		};
	}

	onMount(() => {
		if (!canvas) return;
		const ctx = canvas.getContext("2d");
		if (!ctx) return;

		chart = new Chart(ctx, {
			type: "doughnut",
			data: formatData(chartData),
			options: {
				responsive: true,
				maintainAspectRatio: false,
				animation: {
					animateRotate: true,
					animateScale: true,
					duration: 1000,
					easing: "easeInOutQuart",
				},
				plugins: {
					legend: {
						position: "right",
						labels: {
							usePointStyle: true,
							pointStyle: "circle",
							boxWidth: 12,
							padding: 15,
							font: {
								size: 13,
								weight: "500",
							},
							generateLabels: (chart) => {
								const data = chart.data;
								if (
									data.labels?.length &&
									data.datasets?.length
								) {
									const total = data.datasets[0].data.reduce(
										(a: number, b: number) => a + b,
										0,
									) as number;
									return data.labels.map((label, i) => {
										const value = data.datasets[0].data[
											i
										] as number;
										const percentage = (
											(value / total) *
											100
										).toFixed(1);
										return {
											text: `${label} (${percentage}%)`,
											fillStyle:
												data.datasets[0]
													.backgroundColor[i],
											hidden: false,
											index: i,
										};
									});
								}
								return [];
							},
						},
					},
					tooltip: {
						backgroundColor: "rgba(0, 0, 0, 0.8)",
						padding: 12,
						titleFont: {
							size: 14,
							weight: "bold",
						},
						bodyFont: {
							size: 13,
						},
						cornerRadius: 8,
						callbacks: {
							label: function (context) {
								let label = context.label || "";
								const value = context.parsed;
								const total = context.dataset.data.reduce(
									(a: number, b: number) => a + b,
									0,
								) as number;
								const percentage = (
									(value / total) *
									100
								).toFixed(1);

								if (label) {
									label += ": ";
								}
								if (context.parsed !== null) {
									label += `${value.toFixed(2)} kr (${percentage}%)`;
								}
								return label;
							},
						},
					},
				},
				cutout: "65%",
			},
		});

		return () => {
			chart.destroy();
		};
	});
</script>

<div class="h-80 w-full relative">
	{#if chartData.length === 0}
		<div
			class="absolute inset-0 flex items-center justify-center text-gray-500"
		>
			<div class="text-center">
				<p class="text-lg font-medium">No expense data</p>
				<p class="text-sm mt-1">
					Add transactions to see your spending breakdown
				</p>
			</div>
		</div>
	{/if}
	<canvas bind:this={canvas}></canvas>
</div>
