<script setup lang="ts">
import { ref } from 'vue'
import { votesAPI } from '../api/votes'
import { useAuthStore } from '../stores/auth'

const props = defineProps<{ postId: number; votes: number }>()
const emit = defineEmits<{ vote: [] }>()

const auth = useAuthStore()
const voteCount = ref(props.votes)
const loading = ref(false)

async function handleVote() {
  if (!auth.isAuthenticated) return
  loading.value = true
  try {
    await votesAPI.vote({ post_id: props.postId, dir: 1 })
    voteCount.value++
    emit('vote')
  } catch {
    // Likely already voted — try to remove vote
    try {
      await votesAPI.vote({ post_id: props.postId, dir: 0 })
      voteCount.value--
      emit('vote')
    } catch {
      // ignore
    }
  }
  loading.value = false
}
</script>

<template>
  <button
    @click="handleVote"
    :disabled="loading || !auth.isAuthenticated"
    class="flex flex-col items-center gap-0.5 min-w-[2.5rem] px-2 py-1.5 rounded-lg transition-colors"
    :class="auth.isAuthenticated
      ? 'hover:bg-indigo-500/10 hover:text-indigo-400 text-slate-500'
      : 'text-slate-600 cursor-not-allowed'"
  >
    <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7" />
    </svg>
    <span class="text-sm font-semibold">{{ voteCount }}</span>
  </button>
</template>
