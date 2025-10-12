'use client'

import DashboardLayout from '@/components/DashboardLayout'
import { useState } from 'react'
import { 
  User, 
  Bell, 
  Shield, 
  CreditCard, 
  Globe, 
  Mail,
  Phone,
  Building,
  MapPin,
  Save,
  Moon,
  Sun
} from 'lucide-react'
import { useTheme } from '@/components/ThemeProvider'

export default function SettingsPage() {
  const { theme, toggleTheme } = useTheme()
  const [activeTab, setActiveTab] = useState('profile')

  const tabs = [
    { id: 'profile', name: 'Profile', icon: User },
    { id: 'notifications', name: 'Notifications', icon: Bell },
    { id: 'security', name: 'Security', icon: Shield },
    { id: 'billing', name: 'Billing', icon: CreditCard },
    { id: 'preferences', name: 'Preferences', icon: Globe },
  ]

  return (
    <DashboardLayout>
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Settings</h1>
          <p className="text-gray-600 dark:text-gray-400 mt-1">Manage your account settings and preferences.</p>
        </div>

        <div className="grid lg:grid-cols-4 gap-6">
          {/* Sidebar Tabs */}
          <div className="lg:col-span-1">
            <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-2">
              <nav className="space-y-1">
                {tabs.map((tab) => {
                  const Icon = tab.icon
                  return (
                    <button
                      key={tab.id}
                      onClick={() => setActiveTab(tab.id)}
                      className={`
                        w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-colors text-left
                        ${activeTab === tab.id
                          ? 'bg-blue-50 dark:bg-blue-900/50 text-blue-600 dark:text-blue-400 font-semibold'
                          : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
                        }
                      `}
                    >
                      <Icon className="w-5 h-5" />
                      <span>{tab.name}</span>
                    </button>
                  )
                })}
              </nav>
            </div>
          </div>

          {/* Content Area */}
          <div className="lg:col-span-3">
            <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-6">
              {/* Profile Tab */}
              {activeTab === 'profile' && (
                <div className="space-y-6">
                  <div>
                    <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">Profile Information</h2>
                    <p className="text-gray-600 dark:text-gray-400 text-sm mb-6">Update your account profile information and email address.</p>
                  </div>

                  <div className="space-y-4">
                    <div className="grid md:grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                          Full Name
                        </label>
                        <input
                          type="text"
                          defaultValue="John Doe"
                          className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 focus:border-transparent transition-colors"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                          <Mail className="w-4 h-4 inline mr-1" />
                          Email Address
                        </label>
                        <input
                          type="email"
                          defaultValue="john@example.com"
                          className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 focus:border-transparent transition-colors"
                        />
                      </div>
                    </div>

                    <div className="grid md:grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                          <Phone className="w-4 h-4 inline mr-1" />
                          Phone Number
                        </label>
                        <input
                          type="tel"
                          defaultValue="+91 98765 43210"
                          className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 focus:border-transparent transition-colors"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                          <Building className="w-4 h-4 inline mr-1" />
                          Company Name
                        </label>
                        <input
                          type="text"
                          defaultValue="Acme Corp"
                          className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 focus:border-transparent transition-colors"
                        />
                      </div>
                    </div>

                    <div>
                      <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                        <MapPin className="w-4 h-4 inline mr-1" />
                        Address
                      </label>
                      <textarea
                        rows={3}
                        defaultValue="123 Main Street, Mumbai, Maharashtra 400001"
                        className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 focus:border-transparent transition-colors"
                      />
                    </div>

                    <div className="flex justify-end pt-4">
                      <button className="flex items-center gap-2 px-6 py-2.5 bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 text-white rounded-lg font-semibold transition-colors">
                        <Save className="w-4 h-4" />
                        Save Changes
                      </button>
                    </div>
                  </div>
                </div>
              )}

              {/* Notifications Tab */}
              {activeTab === 'notifications' && (
                <div className="space-y-6">
                  <div>
                    <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">Notification Preferences</h2>
                    <p className="text-gray-600 dark:text-gray-400 text-sm mb-6">Manage how you receive notifications.</p>
                  </div>

                  <div className="space-y-4">
                    {[
                      { title: 'Email Notifications', description: 'Receive email updates about your invoices' },
                      { title: 'Invoice Processing', description: 'Get notified when invoices are processed' },
                      { title: 'Monthly Reports', description: 'Receive monthly summary reports' },
                      { title: 'Payment Reminders', description: 'Get reminders for unpaid invoices' },
                      { title: 'New Features', description: 'Learn about new features and updates' },
                    ].map((item, index) => (
                      <div key={index} className="flex items-center justify-between p-4 rounded-lg border border-gray-200 dark:border-gray-700">
                        <div>
                          <h3 className="font-semibold text-gray-900 dark:text-white">{item.title}</h3>
                          <p className="text-sm text-gray-600 dark:text-gray-400">{item.description}</p>
                        </div>
                        <label className="relative inline-flex items-center cursor-pointer">
                          <input type="checkbox" defaultChecked={index < 3} className="sr-only peer" />
                          <div className="w-11 h-6 bg-gray-300 dark:bg-gray-600 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                        </label>
                      </div>
                    ))}
                  </div>

                  <div className="flex justify-end pt-4">
                    <button className="flex items-center gap-2 px-6 py-2.5 bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 text-white rounded-lg font-semibold transition-colors">
                      <Save className="w-4 h-4" />
                      Save Preferences
                    </button>
                  </div>
                </div>
              )}

              {/* Security Tab */}
              {activeTab === 'security' && (
                <div className="space-y-6">
                  <div>
                    <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">Security Settings</h2>
                    <p className="text-gray-600 dark:text-gray-400 text-sm mb-6">Manage your password and security preferences.</p>
                  </div>

                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                        Current Password
                      </label>
                      <input
                        type="password"
                        className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 focus:border-transparent transition-colors"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                        New Password
                      </label>
                      <input
                        type="password"
                        className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 focus:border-transparent transition-colors"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                        Confirm New Password
                      </label>
                      <input
                        type="password"
                        className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 focus:border-transparent transition-colors"
                      />
                    </div>

                    <div className="flex justify-end pt-4">
                      <button className="flex items-center gap-2 px-6 py-2.5 bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 text-white rounded-lg font-semibold transition-colors">
                        Update Password
                      </button>
                    </div>
                  </div>
                </div>
              )}

              {/* Billing Tab */}
              {activeTab === 'billing' && (
                <div className="space-y-6">
                  <div>
                    <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">Billing & Subscription</h2>
                    <p className="text-gray-600 dark:text-gray-400 text-sm mb-6">Manage your subscription and payment methods.</p>
                  </div>

                  <div className="p-6 rounded-lg bg-gradient-to-br from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20 border border-blue-200 dark:border-blue-800">
                    <div className="flex items-center justify-between mb-4">
                      <div>
                        <h3 className="text-lg font-bold text-gray-900 dark:text-white">Starter Plan</h3>
                        <p className="text-sm text-gray-600 dark:text-gray-400">Up to 100 invoices per month</p>
                      </div>
                      <div className="text-right">
                        <p className="text-3xl font-bold text-gray-900 dark:text-white">Free</p>
                        <p className="text-sm text-gray-600 dark:text-gray-400">Forever</p>
                      </div>
                    </div>
                    <button className="w-full mt-4 px-6 py-2.5 bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 text-white rounded-lg font-semibold transition-colors">
                      Upgrade to Pro
                    </button>
                  </div>

                  <div>
                    <h3 className="font-semibold text-gray-900 dark:text-white mb-3">Payment Methods</h3>
                    <div className="p-4 rounded-lg border border-gray-200 dark:border-gray-700 text-center">
                      <p className="text-gray-500 dark:text-gray-400">No payment methods added</p>
                      <button className="mt-2 text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 font-semibold">
                        + Add Payment Method
                      </button>
                    </div>
                  </div>
                </div>
              )}

              {/* Preferences Tab */}
              {activeTab === 'preferences' && (
                <div className="space-y-6">
                  <div>
                    <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">Preferences</h2>
                    <p className="text-gray-600 dark:text-gray-400 text-sm mb-6">Customize your experience.</p>
                  </div>

                  <div className="space-y-4">
                    {/* Theme Toggle */}
                    <div className="flex items-center justify-between p-4 rounded-lg border border-gray-200 dark:border-gray-700">
                      <div>
                        <h3 className="font-semibold text-gray-900 dark:text-white flex items-center gap-2">
                          {theme === 'light' ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
                          Theme
                        </h3>
                        <p className="text-sm text-gray-600 dark:text-gray-400">
                          Current: {theme === 'light' ? 'Light Mode' : 'Dark Mode'}
                        </p>
                      </div>
                      <button
                        onClick={toggleTheme}
                        className="px-4 py-2 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 rounded-lg font-semibold text-gray-700 dark:text-gray-300 transition-colors"
                      >
                        Switch to {theme === 'light' ? 'Dark' : 'Light'}
                      </button>
                    </div>

                    {/* Language */}
                    <div className="flex items-center justify-between p-4 rounded-lg border border-gray-200 dark:border-gray-700">
                      <div>
                        <h3 className="font-semibold text-gray-900 dark:text-white">Language</h3>
                        <p className="text-sm text-gray-600 dark:text-gray-400">Select your preferred language</p>
                      </div>
                      <select className="px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 transition-colors">
                        <option>English</option>
                        <option>हिन्दी (Hindi)</option>
                        <option>తెలుగు (Telugu)</option>
                        <option>தமிழ் (Tamil)</option>
                      </select>
                    </div>

                    {/* Currency */}
                    <div className="flex items-center justify-between p-4 rounded-lg border border-gray-200 dark:border-gray-700">
                      <div>
                        <h3 className="font-semibold text-gray-900 dark:text-white">Currency</h3>
                        <p className="text-sm text-gray-600 dark:text-gray-400">Default currency for invoices</p>
                      </div>
                      <select className="px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 transition-colors">
                        <option>₹ INR (Indian Rupee)</option>
                        <option>$ USD (US Dollar)</option>
                        <option>€ EUR (Euro)</option>
                      </select>
                    </div>

                    {/* Date Format */}
                    <div className="flex items-center justify-between p-4 rounded-lg border border-gray-200 dark:border-gray-700">
                      <div>
                        <h3 className="font-semibold text-gray-900 dark:text-white">Date Format</h3>
                        <p className="text-sm text-gray-600 dark:text-gray-400">How dates are displayed</p>
                      </div>
                      <select className="px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 transition-colors">
                        <option>DD/MM/YYYY</option>
                        <option>MM/DD/YYYY</option>
                        <option>YYYY-MM-DD</option>
                      </select>
                    </div>
                  </div>

                  <div className="flex justify-end pt-4">
                    <button className="flex items-center gap-2 px-6 py-2.5 bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 text-white rounded-lg font-semibold transition-colors">
                      <Save className="w-4 h-4" />
                      Save Preferences
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  )
}
