<script setup lang="ts">
import { useToast } from '../composables/useToast'

const { message, dismissToast } = useToast()
</script>

<template>
  <Transition
    enter-active-class="transition duration-200 ease-out"
    enter-from-class="translate-y-2 opacity-0"
    enter-to-class="translate-y-0 opacity-100"
    leave-active-class="transition duration-150 ease-in"
    leave-from-class="translate-y-0 opacity-100"
    leave-to-class="translate-y-2 opacity-0"
  >
    <div
      v-if="message"
      role="status"
      class="fixed bottom-6 right-6 z-50 flex max-w-sm items-start gap-3 rounded-lg border border-success/40 bg-dark-card px-4 py-3 shadow-lg"
    >
      <span class="mt-0.5 text-success-light" aria-hidden="true">✓</span>
      <p class="flex-1 text-sm text-gray-primary">{{ message }}</p>
      <button
        type="button"
        class="text-gray-tertiary transition hover:text-gray-secondary"
        aria-label="Dismiss notification"
        @click="dismissToast"
      >
        ×
      </button>
    </div>
  </Transition>
</template>
