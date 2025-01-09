<script setup>

    const nuxtApp = useNuxtApp()

    const { data : holidaysTotalWorld } = await useAsyncData(
        `holidays-totals-world`,
        () => $fetch('/api/holidays/total'), {
            getCachedData: key => nuxtApp?.payload?.data[key] || null
        }
    )

    const { data : passengersTotalsWorld } = await useAsyncData(
        `passengers-totals-world`,
        () => $fetch('/api/passengers/passengers-totals-world'), {
            getCachedData: key => nuxtApp?.payload?.data[key] || null
        }
    )

    const holidaysRepartitionType = ref(null)

    const selectedCountryRepartitionType = ref('World')
    const fetchHolidayData = async (country) => {
        try {
            const { data } = await useAsyncData(
                `holidays-repartition-by-type-${country}`,
                () => $fetch('/api/holidays/repartition-by-type', {
                    query: country !== 'World' ? { country } : undefined
                }, {
                    getCachedData: key => nuxtApp?.payload?.data[key] || null
                })
            )
            holidaysRepartitionType.value = data.value
        } catch (error) {
            holidaysRepartitionType.value = null
        }
    }

    await fetchHolidayData(selectedCountryRepartitionType.value)

    const updateSelectedCountryRepartitionType = async (newCountry) => {
        selectedCountryRepartitionType.value = newCountry
        await fetchHolidayData(newCountry)
    }

    watch(selectedCountryRepartitionType, async (newCountry) => {
        await fetchHolidayData(newCountry)
    })

    const holidaysCountries = ref(null)

    const selectedHolidayTypeHolidaysCountries = ref('All')
    const fetchHolidayCountriesData = async (holidayType) => {
        try {
            const { data } = await useAsyncData(
                `holidays-by-countries-${holidayType}`,
                () => $fetch('/api/holidays/holidays-by-countries', {
                    query: holidayType !== 'All' ? { holidayType } : undefined
                }, {
                    getCachedData: key => nuxtApp?.payload?.data[key] || null
                })
            )
            holidaysCountries.value = data.value
        } catch (error) {
            holidaysCountries.value = null
        }
    }

    await fetchHolidayCountriesData(selectedHolidayTypeHolidaysCountries.value)

    const updateSelectedHolidayTypeHolidaysCountries = async (newType) => {
        selectedHolidayTypeHolidaysCountries.value = newType
        await fetchHolidayCountriesData(newType)
    }

    watch(selectedHolidayTypeHolidaysCountries, async (newType) => {
        await fetchHolidayCountriesData(newType)
    })

    const holidaysByYear = ref(null)

    const selectedCountryHolidaysByYear = ref('World')
    const fetchHolidaysByYearData = async (country) => {
        try {
            const { data } = await useAsyncData(
                `holiday-by-year-${country}`,
                () => $fetch('/api/holidays/year', {
                    query: country !== 'World' ? { country } : undefined
                }, {
                    getCachedData: key => nuxtApp?.payload?.data[key] || null
                })
            )
            holidaysByYear.value = data.value
        } catch (error) {
            holidaysByYear.value = null
        }
    }

    await fetchHolidaysByYearData(selectedCountryHolidaysByYear.value)

    const updateSelectedCountryHolidaysByYear = async (newCountry) => {
        selectedCountryHolidaysByYear.value = newCountry
        await fetchHolidaysByYearData(newCountry)
    }

    watch(selectedCountryHolidaysByYear, async (newCountry) => {
        await fetchHolidaysByYearData(newCountry)
    })

    const holidaysMinMax = ref(null)

    const selectedHolidayTypeHolidaysMinMax = ref('All')
    const fetchHolidaysMinMaxData = async (holidayType) => {
        try {
            const { data } = await useAsyncData(
                `holiday-min-max-${holidayType}`,
                () => $fetch('/api/holidays/min-max', {
                    query: holidayType !== 'All' ? { holidayType } : undefined
                }, {
                    getCachedData: key => nuxtApp?.payload?.data[key] || null
                })
            )
            holidaysMinMax.value = data.value
        } catch (error) {
            holidaysMinMax.value = null
        }
    }

    await fetchHolidaysMinMaxData(selectedHolidayTypeHolidaysMinMax.value)

    const updateSelectedHolidayTypeHolidaysMinMax = async (newHolidayType) => {
        selectedHolidayTypeHolidaysMinMax.value = newHolidayType
        await fetchHolidaysMinMaxData(newHolidayType)
    }

    watch(selectedHolidayTypeHolidaysMinMax, async (newHolidayType) => {
        await fetchHolidaysMinMaxData(newHolidayType)
    })
    
    const countriesTotal = Object.values(passengersTotalsWorld.value)[0]

</script>

<template>
    <div class="bg-background border-t w-full h-full overflow-y-auto">
        <header class="flex gap-2 items-center p-6">
            <h2 class="font-semibold text-6xl">Holidays</h2>
        </header>
        <div class="grid grid-cols-3 auto-rows-auto gap-6 px-6">
            <div class="col-span-2 bg-card rounded-xl p-6 relative flex flex-col justify-end items-center h-60">
                <p class="text-8xl font-semibold tracking-tight text-primary absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2">{{ countriesTotal }}</p>
                <p class="text-2xl font-medium text-center mt-24">Pays</p>
            </div>

            <div class="col-span-1 bg-card rounded-xl p-6 relative flex flex-col justify-end items-center h-60">
                <p class="text-8xl font-semibold tracking-tight text-primary absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2">{{ holidaysTotalWorld.total }}</p>
                <p class="text-2xl font-medium text-center mt-24">Jours fériés</p>
            </div>

            <div class="col-span-3 bg-card rounded-xl p-6 h-96 flex justify-center relative">
                <div class="absolute left-6">
                    <CountryFullNameSelect
                        :selected="selectedCountryRepartitionType"
                        @update="updateSelectedCountryRepartitionType"
                    />
                </div>

                <DoughnutChart
                    :data="Object.values(holidaysRepartitionType)"
                    :labels="Object.keys(holidaysRepartitionType)"
                />
            </div>

            <div class="col-span-3 bg-card rounded-xl p-6">
                <div class="mb-4">
                    <HolidayTypeSelect
                        :selected="selectedHolidayTypeHolidaysMinMax"
                        @update="updateSelectedHolidayTypeHolidaysMinMax"
                    />
                </div>
                <div class="flex justify-between w-full">
                    <div>
                        <p class="text-5xl uppercase">max</p>
                        <div class="flex gap-4 items-center">
                            <div class="size-4 bg-green-500 rounded-full"></div>
                            <p><span class="text-2xl">{{ holidaysMinMax.max.country }}</span> with <span class="text-2xl">{{ holidaysMinMax.max.data }}</span> holidays</p>
                        </div>
                    </div>

                    <div>
                        <p class="text-5xl uppercase">min</p>
                        <div class="flex gap-4 items-center">
                            <div class="size-4 bg-red-500 rounded-full"></div>
                            <p><span class="text-2xl">{{ holidaysMinMax.min.country }}</span> with only <span class="text-2xl">{{ holidaysMinMax.min.data }}</span> holidays</p>
                        </div>
                    </div>
                </div>
            </div>

            <div class="col-span-3 bg-card rounded-xl p-6">
                <div class="mb-4">
                    <CountryFullNameSelect
                        :selected="selectedCountryHolidaysByYear"
                        @update="updateSelectedCountryHolidaysByYear"
                    />
                </div>

                <BarChart
                    :data="Object.values(holidaysByYear)"
                    :labels="Object.keys(holidaysByYear)"
                    :datasets-label="['Nombre de jours fériés']"
                />
            </div>

            <div class="col-span-3 bg-card rounded-xl p-6">
                <div class="mb-4">
                    <HolidayTypeSelect
                        :selected="selectedHolidayTypeHolidaysCountries"
                        @update="updateSelectedHolidayTypeHolidaysCountries"
                    />
                </div>

                <BarChart
                    :data="Object.values(holidaysCountries)"
                    :labels="Object.keys(holidaysCountries)"
                    :datasets-label="['Nombre de jours fériés']"
                />
            </div>
        </div>
    </div>
</template>
