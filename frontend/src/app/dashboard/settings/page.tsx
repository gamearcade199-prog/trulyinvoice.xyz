'use client'

import DashboardLayout from '@/components/DashboardLayout'
import { useState, useEffect } from 'react'
import { 
  User, 
  Shield, 
  CreditCard, 
  Mail,
  Phone,
  Building,
  MapPin,
  Save,
  Loader2
} from 'lucide-react'
import { supabase } from '@/lib/supabase'
import BillingDashboard from '@/components/BillingDashboard'

export default function SettingsPage() {
  const [activeTab, setActiveTab] = useState('profile')
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [updatingPassword, setUpdatingPassword] = useState(false)
  const [user, setUser] = useState<any>(null)
  const [profile, setProfile] = useState({
    full_name: '',
    email: '',
    phone: '',
    company: '',
    address: ''
  })
  const [passwords, setPasswords] = useState({
    newPassword: '',
    confirmPassword: ''
  })

  useEffect(() => {
    loadUserData()
  }, [])

  async function loadUserData() {
    try {
      // Get current user
      const { data: { user: authUser }, error: authError } = await supabase.auth.getUser()
      
      if (authError || !authUser) {
        console.error('Error loading user:', authError)
        setLoading(false)
        return
      }

      console.log('Loaded user:', authUser) // Debug log
      console.log('User email:', authUser.email) // Debug log

      setUser(authUser)

      // Get user profile from users table
      const { data: profileData, error: profileError } = await supabase
        .from('users')
        .select('*')
        .eq('id', authUser.id)
        .single()

      console.log('Profile data:', profileData) // Debug log

      const userEmail = authUser.email || ''
      
      if (profileData) {
        setProfile({
          full_name: profileData.full_name || authUser.user_metadata?.full_name || '',
          email: userEmail,
          phone: profileData.phone || '',
          company: profileData.company || '',
          address: profileData.address || ''
        })
      } else {
        // Use auth metadata if profile doesn't exist
        setProfile({
          full_name: authUser.user_metadata?.full_name || '',
          email: userEmail,
          phone: '',
          company: '',
          address: ''
        })
      }

      console.log('Profile state set to:', { email: userEmail }) // Debug log

      setLoading(false)
    } catch (error) {
      console.error('Error loading user data:', error)
      setLoading(false)
    }
  }

  async function handleSaveProfile() {
    try {
      setSaving(true)

      if (!user) {
        alert('User not found. Please try logging in again.')
        setSaving(false)
        return
      }

      // Update or insert user profile
      const { error } = await supabase
        .from('users')
        .upsert({
          id: user.id,
          email: user.email,
          full_name: profile.full_name,
          phone: profile.phone,
          company: profile.company,
          address: profile.address,
          updated_at: new Date().toISOString()
        })

      if (error) {
        console.error('Error saving profile:', error)
        alert('Failed to save profile: ' + error.message)
        setSaving(false)
      } else {
        alert('Profile updated successfully!')
        setSaving(false)
      }
    } catch (error) {
      console.error('Error saving profile:', error)
      alert('Failed to save profile')
      setSaving(false)
    }
  }

  async function handleUpdatePassword() {
    try {
      // Validate passwords
      if (!passwords.newPassword || !passwords.confirmPassword) {
        alert('Please fill in both password fields')
        return
      }

      if (passwords.newPassword.length < 6) {
        alert('Password must be at least 6 characters long')
        return
      }

      if (passwords.newPassword !== passwords.confirmPassword) {
        alert('Passwords do not match')
        return
      }

      setUpdatingPassword(true)

      // Update password
      const { error } = await supabase.auth.updateUser({
        password: passwords.newPassword
      })

      if (error) {
        console.error('Error updating password:', error)
        alert('Failed to update password: ' + error.message)
        setUpdatingPassword(false)
      } else {
        alert('Password updated successfully!')
        setPasswords({ newPassword: '', confirmPassword: '' })
        setUpdatingPassword(false)
      }
    } catch (error) {
      console.error('Error updating password:', error)
      alert('Failed to update password')
      setUpdatingPassword(false)
    }
  }

  const tabs = [
    { id: 'profile', name: 'Profile', icon: User },
    { id: 'security', name: 'Security', icon: Shield },
    { id: 'billing', name: 'Billing', icon: CreditCard },
  ]

  return (
    <DashboardLayout>
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Settings</h1>
          <p className="text-gray-600 dark:text-gray-400 mt-1">Manage your account settings and billing.</p>
        </div>

        <div className="grid lg:grid-cols-4 gap-6">
          {/* Sidebar Tabs */}
          <div className="lg:col-span-1">
            <div className="bg-gray-50 dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 p-2">
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
            <div className="bg-gray-50 dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 p-6">
              {/* Loading State */}
              {loading ? (
                <div className="flex items-center justify-center py-12">
                  <Loader2 className="w-8 h-8 animate-spin text-blue-600 dark:text-blue-400" />
                </div>
              ) : (
                <>
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
                              value={profile.full_name}
                              onChange={(e) => setProfile({ ...profile, full_name: e.target.value })}
                              placeholder="Enter your full name"
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
                              value={profile.email}
                              placeholder="your.email@example.com"
                              disabled
                              className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-gray-100 dark:bg-gray-600 text-gray-900 dark:text-gray-300 cursor-not-allowed"
                              title="Email cannot be changed"
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
                              value={profile.phone}
                              onChange={(e) => setProfile({ ...profile, phone: e.target.value })}
                              placeholder="+91 98765 43210"
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
                              value={profile.company}
                              onChange={(e) => setProfile({ ...profile, company: e.target.value })}
                              placeholder="Your company name"
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
                            value={profile.address}
                            onChange={(e) => setProfile({ ...profile, address: e.target.value })}
                            placeholder="123 Main Street, Mumbai, Maharashtra 400001"
                            className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 focus:border-transparent transition-colors"
                          />
                        </div>

                        <div className="flex justify-end pt-4">
                          <button 
                            onClick={handleSaveProfile}
                            disabled={saving}
                            className="flex items-center gap-2 px-6 py-2.5 bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 text-white rounded-lg font-semibold transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                          >
                            {saving ? (
                              <>
                                <Loader2 className="w-4 h-4 animate-spin" />
                                Saving...
                              </>
                            ) : (
                              <>
                                <Save className="w-4 h-4" />
                                Save Changes
                              </>
                            )}
                          </button>
                        </div>
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
                        New Password
                      </label>
                      <input
                        type="password"
                        value={passwords.newPassword}
                        onChange={(e) => setPasswords({ ...passwords, newPassword: e.target.value })}
                        placeholder="Enter new password"
                        className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 focus:border-transparent transition-colors"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                        Confirm New Password
                      </label>
                      <input
                        type="password"
                        value={passwords.confirmPassword}
                        onChange={(e) => setPasswords({ ...passwords, confirmPassword: e.target.value })}
                        placeholder="Re-enter new password"
                        className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 focus:border-transparent transition-colors"
                      />
                    </div>

                    <div className="flex justify-end pt-4">
                      <button 
                        onClick={handleUpdatePassword}
                        disabled={updatingPassword}
                        className="flex items-center gap-2 px-6 py-2.5 bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 text-white rounded-lg font-semibold transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                      >
                        {updatingPassword ? (
                          <>
                            <Loader2 className="w-4 h-4 animate-spin" />
                            Updating...
                          </>
                        ) : (
                          'Update Password'
                        )}
                      </button>
                    </div>
                  </div>
                </div>
              )}

              {/* Billing Tab */}
              {activeTab === 'billing' && <BillingDashboard />}
                </>
              )}
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  )
}

