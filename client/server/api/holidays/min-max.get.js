export default defineEventHandler(async (event) => {
    const { apiBaseUrl } = useRuntimeConfig(event).public
    const { holidayType } = getQuery(event)

    try {
        const url = `${apiBaseUrl}/holidays/min-max`
        const query = holidayType ? { 'holiday-type': holidayType } : undefined

        const data = await $fetch(url, { query })
        
        if (!data || typeof data !== 'object') {
            throw createError({
                statusCode: 500,
                message: "Format de données invalide"
            })
        }
        
        return data
    } catch(err) {
        throw createError({
            statusCode: err?.response?.status,
            message: err?.response?._data?.message || "une erreur est survenue"
        })
    }
})
