<script setup lang="ts">
import type { PostOut } from '../types'
import VoteButton from './VoteButton.vue'

const props = defineProps<{ postOut: PostOut }>()
const emit = defineEmits<{ vote: [postId: number] }>()

const post = props.postOut.Post

function formatDate(dateStr: string): string {
  return new Date(dateStr).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  })
}
</script>

<template>
  <div class="bg-slate-800 rounded-xl border border-slate-700 hover:border-slate-600 transition-all shadow-lg hover:shadow-xl">
    <div class="p-5">
      <div class="flex items-start gap-4">
        <VoteButton
          :post-id="post.id"
          :votes="postOut.votes"
          @vote="emit('vote', post.id)"
        />
        <div class="flex-1 min-w-0">
          <div class="flex items-center gap-2 mb-1">
            <span class="text-xs font-medium text-indigo-400 bg-indigo-500/10 px-2 py-0.5 rounded-full">
              {{ post.author.email.split('@')[0] }}
            </span>
            <span class="text-xs text-slate-500">&middot;</span>
            <span class="text-xs text-slate-500">{{ formatDate(post.created_at) }}</span>
          </div>
          <router-link
            :to="`/posts/${post.id}`"
            class="block"
          >
            <h3 class="text-lg font-semibold text-slate-100 hover:text-indigo-300 transition-colors truncate">
              {{ post.title }}
            </h3>
          </router-link>
          <p class="mt-1 text-sm text-slate-400 line-clamp-2">
            {{ post.content }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>
