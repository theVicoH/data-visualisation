<script setup lang="ts">

    const { apiBaseUrl } = useRuntimeConfig().public

</script>

<template>
    <h1>{{ apiBaseUrl }}</h1>

    <div class="bg-blue-400/80 space-x-10">
        <Button>Click me</Button>
        <Button variant="destructive">Click me</Button>
    </div>
</template>
