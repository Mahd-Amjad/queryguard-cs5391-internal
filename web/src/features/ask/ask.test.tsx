import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi, beforeEach } from 'vitest'
import { AskView } from './index'

function renderAsk() {
  const client = new QueryClient({ defaultOptions: { queries: { retry: false } } })
  return render(
    <QueryClientProvider client={client}>
      <AskView />
    </QueryClientProvider>,
  )
}

function stubFetch(responses: Record<string, unknown>) {
  vi.stubGlobal(
    'fetch',
    vi.fn((input: RequestInfo | URL) => {
      const path = String(input)
      const key = Object.keys(responses).find((k) => path.startsWith(k)) ?? ''
      return Promise.resolve({
        ok: true,
        json: () => Promise.resolve(responses[key] ?? {}),
      } as Response)
    }),
  )
}

const meta = { examples: ['Example one', 'Example two'], target_latency_ms: 50 }
const explain = {
  rules: [{ id: 'G-05', name: 'Private columns stay private', plain: 'Private columns are removed.' }],
  verdicts: { PASS: 'Ran normally.', MASK: 'Private columns removed.', BLOCK: 'Blocked.', ERROR: 'Error.' },
}
const blocked = {
  question: 'Delete everything',
  verdict: 'BLOCK',
  rule_id: 'G-01',
  reason: 'destructive',
  reason_plain: 'Delete statements are not allowed.',
  sql: 'DELETE FROM billing',
  answer: null,
  elapsed_ms: 2,
  suggestion: '',
}

beforeEach(() => vi.unstubAllGlobals())

describe('AskView', () => {
  it('serves the example chips from the API meta', async () => {
    stubFetch({ '/api/meta': meta, '/api/explain': explain })
    renderAsk()
    expect(await screen.findByText('Example one')).toBeInTheDocument()
  })

  it('renders a blocked verdict without any answer table', async () => {
    stubFetch({ '/api/meta': meta, '/api/explain': explain, '/api/ask': blocked })
    renderAsk()
    await screen.findByText('Example one')
    await userEvent.click(screen.getByText('Example one'))
    await waitFor(() => expect(screen.getByText('The safety check')).toBeInTheDocument())
    expect(screen.getAllByText('BLOCK').length).toBeGreaterThan(0)
    expect(screen.getByText('Delete statements are not allowed.')).toBeInTheDocument()
    expect(screen.queryByText('Answer')).not.toBeNull()
  })
})
