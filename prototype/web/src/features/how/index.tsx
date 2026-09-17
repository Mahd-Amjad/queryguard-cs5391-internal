import { useQuery } from '@tanstack/react-query'
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
import { fetchExplain } from '@/lib/api'

export function HowView() {
  useEffect(() => {
    document.title = 'How it works - QueryGuard'
  }, [])
  const explain = useQuery({ queryKey: ['explain'], queryFn: fetchExplain })

  return (
    <div className='flex flex-col gap-3'>
      <Card>
        <CardHeader>
          <CardTitle>What QueryGuard does</CardTitle>
          <CardDescription>
            The three-step story: you ask, an AI drafts the SQL, the gate checks it before the
            database ever sees it.
          </CardDescription>
        </CardHeader>
        <CardContent className='grid gap-3 text-sm md:grid-cols-3'>
          <div className='rounded-xl border p-3'>
            <div className='mb-1 font-semibold'>1. You ask</div>
            Plain English in: "How many appointments are scheduled in March?"
          </div>
          <div className='rounded-xl border p-3'>
            <div className='mb-1 font-semibold'>2. AI drafts SQL</div>
            A candidate query is produced for your question (mock generator by default).
          </div>
          <div className='rounded-xl border p-3'>
            <div className='mb-1 font-semibold'>3. The gate checks</div>
            Deterministic rules judge the query on its parsed structure - before anything runs.
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>The rules</CardTitle>
          <CardDescription>
            Every candidate query passes through all of them. Internal ids are shown once, then
            never needed again.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className='w-20'>Id</TableHead>
                <TableHead className='w-56'>Rule</TableHead>
                <TableHead>What it means</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {(explain.data?.rules ?? []).map((r) => (
                <TableRow key={r.id}>
                  <TableCell className='font-mono text-xs'>{r.id}</TableCell>
                  <TableCell className='font-medium'>{r.name}</TableCell>
                  <TableCell className='text-muted-foreground'>{r.plain}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>What the verdicts mean</CardTitle>
        </CardHeader>
        <CardContent className='space-y-2 text-sm'>
          {Object.entries(explain.data?.verdicts ?? {}).map(([verdict, copy]) => (
            <p key={verdict}>
              <span className='font-semibold'>{verdict}:</span> {copy}
            </p>
          ))}
        </CardContent>
      </Card>
    </div>
  )
}
