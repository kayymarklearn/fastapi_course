import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authAPI } from '../api/auth'
import type { User } from '../types'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('token'))
  const currentUser = ref<User | null>(
    JSON.parse(localStorage.getItem('currentUser') || 'null'),
  )

  const isAuthenticated = computed(() => !!token.value)

  async function login(email: string, password: string) {
    const { token: t, user } = await authAPI.login(email, password)
    token.value = t.access_token
    currentUser.value = user
    localStorage.setItem('currentUser', JSON.stringify(user))
  }

  async function register(email: string, password: string) {
    const user = await authAPI.register(email, password)
    return user
  }

  async function fetchCurrentUser() {
    if (!token.value) return
    try {
      const user = await authAPI.getCurrentUser()
      currentUser.value = user
      localStorage.setItem('currentUser', JSON.stringify(user))
    } catch {
      logout()
    }
  }

  function logout() {
    token.value = null
    currentUser.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('currentUser')
  }

  return { token, currentUser, isAuthenticated, login, register, fetchCurrentUser, logout }
})
