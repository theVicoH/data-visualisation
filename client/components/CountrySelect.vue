<script setup lang="ts">
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'

const props = defineProps<{
  selected: string;
}>()

const emit = defineEmits(['update'])

const countries = [
  "ALB", "ARE", "ARG", "ARM", "AUS", "AUT", "BEL", "BGR", "BHR", "BIH", "BLR", "BRA", "BRB",
  "CAN", "CHE", "CHL", "CHN", "COL", "CRI", "CYM", "CYP", "CZE", "DEU", "DNK", "DOM", "ECU",
  "EGY", "ESP", "EST", "FIN", "FRA", "FRO", "GBR", "GEO", "GIB", "GLP", "GRC", "GTM", "HKG",
  "HRV", "HUN", "IND", "IRL", "ISL", "ISR", "ITA", "JAM", "JPN", "KHM", "KOR", "KOS", "LCA",
  "LTU", "LUX", "LVA", "MAC", "MAR", "MDA", "MEX", "MKD", "MLT", "MNE", "MTQ", "MYS", "NGA",
  "NLD", "NOR", "NZL", "OMN", "PAN", "PER", "PHL", "POL", "PRT", "PRY", "ROU", "RUS", "SGP",
  "SLV", "SRB", "SVK", "SVN", "SWE", "THA", "TUR", "TWN", "UKR", "URY", "USA", "ZAF"
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
      <SelectItem v-for="country in countries" :key="country" :value="country">
        {{ country }}
      </SelectItem>
    </SelectContent>
  </Select>
</template>