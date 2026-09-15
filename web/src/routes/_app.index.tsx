import { createFileRoute } from '@tanstack/react-router'
import { AskView } from '@/features/ask'

export const Route = createFileRoute('/_app/')({
  component: AskView,
})
