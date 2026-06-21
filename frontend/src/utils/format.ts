const RESEND_COOLDOWN_SECONDS = 30

/** Format an ISO timestamp for display. */
export function formatDate(iso: string): string {
  return new Date(iso).toLocaleDateString(undefined, {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  })
}

/** Seconds remaining before a referral can be resent again. */
export function resendCooldownSeconds(lastSentAt: string): number {
  const elapsed = (Date.now() - new Date(lastSentAt).getTime()) / 1000
  return Math.max(0, Math.ceil(RESEND_COOLDOWN_SECONDS - elapsed))
}
