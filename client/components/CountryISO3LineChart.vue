<script setup>
import Chart from 'chart.js/auto'

const chartRef = ref(null)
let chart = null
const props = defineProps({
  data: {
    type: Array,
    required: true,
    default: () => []
  }
})

const updateChart = () => {
  if (!chartRef.value) return

  const ctx = chartRef.value.getContext('2d')
  const labels = props.data.map(item => `${item.month}/${item.year}`)
  const totals = props.data.map(item => item.total)

  // Si le graphique existe déjà, le mettre à jour
  if (chart) {
    chart.data.labels = labels
    chart.data.datasets[0].data = totals
    chart.update()
    return
  }

  chart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: 'Total passagers',
        data: totals,
        borderColor: "#1C2222",
        tension: 0.4,
        fill: true
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      plugins: {
        legend: {
          display: true,
          position: 'top'
        }
      },
      scales: {
        x: {
          grid: {
            display: false
          }
        },
        y: {
          beginAtZero: true,
          ticks: {
            callback: function(value) {
              return new Intl.NumberFormat('fr-FR').format(value)
            }
          },
          grid: {
            display: false
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