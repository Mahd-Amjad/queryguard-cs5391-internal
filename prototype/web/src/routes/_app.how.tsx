import { createFileRoute } from '@tanstack/react-router'
import { HowView } from '@/features/how'

export const Route = createFileRoute('/_app/how')({
  component: HowView,
})
