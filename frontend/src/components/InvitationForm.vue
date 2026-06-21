<script setup lang="ts">
import { reactive, ref } from 'vue'
import { storeToRefs } from 'pinia'

import { useReferralsStore } from '../stores/referrals'

const store = useReferralsStore()
const { submitting } = storeToRefs(store)

const form = reactive({
  first_name: '',
  last_name: '',
  email: '',
})

const fieldErrors = reactive({
  first_name: '',
  last_name: '',
  email: '',
})

const formError = ref('')

function validateForm(): boolean {
  fieldErrors.first_name = form.first_name.trim() ? '' : 'First name is required.'
  fieldErrors.last_name = form.last_name.trim() ? '' : 'Last name is required.'
  fieldErrors.email = form.email.trim() ? '' : 'Email is required.'

  return !fieldErrors.first_name && !fieldErrors.last_name && !fieldErrors.email
}

function resetForm(): void {
  form.first_name = ''
  form.last_name = ''
  form.email = ''
  fieldErrors.first_name = ''
  fieldErrors.last_name = ''
  fieldErrors.email = ''
}

async function handleSubmit(): Promise<void> {
  formError.value = ''

  if (!validateForm()) {
    return
  }

  const errorMessage = await store.createReferral({
    first_name: form.first_name.trim(),
    last_name: form.last_name.trim(),
    email: form.email.trim(),
  })

  if (errorMessage) {
    formError.value = errorMessage
    return
  }

  resetForm()
}
</script>

<template>
  <section class="rounded-xl border border-dark-border bg-dark-card p-6">
    <h2 class="font-serif text-2xl text-gray-primary">Invite a Member</h2>
    <p class="mt-1 text-sm text-gray-secondary">
      Send a referral invitation with name and email.
    </p>

    <form class="mt-6 space-y-4" @submit.prevent="handleSubmit">
      <div>
        <label class="mb-1 block text-sm text-gray-secondary" for="first_name">
          First Name
        </label>
        <input
          id="first_name"
          v-model="form.first_name"
          type="text"
          autocomplete="given-name"
          class="w-full rounded-lg border border-dark-border bg-dark-bg px-4 py-2.5 text-gray-primary outline-none transition focus:border-copper"
          :disabled="submitting"
        />
        <p v-if="fieldErrors.first_name" class="mt-1 text-sm text-red-400">
          {{ fieldErrors.first_name }}
        </p>
      </div>

      <div>
        <label class="mb-1 block text-sm text-gray-secondary" for="last_name">
          Last Name
        </label>
        <input
          id="last_name"
          v-model="form.last_name"
          type="text"
          autocomplete="family-name"
          class="w-full rounded-lg border border-dark-border bg-dark-bg px-4 py-2.5 text-gray-primary outline-none transition focus:border-copper"
          :disabled="submitting"
        />
        <p v-if="fieldErrors.last_name" class="mt-1 text-sm text-red-400">
          {{ fieldErrors.last_name }}
        </p>
      </div>

      <div>
        <label class="mb-1 block text-sm text-gray-secondary" for="email">
          Email
        </label>
        <input
          id="email"
          v-model="form.email"
          type="email"
          autocomplete="email"
          class="w-full rounded-lg border border-dark-border bg-dark-bg px-4 py-2.5 text-gray-primary outline-none transition focus:border-copper"
          :disabled="submitting"
        />
        <p v-if="fieldErrors.email" class="mt-1 text-sm text-red-400">
          {{ fieldErrors.email }}
        </p>
      </div>

      <p v-if="formError" class="rounded-lg border border-red-500/40 bg-red-500/10 px-3 py-2 text-sm text-red-300">
        {{ formError }}
      </p>

      <button
        type="submit"
        class="w-full rounded-lg bg-copper px-4 py-2.5 font-medium text-white transition hover:bg-copper-light disabled:cursor-not-allowed disabled:opacity-60"
        :disabled="submitting"
      >
        {{ submitting ? 'Sending…' : 'Send Invitation' }}
      </button>
    </form>
  </section>
</template>
