import { NavLink, Outlet } from 'react-router-dom'

interface LayoutProps {
  role: 'admin' | 'student'
}

export function Layout({ role }: LayoutProps) {
  const links = role === 'admin'
    ? [
        { to: '/admin', label: 'Dashboard' },
        { to: '/admin/courses', label: 'Courses' },
        { to: '/admin/staging', label: 'Review' },
      ]
    : [
        { to: '/student', label: 'Dashboard' },
      ]

  return (
    <div className="layout">
      <nav className="sidebar">
        <div className="sidebar-brand">thecgpaguy <span>●</span></div>
        {links.map(l => (
          <NavLink key={l.to} to={l.to} end className={({ isActive }) => `sidebar-link ${isActive ? 'active' : ''}`}>
            {l.label}
          </NavLink>
        ))}
        <div style={{ flex: 1 }} />
        <NavLink to="/" className="sidebar-link" style={{ borderTop: '1px solid rgba(255,255,255,0.1)', paddingTop: '1rem' }}>
          ← Switch Role
        </NavLink>
      </nav>
      <main className="main-content">
        <Outlet />
      </main>
    </div>
  )
}
