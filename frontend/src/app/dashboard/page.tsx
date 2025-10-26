'use client'

import { useEffect, useState } from 'react'
import DashboardLayout from '@/components/DashboardLayout'
import Link from 'next/link'
import { 
  FileText, 
  TrendingUp, 
  Clock, 
  CheckCircle2,
  AlertCircle,
  Upload,
  ArrowRight,
  Calendar
} from 'lucide-react'
import { supabase } from '@/lib/supabase'

export default function DashboardPage() {
  const [stats, setStats] = useState([
    {
      title: 'Total Invoices',
      value: '0',
      change: '+0%',
      trend: 'up',
      icon: FileText,
      color: 'blue'
    },
    {
      title: 'Total Amount',
      value: '₹0',
      change: '+0%',
      trend: 'up',
      icon: TrendingUp,
      color: 'purple'
    }
  ])
  
  const [recentInvoices, setRecentInvoices] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      // Get current user
      const { data: { user } } = await supabase.auth.getUser()
      if (!user) return

      // Fetch all invoices for this user (excluding dummy/NULL user_id invoices)
      const { data: invoices, error } = await supabase
        .from('invoices')
        .select('*')
        .eq('user_id', user.id)
        .order('invoice_date', { ascending: false })

      if (error) throw error

      // Calculate stats
      const totalInvoices = invoices?.length || 0
      const totalAmount = invoices?.reduce((sum, inv) => sum + (parseFloat(inv.total_amount) || 0), 0) || 0

      // Update stats
      setStats([
        {
          title: 'Total Invoices',
          value: totalInvoices.toString(),
          change: '+0%',
          trend: 'up',
          icon: FileText,
          color: 'blue'
        },
        {
          title: 'Total Amount',
          value: `₹${totalAmount.toLocaleString('en-IN')}`,
          change: '+0%',
          trend: 'up',
          icon: TrendingUp,
          color: 'purple'
        }
      ])

      // Set recent invoices (top 5)
      setRecentInvoices(invoices?.slice(0, 5) || [])
      setLoading(false)
    } catch (error) {
      console.error('Error fetching dashboard data:', error)
      setLoading(false)
    }
  }

  const getColorClasses = (color: string) => {
    switch (color) {
      case 'blue':
        return 'bg-blue-50 dark:bg-blue-900/50 text-blue-600 dark:text-blue-400'
      case 'yellow':
        return 'bg-yellow-50 dark:bg-yellow-900/50 text-yellow-600 dark:text-yellow-400'
      case 'green':
        return 'bg-green-50 dark:bg-green-900/50 text-green-600 dark:text-green-400'
      case 'purple':
        return 'bg-purple-50 dark:bg-purple-900/50 text-purple-600 dark:text-purple-400'
      default:
        return 'bg-gray-50 dark:bg-gray-700 text-gray-600 dark:text-gray-400'
    }
  }

  return (
    <DashboardLayout>
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Dashboard - Your Invoice History & Statistics</h1>
            <p className="text-gray-600 dark:text-gray-400 mt-1">Welcome back! Here's your invoice overview.</p>
          </div>
          <Link
            href="/upload"
            className="flex items-center gap-2 px-6 py-3 bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 text-white rounded-lg transition-colors font-semibold"
          >
            <Upload className="w-5 h-5" />
            Upload Invoice
          </Link>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {stats.map((stat) => {
            const Icon = stat.icon
            return (
              <div
                key={stat.title}
                className="bg-gray-50 dark:bg-gray-900 p-6 rounded-xl border border-gray-200 dark:border-gray-800 hover:shadow-lg transition-shadow"
              >
                <div className="flex items-center justify-between mb-4">
                  <div className={`p-3 rounded-lg ${getColorClasses(stat.color)}`}>
                    <Icon className="w-6 h-6" />
                  </div>
                  <span className={`text-sm font-semibold ${
                    stat.trend === 'up' ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'
                  }`}>
                    {stat.change}
                  </span>
                </div>
                <h3 className="text-gray-600 dark:text-gray-400 text-sm mb-1">{stat.title}</h3>
                <p className="text-3xl font-bold text-gray-900 dark:text-white">{stat.value}</p>
              </div>
            )
          })}
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Link
            href="/upload"
            className="bg-gradient-to-br from-blue-500 to-blue-600 dark:from-blue-600 dark:to-blue-700 p-6 rounded-xl text-white hover:shadow-xl transition-all group"
          >
            <Upload className="w-8 h-8 mb-3" />
            <h3 className="text-xl font-semibold mb-2">Upload Invoice</h3>
            <p className="text-blue-100 dark:text-blue-200 mb-4">Drag and drop or browse files</p>
            <div className="flex items-center gap-2 text-sm font-semibold group-hover:gap-3 transition-all">
              Get Started <ArrowRight className="w-4 h-4" />
            </div>
          </Link>

          <Link
            href="/invoices"
            className="bg-gray-50 dark:bg-gray-900 p-6 rounded-xl border border-gray-200 dark:border-gray-800 hover:shadow-lg transition-all group"
          >
            <FileText className="w-8 h-8 mb-3 text-blue-600 dark:text-blue-400" />
            <h3 className="text-xl font-semibold mb-2 text-gray-900 dark:text-white">View All Invoices</h3>
            <p className="text-gray-600 dark:text-gray-400 mb-4">Manage and track your invoices</p>
            <div className="flex items-center gap-2 text-sm font-semibold text-blue-600 dark:text-blue-400 group-hover:gap-3 transition-all">
              Browse <ArrowRight className="w-4 h-4" />
            </div>
          </Link>

          <div className="bg-gray-50 dark:bg-gray-900 p-6 rounded-xl border border-gray-200 dark:border-gray-800 hover:shadow-lg transition-shadow">
            <Calendar className="w-8 h-8 mb-3 text-purple-600 dark:text-purple-400" />
            <h3 className="text-xl font-semibold mb-2 text-gray-900 dark:text-white">Monthly Report</h3>
            <p className="text-gray-600 dark:text-gray-400 mb-4">Download your analytics</p>
            <button className="flex items-center gap-2 text-sm font-semibold text-purple-600 dark:text-purple-400 hover:gap-3 transition-all">
              Download <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Recent Invoices */}
        <div className="bg-gray-50 dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800">
          <div className="p-6 border-b border-gray-200 dark:border-gray-800">
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-bold text-gray-900 dark:text-white">Recent Invoices</h2>
              <Link
                href="/invoices"
                className="text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 font-semibold text-sm flex items-center gap-1"
              >
                View All <ArrowRight className="w-4 h-4" />
              </Link>
            </div>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-100 dark:bg-gray-950 border-b border-gray-200 dark:border-gray-800">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-semibold text-gray-600 dark:text-gray-400 uppercase tracking-wider">
                    Vendor
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-semibold text-gray-600 dark:text-gray-400 uppercase tracking-wider">
                    Invoice #
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-semibold text-gray-600 dark:text-gray-400 uppercase tracking-wider">
                    Date
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-semibold text-gray-600 dark:text-gray-400 uppercase tracking-wider">
                    Amount
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-semibold text-gray-600 dark:text-gray-400 uppercase tracking-wider">
                    Status
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200 dark:divide-gray-800">
                {loading ? (
                  <tr>
                    <td colSpan={5} className="px-6 py-12 text-center text-gray-500 dark:text-gray-400">
                      Loading invoices...
                    </td>
                  </tr>
                ) : recentInvoices.length === 0 ? (
                  <tr>
                    <td colSpan={5} className="px-6 py-12 text-center">
                      <div className="flex flex-col items-center gap-3">
                        <FileText className="w-12 h-12 text-gray-300 dark:text-gray-600" />
                        <p className="text-gray-500 dark:text-gray-400">No invoices yet. Upload your first invoice to get started!</p>
                        <Link 
                          href="/upload"
                          className="mt-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 text-white rounded-lg transition-colors font-semibold"
                        >
                          Upload Invoice
                        </Link>
                      </div>
                    </td>
                  </tr>
                ) : (
                  recentInvoices.map((invoice) => (
                    <tr key={invoice.id} className="hover:bg-gray-100 dark:hover:bg-gray-950 cursor-pointer transition-colors">
                      <td className="px-6 py-4">
                        <div className="font-semibold text-gray-900 dark:text-white">{invoice.vendor_name || 'Unknown Vendor'}</div>
                      </td>
                      <td className="px-6 py-4 text-gray-600 dark:text-gray-400">{invoice.invoice_number || 'N/A'}</td>
                      <td className="px-6 py-4 text-gray-600 dark:text-gray-400">
                        {invoice.invoice_date ? new Date(invoice.invoice_date).toLocaleDateString('en-IN') : 'N/A'}
                      </td>
                      <td className="px-6 py-4">
                        <span className="font-semibold text-gray-900 dark:text-white">
                          ₹{parseFloat(invoice.total_amount || 0).toLocaleString('en-IN')}
                        </span>
                      </td>
                      <td className="px-6 py-4">
                        <span className="px-3 py-1 rounded-full text-xs font-semibold bg-green-100 dark:bg-green-900/50 text-green-700 dark:text-green-400">
                          Processed
                        </span>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </DashboardLayout>
  )
}