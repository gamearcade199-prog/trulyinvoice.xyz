'use client'

import React from 'react'

interface TrulyInvoiceLogoProps {
  size?: 'sm' | 'md' | 'lg'
  showText?: boolean
  className?: string
}

export default function TrulyInvoiceLogo({ 
  size = 'md', 
  showText = true,
  className = '' 
}: TrulyInvoiceLogoProps) {
  const sizes = {
    sm: { box: 'w-8 h-8', icon: 'w-5 h-5', text: 'text-lg' },
    md: { box: 'w-10 h-10', icon: 'w-6 h-6', text: 'text-xl' },
    lg: { box: 'w-12 h-12', icon: 'w-7 h-7', text: 'text-2xl' }
  }

  const currentSize = sizes[size]

  return (
    <div className={`flex items-center gap-2.5 ${className}`}>
      {/* Custom Invoice Icon with Checkmark */}
      <div className={`${currentSize.box} bg-gradient-to-br from-blue-500 via-blue-600 to-indigo-600 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105 flex items-center justify-center relative group`}>
        {/* Invoice Document Shape */}
        <svg 
          className={currentSize.icon}
          viewBox="0 0 24 24" 
          fill="none" 
          xmlns="http://www.w3.org/2000/svg"
        >
          {/* Document Background */}
          <path 
            d="M14 2H6C5.46957 2 4.96086 2.21071 4.58579 2.58579C4.21071 2.96086 4 3.46957 4 4V20C4 20.5304 4.21071 21.0391 4.58579 21.4142C4.96086 21.7893 5.46957 22 6 22H18C18.5304 22 19.0391 21.7893 19.4142 21.4142C19.7893 21.0391 20 20.5304 20 20V8L14 2Z" 
            fill="white"
            opacity="0.9"
          />
          
          {/* Folded Corner */}
          <path 
            d="M14 2V8H20" 
            stroke="white" 
            strokeWidth="1.5" 
            strokeLinecap="round" 
            strokeLinejoin="round"
            opacity="0.7"
          />
          
          {/* Invoice Lines */}
          <line x1="8" y1="12" x2="16" y2="12" stroke="#3B82F6" strokeWidth="1.5" strokeLinecap="round" />
          <line x1="8" y1="15" x2="14" y2="15" stroke="#3B82F6" strokeWidth="1.5" strokeLinecap="round" />
          <line x1="8" y1="18" x2="12" y2="18" stroke="#3B82F6" strokeWidth="1.5" strokeLinecap="round" />
          
          {/* AI Sparkle Effect */}
          <circle cx="17" cy="6" r="1.5" fill="#10B981" className="animate-pulse" />
          <circle cx="16" cy="8.5" r="0.8" fill="#34D399" className="animate-pulse" style={{ animationDelay: '0.3s' }} />
        </svg>

        {/* Hover Glow Effect */}
        <div className="absolute inset-0 rounded-xl bg-blue-400 opacity-0 group-hover:opacity-20 blur-xl transition-opacity duration-300"></div>
      </div>

      {/* Brand Text */}
      {showText && (
        <span className={`${currentSize.text} font-bold bg-gradient-to-r from-gray-900 via-gray-800 to-gray-900 dark:from-white dark:via-gray-100 dark:to-white bg-clip-text text-transparent tracking-tight`}>
          Truly<span className="bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">Invoice</span>
        </span>
      )}
    </div>
  )
}
