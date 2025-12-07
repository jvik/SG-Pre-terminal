<script lang="ts">
	import { onMount } from 'svelte';
	import Chart from 'chart.js/auto';

	export let chartData: { category_name: string; total_amount: number }[] = [];

	let canvas: HTMLCanvasElement;
	let chart: Chart;

	$: if (chart && chartData) {
		chart.data = formatData(chartData);
		chart.update();
	}

	function formatData(rawData: typeof chartData) {
		return {
			labels: rawData.map((d) => d.category_name),
			datasets: [
				{
					data: rawData.map((d) => d.total_amount),
					backgroundColor: [
						'#3B82F6', // blue-500
						'#EF4444', // red-500
						'#10B981', // green-500
						'#F59E0B', // yellow-500
						'#8B5CF6', // violet-500
						'#EC4899', // pink-500
						'#6366F1', // indigo-500
						'#14B8A6'  // teal-500
					],
					borderWidth: 0
				}
			]
		};
	}

	onMount(() => {
		if (!canvas) return;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

		chart = new Chart(ctx, {
			type: 'doughnut',
			data: formatData(chartData),
			options: {
				responsive: true,
				maintainAspectRatio: false,
				plugins: {
					legend: {
						position: 'right',
                        labels: {
                            usePointStyle: true,
                            boxWidth: 10
                        }
					},
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                let label = context.label || '';
                                if (label) {
                                    label += ': ';
                                }
                                if (context.parsed !== null) {
                                    label += new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(context.parsed);
                                }
                                return label;
                            }
                        }
                    }
				},
                cutout: '60%'
			}
		});

		return () => {
			chart.destroy();
		};
	});
</script>

<div class="h-64 w-full relative">
    {#if chartData.length === 0}
        <div class="absolute inset-0 flex items-center justify-center text-gray-500">
            No expense data
        </div>
    {/if}
	<canvas bind:this={canvas}></canvas>
</div>
