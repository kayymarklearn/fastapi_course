<script setup lang="ts">
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()

function handleLogout() {
  auth.logout()
  router.push('/login')
}
</script>

<template>
  <nav class="bg-slate-800 border-b border-slate-700 sticky top-0 z-50">
    <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">
        <router-link to="/" class="text-xl font-bold text-indigo-400 hover:text-indigo-300 transition-colors">
          FastAPI Social
        </router-link>

        <div class="flex items-center gap-4">
          <template v-if="auth.isAuthenticated">
            <router-link
              to="/posts/new"
              class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-indigo-600 hover:bg-indigo-500 text-sm font-medium rounded-lg transition-colors"
            >
              <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
              </svg>
              New Post
            </router-link>
            <span class="text-sm text-slate-400">{{ auth.currentUser?.email }}</span>
            <button
              @click="handleLogout"
              class="px-3 py-1.5 text-sm font-medium text-slate-300 hover:text-white hover:bg-slate-700 rounded-lg transition-colors"
            >
              Logout
            </button>
          </template>
          <template v-else>
            <router-link
              to="/login"
              class="px-3 py-1.5 text-sm font-medium text-slate-300 hover:text-white transition-colors"
            >
              Login
            </router-link>
            <router-link
              to="/register"
              class="px-3 py-1.5 bg-indigo-600 hover:bg-indigo-500 text-sm font-medium rounded-lg transition-colors"
            >
              Register
            </router-link>
          </template>
        </div>
      </div>
    </div>
  </nav>
</template>
