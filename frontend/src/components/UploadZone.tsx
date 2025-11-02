'use client'

import { useState, useRef, DragEvent } from 'react'
import { Upload, File, X, CheckCircle2 } from 'lucide-react'

interface UploadZoneProps {
  onFileSelect: (files: File[]) => void
  acceptedTypes?: string
  multiple?: boolean
  maxSizeMB?: number
}

export default function UploadZone({
  onFileSelect,
  acceptedTypes = '.pdf,.jpg,.jpeg,.png',
  multiple = true,
  maxSizeMB = 25
}: UploadZoneProps) {
  const [isDragging, setIsDragging] = useState(false)
  const [selectedFiles, setSelectedFiles] = useState<File[]>([])
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleDrag = (e: DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
  }

  const handleDragIn = (e: DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(true)
  }

  const handleDragOut = (e: DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(false)
  }

  const handleDrop = (e: DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(false)

    const files = Array.from(e.dataTransfer.files)
    handleFiles(files)
  }

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const files = Array.from(e.target.files)
      handleFiles(files)
    }
  }

  const handleFiles = (files: File[]) => {
    // Filter valid files
    const validFiles = files.filter(file => {
      const sizeMB = file.size / (1024 * 1024)
      return sizeMB <= maxSizeMB
    })

    setSelectedFiles(validFiles)
    onFileSelect(validFiles)
  }

  const removeFile = (index: number) => {
    const newFiles = selectedFiles.filter((_, i) => i !== index)
    setSelectedFiles(newFiles)
    onFileSelect(newFiles)
  }

  return (
    <div className="w-full">
      {/* Upload Zone */}
      <div
        onDragEnter={handleDragIn}
        onDragLeave={handleDragOut}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
        className={`
          relative border-3 border-dashed rounded-2xl lg:rounded-3xl p-4 md:p-6 lg:p-4 text-center cursor-pointer
          transition-all duration-300 ease-in-out hover:scale-[1.01] lg:hover:scale-[1.02]
          ${isDragging 
            ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/30 scale-[1.02] lg:scale-[1.03] shadow-2xl' 
            : 'border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 hover:border-blue-400 hover:bg-blue-50/50 dark:hover:bg-blue-900/20 hover:shadow-xl'
          }
        `}
      >
        <input
          ref={fileInputRef}
          type="file"
          multiple={multiple}
          accept={acceptedTypes}
          onChange={handleFileInput}
          className="hidden"
        />

        <div className="flex flex-col items-center gap-2 md:gap-3 lg:gap-2">
          <div className={`
            p-2 md:p-3 lg:p-2 rounded-full transition-all duration-300
            ${isDragging ? 'bg-blue-100 dark:bg-blue-900/50 scale-110 lg:scale-125' : 'bg-blue-50 dark:bg-blue-900/30'}
          `}>
            <Upload className={`w-6 h-6 md:w-8 md:h-8 lg:w-8 lg:h-8 ${isDragging ? 'text-blue-600 dark:text-blue-400' : 'text-blue-500 dark:text-blue-400'}`} />
          </div>

          <div>
            <h3 className="text-base md:text-lg lg:text-base font-semibold text-gray-800 dark:text-white mb-1 md:mb-2 lg:mb-1">
              Upload your invoices
            </h3>
            <p className="text-sm md:text-base lg:text-sm text-gray-600 dark:text-gray-400">
              Drag and drop your files here, or{' '}
              <span className="text-blue-600 dark:text-blue-400 font-semibold">browse</span>
            </p>
            <div className="hidden lg:block mt-2 text-sm text-gray-500 dark:text-gray-500">
              Multiple files supported • Instant AI processing • No account required for preview
            </div>
          </div>

          <div className="text-xs md:text-sm lg:text-xs text-gray-500 dark:text-gray-500">
            Supports PDF, JPG, PNG • Max {maxSizeMB}MB per file
          </div>
        </div>
      </div>

      {/* Selected Files */}
      {selectedFiles.length > 0 && (
        <div className="mt-3 md:mt-4 space-y-2 md:space-y-3">
          <h4 className="font-semibold text-gray-700 dark:text-gray-300 text-sm md:text-base">
            Selected Files ({selectedFiles.length})
          </h4>
          {selectedFiles.map((file, index) => (
            <div
              key={index}
              className="flex items-center justify-between p-2 md:p-3 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg hover:border-blue-300 dark:hover:border-blue-600 transition-colors"
            >
              <div className="flex items-center gap-3">
                <div className="p-2 bg-blue-50 dark:bg-blue-900/30 rounded-lg">
                  <File className="w-4 h-4 md:w-5 md:h-5 text-blue-600 dark:text-blue-400" />
                </div>
                <div className="min-w-0 flex-1">
                  <p className="font-medium text-gray-800 dark:text-white text-sm md:text-base truncate">
                    {file.name}
                  </p>
                  <p className="text-xs md:text-sm text-gray-500 dark:text-gray-400">
                    {(file.size / 1024 / 1024).toFixed(2)} MB
                  </p>
                </div>
              </div>
              <button
                onClick={(e) => {
                  e.stopPropagation()
                  removeFile(index)
                }}
                className="p-2 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-colors flex-shrink-0"
              >
                <X className="w-4 h-4 md:w-5 md:h-5 text-gray-400 dark:text-gray-500 hover:text-red-500 dark:hover:text-red-400" />
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}