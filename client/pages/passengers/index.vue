<script setup lang="ts">
const nuxtApp = useNuxtApp()
const selectedCountry = ref('FRA')

const { data : passengersTotalsWorld } = await useAsyncData(
    `passengers-totals-world`,
    () => $fetch('/api/passengers/passengers-totals-world'), {
        getCachedData: key => nuxtApp?.payload?.data[key] || null
    }
)

const countriesTotal = Object.values(passengersTotalsWorld.value)[0]

const passengersTotalsWorldData = Object.values(passengersTotalsWorld.value)
    .filter((_, index) => index !== 0)

const passengersTotalsWorldLabel = Object.keys(passengersTotalsWorld.value)
    .filter(label => label !== 'countries')

const { data: passengersCountryData } = await useAsyncData(
    'passengers-country-by-iso3',
    () => $fetch(`/api/passengers/passengers-country-by-iso3/${selectedCountry.value}`), {
        getCachedData: key => nuxtApp?.payload?.data[key] || null
    }
)

const countryData = computed(() => Object.values(passengersCountryData.value)[1])

const updateCountry = async (newCountry: string) => {
  selectedCountry.value = newCountry
  await refreshNuxtData('passengers-country-by-iso3')
}
</script>

<template>
    <div class="bg-background border-t w-full h-full overflow-y-auto">
        <header class="flex gap-2 items-center p-6">
            <h2 class="font-semibold text-6xl">Passengers</h2>
        </header>
        <div class="grid grid-cols-3 auto-rows-auto gap-6 px-6">
            <div class="col-span-2 bg-card rounded-xl p-6 relative flex flex-col justify-end items-center h-60">
                <p class="text-8xl font-semibold tracking-tight text-primary absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2">{{ countriesTotal }}</p>
                <p class="text-2xl font-medium text-center mt-24">Pays</p>
            </div>

            <div class="bg-card rounded-xl p-6 relative flex flex-col justify-end items-center h-60">
                <p class="text-8xl font-semibold tracking-tight text-primary absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2">25</p>
                <p class="text-2xl font-medium text-center mt-24">Milliard de voyageur</p>
            </div>

            <div class="col-span-3 bg-card rounded-xl p-6 h-96">
                <DoughnutChart
                    :data="passengersTotalsWorldData"
                    :labels="passengersTotalsWorldLabel"
                />
            </div>
            <div class="col-span-3 bg-card rounded-xl p-6">
                <div class="mb-4">
                    <CountrySelect 
                        :selected="selectedCountry"
                        @update="updateCountry"
                    />
                </div>
                <div class="h-[500px]">
                    <CountryISO3LineChart :data="countryData" />
                </div>
            </div>
        </div>
    </div>
</template>