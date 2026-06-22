import client from './client'
import type { User, Token } from '../types'

export const authAPI = {
  async login(email: string, password: string): Promise<{ token: Token; user: User }> {
    const formData = new URLSearchParams()
    formData.append('username', email)
    formData.append('password', password)
    const { data: token } = await client.post<Token>('/login', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    })
    localStorage.setItem('token', token.access_token)
    const { data: user } = await client.get<User>('/users/me')
    return { token, user }
  },

  async register(email: string, password: string): Promise<User> {
    const { data } = await client.post<User>('/users/', { email, password })
    return data
  },

  async getCurrentUser(): Promise<User> {
    const { data } = await client.get<User>('/users/me')
    return data
  },
}
