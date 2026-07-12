import { motion } from "framer-motion"
import type { HTMLMotionProps } from "framer-motion"
import React from "react"

export const PageTransition = ({ children, ...props }: HTMLMotionProps<"div"> & { children?: React.ReactNode }) => (
  <motion.div
    initial={{ opacity: 0, y: 12 }}
    animate={{ opacity: 1, y: 0 }}
    exit={{ opacity: 0, y: -12 }}
    transition={{ duration: 0.25, ease: "easeOut" }}
    {...props}
  >
    {children}
  </motion.div>
)
