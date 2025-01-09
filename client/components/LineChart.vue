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
            default: () => ["#1C2222", "#495A5A", "#789191", "#B0BFBF"]
        },

        grid: {
            type: Boolean,
            default: false
        },

        datasetsLabel: {
            type: String,
            default: ''
        }
    })

    const datasets = [
        {
            label:props.datasetsLabel,
            data: props.data,
            borderColor: props.colorChart[0]
        }
    ]

    const data = {
        labels: props.labels,
        datasets
    }

    const chartRef = ref<HTMLCanvasElement | null>(null)

    onMounted(() => {
        const ctx = chartRef.value.getContext('2d')
        if (ctx) {
            new Chart(ctx, {
                type: 'line',
                data: data,
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    scales: {
                        x: {
                            grid: {
                                display: props.grid
                            }
                        },
                        y: {
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
