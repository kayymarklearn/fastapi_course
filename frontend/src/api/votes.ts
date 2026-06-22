import client from './client'
import type { VoteBody } from '../types'

export const votesAPI = {
  async vote(body: VoteBody): Promise<void> {
    await client.post('/vote/', body)
  },
}
