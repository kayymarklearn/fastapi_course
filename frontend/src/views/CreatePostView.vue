<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { postsAPI } from '../api/posts'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const auth = useAuthStore()

if (!auth.isAuthenticated) {
  router.push('/login')
}

const title = ref('')
const content = ref('')
const published = ref(true)
const error = ref('')
const loading = ref(false)

async function handleSubmit() {
  if (!title.value.trim() || !content.value.trim()) {
    error.value = 'Title and content are required'
    return
  }
  error.value = ''
  loading.value = true
  try {
    const post = await postsAPI.create({
      title: title.value,
      content: content.value,
      published: published.value,
    })
    router.push(`/posts/${post.id}`)
  } catch (err: unknown) {
    if (err && typeof err === 'object' && 'response' in err) {
      const axiosErr = err as { response?: { data?: { detail?: string } } }
      error.value = axiosErr.response?.data?.detail || 'Failed to create post'
    } else {
      error.value = 'Failed to create post'
    }
  }
  loading.value = false
}
</script>

<template>
  <div class="max-w-3xl mx-auto px-4 py-8">
    <div class="bg-slate-800 rounded-2xl border border-slate-700 p-8 shadow-2xl">
      <h1 class="text-2xl font-bold mb-8">Create Post</h1>

      <form @submit.prevent="handleSubmit" class="space-y-6">
        <div>
          <label for="title" class="block text-sm font-medium text-slate-300 mb-1.5">Title</label>
          <input
            id="title"
            v-model="title"
            type="text"
            required
            placeholder="Post title"
            class="w-full px-4 py-2.5 bg-slate-700 border border-slate-600 rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
          />
        </div>

        <div>
          <label for="content" class="block text-sm font-medium text-slate-300 mb-1.5">Content</label>
          <textarea
            id="content"
            v-model="content"
            required
            rows="8"
            placeholder="Write your post content here..."
            class="w-full px-4 py-2.5 bg-slate-700 border border-slate-600 rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all resize-y"
          ></textarea>
        </div>

        <div class="flex items-center gap-3">
          <label class="relative inline-flex items-center cursor-pointer">
            <input
              v-model="published"
              type="checkbox"
              class="sr-only peer"
            />
            <div class="w-11 h-6 bg-slate-600 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-indigo-500 rounded-full peer peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-indigo-600"></div>
          </label>
          <span class="text-sm text-slate-300">Publish immediately</span>
        </div>

        <p v-if="error" class="text-sm text-red-400">{{ error }}</p>

        <div class="flex items-center gap-3">
          <button
            type="submit"
            :disabled="loading"
            class="px-6 py-2.5 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed text-white font-medium rounded-lg transition-colors"
          >
            {{ loading ? 'Creating...' : 'Create Post' }}
          </button>
          <router-link
            to="/"
            class="px-6 py-2.5 text-sm font-medium text-slate-400 hover:text-white transition-colors"
          >
            Cancel
          </router-link>
        </div>
      </form>
    </div>
  </div>
</template>
