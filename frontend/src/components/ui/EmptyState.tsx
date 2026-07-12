import React from 'react'
import { Button } from './Button'

interface EmptyStateProps {
  icon?: React.ReactNode
  title: string
  description?: string
  action?: { label: string; onClick: () => void }
}

export function EmptyState({ icon, title, description, action }: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-16 gap-4 text-center">
      {icon && (
        <div className="w-16 h-16 rounded-2xl bg-black/5 flex items-center justify-center text-textSecondary">
          {icon}
        </div>
      )}
      <div>
        <h3 className="font-semibold text-textPrimary">{title}</h3>
        {description && <p className="text-sm text-textSecondary mt-1 max-w-sm">{description}</p>}
      </div>
      {action && (
        <Button variant="primary" size="sm" onClick={action.onClick}>
          {action.label}
        </Button>
      )}
    </div>
  )
}
