<script setup>

    const nuxtApp = useNuxtApp()

    const countries = [
        "ALB", "ARE", "ARG", "ARM", "AUS", "AUT", "BEL", "BGR", "BHR", "BIH", "BLR", "BRA", "BRB",
        "CAN", "CHE", "CHL", "CHN", "COL", "CRI", "CYM", "CYP", "CZE", "DEU", "DNK", "DOM", "ECU",
        "EGY", "ESP", "EST", "FIN", "FRA", "FRO", "GBR", "GEO", "GIB", "GLP", "GRC", "GTM", "HKG",
        "HRV", "HUN", "IND", "IRL", "ISL", "ISR", "ITA", "JAM", "JPN", "KHM", "KOR", "KOS", "LCA",
        "LTU", "LUX", "LVA", "MAC", "MAR", "MDA", "MEX", "MKD", "MLT", "MNE", "MTQ", "MYS", "NGA",
        "NLD", "NOR", "NZL", "OMN", "PAN", "PER", "PHL", "POL", "PRT", "PRY", "ROU", "RUS", "SGP",
        "SLV", "SRB", "SVK", "SVN", "SWE", "THA", "TUR", "TWN", "UKR", "URY", "USA", "ZAF"
    ]

    const fetchAllData = async () => {
        const promises = countries.map(async (iso3) => {
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

    const allData = await fetchAllData()

    const datasetsLabel = [
        'Nombre de jours fériés',
        'Nombre de passagers domestiques',
        'Nombre de passagers internationaux',
        'Nombre de passagers totaux'
    ]

</script>

<template>
    <BarChart
        :data="allData"
        :labels="countries"
        :datasets-label="datasetsLabel"
        stacked-bars
    />
</template>