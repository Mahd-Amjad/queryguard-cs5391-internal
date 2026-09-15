import { useLayout } from '@/context/layout-provider'
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarRail,
} from '@/components/ui/sidebar'
import { sidebarData } from './data/sidebar-data'
import { NavGroup } from './nav-group'

export function AppSidebar() {
  const { collapsible, variant } = useLayout()
  return (
    <Sidebar collapsible={collapsible} variant={variant}>
      <SidebarHeader>
        <div className='group-data-[collapsible=icon]:flex flex items-center gap-2 px-2 py-1.5 justify-center'>
          <svg aria-hidden='true' viewBox='0 0 24 24' fill='none' stroke='#e74c3c' strokeWidth='2' strokeLinecap='round' strokeLinejoin='round' className='h-6 w-6'>
            <path d='M12 3l7 3v5c0 4.6-2.9 8-7 10-4.1-2-7-5.4-7-10V6z' />
            <path d='M9 12l2 2 4-4' />
          </svg>
          <div className='group-data-[collapsible=icon]:hidden'>
            <div className='text-sm leading-none font-bold'>QueryGuard</div>
            <div className='text-secondary small text-end' style={{ marginTop: '-0.35rem;' }}>
              <span className='font-script text-xs'>check first,</span> then run
            </div>
          </div>
        </div>
      </SidebarHeader>
      <SidebarContent>
        {sidebarData.navGroups.map((props) => (
          <NavGroup key={props.title} {...props} />
        ))}
      </SidebarContent>
      <SidebarFooter>
        <div className='text-muted-foreground group-data-[collapsible=icon]:justify-center flex items-start gap-2 p-2 text-xs'>
          <svg viewBox='0 0 24 24' fill='none' stroke='currentColor' strokeWidth='2' strokeLinecap='round' strokeLinejoin='round' className='mt-0.5 h-3.5 w-3.5 shrink-0'>
            <rect x='5' y='11' width='14' height='9' rx='2' />
            <path d='M8 11V7a4 4 0 0 1 8 0v4' />
          </svg>
          <span className='group-data-[collapsible=icon]:hidden'>Every query checked before it touches the database.</span>
        </div>
      </SidebarFooter>
      <SidebarRail />
    </Sidebar>
  )
}
