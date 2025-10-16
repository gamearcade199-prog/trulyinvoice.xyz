import React from 'react'

interface ConfidenceIndicatorProps {
  confidence: number
  label?: string
  size?: 'sm' | 'md' | 'lg'
}

export default function ConfidenceIndicator({ 
  confidence, 
  label,
  size = 'sm' 
}: ConfidenceIndicatorProps) {
  // Convert confidence (0-1) to rating (1-10)
  const rating = Math.round(confidence * 10)
  
  // Determine color based on confidence level
  const getColorClass = (rating: number) => {
    if (rating >= 9) return 'text-green-600 bg-green-100 border-green-200'
    if (rating >= 7) return 'text-yellow-600 bg-yellow-100 border-yellow-200'
    if (rating >= 5) return 'text-orange-600 bg-orange-100 border-orange-200'
    return 'text-red-600 bg-red-100 border-red-200'
  }
  
  // Determine size classes
  const getSizeClass = (size: string) => {
    switch (size) {
      case 'lg': return 'px-3 py-1 text-sm'
      case 'md': return 'px-2 py-1 text-xs'
      case 'sm': return 'px-1.5 py-0.5 text-xs'
      default: return 'px-1.5 py-0.5 text-xs'
    }
  }
  
  if (!confidence || confidence === 0) {
    return (
      <span className="px-1.5 py-0.5 text-xs rounded-full bg-gray-100 text-gray-500 border border-gray-200">
        N/A
      </span>
    )
  }
  
  return (
    <div className="flex items-center gap-1">
      {label && (
        <span className="text-xs text-gray-500">{label}:</span>
      )}
      <span 
        className={`${getSizeClass(size)} rounded-full border font-medium ${getColorClass(rating)}`}
        title={`Confidence: ${(confidence * 100).toFixed(1)}% (${rating}/10)`}
      >
        {rating}/10
      </span>
    </div>
  )
}