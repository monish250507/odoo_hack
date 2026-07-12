import React from "react"
import { NavLink, useLocation } from "react-router-dom"
import { motion, AnimatePresence } from "framer-motion"
import { Leaf, LayoutDashboard, ShieldCheck, Activity, Award, FileText, Settings, User } from "lucide-react"
import { cn } from "../../lib/utils"

const NAV_ITEMS = [
  { id: "/", label: "Dashboard", icon: LayoutDashboard },
  { id: "/environmental", label: "Environmental", icon: Leaf },
  { id: "/social", label: "Social", icon: Activity },
  { id: "/governance", label: "Governance", icon: ShieldCheck },
  { id: "/gamification", label: "Gamification", icon: Award },
  { id: "/reports", label: "Reports", icon: FileText },
]

const BOTTOM_NAV_ITEMS = [
  { id: "/profile", label: "Profile", icon: User },
  { id: "/settings", label: "Settings", icon: Settings },
]

export const Sidebar = () => {
  const location = useLocation()

  return (
    <div className="w-64 min-h-screen glass border-r border-y-0 border-l-0 flex flex-col py-6">
      <div className="px-6 mb-8 flex items-center gap-3">
        <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-primary to-accent flex items-center justify-center shadow-lg shadow-primary/20">
          <Leaf className="w-4 h-4 text-white" />
        </div>
        <span className="font-semibold text-lg tracking-tight text-textPrimary">EcoSphere</span>
      </div>

      <nav className="flex-1 px-3 space-y-1">
        {NAV_ITEMS.map((item) => {
          const isActive = location.pathname === item.id
          const Icon = item.icon
          
          return (
            <NavLink
              key={item.id}
              to={item.id}
              className={({ isActive }) => cn(
                "relative w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors",
                isActive ? "text-primary" : "text-textSecondary hover:text-textPrimary hover:bg-black/5"
              )}
            >
              {/* Animated active background pill */}
              {isActive && (
                <motion.div
                  layoutId="active-pill"
                  className="absolute inset-0 bg-primary/10 rounded-lg"
                  transition={{ type: "spring", stiffness: 350, damping: 30 }}
                />
              )}
              
              {/* Animated left glowing indicator */}
              <AnimatePresence>
                {isActive && (
                  <motion.div
                    initial={{ opacity: 0, scaleY: 0 }}
                    animate={{ opacity: 1, scaleY: 1 }}
                    exit={{ opacity: 0, scaleY: 0 }}
                    transition={{ duration: 0.2 }}
                    className="absolute left-0 top-1.5 bottom-1.5 w-1 bg-primary rounded-r-full shadow-[0_0_8px_rgba(15,118,110,0.6)]"
                  />
                )}
              </AnimatePresence>

              <Icon className={cn("w-5 h-5 relative z-10", isActive ? "text-primary" : "text-textSecondary")} />
              <span className="relative z-10">{item.label}</span>
            </NavLink>
          )
        })}
      </nav>

      <div className="px-3 mt-auto space-y-1">
        {BOTTOM_NAV_ITEMS.map((item) => {
          const isActive = location.pathname === item.id
          const Icon = item.icon
          
          return (
            <NavLink
              key={item.id}
              to={item.id}
              className={({ isActive }) => cn(
                "relative w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors",
                isActive ? "text-primary" : "text-textSecondary hover:text-textPrimary hover:bg-black/5"
              )}
            >
              {isActive && (
                <motion.div
                  layoutId="active-pill"
                  className="absolute inset-0 bg-primary/10 rounded-lg"
                  transition={{ type: "spring", stiffness: 350, damping: 30 }}
                />
              )}
              <Icon className={cn("w-5 h-5 relative z-10", isActive ? "text-primary" : "text-textSecondary")} />
              <span className="relative z-10">{item.label}</span>
            </NavLink>
          )
        })}
      </div>
    </div>
  )
}
