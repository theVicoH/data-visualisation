export default defineEventHandler(async (event) => {
    const { apiBaseUrl } = useRuntimeConfig(event).public
    const iso3 = getRouterParam(event, 'iso3')
    try {
        const data = await $fetch(`${apiBaseUrl}/passengers/country/${iso3}`)
        return data
    } catch(err) {
        throw createError({
            statusCode: err?.response?.status,
            message: err?.response?._data?.message || "une erreur est survenue"
        })
    }
})
