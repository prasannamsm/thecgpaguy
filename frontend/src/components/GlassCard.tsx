import { ReactNode } from 'react'

export function GlassCard({ children, className = '', ...props }: { children: ReactNode; className?: string; [key: string]: any }) {
  return <div className={`card glass ${className}`} {...props}>{children}</div>
}
