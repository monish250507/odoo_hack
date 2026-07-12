import React, { Component } from "react"
import type { ReactNode, ErrorInfo } from "react"
import { Button } from "./Button"

interface Props { children: ReactNode; fallback?: ReactNode }
interface State { hasError: boolean; error?: Error }

export class ErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false }
  static getDerivedStateFromError(error: Error): State { return { hasError: true, error } }
  componentDidCatch(error: Error, info: ErrorInfo) { console.error("[ErrorBoundary]", error, info) }
  render() {
    if (this.state.hasError) {
      if (this.props.fallback) return this.props.fallback
      return (
        <div className="flex flex-col items-center justify-center h-64 gap-4 text-center p-8">
          <div className="w-12 h-12 rounded-full bg-danger/10 flex items-center justify-center">
            <span className="text-xl">!</span>
          </div>
          <div>
            <h3 className="font-semibold" style={{ color: "var(--color-text-primary)" }}>Something went wrong</h3>
            <p className="text-sm mt-1" style={{ color: "var(--color-text-secondary)" }}>{this.state.error?.message}</p>
          </div>
          <Button variant="outline" size="sm" onClick={() => this.setState({ hasError: false })}>Try again</Button>
        </div>
      )
    }
    return this.props.children
  }
}
