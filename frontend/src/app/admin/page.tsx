'use client'

import { useState, useEffect } from 'react'
import { supabase } from '@/lib/supabase'
import { useRouter } from 'next/navigation'
import { 
  Search, 
  Users, 
  Crown, 
  TrendingUp, 
  Activity,
  Shield,
  X,
  Check,
  AlertCircle,
  ChevronDown,
  RefreshCw,
  Download,
  Filter
} from 'lucide-react'
import DashboardLayout from '@/components/DashboardLayout'

// ⚠️ ADMIN EMAILS - Only these can access admin panel
const ADMIN_EMAILS = [
  'akibhusain830@gmail.com',  // Primary admin
  'admin@trulyinvoice.com',
]

interface User {
  id: string
  email: string
  plan: string
  custom_batch_limit: number | null
  created_at: string
  last_sign_in_at: string | null
}

interface AdminStats {
  totalUsers: number
  freeUsers: number
  paidUsers: number
  enterpriseUsers: number
  totalRevenue: number
}

export default function AdminPanel() {
  const router = useRouter()
  const [isAdmin, setIsAdmin] = useState(false)
  const [loading, setLoading] = useState(true)
  const [currentUser, setCurrentUser] = useState<any>(null)
  
  // User management
  const [users, setUsers] = useState<User[]>([])
  const [filteredUsers, setFilteredUsers] = useState<User[]>([])
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedPlanFilter, setSelectedPlanFilter] = useState('all')
  
  // Statistics
  const [stats, setStats] = useState<AdminStats>({
    totalUsers: 0,
    freeUsers: 0,
    paidUsers: 0,
    enterpriseUsers: 0,
    totalRevenue: 0
  })
  
  // UI state
  const [editingUser, setEditingUser] = useState<User | null>(null)
  const [editPlan, setEditPlan] = useState('')
  const [editCustomLimit, setEditCustomLimit] = useState('')
  const [saveLoading, setSaveLoading] = useState(false)
  const [successMessage, setSuccessMessage] = useState('')
  const [errorMessage, setErrorMessage] = useState('')

  useEffect(() => {
    checkAdmin()
  }, [])

  useEffect(() => {
    if (isAdmin) {
      loadUsers()
      loadStats()
    }
  }, [isAdmin])

  useEffect(() => {
    filterUsers()
  }, [searchQuery, selectedPlanFilter, users])

  async function checkAdmin() {
    const { data: { user } } = await supabase.auth.getUser()
    
    if (!user) {
      router.push('/auth?mode=login&redirect=/admin')
      return
    }

    if (ADMIN_EMAILS.includes(user.email || '')) {
      setIsAdmin(true)
      setCurrentUser(user)
    } else {
      router.push('/')
    }
    
    setLoading(false)
  }

  async function loadUsers() {
    const { data, error } = await supabase
      .from('users')
      .select('id, email, plan, custom_batch_limit, created_at, last_sign_in_at')
      .order('created_at', { ascending: false })
      .limit(100)

    if (error) {
      console.error('Error loading users:', error)
      setErrorMessage('Failed to load users')
      return
    }

    setUsers(data || [])
  }

  async function loadStats() {
    const { data: allUsers, error } = await supabase
      .from('users')
      .select('plan')

    if (error || !allUsers) return

    const stats: AdminStats = {
      totalUsers: allUsers.length,
      freeUsers: allUsers.filter(u => u.plan === 'Free').length,
      paidUsers: allUsers.filter(u => ['Basic', 'Pro', 'Ultra', 'Max'].includes(u.plan)).length,
      enterpriseUsers: allUsers.filter(u => u.plan === 'Enterprise').length,
      totalRevenue: 0 // TODO: Calculate from subscription data
    }

    setStats(stats)
  }

  function filterUsers() {
    let filtered = users

    // Filter by search query
    if (searchQuery) {
      filtered = filtered.filter(u => 
        u.email.toLowerCase().includes(searchQuery.toLowerCase()) ||
        u.id.toLowerCase().includes(searchQuery.toLowerCase())
      )
    }

    // Filter by plan
    if (selectedPlanFilter !== 'all') {
      filtered = filtered.filter(u => u.plan === selectedPlanFilter)
    }

    setFilteredUsers(filtered)
  }

  function openEditModal(user: User) {
    setEditingUser(user)
    setEditPlan(user.plan)
    setEditCustomLimit(user.custom_batch_limit?.toString() || '')
    setSuccessMessage('')
    setErrorMessage('')
  }

  function closeEditModal() {
    setEditingUser(null)
    setEditPlan('')
    setEditCustomLimit('')
  }

  async function saveUserChanges() {
    if (!editingUser) return

    setSaveLoading(true)
    setSuccessMessage('')
    setErrorMessage('')

    const updates: any = {
      plan: editPlan
    }

    if (editCustomLimit) {
      updates.custom_batch_limit = parseInt(editCustomLimit)
    } else {
      updates.custom_batch_limit = null
    }

    const { error } = await supabase
      .from('users')
      .update(updates)
      .eq('id', editingUser.id)

    setSaveLoading(false)

    if (error) {
      setErrorMessage(`Failed to update user: ${error.message}`)
      return
    }

    setSuccessMessage(`✅ Updated ${editingUser.email}`)
    
    // Reload users
    await loadUsers()
    await loadStats()
    
    setTimeout(() => {
      closeEditModal()
    }, 1500)
  }

  function getPlanBadgeColor(plan: string) {
    const colors: Record<string, string> = {
      'Free': 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-200',
      'Basic': 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
      'Pro': 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200',
      'Ultra': 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-200',
      'Max': 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
      'Enterprise': 'bg-gradient-to-r from-yellow-400 to-yellow-600 text-white font-bold'
    }
    return colors[plan] || colors['Free']
  }

  function getPlanLimit(plan: string) {
    const limits: Record<string, string> = {
      'Free': '1 file',
      'Basic': '5 files',
      'Pro': '10 files',
      'Ultra': '50 files',
      'Max': '100 files',
      'Enterprise': 'Custom'
    }
    return limits[plan] || '1 file'
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900">
        <div className="text-center">
          <RefreshCw className="w-8 h-8 animate-spin text-blue-600 mx-auto mb-4" />
          <p className="text-gray-600 dark:text-gray-400">Checking access...</p>
        </div>
      </div>
    )
  }

  if (!isAdmin) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900">
        <div className="text-center">
          <Shield className="w-16 h-16 text-red-500 mx-auto mb-4" />
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">Access Denied</h1>
          <p className="text-gray-600 dark:text-gray-400">You don't have permission to access this page.</p>
        </div>
      </div>
    )
  }

  return (
    <DashboardLayout>
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
        {/* Header */}
        <div className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-3xl font-bold text-gray-900 dark:text-white flex items-center gap-3">
                  <Shield className="w-8 h-8 text-blue-600" />
                  Admin Panel
                </h1>
                <p className="text-gray-600 dark:text-gray-400 mt-1">
                  Manage users, plans, and limits • Logged in as {currentUser?.email}
                </p>
              </div>
              <button
                onClick={() => loadUsers()}
                className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                <RefreshCw className="w-4 h-4" />
                Refresh
              </button>
            </div>
          </div>
        </div>

        {/* Statistics Cards */}
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            {/* Total Users */}
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 border border-gray-200 dark:border-gray-700">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600 dark:text-gray-400">Total Users</p>
                  <p className="text-3xl font-bold text-gray-900 dark:text-white mt-1">{stats.totalUsers}</p>
                </div>
                <Users className="w-10 h-10 text-blue-600" />
              </div>
              <p className="text-sm text-green-600 dark:text-green-400 mt-2">All registered users</p>
            </div>

            {/* Free Users */}
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 border border-gray-200 dark:border-gray-700">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600 dark:text-gray-400">Free Plan</p>
                  <p className="text-3xl font-bold text-gray-900 dark:text-white mt-1">{stats.freeUsers}</p>
                </div>
                <Activity className="w-10 h-10 text-gray-600" />
              </div>
              <p className="text-sm text-gray-600 dark:text-gray-400 mt-2">
                {Math.round((stats.freeUsers / stats.totalUsers) * 100)}% of total
              </p>
            </div>

            {/* Paid Users */}
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 border border-gray-200 dark:border-gray-700">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600 dark:text-gray-400">Paid Plans</p>
                  <p className="text-3xl font-bold text-gray-900 dark:text-white mt-1">{stats.paidUsers}</p>
                </div>
                <TrendingUp className="w-10 h-10 text-green-600" />
              </div>
              <p className="text-sm text-green-600 dark:text-green-400 mt-2">
                {Math.round((stats.paidUsers / stats.totalUsers) * 100)}% conversion
              </p>
            </div>

            {/* Enterprise */}
            <div className="bg-gradient-to-br from-yellow-400 to-yellow-600 rounded-lg shadow p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-yellow-50">Enterprise</p>
                  <p className="text-3xl font-bold text-white mt-1">{stats.enterpriseUsers}</p>
                </div>
                <Crown className="w-10 h-10 text-white" />
              </div>
              <p className="text-sm text-yellow-50 mt-2">Premium customers</p>
            </div>
          </div>

          {/* Search and Filters */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow border border-gray-200 dark:border-gray-700 p-6 mb-6">
            <div className="flex flex-col md:flex-row gap-4">
              {/* Search */}
              <div className="flex-1 relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                <input
                  type="text"
                  placeholder="Search by email or user ID..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                />
              </div>

              {/* Plan Filter */}
              <div className="relative">
                <Filter className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                <select
                  value={selectedPlanFilter}
                  onChange={(e) => setSelectedPlanFilter(e.target.value)}
                  className="pl-10 pr-10 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white appearance-none"
                >
                  <option value="all">All Plans</option>
                  <option value="Free">Free</option>
                  <option value="Basic">Basic</option>
                  <option value="Pro">Pro</option>
                  <option value="Ultra">Ultra</option>
                  <option value="Max">Max</option>
                  <option value="Enterprise">Enterprise</option>
                </select>
                <ChevronDown className="absolute right-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400 pointer-events-none" />
              </div>

              {/* Export */}
              <button className="flex items-center gap-2 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors text-gray-900 dark:text-white">
                <Download className="w-4 h-4" />
                Export
              </button>
            </div>

            <div className="mt-4 text-sm text-gray-600 dark:text-gray-400">
              Showing {filteredUsers.length} of {users.length} users
            </div>
          </div>

          {/* Users Table */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow border border-gray-200 dark:border-gray-700 overflow-hidden">
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                <thead className="bg-gray-50 dark:bg-gray-900">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                      User
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                      Plan
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                      Batch Limit
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                      Joined
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                      Last Active
                    </th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                  {filteredUsers.length === 0 ? (
                    <tr>
                      <td colSpan={6} className="px-6 py-12 text-center text-gray-500 dark:text-gray-400">
                        <AlertCircle className="w-12 h-12 mx-auto mb-3 opacity-50" />
                        <p>No users found</p>
                      </td>
                    </tr>
                  ) : (
                    filteredUsers.map((user) => (
                      <tr key={user.id} className="hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="text-sm font-medium text-gray-900 dark:text-white">{user.email}</div>
                          <div className="text-xs text-gray-500 dark:text-gray-400 font-mono">{user.id.slice(0, 8)}...</div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className={`px-3 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${getPlanBadgeColor(user.plan)}`}>
                            {user.plan}
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                          {user.custom_batch_limit ? (
                            <span className="font-bold text-yellow-600 dark:text-yellow-400">
                              {user.custom_batch_limit} files (Custom)
                            </span>
                          ) : (
                            <span className="text-gray-600 dark:text-gray-400">
                              {getPlanLimit(user.plan)}
                            </span>
                          )}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                          {new Date(user.created_at).toLocaleDateString()}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                          {user.last_sign_in_at 
                            ? new Date(user.last_sign_in_at).toLocaleDateString()
                            : 'Never'}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                          <button
                            onClick={() => openEditModal(user)}
                            className="text-blue-600 hover:text-blue-900 dark:text-blue-400 dark:hover:text-blue-300"
                          >
                            Edit
                          </button>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        {/* Edit User Modal */}
        {editingUser && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-md w-full p-6">
              {/* Modal Header */}
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Edit User</h2>
                <button
                  onClick={closeEditModal}
                  className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                >
                  <X className="w-6 h-6" />
                </button>
              </div>

              {/* User Info */}
              <div className="mb-6 p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                <p className="text-sm font-medium text-gray-900 dark:text-white">{editingUser.email}</p>
                <p className="text-xs text-gray-500 dark:text-gray-400 mt-1 font-mono">{editingUser.id}</p>
              </div>

              {/* Edit Form */}
              <div className="space-y-4 mb-6">
                {/* Plan Selection */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Plan
                  </label>
                  <select
                    value={editPlan}
                    onChange={(e) => setEditPlan(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                  >
                    <option value="Free">Free (1 file)</option>
                    <option value="Basic">Basic (5 files)</option>
                    <option value="Pro">Pro (10 files)</option>
                    <option value="Ultra">Ultra (50 files)</option>
                    <option value="Max">Max (100 files)</option>
                    <option value="Enterprise">Enterprise (Custom)</option>
                  </select>
                </div>

                {/* Custom Limit */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Custom Batch Limit (optional)
                  </label>
                  <input
                    type="number"
                    value={editCustomLimit}
                    onChange={(e) => setEditCustomLimit(e.target.value)}
                    placeholder="Leave empty for plan default"
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                  />
                  <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                    Set a custom limit to override the plan default. For Enterprise users especially.
                  </p>
                </div>
              </div>

              {/* Messages */}
              {successMessage && (
                <div className="mb-4 p-3 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg flex items-center gap-2 text-green-800 dark:text-green-200">
                  <Check className="w-5 h-5" />
                  <span>{successMessage}</span>
                </div>
              )}

              {errorMessage && (
                <div className="mb-4 p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg flex items-center gap-2 text-red-800 dark:text-red-200">
                  <AlertCircle className="w-5 h-5" />
                  <span>{errorMessage}</span>
                </div>
              )}

              {/* Actions */}
              <div className="flex gap-3">
                <button
                  onClick={closeEditModal}
                  className="flex-1 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors text-gray-900 dark:text-white"
                >
                  Cancel
                </button>
                <button
                  onClick={saveUserChanges}
                  disabled={saveLoading}
                  className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                >
                  {saveLoading ? (
                    <>
                      <RefreshCw className="w-4 h-4 animate-spin" />
                      Saving...
                    </>
                  ) : (
                    <>
                      <Check className="w-4 h-4" />
                      Save Changes
                    </>
                  )}
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </DashboardLayout>
  )
}
