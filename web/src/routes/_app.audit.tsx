import { createFileRoute } from '@tanstack/react-router'
import { AuditView } from '@/features/audit'

export const Route = createFileRoute('/_app/audit')({
  component: AuditView,
})
