<script setup lang="ts">

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

    const { data: holidaysTypeByPassengers } = await useAsyncData(
        `holidays-type-by-passengers`,
        () => $fetch('/api/holidays-and-passengers/holidays-type-by-passengers'), {
            getCachedData: key => nuxtApp?.payload?.data[key] || null
        }
    )

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

    const fetchAllData = async () => {
        const promises = countries.value.map(async (iso3) => {
            const [holidaysResponse, passengersResponse] = await Promise.all([
                useAsyncData(
                    `holidays-by-country-${iso3}`,
                    () => $fetch('/api/holidays/holidays-by-country', {
                        query: { iso3 }
                    }), {
                        transform: (data) => {
                            return data.data
                        },
                        getCachedData: key => nuxtApp?.payload?.data[key] || null
                    }
                ),
                useAsyncData(
                    `passengers-by-country-${iso3}`,
                    () => $fetch('/api/passengers/passengers-by-country', {
                        query: { iso3 }
                    }), {
                        transform: (data) => {
                            const totals = data["monthly_data"].reduce((acc, curr) => {
                                acc.domestic += curr.domestic
                                acc.international += curr.international
                                acc.total += curr.total
                                return acc
                            }, { domestic: 0, international: 0, total: 0 })
                            return {
                                domesticTotal: totals.domestic,
                                internationalTotal: totals.international,
                                overallTotal: totals.total,
                            }
                        },
                        getCachedData: key => nuxtApp?.payload?.data[key] || null
                    }
                )
            ])

            return {
                holidays: holidaysResponse.data.value,
                domestic: passengersResponse.data.value.domesticTotal,
                international: passengersResponse.data.value.internationalTotal,
                overall: passengersResponse.data.value.overallTotal
            }
        })

        const results = await Promise.all(promises)
        
        return [
            results.map(r => r.holidays),
            results.map(r => r.domestic),
            results.map(r => r.international),
            results.map(r => r.overall)
        ]
    }

    const countriesTotal = Object.values(passengersTotalsWorld.value)[0]

    const datasetsLabel = [
        'Nombre de jours fériés',
        'Nombre de passagers domestiques',
        'Nombre de passagers internationaux',
        'Nombre de passagers totaux'
    ]

    const holidaysTypeByPassengersData = Object.values(holidaysTypeByPassengers.value)
    
    const holidaysTypeByPassengersLabels = Object.keys(holidaysTypeByPassengers.value)

    const countries = ref([
        "ALB", "ARE", "ARG", "ARM", "AUS", "AUT", "BEL", "BGR", "BHR", "BIH", "BLR", "BRA", "BRB",
        "CAN", "CHE", "CHL", "CHN", "COL", "CRI", "CYM", "CYP", "CZE", "DEU", "DNK", "DOM", "ECU",
        "EGY", "ESP", "EST", "FIN", "FRA", "FRO", "GBR", "GEO", "GIB", "GLP", "GRC", "GTM", "HKG",
        "HRV", "HUN", "IND", "IRL", "ISL", "ISR", "ITA", "JAM", "JPN", "KHM", "KOR", "KOS", "LCA",
        "LTU", "LUX", "LVA", "MAC", "MAR", "MDA", "MEX", "MKD", "MLT", "MNE", "MTQ", "MYS", "NGA",
        "NLD", "NOR", "NZL", "OMN", "PAN", "PER", "PHL", "POL", "PRT", "PRY", "ROU", "RUS", "SGP",
        "SLV", "SRB", "SVK", "SVN", "SWE", "THA", "TUR", "TWN", "UKR", "URY", "USA", "ZAF"
    ])

    const allData = await fetchAllData()

</script>

<template>
    <div class="bg-background border-t w-full h-full overflow-y-auto">
        <header class="flex gap-2 items-center p-6">
            <h2 class="font-semibold text-6xl">Holidays & Passengers</h2>
        </header>
        <div class="grid grid-cols-3 auto-rows-auto gap-6 px-6">
            <div class="col-span-1 bg-card rounded-xl p-6 relative flex flex-col justify-end items-center h-60">
                <p class="text-8xl font-semibold tracking-tight text-primary absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2">{{ countriesTotal }}</p>
                <p class="text-2xl font-medium text-center mt-24">Pays</p>
            </div>

            <div class="col-span-1 bg-card rounded-xl p-6 relative flex flex-col justify-end items-center h-60">
                <p class="text-8xl font-semibold tracking-tight text-primary absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2">{{ holidaysTotalWorld.total }}</p>
                <p class="text-2xl font-medium text-center mt-24">Jours fériés</p>
            </div>

            <div class="bg-card rounded-xl p-6 relative flex flex-col justify-end items-center h-60">
                <p class="text-8xl font-semibold tracking-tight text-primary absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2">25</p>
                <p class="text-2xl font-medium text-center mt-24">Milliard de voyageur</p>
            </div>

            <div class="col-span-3 bg-card rounded-xl p-6">
                <BarChart
                    :data="holidaysTypeByPassengersData"
                    :labels="holidaysTypeByPassengersLabels"
                    :datasets-label="['Nombre de passagers']"
                />
            </div>

            <div class="col-span-3 bg-card rounded-xl p-6">
                <BarChart
                    :data="allData"
                    :labels="countries"
                    :datasets-label="datasetsLabel"
                    stacked-bars
                />
            </div>

            <div class="col-span-3 bg-card rounded-xl p-6">
                <LineChart
                    :data="Object.values(holidaysMonthly)"
                    :labels="Object.keys(holidaysMonthly)"
                    datasets-label="Nombre de jours fériés"
                />
            </div>

            <div class="col-span-3 bg-card rounded-xl p-6">
                <LineChart
                    :data="Object.values(passagersMonthly)"
                    :labels="Object.keys(passagersMonthly)"
                    datasets-label="Nombre de passagers"
                />
            </div>
        </div>
    </div>
</template>
