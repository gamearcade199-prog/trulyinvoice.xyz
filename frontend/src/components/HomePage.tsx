'use client'

import { useState, useRef, useEffect } from 'react'
import Link from 'next/link'
import dynamic from 'next/dynamic'
import { useRouter } from 'next/navigation'
import { ArrowRight, CheckCircle2, Upload, Zap, FileText, Sparkles, TrendingUp, Shield, X, Loader2, Eye, Moon, Sun, LayoutDashboard, LogOut, Menu, CreditCard } from 'lucide-react'
import { useTheme } from '@/components/ThemeProvider'
import { supabase } from '@/lib/supabase'
import { uploadInvoiceAnonymous, linkTempInvoicesToUser } from '@/lib/invoiceUpload'
import { getCurrencySymbol, formatCurrency } from '@/lib/currency'

// Lazy load below-fold components for better performance
const TrustedBy = dynamic(() => import('@/components/TrustedBy'), { loading: () => null })
const SavingsCalculator = dynamic(() => import('@/components/SavingsCalculator'), { loading: () => null })
const WhatYouGet = dynamic(() => import('@/components/WhatYouGet'), { loading: () => null })
const Footer = dynamic(() => import('@/components/Footer'), { loading: () => null })

import UpgradeModal from '@/components/UpgradeModal'
import { useQuotaModal } from '@/hooks/useQuotaModal'
import Breadcrumb from '@/components/Breadcrumb'
import TrulyInvoiceLogo from '@/components/TrulyInvoiceLogo'

export default function HomePage() {
  const { theme, toggleTheme } = useTheme()
  const router = useRouter()
  const [isDragging, setIsDragging] = useState(false)
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [isProcessing, setIsProcessing] = useState(false)
  const [progress, setProgress] = useState(0)
  const [showSignupModal, setShowSignupModal] = useState(false)
  const [showSuccessModal, setShowSuccessModal] = useState(false)
  const [extractedData, setExtractedData] = useState<any>(null)
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [processingError, setProcessingError] = useState('')
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)
  const { isModalOpen, showUpgradeModal, hideUpgradeModal, handleQuotaError, quotaState } = useQuotaModal()

  // Check authentication status
  useEffect(() => {
    checkAuth()
  }, [])

  // Close mobile menu when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (isMobileMenuOpen && !(event.target as Element).closest('nav')) {
        setIsMobileMenuOpen(false)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => {
      document.removeEventListener('mousedown', handleClickOutside)
    }
  }, [isMobileMenuOpen])

  const checkAuth = async () => {
    const { data: { user } } = await supabase.auth.getUser()
    setIsLoggedIn(!!user)

    // If user just logged in, link any temp invoices
    if (user) {
      await linkTempInvoicesToUser(user.id)
    }
  }

  const handleLogout = async () => {
    await supabase.auth.signOut()
    setIsLoggedIn(false)
    router.push('/')
    window.location.reload()
  }

  const handleFileSelect = (file: File) => {
    setSelectedFile(file)
    startProcessing(file)
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

  const startProcessing = async (file: File) => {
    setIsProcessing(true)
    setProgress(0)
    setProcessingError('')
    setExtractedData(null)

    console.log('🚀 Starting upload process for:', file.name)

    // Animate progress while uploading
    const progressInterval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 90) {
          clearInterval(progressInterval)
          return 90
        }
        return prev + 10
      })
    }, 300)

    try {
      console.log('📤 Calling uploadInvoiceAnonymous...')
      // Upload and process invoice (works for both logged-in and anonymous users)
      const result = await uploadInvoiceAnonymous(file)

      console.log('📥 Upload result:', result)

      clearInterval(progressInterval)
      setProgress(100)

      if (result.success && result.data) {
        console.log('✅ Upload successful, extracted data:', result.data)
        setExtractedData(result.data)
        setTimeout(() => {
          setIsProcessing(false)
          if (!isLoggedIn) {
            setShowSignupModal(true)
          } else {
            setShowSuccessModal(true)
          }
        }, 500)
      } else {
        console.error('❌ Upload failed:', result.error)
        setProcessingError(result.error || 'Failed to process invoice')
        setIsProcessing(false)
      }
    } catch (error: any) {
      console.error('🚨 Exception during upload:', error)
      clearInterval(progressInterval)
      
      // Check if it's a quota error (HTTP 429)
      if (handleQuotaError(error)) {
        setIsProcessing(false)
        return
      }
      
      // More detailed error message
      let errorMessage = 'Failed to process invoice'
      if (error.message) {
        errorMessage = error.message
      } else if (error.toString) {
        errorMessage = error.toString()
      }
      
      console.log('Setting error message:', errorMessage)
      setProcessingError(errorMessage)
      setIsProcessing(false)
    }
  }

  return (
    <main className="min-h-screen relative bg-gradient-to-br from-gray-50 via-white to-blue-50 dark:from-gray-900 dark:via-gray-900 dark:to-gray-800 transition-colors">
      {/* Navigation */}
      <nav className="bg-white/90 dark:bg-gray-900/95 backdrop-blur-md border-b border-gray-200 dark:border-gray-700 sticky top-0 z-50 transition-colors">
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-between h-12">
            {/* Logo */}
            <Link href="/" aria-label="TrulyInvoice Homepage">
              <TrulyInvoiceLogo size="md" />
            </Link>

            {/* Desktop Navigation */}
            <div className="hidden md:flex items-center gap-4">
              {/* Dashboard Button */}
              <Link
                href="/dashboard"
                className="flex items-center gap-2 text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white font-semibold transition-colors"
              >
                <LayoutDashboard className="w-5 h-5" />
                Dashboard
              </Link>

              {/* Pricing Button */}
              <Link
                href="/pricing"
                className="flex items-center gap-2 text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white font-semibold transition-colors"
              >
                <CreditCard className="w-5 h-5" />
                Pricing
              </Link>

              {/* Dark Mode Toggle */}
              <button
                onClick={toggleTheme}
                className="p-2 rounded-lg bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
                aria-label={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
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
                  aria-label="Sign out"
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
                    aria-label="Start your free trial"
                  >
                    Start Free
                  </Link>
                </>
              )}
            </div>

            {/* Mobile Menu Button and Dark Mode Toggle */}
            <div className="flex md:hidden items-center gap-2">
              {/* Dark Mode Toggle for Mobile */}
              <button
                onClick={toggleTheme}
                className="p-2 rounded-lg bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
                aria-label={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
              >
                {theme === 'light' ? (
                  <Moon className="w-5 h-5 text-gray-700 dark:text-gray-300" />
                ) : (
                  <Sun className="w-5 h-5 text-gray-700 dark:text-gray-300" />
                )}
              </button>

              {/* Hamburger Menu Button */}
              <button
                onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                className="p-2 rounded-lg bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
                aria-label={isMobileMenuOpen ? "Close mobile menu" : "Open mobile menu"}
                aria-expanded={isMobileMenuOpen}
              >
                {isMobileMenuOpen ? (
                  <X className="w-6 h-6 text-gray-700 dark:text-gray-300" />
                ) : (
                  <Menu className="w-6 h-6 text-gray-700 dark:text-gray-300" />
                )}
              </button>
            </div>
          </div>

          {/* Mobile Menu */}
          {isMobileMenuOpen && (
              <div className="md:hidden border-t border-gray-200 dark:border-gray-700 py-4 space-y-3 bg-white/95 dark:bg-gray-900/95 backdrop-blur-md">
              {/* Dashboard Link */}
              <Link
                href="/dashboard"
                onClick={() => setIsMobileMenuOpen(false)}
                className="flex items-center gap-3 px-4 py-2 text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg font-semibold transition-colors"
              >
                <LayoutDashboard className="w-5 h-5" />
                Dashboard
              </Link>

              {/* Pricing Link */}
              <Link
                href="/pricing"
                onClick={() => setIsMobileMenuOpen(false)}
                className="flex items-center gap-3 px-4 py-2 text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg font-semibold transition-colors"
              >
                <CreditCard className="w-5 h-5" />
                Pricing
              </Link>

              {/* Conditional Auth Links */}
              {isLoggedIn ? (
                <button
                  onClick={() => {
                    handleLogout()
                    setIsMobileMenuOpen(false)
                  }}
                  className="flex items-center gap-3 px-4 py-2 w-full text-left text-gray-700 dark:text-gray-300 hover:text-red-600 dark:hover:text-red-400 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg font-semibold transition-colors"
                >
                  <LogOut className="w-5 h-5" />
                  Sign Out
                </button>
              ) : (
                <>
                  <Link
                    href="/login"
                    onClick={() => setIsMobileMenuOpen(false)}
                    className="flex items-center gap-3 px-4 py-2 text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg font-semibold transition-colors"
                  >
                    Sign In
                  </Link>
                  <Link
                    href="/register"
                    onClick={() => setIsMobileMenuOpen(false)}
                    className="flex items-center gap-3 px-4 py-2 bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 text-white rounded-lg font-semibold transition-colors mx-4"
                  >
                    Start Free
                  </Link>
                </>
              )}
            </div>
          )}
        </div>
      </nav>

      {/* Hero Section with Interactive Upload */}
            {/* Hero Section with Interactive Upload */}
      <section className="relative flex items-center overflow-hidden" style={{ height: 'calc(100vh - 64px)' }}>
        {/* Decorative Background Blobs */}
        <div className="absolute top-0 right-0 w-72 h-72 bg-blue-200 dark:bg-blue-800/40 rounded-full mix-blend-multiply dark:mix-blend-lighten filter blur-3xl opacity-20"></div>
        <div className="absolute bottom-0 left-0 w-72 h-72 bg-purple-200 dark:bg-purple-800/40 rounded-full mix-blend-multiply dark:mix-blend-lighten filter blur-3xl opacity-20"></div>

        <div className="container mx-auto px-4 sm:px-6 lg:px-8 relative z-10 w-full">
          <div className="max-w-4xl mx-auto text-center">
            {/* AI Badge */}
            <div className="mt-4 sm:mt-6 flex justify-center px-4">
              <div className="inline-flex items-center gap-1.5 sm:gap-2 bg-gradient-to-r from-blue-600 to-indigo-600 dark:from-blue-500 dark:to-indigo-500 text-white px-3 py-1.5 sm:px-4 sm:py-2 rounded-full text-xs sm:text-sm font-semibold shadow-lg shadow-blue-500/30 dark:shadow-blue-500/20 hover:shadow-xl hover:scale-105 transition-all duration-300">
                <Sparkles className="w-3 h-3 sm:w-4 sm:h-4" fill="currentColor" />
                <span className="whitespace-nowrap">AI-Powered • High Accuracy</span>
              </div>
            </div>
            
            <h1 className="text-4xl sm:text-5xl md:text-6xl font-bold text-gray-900 dark:text-gray-50 mb-4 leading-tight">
              Convert Invoice to Excel with <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">99% AI Accuracy</span>
            </h1>
            <p className="text-lg md:text-xl text-gray-600 dark:text-gray-200 mb-8 max-w-3xl mx-auto">
              Transform invoice PDFs into <a href="/export/excel" className="text-blue-600 dark:text-blue-400 hover:underline font-medium">Excel spreadsheets</a> instantly. Auto-extract vendor names, <a href="/features" className="text-blue-600 dark:text-blue-400 hover:underline font-medium">GST numbers</a>, line items, totals with 99% accuracy. Export to <a href="/export/quickbooks" className="text-blue-600 dark:text-blue-400 hover:underline font-medium">QuickBooks</a>, <a href="/export/zoho-books" className="text-blue-600 dark:text-blue-400 hover:underline font-medium">Zoho Books</a>, or <a href="/export/csv" className="text-blue-600 dark:text-blue-400 hover:underline font-medium">CSV</a>. <strong>FREE for 10 invoices/month.</strong>
            </p>

            {/* Interactive Upload Zone */}
            <div
              onDragEnter={(e) => { e.preventDefault(); if (!isProcessing) setIsDragging(true) }}
              onDragLeave={(e) => { e.preventDefault(); setIsDragging(false) }}
              onDragOver={(e) => e.preventDefault()}
              onDrop={isProcessing ? undefined : handleDrop}
              onClick={isProcessing ? undefined : () => fileInputRef.current?.click()}
              className={`relative max-w-3xl mx-auto border-4 border-dashed rounded-3xl p-8 sm:p-12 transition-all duration-300 ease-in-out transform ${
                isProcessing 
                  ? 'border-blue-500 bg-blue-50/50 dark:bg-blue-900/30' 
                  : isDragging 
                    ? 'border-blue-600 dark:border-blue-400 bg-blue-50/50 dark:bg-blue-900/30 scale-105 cursor-pointer' 
                    : 'border-gray-300 dark:border-gray-600 hover:border-blue-500 dark:hover:border-blue-400 cursor-pointer'
              }`}
            >
              <input
                ref={fileInputRef}
                type="file"
                accept=".pdf,.jpg,.jpeg,.png"
                onChange={(e) => e.target.files?.[0] && handleFileSelect(e.target.files[0])}
                className="hidden"
                disabled={isProcessing}
              />
              
              {/* Processing Overlay */}
              {isProcessing && (
                <div className="absolute inset-0 bg-white/90 dark:bg-gray-900/90 backdrop-blur-sm rounded-3xl flex flex-col items-center justify-center z-10">
                  <div className="flex flex-col items-center gap-4">
                    {/* Spinning loader */}
                    <div className="w-16 h-16 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin"></div>
                    
                    {/* Progress bar */}
                    <div className="w-64 bg-gray-200 dark:bg-gray-700 rounded-full h-2 overflow-hidden">
                      <div 
                        className="bg-gradient-to-r from-blue-500 to-purple-500 h-2 rounded-full transition-all duration-300 ease-out"
                        style={{ width: `${progress}%` }}
                      ></div>
                    </div>
                    
                    {/* Status text */}
                    <div className="text-center">
                      <h3 className="text-xl font-bold text-gray-800 dark:text-gray-100 mb-1">
                        Processing Your Invoice...
                      </h3>
                      <p className="text-gray-600 dark:text-gray-400">
                        AI is extracting data • {progress}% complete
                      </p>
                    </div>
                  </div>
                </div>
              )}
              
              {/* Normal upload UI */}
              <div className={`flex flex-col items-center gap-4 ${isProcessing ? 'opacity-30' : ''}`}>
                <div className="p-4 rounded-full bg-gradient-to-br from-blue-500 to-purple-500">
                  <Upload className="w-12 h-12 text-white" />
                </div>
                <div>
                  <h3 className="text-xl font-bold text-gray-800 dark:text-gray-100 mb-1">
                    Try It Now - Upload Any Invoice
                  </h3>
                  <p className="text-gray-600 dark:text-gray-400">
                    Drag & drop a PDF or image, or <span className="text-blue-600 dark:text-blue-400 font-semibold">click to browse</span>
                  </p>
                </div>
              </div>
            </div>

            {/* Error Message */}
            {processingError && (
              <div className="mt-4 max-w-3xl mx-auto p-4 bg-red-50 dark:bg-red-900/30 border border-red-200 dark:border-red-800 rounded-xl">
                <div className="flex items-center gap-2">
                  <div className="w-5 h-5 bg-red-500 rounded-full flex items-center justify-center flex-shrink-0">
                    <X className="w-3 h-3 text-white" />
                  </div>
                  <p className="text-red-700 dark:text-red-300 text-sm font-medium">
                    {processingError}
                  </p>
                </div>
              </div>
            )}

            {/* Security Guarantee */}
            <div className="mt-6 flex items-center justify-center gap-2 text-xs sm:text-sm text-gray-500 dark:text-gray-400 px-4">
              <Shield className="w-4 h-4 flex-shrink-0 mt-0.5" />
              <span className="text-center">Encrypted & Secure. Your files are safe.</span>
            </div>
          </div>
        </div>
      </section>

      <SavingsCalculator />

      <WhatYouGet />

      {/* How It Works */}
      <section className="py-12 md:py-20 bg-gray-50 dark:bg-gray-900 transition-colors">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl md:text-4xl font-bold text-center mb-3 md:mb-4 text-gray-900 dark:text-white">How It Works</h2>
          <p className="text-center text-sm md:text-base text-gray-600 dark:text-gray-400 mb-8 md:mb-12 max-w-2xl mx-auto px-4">
            Three simple steps to transform your invoice management
          </p>
          <div className="grid sm:grid-cols-2 md:grid-cols-3 gap-6 md:gap-8 max-w-5xl mx-auto px-4">
            <div className="text-center group">
              <div className="bg-gradient-to-br from-blue-500 to-blue-600 w-20 h-20 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform shadow-lg">
                <Upload className="w-10 h-10 text-white" />
              </div>
              <h3 className="text-xl md:text-2xl font-bold mb-3 text-gray-900 dark:text-white">1. Upload Any Invoice</h3>
              <p className="text-sm md:text-base text-gray-600 dark:text-gray-400 px-2">
                Drag & drop a PDF, JPG, or PNG. No signup needed to try.
              </p>
            </div>
              <div className="text-center group">
              <div className="bg-gradient-to-br from-purple-500 to-purple-600 w-20 h-20 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform shadow-lg">
                <Zap className="w-10 h-10 text-white" />
              </div>
              <h3 className="text-xl md:text-2xl font-bold mb-3 text-gray-900 dark:text-white">2. AI Extracts the Data</h3>
              <p className="text-sm md:text-base text-gray-600 dark:text-gray-400 px-2">
                Our <a href="/features" className="text-blue-600 dark:text-blue-400 hover:underline">AI technology</a> reads vendor names, amounts, GST, and line items in seconds.
              </p>
            </div>
              <div className="text-center group sm:col-span-2 md:col-span-1">
              <div className="bg-gradient-to-br from-green-500 to-green-600 w-20 h-20 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform shadow-lg">
                <TrendingUp className="w-10 h-10 text-white" />
              </div>
              <h3 className="text-xl md:text-2xl font-bold mb-3 text-gray-900 dark:text-white">3. Export Instantly</h3>
              <p className="text-sm md:text-base text-gray-600 dark:text-gray-400 px-2">
                Choose from <a href="/export/excel" className="text-blue-600 dark:text-blue-400 hover:underline">Excel</a>, <a href="/export/csv" className="text-blue-600 dark:text-blue-400 hover:underline">CSV</a>, <a href="/export/excel" className="text-blue-600 dark:text-blue-400 hover:underline">ERP 9</a>, <a href="/export/quickbooks" className="text-blue-600 dark:text-blue-400 hover:underline">QuickBooks India</a>, or <a href="/export/zoho-books" className="text-blue-600 dark:text-blue-400 hover:underline">Zoho Books</a>. Ready for accounting software import.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Why Choose Us - Problem/Solution */}
      <section className="py-12 md:py-20 bg-gray-50 dark:bg-gray-900 transition-colors">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-5xl mx-auto">
            <div className="grid md:grid-cols-2 gap-8 md:gap-12 items-center">
              {/* Problem Side */}
              <div className="bg-gradient-to-br from-red-50 to-orange-50 dark:from-red-900/20 dark:to-orange-900/20 p-6 md:p-8 rounded-2xl border-2 border-red-200 dark:border-red-800">
                <h3 className="text-2xl md:text-3xl font-bold text-red-900 dark:text-red-300 mb-4">
                  😫 The Old Way
                </h3>
                <ul className="space-y-3 text-sm md:text-base text-gray-700 dark:text-gray-300">
                  <li className="flex items-start gap-2">
                    <span className="text-red-500 font-bold mt-1">✗</span>
                    <span>Hours wasted typing invoice details manually</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-red-500 font-bold mt-1">✗</span>
                    <span>Constant errors in data entry (wrong amounts, dates)</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-red-500 font-bold mt-1">✗</span>
                    <span>Lost invoices and missing GST numbers</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-red-500 font-bold mt-1">✗</span>
                    <span>Difficult to track expenses and vendor payments</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-red-500 font-bold mt-1">✗</span>
                    <span>Messy folders full of paper and PDF files</span>
                  </li>
                </ul>
              </div>

              {/* Solution Side */}
              <div className="bg-gradient-to-br from-green-50 to-blue-50 dark:from-green-900/20 dark:to-blue-900/20 p-6 md:p-8 rounded-2xl border-2 border-green-200 dark:border-green-800">
                <h3 className="text-2xl md:text-3xl font-bold text-green-900 dark:text-green-300 mb-4">
                  ✨ With TrulyInvoice
                </h3>
                <ul className="space-y-3 text-sm md:text-base text-gray-700 dark:text-gray-300">
                  <li className="flex items-start gap-2">
                    <span className="text-green-500 font-bold mt-1">✓</span>
                    <span>Scan and extract all data in under 5 seconds</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-green-500 font-bold mt-1">✓</span>
                    <span>99% accuracy - AI reads better than humans</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-green-500 font-bold mt-1">✓</span>
                    <span>All invoices searchable and organized in one place</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-green-500 font-bold mt-1">✓</span>
                    <span>Track payments, vendors, and GST automatically</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-green-500 font-bold mt-1">✓</span>
                    <span>Export to Excel, CSV QuickBooks, or Zoho Books instantly</span>
                  </li>
                </ul>
              </div>
            </div>

            {/* Time Saved Calculator */}
            <div className="mt-10 md:mt-12 bg-gradient-to-r from-blue-600 to-purple-600 dark:from-blue-700 dark:to-purple-700 p-6 md:p-8 rounded-2xl text-white text-center">
              <h4 className="text-xl md:text-2xl font-bold mb-3">
                ⏱️ Average Time Saved Per Invoice
              </h4>
              <div className="flex items-center justify-center gap-4 md:gap-8 flex-wrap">
                <div>
                  <p className="text-3xl md:text-4xl font-bold">5 min</p>
                  <p className="text-sm md:text-base text-blue-100">Manual Entry</p>
                </div>
                <div className="text-3xl md:text-4xl">→</div>
                <div>
                  <p className="text-3xl md:text-4xl font-bold">5 sec</p>
                  <p className="text-sm md:text-base text-blue-100">With TrulyInvoice</p>
                </div>
              </div>
              <p className="mt-4 text-sm md:text-base text-blue-100 dark:text-blue-200">
                Process 100 invoices per month? <span className="font-bold">Save 8+ hours monthly!</span>
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
                  title: 'High Accuracy',
                  description: 'Industry-leading accuracy for Indian invoice formats with AI'
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
                    className="bg-gray-50 dark:bg-gray-900 p-6 md:p-8 rounded-2xl shadow-lg hover:shadow-xl transition-all border border-gray-100 dark:border-gray-700 group hover:-translate-y-1"
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

      {/* Testimonials Section */}
      <section className="py-12 md:py-20 bg-gray-50 dark:bg-gray-900 transition-colors">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-10 md:mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-3 md:mb-4 text-gray-900 dark:text-white">
              Loved by Business Owners & Accountants
            </h2>
            <p className="text-sm md:text-base text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
              See what our customers have to say about transforming their invoice workflow
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-6 md:gap-8 max-w-6xl mx-auto">
            {/* Testimonial 1 */}
            <div className="bg-gradient-to-br from-blue-50 to-purple-50 dark:from-gray-700 dark:to-gray-800 p-6 md:p-8 rounded-2xl shadow-lg border border-blue-100 dark:border-gray-600 hover:shadow-xl transition-all">
              <div className="flex items-center gap-1 mb-4">
                {[...Array(5)].map((_, i) => (
                  <span key={i} className="text-yellow-400 text-lg">★</span>
                ))}
              </div>
              <p className="text-sm md:text-base text-gray-700 dark:text-gray-300 mb-4 italic">
                &ldquo;TrulyInvoice saved me significant time each week. I was manually entering hundreds of invoices monthly. Now it&apos;s done much faster. The <a href="/features" className="text-blue-600 dark:text-blue-400 hover:underline">GST extraction</a> works very well!&rdquo;
              </p>
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 md:w-12 md:h-12 rounded-full bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center text-white font-bold text-sm md:text-base">
                  RP
                </div>
                <div>
                  <p className="font-semibold text-gray-900 dark:text-white text-sm md:text-base">Rajesh P.</p>
                  <p className="text-xs md:text-sm text-gray-600 dark:text-gray-400">Accountant, Mumbai</p>
                </div>
              </div>
            </div>

            {/* Testimonial 2 */}
            <div className="bg-gradient-to-br from-green-50 to-blue-50 dark:from-gray-700 dark:to-gray-800 p-6 md:p-8 rounded-2xl shadow-lg border border-green-100 dark:border-gray-600 hover:shadow-xl transition-all">
              <div className="flex items-center gap-1 mb-4">
                {[...Array(5)].map((_, i) => (
                  <span key={i} className="text-yellow-400 text-lg">★</span>
                ))}
              </div>
              <p className="text-sm md:text-base text-gray-700 dark:text-gray-300 mb-4 italic">
                &ldquo;As a small business owner, I don&apos;t have time for data entry. This tool is very helpful. Just upload and the <a href="/features" className="text-blue-600 dark:text-blue-400 hover:underline">extraction is accurate</a>!&rdquo;
              </p>
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 md:w-12 md:h-12 rounded-full bg-gradient-to-br from-green-500 to-blue-500 flex items-center justify-center text-white font-bold text-sm md:text-base">
                  SK
                </div>
                <div>
                  <p className="font-semibold text-gray-900 dark:text-white text-sm md:text-base">Sneha K.</p>
                  <p className="text-xs md:text-sm text-gray-600 dark:text-gray-400">Restaurant Owner, Pune</p>
                </div>
              </div>
            </div>

            {/* Testimonial 3 */}
            <div className="bg-gradient-to-br from-purple-50 to-pink-50 dark:from-gray-700 dark:to-gray-800 p-6 md:p-8 rounded-2xl shadow-lg border border-purple-100 dark:border-gray-600 hover:shadow-xl transition-all">
              <div className="flex items-center gap-1 mb-4">
                {[...Array(5)].map((_, i) => (
                  <span key={i} className="text-yellow-400 text-lg">★</span>
                ))}
              </div>
              <p className="text-sm md:text-base text-gray-700 dark:text-gray-300 mb-4 italic">
                &ldquo;The accuracy is very good. I tested it with many invoices and only had to correct a few fields. Export to <a href="/export/excel" className="text-blue-600 dark:text-blue-400 hover:underline">works smoothly</a>. Highly recommended!&rdquo;
              </p>
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 md:w-12 md:h-12 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center text-white font-bold text-sm md:text-base">
                  AV
                </div>
                <div>
                  <p className="font-semibold text-gray-900 dark:text-white text-sm md:text-base">Amit V.</p>
                  <p className="text-xs md:text-sm text-gray-600 dark:text-gray-400">CA Firm, Delhi</p>
                </div>
              </div>
            </div>
          </div>

          {/* Additional short testimonial bar */}
          <div className="mt-10 md:mt-16 grid grid-cols-1 md:grid-cols-3 gap-4 md:gap-6 max-w-5xl mx-auto">
            <div className="bg-white dark:bg-gray-700 p-4 md:p-6 rounded-xl shadow border border-gray-200 dark:border-gray-600 text-center">
              <p className="text-2xl md:text-3xl font-bold text-blue-600 dark:text-blue-400 mb-1">High Accuracy</p>
              <p className="text-xs md:text-sm text-gray-600 dark:text-gray-400">AI-Powered Extraction</p>
            </div>
            <div className="bg-white dark:bg-gray-700 p-4 md:p-6 rounded-xl shadow border border-gray-200 dark:border-gray-600 text-center">
              <p className="text-2xl md:text-3xl font-bold text-green-600 dark:text-green-400 mb-1">Fast</p>
              <p className="text-xs md:text-sm text-gray-600 dark:text-gray-400">Significant Time Savings</p>
            </div>
            <div className="bg-white dark:bg-gray-700 p-4 md:p-6 rounded-xl shadow border border-gray-200 dark:border-gray-600 text-center">
              <p className="text-2xl md:text-3xl font-bold text-purple-600 dark:text-purple-400 mb-1">&lt;10 sec</p>
              <p className="text-xs md:text-sm text-gray-600 dark:text-gray-400">Processing Time</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-12 md:py-20 bg-gradient-to-r from-blue-600 to-purple-600 dark:from-blue-700 dark:to-purple-700 transition-colors">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-bold text-white mb-4 md:mb-6 px-4">
            Ready to Automate Your Invoices?
          </h2>
          <p className="text-base sm:text-lg md:text-xl text-blue-100 dark:text-blue-200 mb-6 md:mb-8 max-w-2xl mx-auto px-4">
            Join hundreds of Indian businesses saving time with AI-powered invoice processing
          </p>
          <Link
            href="/register"
            className="inline-flex items-center gap-2 bg-white text-blue-600 px-6 md:px-8 py-3 md:py-4 rounded-xl font-bold text-base md:text-lg hover:shadow-2xl transition-all hover:scale-105"
          >
            Start Free <ArrowRight className="w-4 h-4 md:w-5 md:h-5" />
          </Link>
          <p className="text-sm md:text-base text-blue-100 dark:text-blue-200 mt-3 md:mt-4 px-4">10 free scans per month • Upgrade anytime</p>
        </div>
      </section>

      {/* Related Links Section */}
      <section className="py-12 md:py-16 bg-gray-50 dark:bg-gray-900/50">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-8 text-center">Learn More About TrulyInvoice</h2>
          <div className="grid md:grid-cols-3 gap-6 max-w-4xl mx-auto">
            <Link 
              href="/features"
              className="group p-6 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 hover:border-blue-500 dark:hover:border-blue-500 transition-all hover:shadow-lg"
            >
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
                Features
              </h3>
              <p className="text-gray-600 dark:text-gray-400">
                Explore our powerful AI-powered invoice processing capabilities and automation features.
              </p>
            </Link>

            <Link 
              href="/pricing"
              className="group p-6 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 hover:border-blue-500 dark:hover:border-blue-500 transition-all hover:shadow-lg"
            >
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
                Pricing Plans
              </h3>
              <p className="text-gray-600 dark:text-gray-400">
                Choose the perfect plan for your invoice processing needs. From free to enterprise.
              </p>
            </Link>

            <Link 
              href="/about"
              className="group p-6 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 hover:border-blue-500 dark:hover:border-blue-500 transition-all hover:shadow-lg"
            >
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
                About Us
              </h3>
              <p className="text-gray-600 dark:text-gray-400">
                Discover our mission to revolutionize invoice processing with AI technology.
              </p>
            </Link>
          </div>
        </div>
      </section>

      {/* Signup Modal */}
      {showSignupModal && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="bg-gray-50 dark:bg-gray-900 rounded-2xl max-w-md w-full p-6 md:p-8 relative transition-colors max-h-[90vh] overflow-y-auto">
            <button
              onClick={() => setShowSignupModal(false)}
              className="absolute top-3 right-3 md:top-4 md:right-4 p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
              aria-label="Close signup modal"
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
              <h4 className="font-semibold text-sm md:text-base text-gray-900 dark:text-white mb-3 md:mb-4">Extracted Amount:</h4>
              <div className="text-center mb-4">
                <p className="text-2xl md:text-3xl font-bold text-green-600 dark:text-green-400 mb-1">
                  {getCurrencySymbol('INR')} {formatCurrency(extractedData?.total_amount || extractedData?.amount || 0, 'INR')}
                </p>
                <p className="text-xs md:text-sm text-gray-600 dark:text-gray-400">
                  From {extractedData?.vendor_name || extractedData?.vendor || 'Vendor'}
                </p>
              </div>
              <div className="border-t border-gray-200 dark:border-gray-600 pt-3">
                <h5 className="font-medium text-xs md:text-sm text-gray-700 dark:text-gray-300 mb-2">Additional Details:</h5>
                <div className="space-y-1 text-xs md:text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-600 dark:text-gray-400">Invoice #:</span>
                    <span className="font-semibold text-gray-900 dark:text-white truncate">{extractedData?.invoice_number || extractedData?.invoiceNumber || 'Not found'}</span>
                  </div>
                </div>
              </div>
            </div>

            <div className="space-y-2 md:space-y-3">
              <Link
                href="/register"
                className="w-full bg-gradient-to-r from-blue-600 to-purple-600 dark:from-blue-500 dark:to-purple-500 text-white py-2.5 md:py-3 rounded-xl font-semibold text-sm md:text-base hover:shadow-lg transition-all flex items-center justify-center gap-2"
                aria-label="Create a free account to view full invoice details"
              >
                <span className="truncate">Create Free Account to View Full Details</span> <ArrowRight className="w-4 h-4 md:w-5 md:h-5 flex-shrink-0" />
              </Link>
              <Link
                href="/login"
                className="w-full bg-white dark:bg-gray-700 border-2 border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 py-2.5 md:py-3 rounded-xl font-semibold text-sm md:text-base hover:bg-gray-50 dark:hover:bg-gray-600 transition-all flex items-center justify-center gap-2"
                aria-label="Sign in to your existing account"
              >
                Already have an account? Sign In
              </Link>
            </div>

            <p className="text-xs text-gray-500 dark:text-gray-400 text-center mt-3 md:mt-4">
              ✨ 10 free scans per month • Forever free plan
            </p>
          </div>
        </div>
      )}

      {/* Success Modal for Logged-in Users */}
      {showSuccessModal && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="bg-gray-50 dark:bg-gray-900 rounded-2xl max-w-md w-full p-6 md:p-8 relative transition-colors max-h-[90vh] overflow-y-auto">
            <button
              onClick={() => setShowSuccessModal(false)}
              className="absolute top-3 right-3 md:top-4 md:right-4 p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
              aria-label="Close success modal"
            >
              <X className="w-4 h-4 md:w-5 md:h-5 text-gray-600 dark:text-gray-400" />
            </button>

            <div className="text-center mb-4 md:mb-6">
              <div className="w-14 h-14 md:w-16 md:h-16 bg-gradient-to-br from-green-400 to-green-500 rounded-full flex items-center justify-center mx-auto mb-3 md:mb-4">
                <CheckCircle2 className="w-8 h-8 md:w-10 md:h-10 text-white" />
              </div>
              <h3 className="text-xl md:text-2xl font-bold text-gray-900 dark:text-white mb-2">
                Invoice Processed Successfully! 🎉
              </h3>
              <p className="text-sm md:text-base text-gray-600 dark:text-gray-400">
                Your invoice has been extracted and saved to your dashboard.
              </p>
            </div>

            <div className="bg-gradient-to-br from-blue-50 to-purple-50 dark:from-blue-900/30 dark:to-purple-900/30 rounded-xl p-4 md:p-6 mb-4 md:mb-6">
              <h4 className="font-semibold text-sm md:text-base text-gray-900 dark:text-white mb-2 md:mb-3">Extracted Amount:</h4>
              <div className="text-center">
                <p className="text-2xl md:text-3xl font-bold text-green-600 dark:text-green-400 mb-1">
                  {getCurrencySymbol('INR')} {formatCurrency(extractedData?.total_amount || extractedData?.amount || 0, 'INR')}
                </p>
                <p className="text-xs md:text-sm text-gray-600 dark:text-gray-400">
                  From {extractedData?.vendor_name || extractedData?.vendor || 'Vendor'}
                </p>
              </div>
            </div>

            <div className="space-y-2 md:space-y-3">
              <Link
                href="/dashboard"
                onClick={() => setShowSuccessModal(false)}
                className="w-full bg-gradient-to-r from-blue-600 to-purple-600 dark:from-blue-500 dark:to-purple-500 text-white py-2.5 md:py-3 rounded-xl font-semibold text-sm md:text-base hover:shadow-lg transition-all flex items-center justify-center gap-2"
                aria-label="View invoice in dashboard"
              >
                <span className="truncate">View in Dashboard</span> <ArrowRight className="w-4 h-4 md:w-5 md:h-5 flex-shrink-0" />
              </Link>
              <button
                onClick={() => setShowSuccessModal(false)}
                className="w-full bg-white dark:bg-gray-700 border-2 border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 py-2.5 md:py-3 rounded-xl font-semibold text-sm md:text-base hover:bg-gray-50 dark:hover:bg-gray-600 transition-all"
                aria-label="Continue uploading more invoices"
              >
                Upload Another Invoice
              </button>
            </div>

            <p className="text-xs text-gray-500 dark:text-gray-400 text-center mt-3 md:mt-4">
              💡 You can export this invoice to Excel or other formats from your dashboard
            </p>
          </div>
        </div>
      )}

      {/* Upgrade Modal */}
      <UpgradeModal
        isOpen={isModalOpen}
        onClose={hideUpgradeModal}
        currentPlan={quotaState?.currentPlan || 'free'}
        scansUsed={quotaState?.scansUsed || 0}
        scansLimit={quotaState?.scansLimit || 10}
        reason="quota_exceeded"
      />

      {/* Footer with City Links */}
      <Footer />
    </main>
  )
}
