import { defineStore } from 'pinia'
import { ref } from 'vue'

import {
  createReferral as createReferralRequest,
  fetchAnalytics as fetchAnalyticsRequest,
  fetchReferrals as fetchReferralsRequest,
  getErrorMessage,
  resendReferral as resendReferralRequest,
} from '../api/referrals'
import { showToast } from '../composables/useToast'
import type { Analytics, CreateReferralPayload, Referral } from '../types/referral'

export const useReferralsStore = defineStore('referrals', () => {
  const referrals = ref<Referral[]>([])
  const analytics = ref<Analytics | null>(null)
  const loading = ref(false)
  const submitting = ref(false)
  const resendingId = ref<number | null>(null)
  const resendErrors = ref<Record<number, string>>({})

  async function loadDashboard(): Promise<void> {
    loading.value = true
    try {
      const [referralsData, analyticsData] = await Promise.all([
        fetchReferralsRequest(),
        fetchAnalyticsRequest(),
      ])
      referrals.value = referralsData
      analytics.value = analyticsData
    } finally {
      loading.value = false
    }
  }

  async function refreshDashboard(): Promise<void> {
    const [referralsData, analyticsData] = await Promise.all([
      fetchReferralsRequest(),
      fetchAnalyticsRequest(),
    ])
    referrals.value = referralsData
    analytics.value = analyticsData
  }

  async function createReferral(payload: CreateReferralPayload): Promise<string | null> {
    submitting.value = true
    try {
      await createReferralRequest(payload)
      await refreshDashboard()
      showToast('Invitation sent successfully.')
      return null
    } catch (error) {
      return getErrorMessage(error, 'Unable to send invitation.')
    } finally {
      submitting.value = false
    }
  }

  async function resendReferral(id: number): Promise<void> {
    resendingId.value = id
    const { [id]: _, ...remainingErrors } = resendErrors.value
    resendErrors.value = remainingErrors

    try {
      const updated = await resendReferralRequest(id)
      referrals.value = referrals.value.map((referral) =>
        referral.id === id ? updated : referral,
      )
      analytics.value = await fetchAnalyticsRequest()
      showToast('Invitation resent successfully.')
    } catch (error) {
      resendErrors.value = {
        ...resendErrors.value,
        [id]: getErrorMessage(error, 'Unable to resend invitation.'),
      }
    } finally {
      resendingId.value = null
    }
  }

  return {
    referrals,
    analytics,
    loading,
    submitting,
    resendingId,
    resendErrors,
    loadDashboard,
    createReferral,
    resendReferral,
  }
})
