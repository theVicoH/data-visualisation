<script setup>

    const nuxtApp = useNuxtApp()

    const { data: holidaysTypeByPassengers } = await useAsyncData(
        `holidays-type-by-passengers`,
        () => $fetch('/api/holidays-and-passengers/holidays-type-by-passengers'), {
            getCachedData: key => nuxtApp?.payload?.data[key] || null
        }
    )

    const holidaysTypeByPassengersData = Object.values(holidaysTypeByPassengers.value)
    
    const holidaysTypeByPassengersLabels = Object.keys(holidaysTypeByPassengers.value)

</script>

<template>
    <BarChart
        :data="holidaysTypeByPassengersData"
        :labels="holidaysTypeByPassengersLabels"
        :datasets-label="['Nombre de passagers']"
    />
</template>
