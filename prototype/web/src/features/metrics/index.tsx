import { useQuery } from '@tanstack/react-query'
import { Bar, BarChart, Cell, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { useEffect } from 'react'
import { fetchExplain, fetchMetrics } from '@/lib/api'
import type { Verdict } from '@/types'

const verdictColor: Record<Verdict, string> = {
  PASS: '#2da464',
  BLOCK: '#e74c3c',
  MASK: '#d69e2e',
  ERROR: '#e74c3c',
}

function Stat({
  label,
  value,
  unit,
  color,
}: {
  label: string
  value: number | string
  unit?: string
  color?: string
}) {
  return (
    <Card>
      <CardContent className='pt-0'>
        <div className='text-muted-foreground text-xs uppercase tracking-wide'>{label}</div>
        <div className={`text-3xl font-bold ${color ?? ''}`}>
          {value}
          {unit ? <span className='text-muted-foreground text-base'> {unit}</span> : null}
        </div>
      </CardContent>
    </Card>
  )
}

export function MetricsView() {
  useEffect(() => {
    document.title = 'Metrics - QueryGuard'
  }, [])
  const metrics = useQuery({ queryKey: ['metrics'], queryFn: fetchMetrics, refetchInterval: 5000 })
  const explain = useQuery({ queryKey: ['explain'], queryFn: fetchExplain })

  if (metrics.isPending) return <div className='text-muted-foreground p-6'>Loading metrics...</div>
  if (metrics.isError)
    return <div className='p-6 text-red-600'>Could not load metrics: {String(metrics.error)}</div>

  const m = metrics.data
  const passed = m.total_requests - m.blocked - m.masked
  const ruleName = (id: string) => explain.data?.rules.find((r) => r.id === id)?.name ?? id
  const ruleData = Object.entries(m.block_by_rule).map(([rule, n]) => ({ rule, n, name: ruleName(rule) }))
  const timeline = m.series.verdicts.map((v, i) => ({ i, ok: 1, v, q: m.series.questions[i] }))

  return (
    <div className='flex flex-col gap-3'>
      <Card>
        <CardContent className='pt-6'>
          <div className='mb-1 flex items-center gap-2'>
            <span className='inline-flex items-center gap-1.5 rounded-full bg-emerald-500/10 px-2.5 py-1 text-xs font-medium text-emerald-600 dark:text-emerald-400'>
              <span className='relative flex h-2 w-2'>
                <span className='absolute inline-flex h-full w-full animate-ping rounded-full bg-emerald-400 opacity-60'></span>
                <span className='relative inline-flex h-2 w-2 rounded-full bg-emerald-500'></span>
              </span>
              live
            </span>
            <span className='text-muted-foreground text-xs uppercase tracking-wide'>
              refreshes every 5s
            </span>
          </div>
          <div className='text-muted-foreground text-xs uppercase tracking-wide'>
            What this page tells you
          </div>
          Every question so far was checked by the gate before it touched the database.{' '}
          {m.blocked} of {m.total_requests} requests were attack attempts, and all of them were
          stopped. {m.masked} answers had private columns removed. Safe questions run normally: the
          check itself is far faster than an eye blink (target: under 50 ms).
        </CardContent>
      </Card>

      <div className='grid grid-cols-2 gap-3 md:grid-cols-3 xl:grid-cols-6'>
        <Stat label='questions asked' value={m.total_requests} />
        <Stat label='ran normally' value={passed} color='text-emerald-600 dark:text-emerald-400' />
        <Stat label='attacks stopped' value={m.blocked} color='text-red-600 dark:text-red-400' />
        <Stat label='private data hidden' value={m.masked} color='text-amber-600 dark:text-amber-400' />
        <Stat label='typical check' value={m.latency_p50_ms} unit='ms' />
        <Stat label='slowest 5%' value={m.latency_p95_ms} unit='ms' />
      </div>

      <div className='grid gap-3 lg:grid-cols-5'>
        <Card className='lg:col-span-3'>
          <CardHeader>
            <CardTitle>Every decision, in order</CardTitle>
            <CardDescription>
              Each block is one request: green ran, red was an attack (stopped), amber was answered
              with private columns removed. Hover for the question.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className='h-56'>
              <ResponsiveContainer width='100%' height='100%'>
              <BarChart data={timeline}>
                <XAxis hide dataKey='i' />
                <YAxis hide />
                <Tooltip
                  content={({ active, payload }) =>
                    active && payload?.length ? (
                      <div className='bg-popover text-popover-foreground rounded-md border p-2 text-xs shadow'>
                        {payload[0].payload.v} · {payload[0].payload.q}
                      </div>
                    ) : null
                  }
                />
                <Bar dataKey='ok' radius={3} maxBarSize={18}>
                  {timeline.map((entry) => (
                    <Cell key={entry.i} fill={verdictColor[entry.v]} />
                  ))}
                </Bar>
              </BarChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        <Card className='lg:col-span-2'>
          <CardHeader>
            <CardTitle>Which rules stopped the attacks</CardTitle>
            <CardDescription>
              Each bar is one safety rule; longer means more attacks that rule stopped.{' '}
              <a href='/how' className='text-primary underline'>What each rule means</a>
            </CardDescription>
          </CardHeader>
          <CardContent className='space-y-3'>
            {ruleData.length === 0 && (
              <div className='text-muted-foreground text-sm'>no attacks seen yet</div>
            )}
            {ruleData.map((row) => (
              <div key={row.rule} className='space-y-1'>
                <div className='flex justify-between text-sm'>
                  <span>{row.name}</span>
                  <span className='text-muted-foreground'>
                    {row.rule} · {row.n}
                  </span>
                </div>
                <div className='bg-secondary h-2 w-full overflow-hidden rounded-full'>
                  <div
                    className='h-full rounded-full bg-red-500'
                    style={{
                      width: `${(row.n * 100) / Math.max(...ruleData.map((r) => r.n))}%`,
                    }}
                  />
                </div>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
