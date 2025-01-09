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

  const countries = [
    "World", "Afghanistan", "Albania", "Algeria", "American-samoa", "Andorra", "Angola",
    "Anguilla", "Antigua-and-barbuda", "Argentina", "Armenia", "Aruba", "Australia",
    "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus",
    "Belgium", "Belize", "Benin", "Bermuda", "Bhutan", "Bolivia", "Bosnia", "Botswana",
    "Brazil", "British-virgin-islands", "Brunei", "Bulgaria", "Burkina-faso", "Burundi",
    "Cambodia", "Cameroon", "Canada", "Cape-verde", "Cayman-islands",
    "Central-african-republic", "Chad", "Chile", "China", "Colombia", "Comores",
    "Cook-islands", "Costa-rica", "Croatia", "Cuba", "Curacao", "Cyprus", "Czech",
    "Denmark", "Djibouti", "Dominica", "Dominican-republic", "Dr-congo", "Ecuador",
    "Egypt", "El-salvador", "Eritrea", "Estonia", "Ethiopia", "Falkland-islands",
    "Faroe-islands", "Fiji", "Finland", "France", "French-guiana", "French-polynesia",
    "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Gibraltar", "Greece",
    "Greenland", "Grenada", "Guam", "Guatemala", "Guernsey", "Guinea", "Guinea-bissau",
    "Guineaecuatorial", "Guyana", "Haiti", "Honduras", "Hong-kong", "Hungary",
    "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Isle-of-man",
    "Israel", "Italy", "Ivory-coast", "Jamaica", "Japan", "Jersey", "Jordan",
    "Kazakhstan", "Kenya", "Kiribati", "Kosovo", "Kuwait", "Kyrgyzstan", "Laos",
    "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania",
    "Luxembourg", "Macau", "Macedonia", "Madagascar", "Malawi", "Malaysia", "Maldives",
    "Mali", "Malta", "Marshall-islands", "Martinique", "Mauritania", "Mauritius",
    "Mayotte", "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro",
    "Montserrat", "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal",
    "Netherlands", "New-caledonia", "New-zealand", "Nicaragua", "Niger", "Nigeria",
    "North-korea", "Northern-mariana-islands", "Norway", "Oman", "Pakistan", "Palau",
    "Palestine", "Panama", "Papua-new-guinea", "Paraguay", "Peru", "Philippines",
    "Poland", "Portugal", "Puerto-rico", "Qatar", "Republic-of-the-congo", "Reunion",
    "Romania", "Russia", "Rwanda", "Saint-barthelemy", "Saint-helena",
    "Saint-kitts-and-nevis", "Saint-lucia", "Saint-martin", "Saint-pierre-and-miquelon",
    "Saint-vincent-and-the-grenadines", "Samoa", "San-marino", "Sao-tome-and-principe",
    "Saudi-arabia", "Senegal", "Serbia", "Seychelles", "Sierra-leone", "Singapore",
    "Sint-maarten", "Slovakia", "Slovenia", "Solomon-islands", "Somalia", "South-africa",
    "South-korea", "South-sudan", "Spain", "Sri-lanka", "Sudan", "Suriname",
    "Swaziland", "Sweden", "Switzerland", "Syria", "Taiwan", "Tajikistan", "Tanzania",
    "Thailand", "Timor-leste", "Togo", "Tonga", "Trinidad", "Tunisia", "Turkey",
    "Turkmenistan", "Turks-and-caicos-islands", "Tuvalu", "Uganda", "Uk", "Ukraine",
    "United-arab-emirates", "United-states-virgin-islands", "Uruguay", "Us",
    "Uzbekistan", "Vanuatu", "Vatican-city-state", "Venezuela", "Vietnam",
    "Wallis-and-futuna", "Yemen", "Zambia", "Zimbabwe"
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
