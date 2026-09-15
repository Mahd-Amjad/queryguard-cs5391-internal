import { useMutation, useQuery } from '@tanstack/react-query'
import { useState } from 'react'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import { askQuestion, fetchExplain, fetchMeta } from '@/lib/api'
import type { AskResult } from '@/types'
import { useEffect } from 'react'

const verdictClasses: Record<string, string> = {
  PASS: 'bg-emerald-500/15 text-emerald-600 dark:text-emerald-400',
  BLOCK: 'bg-red-500/15 text-red-600 dark:text-red-400',
  MASK: 'bg-amber-500/15 text-amber-600 dark:text-amber-400',
  ERROR: 'bg-red-500/15 text-red-600 dark:text-red-400',
}

const verdictIcons: Record<string, string> = {
  PASS: 'M9 12l2 2 4-4M12 3l7 3v5c0 4.6-2.9 8-7 10-4.1-2-7-5.4-7-10V6z',
  MASK: 'M3 3l18 18M10.6 10.6a2 2 0 0 0 2.8 2.8M8 4h9a2 2 0 0 1 2 2v9M17 17H6l-2 2V6a2 2 0 0 1 2-2',
  BLOCK: 'M12 3l7 3v5c0 4.6-2.9 8-7 10-4.1-2-7-5.4-7-10V6zM10 10l4 4M14 10l-4 4',
  ERROR: 'M12 9v4M12 17h.01M12 3l7 3v5c0 4.6-2.9 8-7 10-4.1-2-7-5.4-7-10V6z',
}

export function AskView() {
  const [question, setQuestion] = useState('')
  const [result, setResult] = useState<AskResult | null>(null)

  const meta = useQuery({ queryKey: ['meta'], queryFn: fetchMeta })
  const explain = useQuery({ queryKey: ['explain'], queryFn: fetchExplain })

  const ask = useMutation({
    mutationFn: askQuestion,
    onSuccess: (data) => {
      setResult(data)
      setQuestion(data.question)
    },
  })

  const ruleName =
    result && result.rule_id !== 'OK'
      ? (explain.data?.rules.find((r) => r.id === result.rule_id)?.name ?? result.rule_id)
      : 'No rule broken'
  const verdictCopy =
    result && explain.data ? explain.data.verdicts[result.verdict] : ''
  const latencyPct = result
    ? Math.min(100, Math.round((result.elapsed_ms / (meta.data?.target_latency_ms ?? 50)) * 100))
    : 0

  const submit = (q: string) => {
    const text = q.trim()
    if (text && !ask.isPending) ask.mutate(text)
  }

  useEffect(() => {
    document.title = 'Ask - QueryGuard'
  }, [])

  return (
    <div className='qg-wash -mx-4 -my-4 flex min-h-[calc(100vh-3.5rem)] flex-col justify-center px-4 py-8'>
      <div className='mx-auto flex w-full max-w-6xl flex-col justify-center gap-5'>
      <div className='text-center'>
        <h1 className='text-4xl font-bold tracking-tight md:text-5xl'>
          Ask anything.{' '}
          <span className='font-script text-5xl md:text-6xl'>We check everything.</span>
        </h1>
        <p className='text-muted-foreground mx-auto mt-3 max-w-xl text-[15px]'>
          Plain English in, safe SQL out. Every query passes nine deterministic rules before it
          can touch the database - and every decision is recorded.
        </p>
      </div>
      <div className='grid gap-3 lg:grid-cols-3'>
        <Card className='lg:col-span-2'>
          <CardHeader>
            <CardDescription className='uppercase tracking-wide'>Your question</CardDescription>
          </CardHeader>
          <CardContent>
            <form
              onSubmit={(e) => {
                e.preventDefault()
                submit(question)
              }}
            >
              <Input
                className='h-11'
                placeholder='e.g. How many appointments are scheduled in March?'
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                autoComplete='off'
              />
              <div className='mt-2 flex flex-wrap gap-1.5'>
                {(meta.data?.examples ?? []).map((ex) => (
                  <Button
                    key={ex}
                    type='button'
                    variant='outline'
                    size='sm'
                    className='rounded-full'
                    disabled={ask.isPending}
                    onClick={() => {
                      setQuestion(ex)
                      submit(ex)
                    }}
                  >
                    {ex}
                  </Button>
                ))}
              </div>
              <div className='mt-3 flex items-center gap-2'>
                <Button type='submit' disabled={ask.isPending}>
                  {ask.isPending ? 'Checking...' : 'Ask'}
                </Button>
                <span className='text-muted-foreground text-sm'>
                  Nothing runs before the gate passes it.
                </span>
              </div>
            </form>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardDescription className='uppercase tracking-wide'>What this does</CardDescription>
          </CardHeader>
          <CardContent className='text-sm'>
            <p className='mb-1'><strong>1.</strong> You ask a question in plain English.</p>
            <p className='mb-1'><strong>2.</strong> An AI drafts the database query that answers it.</p>
            <p className='mb-0'>
              <strong>3.</strong> The safety gate checks that query before anything runs.{' '}
              <a href='/how' className='text-primary underline'>The nine rules it applies</a>
            </p>
          </CardContent>
        </Card>
      </div>

      {result && (
        <div className='grid gap-3 lg:grid-cols-3'>
          <Card className='lg:col-span-2'>
            <CardHeader className='flex-row items-center justify-between'>
              <CardTitle>Answer</CardTitle>
              <Badge className={verdictClasses[result.verdict]}>{result.verdict}</Badge>
            </CardHeader>
            <CardContent>
              {result.answer && result.answer.rows.length > 0 ? (
                <>
                  <Table>
                    <TableHeader>
                      <TableRow>
                        {result.answer.columns.map((c) => (
                          <TableHead key={c}>{c}</TableHead>
                        ))}
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {result.answer.rows.slice(0, 10).map((row, i) => (
                        <TableRow key={i}>
                          {row.map((v, j) => (
                            <TableCell key={j}>{String(v)}</TableCell>
                          ))}
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                  <div className='text-muted-foreground mt-2 text-sm'>
                    {result.answer.row_count} row{result.answer.row_count === 1 ? '' : 's'}
                  </div>
                </>
              ) : (
                <div className='text-muted-foreground py-6 text-center'>
                  <p className='font-medium'>No answer returned</p>
                  <p className='text-sm'>Nothing ran, nothing changed.</p>
                </div>
              )}
              {result.suggestion && (
                <div className='mt-3 rounded-md border-l-4 border-amber-500 bg-amber-500/10 p-3 text-sm'>
                  Suggestion: {result.suggestion}
                </div>
              )}
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>The safety check</CardTitle>
            </CardHeader>
            <CardContent className='space-y-3 text-sm'>
              <div className='flex items-center gap-3'>
                <span
                  className={`inline-flex h-11 w-11 items-center justify-center rounded-xl ${
                    verdictClasses[result.verdict]
                  }`}
                >
                  <svg viewBox='0 0 24 24' fill='none' stroke='currentColor' strokeWidth='2' strokeLinecap='round' strokeLinejoin='round' className='h-5 w-5'>
                    <path d={verdictIcons[result.verdict] ?? verdictIcons.PASS} />
                  </svg>
                </span>
                <div className='flex flex-wrap items-center gap-1.5'>
                  <Badge className={verdictClasses[result.verdict]}>{result.verdict}</Badge>
                  <Badge variant='secondary'>{ruleName}</Badge>
                </div>
              </div>
              <p className='font-medium'>{verdictCopy}</p>
              <p className='text-muted-foreground'>{result.reason_plain}</p>
              <div className='text-muted-foreground flex items-center gap-2'>
                <span>Checked in {result.elapsed_ms} ms</span>
                <div className='bg-secondary h-1.5 flex-1 overflow-hidden rounded-full'><div className='h-full rounded-full bg-emerald-500' style={{ width: `${latencyPct}%` }} /></div>
                <span className='text-xs'>&lt; 50 ms target</span>
              </div>
              <p className='text-muted-foreground'>
                Recorded on the <a href='/audit' className='text-primary underline'>Audit log</a>
              </p>
              <div>
                <div className='text-muted-foreground uppercase tracking-wide mb-1 text-xs'>Generated SQL</div>
                <pre className='overflow-x-auto rounded-lg bg-zinc-900 p-3 font-mono text-xs text-zinc-100'>
                  {result.sql}
                </pre>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
      </div>
    </div>
  )
}
