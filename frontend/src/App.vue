<script setup lang="ts">
import { onMounted } from 'vue'

import AnalyticsCards from './components/AnalyticsCards.vue'
import InvitationForm from './components/InvitationForm.vue'
import ReferralsList from './components/ReferralsList.vue'
import { useReferralsStore } from './stores/referrals'

const store = useReferralsStore()

onMounted(() => {
  void store.loadDashboard()
})
</script>

<template>
  <div class="container mx-auto max-w-7xl px-4 py-8">
      <header class="mb-8">
        <h1 class="font-serif text-4xl text-gray-primary md:text-5xl">
          Member Referral Dashboard
        </h1>
        <p class="mt-2 text-gray-secondary">
          Invite members, track referrals, and monitor conversion.
        </p>
      </header>

      <div class="space-y-8">
        <AnalyticsCards />

        <div class="grid grid-cols-1 gap-8 lg:grid-cols-3">
          <div class="lg:col-span-1">
            <InvitationForm />
          </div>
          <div class="lg:col-span-2">
            <ReferralsList />
          </div>
        </div>
      </div>
    </div>
</template>
