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

    const chartRef = ref<HTMLCanvasElement | null>(null)
    let chart: any = null

    const updateChart = () => {
        if (!chartRef.value) return
        const ctx = chartRef.value.getContext('2d')
        if (!ctx) return

        const datasets: any = props.stackedBars
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

        if (chart) {
            chart.data.labels = props.labels
            chart.data.datasets = datasets
            chart.update()
            return
        }

        chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: props.labels,
                datasets: datasets
            },
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

    onMounted(() => {
        updateChart()
    })

    watch(() => props.data, () => {
        updateChart()
    }, { deep: true })

    watch(() => props.labels, () => {
        updateChart()
    })

    onUnmounted(() => {
        if (chart) {
            chart.destroy()
            chart = null
        }
    })

</script>

<template>
    <canvas ref="chartRef" />
</template>
