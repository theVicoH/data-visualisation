<script setup lang="ts">
  import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
  } from '@/components/ui/select'

  defineProps<{
    selected: string;
  }>()

  const emit = defineEmits(['update'])

  const holidaysTypes = [
    "All",
    "Public holiday",
    "Observance",
    "Local holiday",
    "Local observance",
    "Special holiday",
    "Half-day holiday",
    "Working day (replacement)"
  ]

  const handleSelect = (value: string) => {
    emit('update', value)
  }
</script>

<template>
  <Select :model-value="selected" @update:model-value="handleSelect">
    <SelectTrigger class="w-[180px]">
      <SelectValue>
        {{ selected }}
      </SelectValue>
    </SelectTrigger>
    <SelectContent>
      <SelectItem v-for="type in holidaysTypes" :key="type" :value="type">
        {{ type }}
      </SelectItem>
    </SelectContent>
  </Select>
</template>