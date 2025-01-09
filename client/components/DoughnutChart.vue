<script setup lang="ts">

  import Chart from 'chart.js/auto'

  const props = defineProps({
    data: {
      type: Array,
      required: true
    },
    labels: {
      type: Array,
      required: true
    }
  })

  const chartRef = ref<HTMLCanvasElement | null>(null)
  let chart: any = null

  const updateChart = () => {
    if (!chartRef.value) return

    const ctx = chartRef.value.getContext('2d')
    if (!ctx) return

    const datasets = [{
      data: props.data,
      borderWidth: 1
    }]

    if (chart) {
      chart.data.labels = props.labels
      chart.data.datasets = datasets
      chart.update()
      return
    }

    chart = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: props.labels,
        datasets: datasets
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
          legend: {
            position: 'bottom',
            labels: {
              padding: 20,
              font: {
                size: 12
              }
            }
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
  <canvas ref="chartRef"></canvas>
</template>