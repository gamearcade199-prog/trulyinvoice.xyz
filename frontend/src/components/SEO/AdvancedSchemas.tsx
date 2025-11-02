// Advanced SEO Schema Components - 10/10 Optimization
'use client'

import React from 'react'
import { advancedSEOSchemas } from '@/config/seo.advanced'

// AggregateRating + Review Schema Component
export const RatingsAndReviewsSchema: React.FC = () => {
  const { aggregateRating, reviews } = advancedSEOSchemas

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify(aggregateRating),
        }}
      />
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify(reviews),
        }}
      />
    </>
  )
}

// HowTo Schema Component
export const HowToSchema: React.FC = () => {
  const { howTo } = advancedSEOSchemas

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{
        __html: JSON.stringify(howTo),
      }}
    />
  )
}

// VideoObject Schema Component
export const VideoSchema: React.FC = () => {
  const { video } = advancedSEOSchemas

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{
        __html: JSON.stringify(video),
      }}
    />
  )
}

// Enhanced LocalBusiness Schema Component
export const EnhancedLocalBusinessSchema: React.FC = () => {
  const { enhancedLocalBusiness } = advancedSEOSchemas

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{
        __html: JSON.stringify(enhancedLocalBusiness),
      }}
    />
  )
}

// Article Schema Component (for Blog Posts)
interface ArticleSchemaProps {
  title: string
  description: string
  datePublished: string
  dateModified: string
  url: string
  imageUrl: string
  authorName: string
  authorUrl?: string
  wordCount: number
}

export const ArticleSchema: React.FC<ArticleSchemaProps> = (props) => {
  const articleSchema = advancedSEOSchemas.createArticle(props)

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{
        __html: JSON.stringify(articleSchema),
      }}
    />
  )
}

// Breadcrumb Schema Component
interface BreadcrumbSchemaProps {
  items: Array<{ name: string; url: string }>
}

export const BreadcrumbSchema: React.FC<BreadcrumbSchemaProps> = ({ items }) => {
  const breadcrumbSchema = advancedSEOSchemas.createBreadcrumb(items)

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{
        __html: JSON.stringify(breadcrumbSchema),
      }}
    />
  )
}

// E-E-A-T Signals Component (Expertise, Experience, Authority, Trust)
export const EEATSignals: React.FC<{ variant?: 'compact' | 'full' }> = ({ variant = 'compact' }) => {
  const { eeatSignals } = advancedSEOSchemas

  if (variant === 'compact') {
    return (
      <div className="eeat-signals bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20 rounded-lg p-6 my-8">
        <div className="grid md:grid-cols-4 gap-4">
          <div className="text-center">
            <div className="text-2xl font-bold text-blue-600 dark:text-blue-400 mb-2">15,000+</div>
            <div className="text-sm text-gray-600 dark:text-gray-400">Active Users</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-green-600 dark:text-green-400 mb-2">2.5M+</div>
            <div className="text-sm text-gray-600 dark:text-gray-400">Invoices Processed</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-purple-600 dark:text-purple-400 mb-2">99%</div>
            <div className="text-sm text-gray-600 dark:text-gray-400">Accuracy Rate</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-orange-600 dark:text-orange-400 mb-2">247</div>
            <div className="text-sm text-gray-600 dark:text-gray-400">5-Star Reviews</div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="eeat-signals space-y-8 my-12">
      {/* Expertise */}
      <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm">
        <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3 flex items-center gap-2">
          <svg className="w-6 h-6 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
            <path d="M10.394 2.08a1 1 0 00-.788 0l-7 3a1 1 0 000 1.84L5.25 8.051a.999.999 0 01.356-.257l4-1.714a1 1 0 11.788 1.838L7.667 9.088l1.94.831a1 1 0 00.787 0l7-3a1 1 0 000-1.838l-7-3zM3.31 9.397L5 10.12v4.102a8.969 8.969 0 00-1.05-.174 1 1 0 01-.89-.89 11.115 11.115 0 01.25-3.762zM9.3 16.573A9.026 9.026 0 007 14.935v-3.957l1.818.78a3 3 0 002.364 0l5.508-2.361a11.026 11.026 0 01.25 3.762 1 1 0 01-.89.89 8.968 8.968 0 00-5.35 2.524 1 1 0 01-1.4 0zM6 18a1 1 0 001-1v-2.065a8.935 8.935 0 00-2-.712V17a1 1 0 001 1z" />
          </svg>
          Expertise
        </h3>
        <p className="text-gray-600 dark:text-gray-400 mb-3">{eeatSignals.expertise.description}</p>
        <ul className="space-y-2">
          {eeatSignals.expertise.credentials.map((item, index) => (
            <li key={index} className="flex items-start gap-2 text-sm text-gray-700 dark:text-gray-300">
              <svg className="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              {item}
            </li>
          ))}
        </ul>
      </div>

      {/* Authority */}
      <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm">
        <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3 flex items-center gap-2">
          <svg className="w-6 h-6 text-purple-600" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M6.267 3.455a3.066 3.066 0 001.745-.723 3.066 3.066 0 013.976 0 3.066 3.066 0 001.745.723 3.066 3.066 0 012.812 2.812c.051.643.304 1.254.723 1.745a3.066 3.066 0 010 3.976 3.066 3.066 0 00-.723 1.745 3.066 3.066 0 01-2.812 2.812 3.066 3.066 0 00-1.745.723 3.066 3.066 0 01-3.976 0 3.066 3.066 0 00-1.745-.723 3.066 3.066 0 01-2.812-2.812 3.066 3.066 0 00-.723-1.745 3.066 3.066 0 010-3.976 3.066 3.066 0 00.723-1.745 3.066 3.066 0 012.812-2.812zm7.44 5.252a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
          </svg>
          Authority & Recognition
        </h3>
        <ul className="space-y-2">
          {eeatSignals.authority.buildingCredibility.map((item, index) => (
            <li key={index} className="flex items-start gap-2 text-sm text-gray-700 dark:text-gray-300">
              <svg className="w-5 h-5 text-purple-500 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
              </svg>
              {item}
            </li>
          ))}
        </ul>
      </div>

      {/* Trust */}
      <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm">
        <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3 flex items-center gap-2">
          <svg className="w-6 h-6 text-green-600" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M2.166 4.999A11.954 11.954 0 0010 1.944 11.954 11.954 0 0017.834 5c.11.65.166 1.32.166 2.001 0 5.225-3.34 9.67-8 11.317C5.34 16.67 2 12.225 2 7c0-.682.057-1.35.166-2.001zm11.541 3.708a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
          </svg>
          Trust & Security
        </h3>
        <div className="grid md:grid-cols-2 gap-4">
          <div>
            <h4 className="font-semibold text-gray-900 dark:text-white mb-2 text-sm">Current Measures:</h4>
            <ul className="space-y-1">
              {eeatSignals.trust.currentMeasures.map((item, index) => (
                <li key={index} className="text-sm text-gray-600 dark:text-gray-400">✓ {item}</li>
              ))}
            </ul>
          </div>
          <div>
            <h4 className="font-semibold text-gray-900 dark:text-white mb-2 text-sm">Future Goals:</h4>
            <ul className="space-y-1">
              {eeatSignals.trust.futureGoals.map((item, index) => (
                <li key={index} className="text-sm text-gray-600 dark:text-gray-400">→ {item}</li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}

// Master SEO Schema Component - Combines all critical schemas
export const MasterSEOSchemas: React.FC<{ includeRatings?: boolean; includeHowTo?: boolean; includeVideo?: boolean }> = ({
  includeRatings = true,
  includeHowTo = false,
  includeVideo = false,
}) => {
  return (
    <>
      <EnhancedLocalBusinessSchema />
      {includeRatings && <RatingsAndReviewsSchema />}
      {includeHowTo && <HowToSchema />}
      {includeVideo && <VideoSchema />}
    </>
  )
}

export default {
  RatingsAndReviewsSchema,
  HowToSchema,
  VideoSchema,
  EnhancedLocalBusinessSchema,
  ArticleSchema,
  BreadcrumbSchema,
  EEATSignals,
  MasterSEOSchemas,
}
