<script setup>

    const nuxtApp = useNuxtApp()

    const { data: holidaysMonthly } = await useAsyncData(
        `holidays-month`,
        () => $fetch('/api/holidays/month'), {
            getCachedData: key => nuxtApp?.payload?.data[key] || null
        }
    )

    const { data: passagersMonthly } = await useAsyncData(
        `passengers-date`,
        () => $fetch('/api/passengers/date'), {
            getCachedData: key => nuxtApp?.payload?.data[key] || null
        }
    )

</script>

<template>
    <div class="space-y-20">
        <div class="space-y-5">
            <p class="text-xl">Nombre de jours fériés dans le monde entier de Janvier 2010 à Novembre 2019</p>
            <LineChart
                :data="Object.values(holidaysMonthly)"
                :labels="Object.keys(holidaysMonthly)"
            />
        </div>
    
        <div class="space-y-5">
            <p class="text-xl">Nombre de passagers dans le monde entier de Janvier 2010 à Novembre 2019</p>
            <LineChart
                :data="Object.values(passagersMonthly)"
                :labels="Object.keys(passagersMonthly)"
            />
        </div>
    </div>
</template>
