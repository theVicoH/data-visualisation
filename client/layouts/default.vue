<script setup lang="ts">
import { PanelRightClose, PanelRightOpen, House, Smile, Caravan, Plane } from 'lucide-vue-next'
import { useSidebarStore } from '~/stores/sidebar'
const sidebarStore = useSidebarStore()
</script>

<template>
    <div class="flex min-h-screen">
        <Sidebar 
            class="p-4" 
            :class="{ 
                'w-56': sidebarStore.isOpen, 
                'w-18': !sidebarStore.isOpen 
            }"
        >
            <SideBarHeader class="flex justify-between items-center" :class="{ 
                    'flex-col space-y-4': !sidebarStore.isOpen
                }">
                <div class="flex-1">
                    <h1
                        class="text-xl font-bold whitespace-nowrap overflow-hidden text-ellipsis"
                        :class="{ 
                            'hidden': !sidebarStore.isOpen
                        }"
                    >
                        Mon App
                    </h1>
                    <h1
                        class="text-xl font-bold whitespace-nowrap overflow-hidden text-ellipsis"
                        :class="{ 
                            'hidden': sidebarStore.isOpen
                        }"
                    >
                        F.
                    </h1>
                </div>
                <Button 
                    variant="ghost" 
                    size="icon"
                    class="flex-shrink-0"
                    @click="sidebarStore.toggle()"
                >
                    <PanelRightOpen
                        v-if="sidebarStore.isOpen" 
                        class="!w-5 !h-5"
                    />
                    <PanelRightClose 
                        v-else 
                        class="!w-5 !h-5"
                    />
                </Button>
            </SideBarHeader>
            <SidebarContent class="mt-4 space-y-2" :class="{ 
                    'w-9': !sidebarStore.isOpen
                }">
                <NuxtLink 
                    v-if="sidebarStore.isOpen"
                    to="/" 
                    active-class="bg-muted"
                    class="px-2 py-2 rounded-lg flex items-center space-x-2 whitespace-nowrap text-ellipsis"
                >
                    <House class="w-4 h-4" />
                    <span>Accueil</span>
                </NuxtLink>
                <NuxtLink 
                    v-else
                    to="/" 
                    active-class="bg-muted"
                    class="w-9 h-9 rounded-lg flex items-center justify-center"
                >
                    <House class="w-5 h-5" />
                </NuxtLink>

                <NuxtLink 
                    v-if="sidebarStore.isOpen"
                    to="/holidays"
                    active-class="bg-muted"
                    class="px-2 py-2 rounded-lg flex items-center space-x-2 whitespace-nowrap text-ellipsis"
                >
                    <Caravan class="w-4 h-4" />
                    <span>Holidays</span>
                </NuxtLink>
                <NuxtLink 
                    v-else
                    to="/holidays"
                    active-class="bg-muted"
                    class="w-9 h-9 rounded-lg flex items-center justify-center"
                >
                    <Caravan class="w-5 h-5" />
                </NuxtLink>

                <NuxtLink 
                    v-if="sidebarStore.isOpen"
                    to="/passengers" 
                    active-class="bg-muted"
                    class="px-2 py-2 rounded-lg flex items-center space-x-2 whitespace-nowrap text-ellipsis"
                >   
                    <Plane class="w-4 h-4" />
                    <span>Passengers</span>
                </NuxtLink>
                <NuxtLink 
                    v-else
                    to="/passengers" 
                    active-class="bg-muted"
                    class="w-9 h-9 rounded-lg flex items-center justify-center"
                >   
                    <Plane class="w-5 h-5" />
                </NuxtLink>
            </SidebarContent>
            <SidebarFooter class="overflow-hidden">
                <span 
                    class="block text-sm text-muted-foreground"
                    :class="{ 
                        'hidden': !sidebarStore.isOpen
                    }"
                >
                    @ 2025 Mon App
                </span>
            </SidebarFooter>
        </Sidebar>
        <main class="flex-1 p-4">
            <slot />
        </main>
    </div>
</template>