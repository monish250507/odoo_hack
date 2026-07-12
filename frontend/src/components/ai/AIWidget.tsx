import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Drawer } from '../ui/Drawer'
import { Button } from '../ui/Button'
import { Input } from '../ui/Input'
import { GlassCard } from '../ui/GlassCard'
import { Sparkles, Send, Loader2, Leaf } from 'lucide-react'

interface Message {
  role: 'user' | 'ai'
  content: string
}

const SUGGESTED_PROMPTS = [
  'Estimate carbon for 500 kWh electricity',
  'Generate Q3 ESG narrative summary',
  'Detect anomalies in my emissions data',
  'Recommend challenges for my team',
]

export const AIWidget = () => {
  const [isOpen, setIsOpen] = useState(false)
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'ai',
      content: "Hello! I'm EcoSphere AI powered by LangGraph. I can help with carbon estimation, ESG report narratives, anomaly detection, and challenge recommendations. How can I help?",
    },
  ])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const handleSend = () => {
    if (!input.trim()) return
    const userMessage = input.trim()
    setInput('')
    setMessages((prev) => [...prev, { role: 'user', content: userMessage }])
    setIsLoading(true)

    // Simulate AI response (will connect to real API later)
    setTimeout(() => {
      setMessages((prev) => [
        ...prev,
        {
          role: 'ai',
          content: `Processing your request: "${userMessage}". In production, this routes through the LangGraph Supervisor to the appropriate agent (Carbon, Narrator, Anomaly, or Challenge).`,
        },
      ])
      setIsLoading(false)
    }, 1500)
  }

  const handleSuggest = (prompt: string) => {
    setInput(prompt)
  }

  return (
    <>
      {/* Floating Trigger Button */}
      <motion.button
        className="fixed bottom-8 right-8 z-40 w-14 h-14 rounded-full bg-gradient-to-br from-primary to-accent flex items-center justify-center shadow-xl shadow-primary/30 text-white"
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.95 }}
        transition={{ type: 'spring', stiffness: 400, damping: 20 }}
        onClick={() => setIsOpen(true)}
      >
        <Sparkles className="w-6 h-6" />
      </motion.button>

      <Drawer isOpen={isOpen} onClose={() => setIsOpen(false)} title="EcoSphere AI">
        <div className="flex flex-col h-full gap-4">
          {/* Suggested prompts */}
          {messages.length <= 1 && (
            <div className="space-y-2">
              <p className="text-xs font-medium text-textSecondary uppercase tracking-wide">Try asking…</p>
              <div className="flex flex-wrap gap-2">
                {SUGGESTED_PROMPTS.map((prompt) => (
                  <button
                    key={prompt}
                    onClick={() => handleSuggest(prompt)}
                    className="text-xs px-3 py-1.5 rounded-full border border-border bg-surface text-textSecondary hover:text-primary hover:border-primary/30 hover:bg-primary/5 transition-all"
                  >
                    {prompt}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Message Thread */}
          <div className="flex-1 overflow-y-auto space-y-4 py-2">
            <AnimatePresence initial={false}>
              {messages.map((msg, i) => (
                <motion.div
                  key={i}
                  initial={{ opacity: 0, y: 8 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.2 }}
                  className={`flex gap-3 ${msg.role === 'user' ? 'flex-row-reverse' : 'flex-row'}`}
                >
                  {msg.role === 'ai' && (
                    <div className="w-7 h-7 shrink-0 rounded-full bg-gradient-to-br from-primary to-accent flex items-center justify-center">
                      <Leaf className="w-3.5 h-3.5 text-white" />
                    </div>
                  )}
                  <div
                    className={`max-w-[85%] rounded-xl px-4 py-3 text-sm leading-relaxed ${
                      msg.role === 'user'
                        ? 'bg-primary text-white rounded-br-none'
                        : 'bg-black/5 text-textPrimary rounded-bl-none'
                    }`}
                  >
                    {msg.content}
                  </div>
                </motion.div>
              ))}

              {isLoading && (
                <motion.div
                  initial={{ opacity: 0, y: 8 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="flex gap-3"
                >
                  <div className="w-7 h-7 shrink-0 rounded-full bg-gradient-to-br from-primary to-accent flex items-center justify-center">
                    <Leaf className="w-3.5 h-3.5 text-white" />
                  </div>
                  <div className="bg-black/5 rounded-xl rounded-bl-none px-4 py-3">
                    <Loader2 className="w-4 h-4 text-textSecondary animate-spin" />
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          {/* Input Bar */}
          <div className="border-t border-border pt-4 flex gap-2">
            <Input
              placeholder="Ask EcoSphere AI…"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSend()}
              className="flex-1"
            />
            <Button
              variant="primary"
              size="md"
              onClick={handleSend}
              disabled={!input.trim() || isLoading}
            >
              <Send className="w-4 h-4" />
            </Button>
          </div>
        </div>
      </Drawer>
    </>
  )
}
