<script setup lang="ts">

    import { VisXYContainer, VisLine, VisAxis } from '@unovis/vue'

    type DataRecord = { x: number, y: number }

    const data = ref<DataRecord[]>([
        { x: 0, y: 0 },
        { x: 1, y: 2 },
        { x: 2, y: 1 },
    ])

    const { apiBaseUrl } = useRuntimeConfig().public

</script>

<template>
    <h1>{{ apiBaseUrl }}</h1>

    <div class="bg-blue-400/80 space-x-10">
        <Button>Click me</Button>
        <Button variant="destructive">Click me</Button>
    </div>

    <VisXYContainer>
        <VisLine :data="data" :x="(d: DataRecord) => d.x" :y="(d: DataRecord) => d.y" />
        <VisAxis type="x" />
        <VisAxis type="y" />
    </VisXYContainer>
</template>
