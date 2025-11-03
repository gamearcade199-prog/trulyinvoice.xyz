// Trust Badges Component - CRITICAL for SEO Trust Signals
'use client'

import React from 'react'
import Image from 'next/image'
import { advancedSEOSchemas } from '@/config/seo.advanced'

interface TrustBadgesProps {
  variant?: 'horizontal' | 'vertical' | 'grid'
  showStats?: boolean
  className?: string
}

export const TrustBadges: React.FC<TrustBadgesProps> = ({
  variant = 'horizontal',
  showStats = false,
  className = '',
}) => {
  const { trustSignals } = advancedSEOSchemas

  const layoutClasses = {
    horizontal: 'flex flex-wrap items-center justify-center gap-4 md:gap-6',
    vertical: 'flex flex-col items-center gap-4',
    grid: 'grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4',
  }

  return (
    <div className={`trust-badges ${className}`}>
      {/* Trust Badges */}
      <div className={layoutClasses[variant]}>
        {trustSignals.badges.map((badge, index) => (
          <div
            key={index}
            className="trust-badge group relative flex items-center gap-2 px-4 py-2 rounded-lg bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 shadow-sm hover:shadow-md transition-all duration-200"
            title={badge.alt}
          >
            <div className="w-8 h-8 flex items-center justify-center">
              {/* Placeholder SVG - Replace with actual badge images */}
              <svg className="w-full h-full text-blue-600 dark:text-blue-400" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M2.166 4.999A11.954 11.954 0 0010 1.944 11.954 11.954 0 0017.834 5c.11.65.166 1.32.166 2.001 0 5.225-3.34 9.67-8 11.317C5.34 16.67 2 12.225 2 7c0-.682.057-1.35.166-2.001zm11.541 3.708a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
            </div>
            <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
              {badge.name}
            </span>
            
            {/* Tooltip */}
            <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-3 py-1 bg-gray-900 text-white text-xs rounded opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap z-10">
              {badge.alt}
            </div>
          </div>
        ))}
      </div>

      {/* Trust Stats (Optional) */}
      {showStats && (
        <div className="mt-8 grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="text-center p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
            <div className="text-3xl font-bold text-blue-600 dark:text-blue-400">
              {trustSignals.stats.totalUsers}
            </div>
            <div className="text-sm text-gray-600 dark:text-gray-400 mt-1">
              Active Users
            </div>
          </div>
          <div className="text-center p-4 bg-green-50 dark:bg-green-900/20 rounded-lg">
            <div className="text-3xl font-bold text-green-600 dark:text-green-400">
              {trustSignals.stats.invoicesProcessed}
            </div>
            <div className="text-sm text-gray-600 dark:text-gray-400 mt-1">
              Invoices Processed
            </div>
          </div>
          <div className="text-center p-4 bg-purple-50 dark:bg-purple-900/20 rounded-lg">
            <div className="text-3xl font-bold text-purple-600 dark:text-purple-400">
              {trustSignals.stats.accuracy}
            </div>
            <div className="text-sm text-gray-600 dark:text-gray-400 mt-1">
              Accuracy Rate
            </div>
          </div>
          <div className="text-center p-4 bg-orange-50 dark:bg-orange-900/20 rounded-lg">
            <div className="text-3xl font-bold text-orange-600 dark:text-orange-400">
              {trustSignals.stats.avgTimeSaved}
            </div>
            <div className="text-sm text-gray-600 dark:text-gray-400 mt-1">
              Avg Time Saved
            </div>
          </div>
        </div>
      )}

      {/* JSON-LD for Trust Signals */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            '@context': 'https://schema.org',
            '@type': 'Organization',
            name: 'TrulyInvoice',
            slogan: 'Convert invoices to Excel, QuickBooks, Zoho Books with 99% AI accuracy',
            certification: trustSignals.badges.map(b => b.name).join(', '),
          }),
        }}
      />
    </div>
  )
}

// Star Rating Component - For AggregateRating Schema
interface StarRatingProps {
  rating: number
  maxRating?: number
  reviewCount?: number
  showCount?: boolean
  size?: 'sm' | 'md' | 'lg'
  className?: string
}

export const StarRating: React.FC<StarRatingProps> = ({
  rating,
  maxRating = 5,
  reviewCount,
  showCount = true,
  size = 'md',
  className = '',
}) => {
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-5 h-5',
    lg: 'w-6 h-6',
  }

  const percentage = (rating / maxRating) * 100

  return (
    <div className={`flex items-center gap-2 ${className}`} itemScope itemType="https://schema.org/AggregateRating">
      <meta itemProp="ratingValue" content={rating.toString()} />
      <meta itemProp="bestRating" content={maxRating.toString()} />
      {reviewCount && <meta itemProp="reviewCount" content={reviewCount.toString()} />}
      
      {/* Stars */}
      <div className="flex items-center gap-0.5">
        {[...Array(maxRating)].map((_, i) => (
          <svg
            key={i}
            className={`${sizeClasses[size]} ${
              i < Math.floor(rating)
                ? 'text-yellow-400'
                : i < rating
                ? 'text-yellow-400 opacity-50'
                : 'text-gray-300 dark:text-gray-600'
            }`}
            fill="currentColor"
            viewBox="0 0 20 20"
          >
            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
          </svg>
        ))}
      </div>

      {/* Rating Text */}
      <div className="flex items-center gap-1">
        <span className="font-semibold text-gray-900 dark:text-white">
          {rating.toFixed(1)}
        </span>
        <span className="text-gray-500 dark:text-gray-400">/ {maxRating}</span>
      </div>

      {/* Review Count */}
      {showCount && reviewCount && (
        <span className="text-sm text-gray-500 dark:text-gray-400">
          ({reviewCount.toLocaleString()} reviews)
        </span>
      )}
    </div>
  )
}

// Last Updated Timestamp Component
interface LastUpdatedProps {
  date: Date | string
  className?: string
}

export const LastUpdated: React.FC<LastUpdatedProps> = ({ date, className = '' }) => {
  const dateObj = typeof date === 'string' ? new Date(date) : date
  const isoString = dateObj.toISOString()
  const formattedDate = dateObj.toLocaleDateString('en-IN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })

  return (
    <div className={`text-sm text-gray-500 dark:text-gray-400 ${className}`}>
      <time dateTime={isoString} itemProp="dateModified">
        Last updated: {formattedDate}
      </time>
    </div>
  )
}

// Breadcrumbs Component
interface BreadcrumbItem {
  name: string
  url: string
}

interface BreadcrumbsProps {
  items: BreadcrumbItem[]
  className?: string
}

export const Breadcrumbs: React.FC<BreadcrumbsProps> = ({ items, className = '' }) => {
  return (
    <nav aria-label="Breadcrumb" className={className}>
      <ol
        className="flex items-center gap-2 text-sm"
        itemScope
        itemType="https://schema.org/BreadcrumbList"
      >
        {items.map((item, index) => (
          <li
            key={index}
            itemProp="itemListElement"
            itemScope
            itemType="https://schema.org/ListItem"
            className="flex items-center gap-2"
          >
            {index > 0 && (
              <svg className="w-4 h-4 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
              </svg>
            )}
            {index === items.length - 1 ? (
              <span
                className="text-gray-900 dark:text-white font-medium"
                itemProp="name"
                aria-current="page"
              >
                {item.name}
              </span>
            ) : (
              <a
                href={item.url}
                itemProp="item"
                className="text-blue-600 dark:text-blue-400 hover:underline"
              >
                <span itemProp="name">{item.name}</span>
              </a>
            )}
            <meta itemProp="position" content={(index + 1).toString()} />
          </li>
        ))}
      </ol>
    </nav>
  )
}

export default TrustBadges
