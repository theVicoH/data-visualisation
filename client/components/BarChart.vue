<script setup lang="ts">
    
    import Chart from 'chart.js/auto'

    const props = defineProps({
        labels: {
            type: Array as () => string[],
            default: []
        },

        data: {
            type: Array as () => number[],
            default: []
        },

        colorChart: {
            type: Array as () => string[],
            default: () => ["#C5D1EB", "#92AFD7", "#5A7684", "#395B50", "#D8DCFF", "#AEADF0", "#C38D94", "#A76571", "#565676"]
        }
    })

    const chartData = {
        labels: props.labels,
        datasets: [{
            label: 'Nombre de passagers',
            data: props.data,
            backgroundColor: props.colorChart
        }]
    }

    const chartRef = ref<any>(null)

    onMounted(() => {
        const ctx = chartRef.value.getContext('2d')
        new Chart(ctx, {
            type: 'bar',
            data: chartData,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return value.toLocaleString()
                            }
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
    })
</script>

<template>
    <canvas ref="chartRef" class="h-full" />
</template>
