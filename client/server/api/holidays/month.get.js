export default defineEventHandler(async (event) => {
    const { apiBaseUrl } = useRuntimeConfig(event).public

    try {
        const data = await $fetch(`${apiBaseUrl}/holidays/month`)
        return data
    } catch(err) {
        throw createError({
            statusCode: err?.response?.status,
            message: err?.response?._data?.message || "une erreur est survenue"
        })
    }
})
