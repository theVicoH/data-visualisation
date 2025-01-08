import { defineStore } from 'pinia'

export const useSidebarStore = defineStore('sidebar', {
  state: () => ({
    isOpen: true
  }),
  actions: {
    toggle() {
      this.isOpen = !this.isOpen
    },
    open() {
      this.isOpen = true
    },
    close() {
      this.isOpen = false
    }
  }
})