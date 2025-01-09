export default defineEventHandler(async (event) => {
    const { apiBaseUrl } = useRuntimeConfig(event).public

    try {
        const {
            iso3
        } = getQuery(event)

        if (!iso3) {
            throw createError({
                statusCode: 400,
                message: "iso3 is missing",
            })
        }

        const data = await $fetch(`${apiBaseUrl}/passengers/country/${iso3}`)
        return data
    } catch(err) {
        throw createError({
            statusCode: err?.response?.status,
            message: err?.response?._data?.message || "une erreur est survenue"
        })
    }
})
