import axios from 'axios'

import type {
  Analytics,
  ApiErrorBody,
  CreateReferralPayload,
  PaginatedResponse,
  Referral,
} from '../types/referral'

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

const BASE_PATH = '/referrals'

/** Extract a user-facing message from an API error response. */
export function getErrorMessage(
  error: unknown,
  fallback = 'Something went wrong. Please try again.',
): string {
  if (!axios.isAxiosError(error)) {
    return fallback
  }

  const data = error.response?.data as ApiErrorBody | undefined
  if (!data) {
    return fallback
  }

  if (typeof data.error === 'string') {
    return data.error
  }

  if (typeof data.detail === 'string') {
    return data.detail
  }

  const fieldMessages = [data.email, data.first_name, data.last_name]
    .flat()
    .filter((message): message is string => typeof message === 'string')

  if (fieldMessages.length > 0) {
    return fieldMessages[0]!
  }

  return fallback
}

export async function fetchReferrals(): Promise<Referral[]> {
  const { data } = await apiClient.get<PaginatedResponse<Referral>>(`${BASE_PATH}/`)
  return data.results
}

export async function createReferral(payload: CreateReferralPayload): Promise<Referral> {
  const { data } = await apiClient.post<Referral>(`${BASE_PATH}/`, payload)
  return data
}

export async function resendReferral(id: number): Promise<Referral> {
  const { data } = await apiClient.post<Referral>(`${BASE_PATH}/${id}/resend/`)
  return data
}

export async function fetchAnalytics(): Promise<Analytics> {
  const { data } = await apiClient.get<Analytics>(`${BASE_PATH}/analytics/`)
  return data
}
