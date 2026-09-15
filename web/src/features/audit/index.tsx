import { useQuery, keepPreviousData } from '@tanstack/react-query'
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
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import { useEffect } from 'react'
import { fetchAuditPage } from '@/lib/api'

const verdictClasses: Record<string, string> = {
  PASS: 'bg-emerald-500/15 text-emerald-600 dark:text-emerald-400',
  BLOCK: 'bg-red-500/15 text-red-600 dark:text-red-400',
  MASK: 'bg-amber-500/15 text-amber-600 dark:text-amber-400',
  ERROR: 'bg-red-500/15 text-red-600 dark:text-red-400',
}

export function AuditView() {
  useEffect(() => {
    document.title = 'Audit log - QueryGuard'
  }, [])
  const [page, setPage] = useState(1)
  const audit = useQuery({
    queryKey: ['audit', page],
    queryFn: () => fetchAuditPage(page),
    placeholderData: keepPreviousData,
  })

  const entries = audit.data?.entries ?? []
  const hasNext = entries.length === 20

  return (
    <Card>
      <CardHeader>
        <CardTitle>Audit log</CardTitle>
        <CardDescription>
          Every question, the SQL it produced, and what the gate decided. Append-only: entries are
          never edited or removed.
        </CardDescription>
      </CardHeader>
      <CardContent>
        {audit.isPending ? (
          <div className='text-muted-foreground p-6 text-sm'>Loading audit log...</div>
        ) : (
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Time</TableHead>
                <TableHead>Question</TableHead>
                <TableHead>Outcome</TableHead>
                <TableHead>Rule</TableHead>
                <TableHead className='text-right'>Latency</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {entries.map((e) => (
                <TableRow key={e.id}>
                  <TableCell className='whitespace-nowrap text-xs'>{e.ts}</TableCell>
                  <TableCell className='max-w-md truncate'>{e.question}</TableCell>
                  <TableCell>
                    <Badge className={verdictClasses[e.verdict]}>{e.verdict}</Badge>
                  </TableCell>
                  <TableCell className='text-muted-foreground text-xs'>
                    {e.verdict === 'PASS' ? '-' : e.rule_id}
                  </TableCell>
                  <TableCell className='text-right text-xs'>
                    {e.latency_ms != null ? `${e.latency_ms.toFixed(2)} ms` : '-'}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        )}

        <div className='text-muted-foreground mt-3 flex items-center justify-between text-sm'>
          <span>
            Page {audit.data?.page ?? page}
            {entries.length === 20 ? '+' : ''}
            {entries[0] ? ` · last entry ${entries[0].ts}` : ''}
          </span>
          <div className='flex gap-2'>
            <Button
              variant='outline'
              size='sm'
              disabled={page <= 1 || audit.isPending}
              onClick={() => setPage((p) => Math.max(1, p - 1))}
            >
              Previous
            </Button>
            <Button
              variant='outline'
              size='sm'
              disabled={!hasNext || audit.isPending}
              onClick={() => setPage((p) => p + 1)}
            >
              Next
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
