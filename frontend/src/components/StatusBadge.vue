<script setup lang="ts">
import type { ReferralStatus } from '../types/referral'

defineProps<{
  status: ReferralStatus
}>()

const statusConfig: Record<
  ReferralStatus,
  { label: string; className: string }
> = {
  invitation_sent: {
    label: 'Invitation Sent',
    className: 'bg-gray-600/30 text-gray-secondary border-gray-600/50',
  },
  application_received: {
    label: 'Application Received',
    className: 'bg-blue-500/20 text-blue-300 border-blue-500/40',
  },
  joined: {
    label: 'Joined',
    className: 'bg-success/20 text-success-light border-success/40',
  },
  declined: {
    label: 'Declined',
    className: 'bg-red-500/20 text-red-300 border-red-500/40',
  },
}
</script>

<template>
  <span
    class="inline-flex items-center rounded-full border px-3 py-1 text-xs font-medium"
    :class="statusConfig[status].className"
  >
    {{ statusConfig[status].label }}
  </span>
</template>
