'use client'

import { useState, useRef, useEffect } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { ArrowRight, CheckCircle2, Upload, Zap, FileText, Sparkles, TrendingUp, Shield, X, Loader2, Eye, Moon, Sun, LayoutDashboard, LogOut } from 'lucide-react'
import { useTheme } from '@/components/ThemeProvider'
import { supabase } from '@/lib/supabase'

export default function Home() {
  const { theme, toggleTheme } = useTheme()
  const router = useRouter()
  const [isDragging, setIsDragging] = useState(false)
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [isProcessing, setIsProcessing] = useState(false)
  const [progress, setProgress] = useState(0)
  const [showSignupModal, setShowSignupModal] = useState(false)
  const [extractedData, setExtractedData] = useState<any>(null)
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)

  // Check authentication status
  useEffect(() => {
    checkAuth()
  }, [])

  const checkAuth = async () => {
    const { data: { user } } = await supabase.auth.getUser()
    setIsLoggedIn(!!user)
  }

  const handleLogout = async () => {
    await supabase.auth.signOut()
    setIsLoggedIn(false)
    router.push('/')
  }

  const handleFileSelect = (file: File) => {
    setSelectedFile(file)
    startProcessing()
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(false)
    
    const file = e.dataTransfer.files[0]
    if (file && (file.type === 'application/pdf' || file.type.startsWith('image/'))) {
      handleFileSelect(file)
    }
  }

  const startProcessing = () => {
    setIsProcessing(true)
    setProgress(0)

    // Simulate AI processing
    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval)
          setIsProcessing(false)
          // Mock extracted data
          setExtractedData({
            vendor: 'Amazon Web Services',
            amount: '₹12,500',
            invoiceNumber: 'INV-2024-001',
            date: '10 Oct 2024',
            gst: '₹2,250'
          })
          // Show signup modal after extraction
          setTimeout(() => setShowSignupModal(true), 500)
          return 100
        }
        return prev + 20
      })
    }, 400)
  }

  return (
    <main className="min-h-screen relative bg-gray-50 dark:bg-gray-900 transition-colors">
      {/* Navigation */}
      <nav className="bg-white/90 dark:bg-gray-800/90 backdrop-blur-md border-b border-gray-200 dark:border-gray-700 sticky top-0 z-50 transition-colors">
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg flex items-center justify-center">
                <FileText className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold text-gray-900 dark:text-white">TrulyInvoice</span>
            </div>
            <div className="flex items-center gap-4">
              {/* Dashboard Button */}
              <Link 
                href="/dashboard" 
                className="flex items-center gap-2 text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white font-semibold transition-colors"
              >
                <LayoutDashboard className="w-5 h-5" />
                <span className="hidden sm:inline">Dashboard</span>
              </Link>
              
              {/* Dark Mode Toggle */}
              <button
                onClick={toggleTheme}
                className="p-2 rounded-lg bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
                aria-label="Toggle theme"
              >
                {theme === 'light' ? (
                  <Moon className="w-5 h-5 text-gray-700 dark:text-gray-300" />
                ) : (
                  <Sun className="w-5 h-5 text-gray-700 dark:text-gray-300" />
                )}
              </button>
              
              {/* Conditional Auth Buttons */}
              {isLoggedIn ? (
                <button 
                  onClick={handleLogout}
                  className="flex items-center gap-2 text-gray-700 dark:text-gray-300 hover:text-red-600 dark:hover:text-red-400 font-semibold transition-colors"
                >
                  <LogOut className="w-4 h-4" />
                  Sign Out
                </button>
              ) : (
                <>
                  <Link href="/login" className="text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white font-semibold transition-colors">
                    Sign In
                  </Link>
                  <Link 
                    href="/register" 
                    className="bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 text-white px-6 py-2 rounded-lg font-semibold transition-colors"
                  >
                    Start Free
                  </Link>
                </>
              )}
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section with Interactive Upload */}
      <section className="bg-gradient-to-br from-slate-50 via-blue-50/30 to-purple-50/30 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 py-6 md:py-12 relative overflow-hidden transition-colors">
        {/* Decorative elements */}
        <div className="absolute top-0 right-0 w-48 h-48 md:w-72 md:h-72 bg-blue-200 dark:bg-blue-900/30 rounded-full mix-blend-multiply dark:mix-blend-lighten filter blur-3xl opacity-20 dark:opacity-10"></div>
        <div className="absolute bottom-0 left-0 w-48 h-48 md:w-72 md:h-72 bg-purple-200 dark:bg-purple-900/30 rounded-full mix-blend-multiply dark:mix-blend-lighten filter blur-3xl opacity-20 dark:opacity-10"></div>
        
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
          <div className="max-w-5xl mx-auto text-center">
            <div className="inline-flex items-center gap-2 px-3 py-1 md:px-4 md:py-1.5 bg-blue-100 dark:bg-blue-900/50 text-blue-700 dark:text-blue-300 rounded-full text-xs md:text-sm font-semibold mb-3 md:mb-4">
              <Sparkles className="w-3 h-3 md:w-4 md:h-4" />
              AI-Powered Invoice Management
            </div>
            <h1 className="text-3xl sm:text-4xl md:text-5xl lg:text-5xl xl:text-6xl font-bold text-gray-900 dark:text-white mb-3 md:mb-4 px-4 leading-tight">
              Your Invoices, <br/>
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600 dark:from-blue-400 dark:to-purple-400">
                Instantly Organized
              </span>
            </h1>
            <p className="text-sm sm:text-base md:text-lg text-gray-600 dark:text-gray-300 mb-4 md:mb-6 max-w-2xl mx-auto px-4">
              Stop wasting time on manual data entry. Let AI extract, organize, and analyze your invoices in seconds.
            </p>

            {/* Interactive Upload Zone */}
            <div className="max-w-3xl mx-auto mb-4 md:mb-6 px-4">
              <div
                onDragEnter={(e) => { e.preventDefault(); setIsDragging(true) }}
                onDragLeave={(e) => { e.preventDefault(); setIsDragging(false) }}
                onDragOver={(e) => e.preventDefault()}
                onDrop={handleDrop}
                onClick={() => fileInputRef.current?.click()}
                className={`
                  relative border-3 md:border-4 border-dashed rounded-2xl md:rounded-3xl p-6 sm:p-8 md:p-12 cursor-pointer
                  transition-all duration-300 ease-in-out transform
                  ${isDragging || isProcessing
                    ? 'border-blue-600 dark:border-blue-400 bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-blue-900/30 dark:to-indigo-900/30 shadow-2xl scale-[1.02] ring-2 md:ring-4 ring-blue-200 dark:ring-blue-800' 
                    : 'border-indigo-300 dark:border-indigo-700 bg-gradient-to-br from-white to-blue-50/30 dark:from-gray-800 dark:to-blue-900/10 shadow-xl hover:border-blue-600 dark:hover:border-blue-400 hover:shadow-2xl hover:scale-[1.02] hover:ring-2 md:hover:ring-4 hover:ring-blue-100 dark:hover:ring-blue-900'
                  }
                `}
              >
                <input
                  ref={fileInputRef}
                  type="file"
                  accept=".pdf,.jpg,.jpeg,.png"
                  onChange={(e) => e.target.files?.[0] && handleFileSelect(e.target.files[0])}
                  className="hidden"
                />

                {!isProcessing && !extractedData && (
                  <div className="flex flex-col items-center gap-2 md:gap-3">
                    <div className="p-3 md:p-4 rounded-full bg-gradient-to-br from-blue-500 to-purple-500">
                      <Upload className="w-8 h-8 md:w-12 md:h-12 text-white" />
                    </div>
                    <div>
                      <h3 className="text-base sm:text-lg md:text-xl font-bold text-gray-800 dark:text-gray-100 mb-1">
                        Upload Your Invoices Here
                      </h3>
                      <p className="text-gray-600 dark:text-gray-400 text-xs sm:text-sm md:text-base">
                        Drag and drop your invoice here, or{' '}
                        <span className="text-blue-600 dark:text-blue-400 font-semibold">browse</span>
                      </p>
                    </div>
                    <div className="text-xs text-gray-500 dark:text-gray-400 text-center px-2">
                      Supports PDF, JPG, PNG • See AI extraction in action!
                    </div>
                  </div>
                )}

                {/* Processing State */}
                {isProcessing && (
                  <div className="flex flex-col items-center gap-4 md:gap-6">
                    <Loader2 className="w-12 h-12 md:w-16 md:h-16 text-blue-600 dark:text-blue-400 animate-spin" />
                    <div className="w-full max-w-md px-4">
                      <div className="flex items-center justify-between mb-2">
                        <span className="font-semibold text-sm sm:text-base text-gray-900 dark:text-gray-100">Processing with AI...</span>
                        <span className="text-blue-600 dark:text-blue-400 font-bold text-sm sm:text-base">{progress}%</span>
                      </div>
                      <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2 md:h-3 overflow-hidden">
                        <div
                          className="bg-gradient-to-r from-blue-500 to-purple-500 h-full rounded-full transition-all duration-300 ease-out"
                          style={{ width: `${progress}%` }}
                        />
                      </div>
                      <p className="text-xs sm:text-sm text-gray-600 dark:text-gray-400 mt-2">Extracting vendor, amount, dates, GST...</p>
                    </div>
                  </div>
                )}

                {/* Extraction Complete */}
                {extractedData && !isProcessing && (
                  <div className="flex flex-col items-center gap-4 md:gap-6 px-4">
                    <div className="p-3 md:p-4 bg-green-100 dark:bg-green-900/50 rounded-full">
                      <CheckCircle2 className="w-10 h-10 md:w-12 md:h-12 text-green-600 dark:text-green-400" />
                    </div>
                    <div className="text-center">
                      <h3 className="text-xl md:text-2xl font-bold text-gray-900 dark:text-gray-100 mb-2">
                        ✨ Extraction Complete!
                      </h3>
                      <p className="text-sm md:text-base text-gray-600 dark:text-gray-400">AI successfully extracted your invoice data</p>
                    </div>
                    {/* Preview Card */}
                    <div className="bg-white dark:bg-gray-800 rounded-xl p-4 md:p-6 shadow-lg max-w-md w-full border border-gray-200 dark:border-gray-700">
                      <div className="grid grid-cols-2 gap-3 md:gap-4 text-left">
                        <div>
                          <p className="text-xs md:text-sm text-gray-600 dark:text-gray-400">Vendor</p>
                          <p className="font-semibold text-sm md:text-base text-gray-900 dark:text-gray-100 truncate">{extractedData.vendor}</p>
                        </div>
                        <div>
                          <p className="text-xs md:text-sm text-gray-600 dark:text-gray-400">Amount</p>
                          <p className="font-semibold text-sm md:text-base text-gray-900 dark:text-gray-100">{extractedData.amount}</p>
                        </div>
                        <div>
                          <p className="text-xs md:text-sm text-gray-600 dark:text-gray-400">Invoice #</p>
                          <p className="font-semibold text-sm md:text-base text-gray-900 dark:text-gray-100 truncate">{extractedData.invoiceNumber}</p>
                        </div>
                        <div>
                          <p className="text-xs md:text-sm text-gray-600 dark:text-gray-400">Date</p>
                          <p className="font-semibold text-sm md:text-base text-gray-900 dark:text-gray-100">{extractedData.date}</p>
                        </div>
                      </div>
                      <div className="mt-3 md:mt-4 pt-3 md:pt-4 border-t border-gray-200 dark:border-gray-700 flex items-center justify-center gap-2 text-blue-600 dark:text-blue-400">
                        <Eye className="w-3 h-3 md:w-4 md:h-4" />
                        <span className="text-xs md:text-sm font-semibold">Sign in to view full details</span>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>

            <div className="flex flex-col sm:flex-row gap-2 md:gap-3 justify-center items-center px-4">
              <Link 
                href="/register" 
                className="w-full sm:w-auto bg-gradient-to-r from-blue-600 to-blue-700 dark:from-blue-500 dark:to-blue-600 text-white px-5 md:px-6 py-2.5 md:py-3 rounded-xl font-semibold hover:shadow-xl transition-all flex items-center justify-center gap-2 text-sm md:text-base"
              >
                Start Free Trial <ArrowRight className="w-4 h-4" />
              </Link>
              <p className="text-xs text-gray-600 dark:text-gray-400 text-center">
                ✨ No credit card required • 30 free scans
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-12 md:py-20 bg-white dark:bg-gray-800 transition-colors">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl md:text-4xl font-bold text-center mb-3 md:mb-4 text-gray-900 dark:text-white">How It Works</h2>
          <p className="text-center text-sm md:text-base text-gray-600 dark:text-gray-400 mb-8 md:mb-12 max-w-2xl mx-auto px-4">
            Three simple steps to transform your invoice management
          </p>
          <div className="grid sm:grid-cols-2 md:grid-cols-3 gap-6 md:gap-8 max-w-5xl mx-auto px-4">
            <div className="text-center group">
              <div className="bg-gradient-to-br from-blue-500 to-blue-600 w-16 h-16 md:w-20 md:h-20 rounded-2xl flex items-center justify-center mx-auto mb-4 md:mb-6 group-hover:scale-110 transition-transform shadow-lg">
                <Upload className="w-8 h-8 md:w-10 md:h-10 text-white" />
              </div>
              <div className="bg-blue-50 dark:bg-blue-900/50 w-12 h-1 mx-auto mb-3 md:mb-4 rounded-full"></div>
              <h3 className="text-xl md:text-2xl font-bold mb-2 md:mb-3 text-gray-900 dark:text-white">1. Upload</h3>
              <p className="text-sm md:text-base text-gray-600 dark:text-gray-400 px-2">
                Upload invoices via drag-and-drop, email forwarding, or WhatsApp
              </p>
            </div>
            <div className="text-center group">
              <div className="bg-gradient-to-br from-purple-500 to-purple-600 w-16 h-16 md:w-20 md:h-20 rounded-2xl flex items-center justify-center mx-auto mb-4 md:mb-6 group-hover:scale-110 transition-transform shadow-lg">
                <Zap className="w-8 h-8 md:w-10 md:h-10 text-white" />
              </div>
              <div className="bg-purple-50 dark:bg-purple-900/50 w-12 h-1 mx-auto mb-3 md:mb-4 rounded-full"></div>
              <h3 className="text-xl md:text-2xl font-bold mb-2 md:mb-3 text-gray-900 dark:text-white">2. AI Extracts</h3>
              <p className="text-sm md:text-base text-gray-600 dark:text-gray-400 px-2">
                Our AI reads vendor, amount, GST, and line items automatically in seconds
              </p>
            </div>
            <div className="text-center group sm:col-span-2 md:col-span-1">
              <div className="bg-gradient-to-br from-green-500 to-green-600 w-16 h-16 md:w-20 md:h-20 rounded-2xl flex items-center justify-center mx-auto mb-4 md:mb-6 group-hover:scale-110 transition-transform shadow-lg">
                <TrendingUp className="w-8 h-8 md:w-10 md:h-10 text-white" />
              </div>
              <div className="bg-green-50 dark:bg-green-900/50 w-12 h-1 mx-auto mb-3 md:mb-4 rounded-full"></div>
              <h3 className="text-xl md:text-2xl font-bold mb-2 md:mb-3 text-gray-900 dark:text-white">3. Export</h3>
              <p className="text-sm md:text-base text-gray-600 dark:text-gray-400 px-2">
                Export to Excel, Google Sheets, Tally, or QuickBooks with one click
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-12 md:py-20 bg-gradient-to-br from-slate-50 via-blue-50/30 to-purple-50/30 dark:from-gray-900 dark:via-gray-850 dark:to-gray-900 transition-colors">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-6xl mx-auto">
            <div className="text-center mb-10 md:mb-16 px-4">
              <h2 className="text-3xl md:text-4xl font-bold mb-3 md:mb-4 text-gray-900 dark:text-white">Built for Indian Businesses</h2>
              <p className="text-sm md:text-base lg:text-lg text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
                Designed specifically to handle Indian invoices with GST, GSTIN, PAN, and more
              </p>
            </div>
            <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6 md:gap-8">
              {[
                {
                  icon: Sparkles,
                  title: '98% Accurate',
                  description: 'Industry-leading accuracy for Indian invoice formats'
                },
                {
                  icon: Zap,
                  title: 'Lightning Fast',
                  description: 'Process invoices in under 5 seconds with AI'
                },
                {
                  icon: Shield,
                  title: 'Secure & Private',
                  description: 'Bank-level encryption for your sensitive data'
                },
                {
                  icon: FileText,
                  title: 'All Formats',
                  description: 'PDF, JPG, PNG - we handle them all'
                },
                {
                  icon: CheckCircle2,
                  title: 'GST Compliant',
                  description: 'Automatic GSTIN, PAN, and tax extraction'
                },
                {
                  icon: TrendingUp,
                  title: 'Smart Analytics',
                  description: 'Insights into spending patterns and trends'
                }
              ].map((feature, index) => {
                const Icon = feature.icon
                return (
                  <div
                    key={index}
                    className="bg-white dark:bg-gray-800 p-6 md:p-8 rounded-2xl shadow-lg hover:shadow-xl transition-all border border-gray-100 dark:border-gray-700 group hover:-translate-y-1"
                  >
                    <div className="w-12 h-12 md:w-14 md:h-14 bg-blue-100 dark:bg-blue-900/50 rounded-xl flex items-center justify-center mb-3 md:mb-4 group-hover:scale-110 transition-transform">
                      <Icon className="w-6 h-6 md:w-7 md:h-7 text-blue-600 dark:text-blue-400" />
                    </div>
                    <h3 className="text-lg md:text-xl font-bold mb-2 text-gray-900 dark:text-white">{feature.title}</h3>
                    <p className="text-sm md:text-base text-gray-600 dark:text-gray-400">{feature.description}</p>
                  </div>
                )
              })}
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-12 md:py-20 bg-gradient-to-r from-blue-600 to-purple-600 dark:from-blue-700 dark:to-purple-700 transition-colors">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-bold text-white mb-4 md:mb-6 px-4">
            Ready to Save Hours Every Week?
          </h2>
          <p className="text-base sm:text-lg md:text-xl text-blue-100 dark:text-blue-200 mb-6 md:mb-8 max-w-2xl mx-auto px-4">
            Join thousands of businesses using AI to automate their invoice processing
          </p>
          <Link
            href="/register"
            className="inline-flex items-center gap-2 bg-white text-blue-600 px-6 md:px-8 py-3 md:py-4 rounded-xl font-bold text-base md:text-lg hover:shadow-2xl transition-all hover:scale-105"
          >
            Start Free Trial <ArrowRight className="w-4 h-4 md:w-5 md:h-5" />
          </Link>
          <p className="text-sm md:text-base text-blue-100 dark:text-blue-200 mt-3 md:mt-4 px-4">No credit card required • Cancel anytime</p>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 dark:bg-gray-950 text-gray-300 py-8 md:py-12 transition-colors">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid sm:grid-cols-2 md:grid-cols-4 gap-6 md:gap-8 mb-6 md:mb-8">
            <div>
              <div className="flex items-center gap-2 mb-3 md:mb-4">
                <div className="w-7 h-7 md:w-8 md:h-8 bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg flex items-center justify-center">
                  <FileText className="w-4 h-4 md:w-5 md:h-5 text-white" />
                </div>
                <span className="text-lg md:text-xl font-bold text-white">TrulyInvoice</span>
              </div>
              <p className="text-xs md:text-sm text-gray-400">
                AI-powered invoice management built for Indian businesses
              </p>
            </div>
            <div>
              <h4 className="font-semibold text-white mb-3 md:mb-4 text-sm md:text-base">Product</h4>
              <ul className="space-y-1.5 md:space-y-2 text-xs md:text-sm">
                <li><Link href="/features" className="hover:text-white transition-colors">Features</Link></li>
                <li><Link href="/pricing" className="hover:text-white transition-colors">Pricing</Link></li>
                <li><Link href="/dashboard" className="hover:text-white transition-colors">Demo</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold text-white mb-3 md:mb-4 text-sm md:text-base">Company</h4>
              <ul className="space-y-1.5 md:space-y-2 text-xs md:text-sm">
                <li><Link href="/about" className="hover:text-white transition-colors">About</Link></li>
                <li><Link href="/contact" className="hover:text-white transition-colors">Contact</Link></li>
                <li><Link href="/careers" className="hover:text-white transition-colors">Careers</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold text-white mb-3 md:mb-4 text-sm md:text-base">Legal</h4>
              <ul className="space-y-1.5 md:space-y-2 text-xs md:text-sm">
                <li><Link href="/privacy" className="hover:text-white transition-colors">Privacy</Link></li>
                <li><Link href="/terms" className="hover:text-white transition-colors">Terms</Link></li>
                <li><Link href="/security" className="hover:text-white transition-colors">Security</Link></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-800 dark:border-gray-900 pt-6 md:pt-8 text-xs md:text-sm text-center text-gray-400">
            <p>© 2025 TrulyInvoice. All rights reserved.</p>
          </div>
        </div>
      </footer>

      {/* Signup Modal */}
      {showSignupModal && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="bg-white dark:bg-gray-800 rounded-2xl max-w-md w-full p-6 md:p-8 relative transition-colors max-h-[90vh] overflow-y-auto">
            <button
              onClick={() => setShowSignupModal(false)}
              className="absolute top-3 right-3 md:top-4 md:right-4 p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
            >
              <X className="w-4 h-4 md:w-5 md:h-5 text-gray-600 dark:text-gray-400" />
            </button>

            <div className="text-center mb-4 md:mb-6">
              <div className="w-14 h-14 md:w-16 md:h-16 bg-gradient-to-br from-green-400 to-green-500 rounded-full flex items-center justify-center mx-auto mb-3 md:mb-4">
                <CheckCircle2 className="w-8 h-8 md:w-10 md:h-10 text-white" />
              </div>
              <h3 className="text-xl md:text-2xl font-bold text-gray-900 dark:text-white mb-2">
                Amazing! 🎉
              </h3>
              <p className="text-sm md:text-base text-gray-600 dark:text-gray-400">
                Your invoice was extracted successfully!
              </p>
            </div>

            <div className="bg-gradient-to-br from-blue-50 to-purple-50 dark:from-blue-900/30 dark:to-purple-900/30 rounded-xl p-4 md:p-6 mb-4 md:mb-6">
              <h4 className="font-semibold text-sm md:text-base text-gray-900 dark:text-white mb-2 md:mb-3">Extracted Data Preview:</h4>
              <div className="space-y-1.5 md:space-y-2 text-xs md:text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-600 dark:text-gray-400">Vendor:</span>
                  <span className="font-semibold text-gray-900 dark:text-white truncate">{extractedData?.vendor}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600 dark:text-gray-400">Amount:</span>
                  <span className="font-semibold text-gray-900 dark:text-white">{extractedData?.amount}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600 dark:text-gray-400">Invoice #:</span>
                  <span className="font-semibold text-gray-900 dark:text-white truncate">{extractedData?.invoiceNumber}</span>
                </div>
              </div>
            </div>

            <div className="space-y-2 md:space-y-3">
              <Link
                href="/register"
                className="w-full bg-gradient-to-r from-blue-600 to-purple-600 dark:from-blue-500 dark:to-purple-500 text-white py-2.5 md:py-3 rounded-xl font-semibold text-sm md:text-base hover:shadow-lg transition-all flex items-center justify-center gap-2"
              >
                <span className="truncate">Create Free Account to View Full Details</span> <ArrowRight className="w-4 h-4 md:w-5 md:h-5 flex-shrink-0" />
              </Link>
              <Link
                href="/login"
                className="w-full bg-white dark:bg-gray-700 border-2 border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 py-2.5 md:py-3 rounded-xl font-semibold text-sm md:text-base hover:bg-gray-50 dark:hover:bg-gray-600 transition-all flex items-center justify-center gap-2"
              >
                Already have an account? Sign In
              </Link>
            </div>

            <p className="text-xs text-gray-500 dark:text-gray-400 text-center mt-3 md:mt-4">
              ✨ Free forever • No credit card required
            </p>
          </div>
        </div>
      )}
    </main>
  )
}