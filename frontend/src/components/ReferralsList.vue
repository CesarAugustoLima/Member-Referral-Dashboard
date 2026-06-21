<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue'
import { storeToRefs } from 'pinia'

import { useReferralsStore } from '../stores/referrals'
import { formatDate, resendCooldownSeconds } from '../utils/format'
import StatusBadge from './StatusBadge.vue'

const store = useReferralsStore()
const { referrals, loading, resendingId, resendErrors } = storeToRefs(store)

const now = ref(Date.now())
let timer: ReturnType<typeof setInterval> | undefined

onMounted(() => {
  timer = setInterval(() => {
    now.value = Date.now()
  }, 1000)
})

onUnmounted(() => {
  if (timer) {
    clearInterval(timer)
  }
})

function cooldownFor(lastSentAt: string): number {
  void now.value
  return resendCooldownSeconds(lastSentAt)
}
</script>

<template>
  <section class="rounded-xl border border-dark-border bg-dark-card p-6">
    <header class="mb-6">
      <h2 class="font-serif text-2xl text-gray-primary">Referrals</h2>
      <p class="mt-1 text-sm text-gray-secondary">
        Track invitation status and resend when needed.
      </p>
    </header>

    <div v-if="loading" class="py-12 text-center text-gray-secondary">
      Loading referrals…
    </div>

    <div
      v-else-if="referrals.length === 0"
      class="flex flex-col items-center py-16 text-center"
    >
      <div class="mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-copper/10 text-2xl text-copper">
        ✉
      </div>
      <h3 class="font-serif text-xl text-gray-primary">No referrals yet</h3>
      <p class="mt-2 max-w-sm text-sm text-gray-secondary">
        Send your first invitation using the form. Referrals will appear here with their status.
      </p>
    </div>

    <div v-else class="overflow-x-auto">
      <table class="min-w-full text-left text-sm">
        <thead>
          <tr class="border-b border-dark-border text-gray-secondary">
            <th class="px-3 py-3 font-medium">Name</th>
            <th class="px-3 py-3 font-medium">Email</th>
            <th class="px-3 py-3 font-medium">Date Referred</th>
            <th class="px-3 py-3 font-medium">Status</th>
            <th class="px-3 py-3 font-medium">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="referral in referrals"
            :key="referral.id"
            class="border-b border-dark-border/60 last:border-b-0"
          >
            <td class="px-3 py-4 text-gray-primary">
              {{ referral.first_name }} {{ referral.last_name }}
            </td>
            <td class="px-3 py-4 text-gray-secondary">{{ referral.email }}</td>
            <td class="px-3 py-4 text-gray-secondary">
              {{ formatDate(referral.created_at) }}
            </td>
            <td class="px-3 py-4">
              <StatusBadge :status="referral.status" />
            </td>
            <td class="px-3 py-4">
              <div v-if="referral.status === 'invitation_sent'" class="space-y-1">
                <button
                  type="button"
                  class="rounded-lg border border-copper/50 px-3 py-1.5 text-xs font-medium text-copper transition hover:bg-copper/10 disabled:cursor-not-allowed disabled:opacity-50"
                  :disabled="resendingId === referral.id || cooldownFor(referral.last_sent_at) > 0"
                  @click="store.resendReferral(referral.id)"
                >
                  <span v-if="resendingId === referral.id">Resending…</span>
                  <span v-else-if="cooldownFor(referral.last_sent_at) > 0">
                    Resend in {{ cooldownFor(referral.last_sent_at) }}s
                  </span>
                  <span v-else>Resend</span>
                </button>
                <p v-if="resendErrors[referral.id]" class="text-xs text-red-400">
                  {{ resendErrors[referral.id] }}
                </p>
              </div>
              <span v-else class="text-xs text-gray-tertiary">—</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>
