<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { postsAPI } from '../api/posts'
import { useAuthStore } from '../stores/auth'
import VoteButton from '../components/VoteButton.vue'
import type { PostOut } from '../types'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

const postOut = ref<PostOut | null>(null)
const loading = ref(true)
const deleting = ref(false)
const notFound = ref(false)

async function loadPost() {
  loading.value = true
  try {
    const id = Number(route.params.id)
    postOut.value = await postsAPI.get(id)
  } catch {
    notFound.value = true
  }
  loading.value = false
}

async function deletePost() {
  if (!postOut.value) return
  if (!confirm('Are you sure you want to delete this post?')) return
  deleting.value = true
  try {
    await postsAPI.delete(postOut.value.Post.id)
    router.push('/')
  } catch {
    // handle error
  }
  deleting.value = false
}

const isOwner = () =>
  auth.currentUser?.id === postOut.value?.Post.user_id

function formatDate(dateStr: string): string {
  return new Date(dateStr).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

onMounted(loadPost)
</script>

<template>
  <div class="max-w-3xl mx-auto px-4 py-8">
    <div v-if="loading" class="animate-pulse space-y-4">
      <div class="h-8 bg-slate-700 rounded w-1/2 mb-4"></div>
      <div class="h-4 bg-slate-700 rounded w-1/4 mb-6"></div>
      <div class="h-4 bg-slate-700 rounded w-full mb-2"></div>
      <div class="h-4 bg-slate-700 rounded w-5/6 mb-2"></div>
      <div class="h-4 bg-slate-700 rounded w-2/3"></div>
    </div>

    <div v-else-if="notFound" class="text-center py-16">
      <h2 class="text-2xl font-bold text-slate-400 mb-2">Post Not Found</h2>
      <p class="text-slate-500 mb-6">This post doesn't exist or has been deleted.</p>
      <router-link
        to="/"
        class="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-sm font-medium rounded-lg transition-colors"
      >
        Back to Posts
      </router-link>
    </div>

    <article v-else-if="postOut" class="bg-slate-800 rounded-2xl border border-slate-700 shadow-2xl overflow-hidden">
      <div class="p-8">
        <div class="flex items-start gap-4">
          <VoteButton
            :post-id="postOut.Post.id"
            :votes="postOut.votes"
            @vote="loadPost"
          />
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-3 mb-2">
              <span class="text-sm font-medium text-indigo-400 bg-indigo-500/10 px-3 py-1 rounded-full">
                {{ postOut.Post.author.email }}
              </span>
              <span class="text-sm text-slate-500">{{ formatDate(postOut.Post.created_at) }}</span>
              <span
                v-if="!postOut.Post.published"
                class="text-xs text-amber-400 bg-amber-400/10 px-2 py-0.5 rounded-full"
              >
                Draft
              </span>
            </div>

            <h1 class="text-3xl font-bold text-slate-100 mb-4">{{ postOut.Post.title }}</h1>

            <div class="prose prose-invert max-w-none">
              <p class="text-slate-300 leading-relaxed whitespace-pre-wrap">{{ postOut.Post.content }}</p>
            </div>

            <div v-if="isOwner()" class="flex items-center gap-3 mt-8 pt-6 border-t border-slate-700">
              <router-link
                :to="`/posts/${postOut.Post.id}/edit`"
                class="px-4 py-2 bg-slate-700 hover:bg-slate-600 text-sm font-medium rounded-lg transition-colors"
              >
                Edit
              </router-link>
              <button
                @click="deletePost"
                :disabled="deleting"
                class="px-4 py-2 bg-red-600/20 hover:bg-red-600/30 text-red-400 text-sm font-medium rounded-lg transition-colors disabled:opacity-50"
              >
                {{ deleting ? 'Deleting...' : 'Delete' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </article>
  </div>
</template>
