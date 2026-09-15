import { createFileRoute } from '@tanstack/react-router'
import { MetricsView } from '@/features/metrics'

export const Route = createFileRoute('/_app/metrics')({
  component: MetricsView,
})
