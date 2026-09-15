// Thin fetch client for the Flask API. Same origin: /api/* is served by Flask,
// which also serves this built SPA. No CORS, no keys, offline at runtime.

import type { AskResult, AuditPage, Explain, Meta, Metrics } from '@/types'

async function get<T>(path: string): Promise<T> {
  const res = await fetch(path)
  if (!res.ok) throw new Error(`GET ${path} failed: ${res.status}`)
  return res.json() as Promise<T>
}

export function fetchExplain() {
  return get<Explain>('/api/explain')
}

export function fetchMeta() {
  return get<Meta>('/api/meta')
}

export function fetchMetrics() {
  return get<Metrics>('/api/metrics')
}

export function fetchAuditPage(page: number) {
  return get<AuditPage>(`/api/audit?page=${page}`)
}

export async function askQuestion(question: string): Promise<AskResult> {
  const res = await fetch('/api/ask', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question }),
  })
  const body = await res.json()
  if (!res.ok) throw new Error(body.error ?? `ask failed: ${res.status}`)
  return body as AskResult
}
