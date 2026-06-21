export type ReferralStatus =
  | 'invitation_sent'
  | 'application_received'
  | 'joined'
  | 'declined'

export interface Referral {
  id: number
  first_name: string
  last_name: string
  email: string
  status: ReferralStatus
  created_at: string
  last_sent_at: string
}

export interface CreateReferralPayload {
  first_name: string
  last_name: string
  email: string
}

export interface Analytics {
  total_invited: number
  invitations_sent: number
  joined: number
  conversion_rate: number
}

export interface PaginatedResponse<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

export interface ApiErrorBody {
  error?: string
  detail?: string
  email?: string[]
  first_name?: string[]
  last_name?: string[]
}
