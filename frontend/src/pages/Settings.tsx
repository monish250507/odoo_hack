import React, { useState } from 'react'
import { PageTransition } from '../components/ui/PageTransition'
import { GlassCard } from '../components/ui/GlassCard'
import { Button } from '../components/ui/Button'
import { Input } from '../components/ui/Input'
import { Select } from '../components/ui/Select'
import { Settings as SettingsIcon, Bell, Lock, Globe } from 'lucide-react'

const SECTIONS = [
  { id: 'general', label: 'General', icon: SettingsIcon },
  { id: 'notifications', label: 'Notifications', icon: Bell },
  { id: 'security', label: 'Security', icon: Lock },
  { id: 'regional', label: 'Regional', icon: Globe },
]

export const Settings = () => {
  const [activeSection, setActiveSection] = useState('general')

  return (
    <PageTransition className="max-w-6xl mx-auto space-y-8">
      <header>
        <h1 className="text-3xl font-semibold tracking-tight text-textPrimary">Settings</h1>
        <p className="text-textSecondary mt-1">Manage system and account preferences.</p>
      </header>

      <div className="grid grid-cols-12 gap-6">
        {/* Settings Nav */}
        <div className="col-span-3">
          <GlassCard className="p-2">
            <nav className="space-y-1">
              {SECTIONS.map((section) => {
                const Icon = section.icon
                const isActive = activeSection === section.id
                return (
                  <button
                    key={section.id}
                    onClick={() => setActiveSection(section.id)}
                    className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all ${
                      isActive
                        ? 'bg-primary/10 text-primary'
                        : 'text-textSecondary hover:text-textPrimary hover:bg-black/5'
                    }`}
                  >
                    <Icon className="w-4 h-4" />
                    {section.label}
                  </button>
                )
              })}
            </nav>
          </GlassCard>
        </div>

        {/* Settings Content */}
        <div className="col-span-9">
          {activeSection === 'general' && (
            <GlassCard>
              <h2 className="text-lg font-semibold text-textPrimary mb-6 pb-4 border-b border-border">General</h2>
              <form className="space-y-6">
                <div className="space-y-2">
                  <label className="text-sm font-medium text-textPrimary">Organisation Name</label>
                  <Input defaultValue="EcoSphere Corp" />
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium text-textPrimary">Industry</label>
                  <Select defaultValue="technology">
                    <option value="technology">Technology</option>
                    <option value="manufacturing">Manufacturing</option>
                    <option value="retail">Retail</option>
                    <option value="finance">Finance</option>
                  </Select>
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium text-textPrimary">Fiscal Year Start</label>
                  <Select defaultValue="01">
                    <option value="01">January</option>
                    <option value="04">April</option>
                    <option value="07">July</option>
                    <option value="10">October</option>
                  </Select>
                </div>
                <div className="pt-4">
                  <Button variant="primary">Save Changes</Button>
                </div>
              </form>
            </GlassCard>
          )}
          {activeSection === 'notifications' && (
            <GlassCard>
              <h2 className="text-lg font-semibold text-textPrimary mb-6 pb-4 border-b border-border">Notifications</h2>
              <div className="space-y-6">
                {[
                  { label: 'New compliance issue', desc: 'Receive alerts when a new issue is flagged' },
                  { label: 'Goal milestone reached', desc: 'Notify when a department reaches a goal milestone' },
                  { label: 'AI Insights ready', desc: 'Get notified when an AI report is generated' },
                ].map((item) => (
                  <div key={item.label} className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-textPrimary">{item.label}</p>
                      <p className="text-xs text-textSecondary mt-0.5">{item.desc}</p>
                    </div>
                    <button className="relative w-11 h-6 bg-primary rounded-full transition-all">
                      <span className="absolute right-1 top-1 w-4 h-4 bg-white rounded-full shadow transition-all" />
                    </button>
                  </div>
                ))}
              </div>
            </GlassCard>
          )}
          {activeSection === 'security' && (
            <GlassCard>
              <h2 className="text-lg font-semibold text-textPrimary mb-6 pb-4 border-b border-border">Security</h2>
              <form className="space-y-6">
                <div className="space-y-2">
                  <label className="text-sm font-medium text-textPrimary">Current Password</label>
                  <Input type="password" placeholder="••••••••" />
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium text-textPrimary">New Password</label>
                  <Input type="password" placeholder="••••••••" />
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium text-textPrimary">Confirm New Password</label>
                  <Input type="password" placeholder="••••••••" />
                </div>
                <div className="pt-4">
                  <Button variant="primary">Update Password</Button>
                </div>
              </form>
            </GlassCard>
          )}
          {activeSection === 'regional' && (
            <GlassCard>
              <h2 className="text-lg font-semibold text-textPrimary mb-6 pb-4 border-b border-border">Regional</h2>
              <form className="space-y-6">
                <div className="space-y-2">
                  <label className="text-sm font-medium text-textPrimary">Timezone</label>
                  <Select defaultValue="Asia/Kolkata">
                    <option value="UTC">UTC</option>
                    <option value="Asia/Kolkata">Asia/Kolkata (IST)</option>
                    <option value="America/New_York">America/New_York (EST)</option>
                  </Select>
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium text-textPrimary">Date Format</label>
                  <Select defaultValue="dd-mm-yyyy">
                    <option value="dd-mm-yyyy">DD-MM-YYYY</option>
                    <option value="mm-dd-yyyy">MM-DD-YYYY</option>
                    <option value="yyyy-mm-dd">YYYY-MM-DD</option>
                  </Select>
                </div>
                <div className="pt-4">
                  <Button variant="primary">Save Preferences</Button>
                </div>
              </form>
            </GlassCard>
          )}
        </div>
      </div>
    </PageTransition>
  )
}
