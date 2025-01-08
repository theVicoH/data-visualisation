<script setup lang="ts">
import { PanelRightClose, PanelRightOpen } from 'lucide-vue-next'
import { useSidebarStore } from '~/stores/sidebar'
const sidebarStore = useSidebarStore()
</script>

<template>
    <div class="flex min-h-screen">
        <Sidebar 
            class="p-4 transition-all duration-300 ease-in-out" 
            :class="{ 
                'w-56': sidebarStore.isOpen, 
                'w-16': !sidebarStore.isOpen 
            }"
            style="transition-delay: 50ms;"
        >
            <SideBarHeader class="flex justify-between items-center">
                <div class="flex-1 overflow-hidden">
                    <h1 
                        class="text-xl font-bold transition-all duration-200 ease-in-out transform"
                        :class="{ 
                            'opacity-0 -translate-x-full': !sidebarStore.isOpen, 
                            'opacity-100 translate-x-0': sidebarStore.isOpen 
                        }"
                        style="transition-delay: 100ms;"
                    >
                        Mon App
                    </h1>
                </div>
                <Button 
                    variant="ghost" 
                    size="icon"
                    class="flex-shrink-0"
                    @click="sidebarStore.toggle()"
                >
                    <PanelRightClose 
                        v-if="sidebarStore.isOpen" 
                        class="!w-5 !h-5"
                    />
                    <PanelRightOpen 
                        v-else 
                        class="!w-5 !h-5"
                    />
                </Button>
            </SideBarHeader>
            <SidebarContent class="mt-4 overflow-hidden">
                <div class="space-y-2">
                    <NuxtLink 
                        to="/"
                        active-class=""
                        class="flex items-center space-x-2 transition-all duration-200 ease-in-out transform"
                        :class="{ 
                            'opacity-0 -translate-x-full': !sidebarStore.isOpen, 
                            'opacity-100 translate-x-0': sidebarStore.isOpen 
                        }"
                        style="transition-delay: 150ms;"
                    >
                        <span>Accueil</span>
                    </NuxtLink>
                    <NuxtLink 
                        to="/about" 
                        active-class=""
                        class="flex items-center space-x-2 transition-all duration-200 ease-in-out transform"
                        :class="{ 
                            'opacity-0 -translate-x-full': !sidebarStore.isOpen, 
                            'opacity-100 translate-x-0': sidebarStore.isOpen 
                        }"
                        style="transition-delay: 200ms;"
                    >
                        <span>À propos</span>
                    </NuxtLink>
                    <NuxtLink 
                        to="/contact" 
                        active-class=""
                        class="flex items-center space-x-2 transition-all duration-200 ease-in-out transform"
                        :class="{ 
                            'opacity-0 -translate-x-full': !sidebarStore.isOpen, 
                            'opacity-100 translate-x-0': sidebarStore.isOpen 
                        }"
                        style="transition-delay: 250ms;"
                    >
                        <span>Contact</span>
                    </NuxtLink>
                </div>
            </SidebarContent>
            <SidebarFooter class="overflow-hidden">
                <span 
                    class="transition-all duration-200 ease-in-out transform block"
                    :class="{ 
                        'opacity-0 -translate-x-full': !sidebarStore.isOpen, 
                        'opacity-100 translate-x-0': sidebarStore.isOpen 
                    }"
                    style="transition-delay: 300ms;"
                >
                    Salut
                </span>
            </SidebarFooter>
        </Sidebar>
        <main class="flex-1 p-4">
            <slot />
        </main>
    </div>
</template>

<style scoped>
.overflow-hidden {
    overflow: hidden;
}
</style>