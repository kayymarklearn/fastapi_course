<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { postsAPI } from '../api/posts'
import PostCard from '../components/PostCard.vue'
import type { PostOut } from '../types'

const posts = ref<PostOut[]>([])
const loading = ref(true)
const search = ref('')
const limit = ref(10)
const skip = ref(0)
const hasMore = ref(true)

async function loadPosts() {
  loading.value = true
  try {
    const data = await postsAPI.list({
      limit: limit.value,
      skip: skip.value,
      search: search.value,
    })
    if (data.length < limit.value) hasMore.value = false
    else hasMore.value = true
    posts.value = data
  } catch {
    posts.value = []
  }
  loading.value = false
}

function onSearch() {
  skip.value = 0
  hasMore.value = true
  loadPosts()
}

function nextPage() {
  skip.value += limit.value
  loadPosts()
}

function prevPage() {
  skip.value = Math.max(0, skip.value - limit.value)
  loadPosts()
}

onMounted(loadPosts)
</script>

<template>
  <div class="max-w-3xl mx-auto px-4 py-8">
    <div class="flex items-center justify-between mb-8">
      <h1 class="text-2xl font-bold">Posts</h1>
      <div class="relative">
        <input
          v-model="search"
          @input="onSearch"
          type="text"
          placeholder="Search posts..."
          class="w-64 px-4 py-2 pl-10 bg-slate-800 border border-slate-700 rounded-lg text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
        />
        <svg
          class="absolute left-3 top-2.5 w-4 h-4 text-slate-500"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
      </div>
    </div>

    <div v-if="loading" class="space-y-4">
      <div v-for="n in 3" :key="n" class="bg-slate-800 rounded-xl border border-slate-700 p-5 animate-pulse">
        <div class="h-4 bg-slate-700 rounded w-1/4 mb-3"></div>
        <div class="h-5 bg-slate-700 rounded w-3/4 mb-2"></div>
        <div class="h-4 bg-slate-700 rounded w-full"></div>
      </div>
    </div>

    <div v-else-if="posts.length === 0" class="text-center py-16">
      <p class="text-slate-500 text-lg">No posts yet</p>
      <router-link
        to="/posts/new"
        class="inline-block mt-4 px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-sm font-medium rounded-lg transition-colors"
      >
        Create the first post
      </router-link>
    </div>

    <div v-else class="space-y-4">
      <PostCard
        v-for="postOut in posts"
        :key="postOut.Post.id"
        :post-out="postOut"
        @vote="loadPosts"
      />

      <div class="flex items-center justify-between pt-4">
        <button
          @click="prevPage"
          :disabled="skip === 0"
          class="px-4 py-2 text-sm font-medium rounded-lg transition-colors disabled:opacity-30 disabled:cursor-not-allowed"
          :class="skip > 0 ? 'bg-slate-700 hover:bg-slate-600 text-slate-200' : 'bg-slate-800 text-slate-600'"
        >
          Previous
        </button>
        <span class="text-sm text-slate-500">Page {{ Math.floor(skip / limit) + 1 }}</span>
        <button
          @click="nextPage"
          :disabled="!hasMore"
          class="px-4 py-2 text-sm font-medium rounded-lg transition-colors disabled:opacity-30 disabled:cursor-not-allowed"
          :class="hasMore ? 'bg-slate-700 hover:bg-slate-600 text-slate-200' : 'bg-slate-800 text-slate-600'"
        >
          Next
        </button>
      </div>
    </div>
  </div>
</template>
