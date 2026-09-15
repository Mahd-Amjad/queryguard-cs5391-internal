// Mirror of the Flask API responses (contract authority: tests/test_app.py + app.py).
// Keep in sync with queryguard/app.py + queryguard/explain.py.

export type Verdict = 'PASS' | 'BLOCK' | 'MASK' | 'ERROR'

export interface AnswerTable {
  columns: string[]
  row_count: number
  rows: unknown[][]
}

export interface AskResult {
  question: string
  verdict: Verdict
  rule_id: string
  reason: string
  reason_plain: string
  sql: string
  answer: AnswerTable | null
  elapsed_ms: number
  suggestion: string
}

export interface AuditEntry {
  id: number
  ts: string
  session: string
  question: string
  intent: string
  sql: string
  verdict: Verdict
  rule_id: string
  action: string
  latency_ms: number
  mode: string
}

export interface AuditPage {
  page: number
  entries: AuditEntry[]
}

export interface Metrics {
  total_requests: number
  pass_rate: number | null
  blocked: number
  masked: number
  block_by_rule: Record<string, number>
  latency_p50_ms: number
  latency_p95_ms: number
  series: {
    labels: string[]
    verdicts: Verdict[]
    questions: string[]
  }
}

export interface RuleExplain {
  id: string
  name: string
  plain: string
}

export interface Explain {
  rules: RuleExplain[]
  verdicts: Record<string, string>
}

export interface Meta {
  examples: string[]
  target_latency_ms: number
}
