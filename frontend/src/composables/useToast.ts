import { ref } from 'vue'

import { TOAST_DURATION_MS } from '../constants/referral'

const message = ref<string | null>(null)
let dismissTimer: ReturnType<typeof setTimeout> | undefined

/** Show a temporary success toast that auto-dismisses. */
export function showToast(text: string, durationMs = TOAST_DURATION_MS): void {
  if (dismissTimer) {
    clearTimeout(dismissTimer)
  }

  message.value = text
  dismissTimer = setTimeout(() => {
    message.value = null
    dismissTimer = undefined
  }, durationMs)
}

export function dismissToast(): void {
  if (dismissTimer) {
    clearTimeout(dismissTimer)
    dismissTimer = undefined
  }
  message.value = null
}

export function useToast() {
  return { message, showToast, dismissToast }
}
