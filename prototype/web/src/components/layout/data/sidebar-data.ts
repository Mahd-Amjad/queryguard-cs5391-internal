import { MessageCircleQuestion, Scale, Activity, ScrollText, ShieldCheck } from 'lucide-react'
import { type SidebarData } from '../types'

export const sidebarData: SidebarData = {
  user: {
    name: 'QueryGuard',
    email: 'safety gate for LLM-generated SQL',
    avatar: '',
  },
  teams: [
    {
      name: 'QueryGuard',
      logo: ShieldCheck,
      plan: 'CS5391 Group Project',
    },
  ],
  navGroups: [
    {
      title: 'Navigation',
      items: [
        {
          title: 'Ask a question',
          url: '/',
          icon: MessageCircleQuestion,
        },
        {
          title: 'How it works',
          url: '/how',
          icon: Scale,
        },
        {
          title: 'Metrics',
          url: '/metrics',
          icon: Activity,
        },
        {
          title: 'Audit log',
          url: '/audit',
          icon: ScrollText,
        },
      ],
    },
  ],
}
