<script setup lang="ts">
import { computed } from 'vue'
import { storeToRefs } from 'pinia'

import { useReferralsStore } from '../stores/referrals'

const store = useReferralsStore()
const { analytics, loading } = storeToRefs(store)

const cards = computed(() => [
  {
    label: 'Total Invited',
    value: analytics.value?.total_invited ?? 0,
    hint: 'All referrals created',
  },
  {
    label: 'Invitations Sent',
    value: analytics.value?.invitations_sent ?? 0,
    hint: 'Still pending',
  },
  {
    label: 'Joined',
    value: analytics.value?.joined ?? 0,
    hint: 'Successful conversions',
  },
  {
    label: 'Conversion Rate',
    value: analytics.value ? `${analytics.value.conversion_rate}%` : '0%',
    hint: 'Joined / total invited',
  },
])
</script>

<template>
  <section class="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
    <article
      v-for="card in cards"
      :key="card.label"
      class="rounded-xl border border-dark-border bg-dark-card p-5"
    >
      <p class="text-sm text-gray-secondary">{{ card.label }}</p>
      <p class="mt-2 font-serif text-3xl text-gray-primary">
        <span v-if="loading" class="text-gray-tertiary">—</span>
        <span v-else>{{ card.value }}</span>
      </p>
      <p class="mt-1 text-xs text-gray-tertiary">{{ card.hint }}</p>
    </article>
  </section>
</template>
