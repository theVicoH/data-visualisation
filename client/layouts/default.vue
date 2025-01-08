<script setup lang="ts">
import { PanelRightClose, PanelRightOpen, House, Caravan, Plane, HardDrive } from 'lucide-vue-next'
import { useSidebarStore } from '~/stores/sidebar'
const sidebarStore = useSidebarStore()
</script>

<template>
    <div class="flex min-h-screen bg-background text-foreground ">
        <aside 
            class="bg-background shrink-0 px-2 py-4 border-r border-gray-200 dark:border-gray-800 transition-all duration-300 flex flex-col justify-between"
            :class="{ 
                'w-56': sidebarStore.isOpen, 
                'w-[4.5rem]': !sidebarStore.isOpen 
            }"
        >   
            <div>
                <div class="flex justify-between items-center" :class="{ 
                    'flex-col space-y-4 mb-3': !sidebarStore.isOpen,
                    'mb-2': sidebarStore.isOpen
                }">
                    <div class="flex-1">
                        <h1
                            class="ml-2 text-2xl whitespace-nowrap overflow-hidden text-ellipsis font-bold flex flex-col"
                            :class="{ 
                                'hidden': !sidebarStore.isOpen
                            }"
                        >
                            <span>Fly Days</span>
                        </h1>

                        <h1
                            class="text-xl font-bold whitespace-nowrap overflow-hidden text-ellipsis"
                            :class="{ 
                                'hidden': sidebarStore.isOpen
                            }"
                        >
                            FD.
                        </h1>
                    </div>
                    <button 
                        class="flex items-center justify-center w-9 h-9 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800"
                        @click="sidebarStore.toggle()"
                    >
                        <PanelRightOpen
                            v-if="sidebarStore.isOpen" 
                            class="w-5 h-5"
                        />
                        <PanelRightClose 
                            v-else 
                            class="w-5 h-5"
                        />
                    </button>
                </div>
                <NuxtLink 
                    to="https://www.kaggle.com/datasets/umerhaddii/global-holidays-and-travel-data"
                    target="_blank">
                    <Button v-if="sidebarStore.isOpen" class="w-full mb-4">
                        <HardDrive />
                        Dataset
                    </Button>
                </NuxtLink>
                <hr class="mb-3" />
                <nav class="space-y-1" :class="{ 'h-[128px] flex flex-col justify-between': !sidebarStore.isOpen }">
                    <NuxtLink 
                        to="/"
                        active-class="bg-muted"
                        :class="[
                            sidebarStore.isOpen 
                                ? 'px-2 py-2 space-x-2' 
                                : 'w-9 h-9 mx-auto flex items-center justify-center',
                            'rounded-lg flex items-center hover:bg-gray-100 dark:hover:bg-gray-800',
                        ]"
                    >
                        <House 
                            :class="[
                                sidebarStore.isOpen ? 'w-4 h-4' : 'w-5 h-5'
                            ]" 
                        />
                        <span v-if="sidebarStore.isOpen">Accueil</span>
                    </NuxtLink>

                    <NuxtLink 
                        to="/holidays"
                        active-class="bg-muted"
                        :class="[
                            sidebarStore.isOpen 
                                ? 'px-2 py-2 space-x-2' 
                                : 'w-9 h-9 mx-auto flex items-center justify-center',
                            'rounded-lg flex items-center hover:bg-gray-100 dark:hover:bg-gray-800'
                        ]"
                    >
                        <Caravan 
                            :class="[
                                sidebarStore.isOpen ? 'w-4 h-4' : 'w-5 h-5'
                            ]" 
                        />
                        <span v-if="sidebarStore.isOpen">Holidays</span>
                    </NuxtLink>

                    <NuxtLink 
                        to="/passengers"
                        active-class="bg-muted"
                        :class="[
                            sidebarStore.isOpen 
                                ? 'px-2 py-2 space-x-2' 
                                : 'w-9 h-9 mx-auto flex items-center justify-center',
                            'rounded-lg flex items-center hover:bg-gray-100 dark:hover:bg-gray-800',
                        ]"
                    >   
                        <Plane 
                            :class="[
                                sidebarStore.isOpen ? 'w-4 h-4' : 'w-5 h-5'
                            ]" 
                        />
                        <span v-if="sidebarStore.isOpen">Passengers</span>
                    </NuxtLink>
                </nav>
            </div>

          
            <span 
                v-if="sidebarStore.isOpen"
                class="block text-sm text-gray-500 dark:text-gray-400"
            >
                @ 2025 Mon App
            </span>
        </aside>

        <main class="flex-1 overflow-hidden">
            <slot />
        </main>
    </div>
</template>