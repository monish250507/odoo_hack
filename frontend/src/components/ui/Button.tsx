import React from "react"
import { motion } from "framer-motion"
import type { HTMLMotionProps } from "framer-motion"
import { cn } from "../../lib/utils"

interface ButtonProps extends Omit<HTMLMotionProps<"button">, "children"> {
  variant?: "primary" | "secondary" | "outline" | "ghost"
  size?: "sm" | "md" | "lg"
  children?: React.ReactNode
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "primary", size = "md", children, ...props }, ref) => {
    const baseStyles = "relative inline-flex items-center justify-center font-medium transition-colors overflow-hidden rounded-lg focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary disabled:opacity-50 disabled:pointer-events-none"

    const variants = {
      primary: "bg-primary text-white hover:bg-[#0d645d] border border-transparent shadow-sm",
      secondary: "bg-secondary text-white hover:bg-[#104324] border border-transparent shadow-sm",
      outline: "border text-textPrimary hover:bg-black/5",
      ghost: "bg-transparent text-textSecondary hover:text-textPrimary hover:bg-black/5",
    }

    const sizes = { sm: "h-8 px-3 text-sm", md: "h-10 px-4 text-sm", lg: "h-12 px-6 text-base" }

    return (
      <motion.button
        ref={ref}
        whileHover={{ y: -2, scale: 1.02, boxShadow: "0 8px 16px -4px rgba(15, 118, 110, 0.3)" }}
        whileTap={{ scale: 0.98 }}
        transition={{ type: "spring", stiffness: 400, damping: 25 }}
        className={cn(baseStyles, variants[variant], sizes[size], className)}
        {...props}
      >
        {(variant === "primary" || variant === "secondary") && (
          <motion.div
            className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent -translate-x-full"
            whileHover={{ translateX: ["-100%", "100%"] }}
            transition={{ duration: 0.8, ease: "easeInOut" }}
          />
        )}
        <span className="relative z-10 flex items-center gap-2">{children}</span>
      </motion.button>
    )
  }
)
Button.displayName = "Button"
