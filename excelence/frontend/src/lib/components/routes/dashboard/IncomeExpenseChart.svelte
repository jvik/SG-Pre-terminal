<script lang="ts">
    import { onMount } from "svelte";
    import Chart from "chart.js/auto";

    export let totalIncome: number = 0;
    export let totalExpenses: number = 0;

    let canvas: HTMLCanvasElement;
    let chart: Chart;

    $: if (chart && (totalIncome || totalExpenses)) {
        updateChart();
    }

    function updateChart() {
        chart.data.datasets[0].data = [totalIncome, totalExpenses];
        chart.update();
    }

    onMount(() => {
        if (!canvas) return;
        const ctx = canvas.getContext("2d");
        if (!ctx) return;

        chart = new Chart(ctx, {
            type: "bar",
            data: {
                labels: ["Income", "Expenses"],
                datasets: [
                    {
                        label: "Amount (kr)",
                        data: [totalIncome, totalExpenses],
                        backgroundColor: [
                            "rgba(34, 197, 94, 0.8)", // green for income
                            "rgba(239, 68, 68, 0.8)", // red for expenses
                        ],
                        borderColor: ["rgb(34, 197, 94)", "rgb(239, 68, 68)"],
                        borderWidth: 2,
                        borderRadius: 8,
                        hoverBackgroundColor: [
                            "rgba(34, 197, 94, 1)",
                            "rgba(239, 68, 68, 1)",
                        ],
                    },
                ],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                animation: {
                    duration: 1000,
                    easing: "easeInOutQuart",
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: "rgba(0, 0, 0, 0.05)",
                        },
                        ticks: {
                            font: {
                                size: 12,
                            },
                            callback: function (value) {
                                return value.toLocaleString() + " kr";
                            },
                        },
                    },
                    x: {
                        grid: {
                            display: false,
                        },
                        ticks: {
                            font: {
                                size: 13,
                                weight: "bold",
                            },
                        },
                    },
                },
                plugins: {
                    legend: {
                        display: false,
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
                                return `${context.parsed.y.toFixed(2)} kr`;
                            },
                        },
                    },
                },
            },
        });

        return () => {
            chart.destroy();
        };
    });
</script>

<div class="h-80 w-full relative">
    {#if totalIncome === 0 && totalExpenses === 0}
        <div
            class="absolute inset-0 flex items-center justify-center text-gray-500"
        >
            <div class="text-center">
                <p class="text-lg font-medium">No financial data</p>
                <p class="text-sm mt-1">
                    Add transactions to see your income vs expenses
                </p>
            </div>
        </div>
    {/if}
    <canvas bind:this={canvas}></canvas>
</div>
