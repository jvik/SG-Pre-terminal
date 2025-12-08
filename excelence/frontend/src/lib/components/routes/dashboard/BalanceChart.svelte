<script lang="ts">
    import { onMount } from "svelte";
    import Chart from "chart.js/auto";

    export let netBalance: number = 0;

    let canvas: HTMLCanvasElement;
    let chart: Chart;

    $: if (chart && netBalance !== undefined) {
        updateChart();
    }

    function updateChart() {
        const isPositive = netBalance >= 0;
        chart.data.datasets[0].data = [netBalance];
        chart.data.datasets[0].backgroundColor = [
            isPositive ? "rgba(34, 197, 94, 0.8)" : "rgba(239, 68, 68, 0.8)",
        ];
        chart.data.datasets[0].borderColor = [
            isPositive ? "rgb(34, 197, 94)" : "rgb(239, 68, 68)",
        ];
        chart.update();
    }

    onMount(() => {
        if (!canvas) return;
        const ctx = canvas.getContext("2d");
        if (!ctx) return;

        const isPositive = netBalance >= 0;

        chart = new Chart(ctx, {
            type: "bar",
            data: {
                labels: ["Net Balance"],
                datasets: [
                    {
                        label: "Balance (kr)",
                        data: [netBalance],
                        backgroundColor: [
                            isPositive
                                ? "rgba(34, 197, 94, 0.8)"
                                : "rgba(239, 68, 68, 0.8)",
                        ],
                        borderColor: [
                            isPositive
                                ? "rgb(34, 197, 94)"
                                : "rgb(239, 68, 68)",
                        ],
                        borderWidth: 3,
                        borderRadius: 8,
                    },
                ],
            },
            options: {
                indexAxis: "y",
                responsive: true,
                maintainAspectRatio: false,
                animation: {
                    duration: 1000,
                    easing: "easeInOutQuart",
                },
                scales: {
                    x: {
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
                    y: {
                        grid: {
                            display: false,
                        },
                        ticks: {
                            font: {
                                size: 14,
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
                                const value = context.parsed.x;
                                return `${value >= 0 ? "+" : ""}${value.toFixed(2)} kr`;
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

<div class="h-32 w-full relative">
    <canvas bind:this={canvas}></canvas>
</div>
