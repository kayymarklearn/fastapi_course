export interface User {
  id: number
  email: string
  created_at: string
}

export interface Post {
  id: number
  title: string
  content: string
  published: boolean
  created_at: string
  user_id: number
  author: User
}

export interface PostOut {
  Post: Post
  votes: number
}

export interface PostCreate {
  title: string
  content: string
  published: boolean
}

export interface PostUpdate extends PostCreate {}

export interface Token {
  access_token: string
  token_type: string
}

export interface PaginationParams {
  limit: number
  skip: number
  search?: string
}

export interface VoteBody {
  post_id: number
  dir: 0 | 1
}
