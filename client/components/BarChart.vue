<script setup lang="ts">
    
    import Chart from 'chart.js/auto'

    const props = defineProps({
        labels: {
            type: Array as () => string[],
            default: () => []
        },

        data: {
            type: Array as () => number[],
            default: () => []
        },

        colorChart: {
            type: Array as () => string[],
            default: () => ["#C5D1EB", "#92AFD7", "#5A7684", "#395B50", "#D8DCFF", "#AEADF0", "#C38D94", "#A76571", "#565676"]
        },

        stackedBars: {
            type: Boolean,
            default: false
        },

        datasetsLabel: {
            type: Array as () => string[],
            default: () => []
        },

        grid: {
            type: Boolean,
            default: false
        }
    })

    const datasets = props.stackedBars
        ? props.data.map((dataset, index) => ({
            label: props.datasetsLabel[index],
            data: dataset,
            backgroundColor: props.colorChart[index % props.colorChart.length]
        }))
        : [{
            label: props.datasetsLabel[0],
            data: props.data,
            backgroundColor: props.colorChart
        }]


    const chartData = {
        labels: props.labels,
        datasets: datasets
    }

    const chartRef = ref<HTMLCanvasElement | null>(null)

    onMounted(() => {
        const ctx = chartRef.value.getContext('2d')
        if (ctx) {
            new Chart(ctx, {
                type: 'bar',
                data: chartData,
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    scales: {
                        x: {
                            stacked: props.stackedBars,
                            grid: {
                                display: props.grid
                            }
                        },
                        y: {
                            stacked: props.stackedBars,
                            beginAtZero: true,
                            ticks: {
                                callback: function(value) {
                                    return value.toLocaleString()
                                }
                            },
                            grid: {
                                display: props.grid
                            }
                        }
                    },
                    plugins: {
                        legend: {
                            display: false
                        }
                    }
                }
            })
        }
    })
</script>

<template>
    <canvas ref="chartRef" />
</template>
