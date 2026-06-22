import client from './client'
import type { PostOut, PostCreate, PostUpdate, PaginationParams, Post } from '../types'

export const postsAPI = {
  async list(params: PaginationParams): Promise<PostOut[]> {
    const { data } = await client.get<PostOut[]>('/posts/', { params })
    return data
  },

  async get(id: number): Promise<PostOut> {
    const { data } = await client.get<PostOut>(`/posts/${id}`)
    return data
  },

  async create(post: PostCreate): Promise<Post> {
    const { data } = await client.post<Post>('/posts/', post)
    return data
  },

  async update(id: number, post: PostUpdate): Promise<Post> {
    const { data } = await client.put<Post>(`/posts/${id}`, post)
    return data
  },

  async delete(id: number): Promise<void> {
    await client.delete(`/posts/${id}`)
  },
}
