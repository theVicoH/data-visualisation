<script setup lang="ts">
const props = defineProps({
  countryTotals: {
    type: Object,
    required: true
  }
})

const transformData = () => {
  const labels = Object.keys(props.countryTotals)
  const values = Object.values(props.countryTotals)
  
  const sortedIndices = values.map((_, idx) => idx)
    .sort((a, b) => values[b] - values[a])
  
  return {
    labels: sortedIndices.map(idx => labels[idx]),
    values: sortedIndices.map(idx => values[idx])
  }
}

const chartData = computed(() => {
  const { labels, values } = transformData()
  return {
    labels,
    data: values
  }
})
</script>

<template>
  <div class="h-[500px]">
    <BarChart 
      :labels="chartData.labels"
      :data="chartData.data"
    />
  </div>
</template>