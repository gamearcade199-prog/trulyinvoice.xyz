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
  maxSizeMB = 10
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
          relative border-3 border-dashed rounded-2xl p-12 text-center cursor-pointer
          transition-all duration-300 ease-in-out
          ${isDragging 
            ? 'border-blue-500 bg-blue-50 scale-[1.02]' 
            : 'border-gray-300 bg-white hover:border-blue-400 hover:bg-blue-50/50'
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

        <div className="flex flex-col items-center gap-4">
          <div className={`
            p-6 rounded-full transition-all duration-300
            ${isDragging ? 'bg-blue-100 scale-110' : 'bg-blue-50'}
          `}>
            <Upload className={`w-12 h-12 ${isDragging ? 'text-blue-600' : 'text-blue-500'}`} />
          </div>

          <div>
            <h3 className="text-2xl font-semibold text-gray-800 mb-2">
              Upload your invoices
            </h3>
            <p className="text-gray-600">
              Drag and drop your files here, or{' '}
              <span className="text-blue-600 font-semibold">browse</span>
            </p>
          </div>

          <div className="text-sm text-gray-500">
            Supports PDF, JPG, PNG • Max {maxSizeMB}MB per file
          </div>
        </div>
      </div>

      {/* Selected Files */}
      {selectedFiles.length > 0 && (
        <div className="mt-6 space-y-3">
          <h4 className="font-semibold text-gray-700">Selected Files ({selectedFiles.length})</h4>
          {selectedFiles.map((file, index) => (
            <div
              key={index}
              className="flex items-center justify-between p-4 bg-white border border-gray-200 rounded-lg hover:border-blue-300 transition-colors"
            >
              <div className="flex items-center gap-3">
                <div className="p-2 bg-blue-50 rounded-lg">
                  <File className="w-5 h-5 text-blue-600" />
                </div>
                <div>
                  <p className="font-medium text-gray-800">{file.name}</p>
                  <p className="text-sm text-gray-500">
                    {(file.size / 1024 / 1024).toFixed(2)} MB
                  </p>
                </div>
              </div>
              <button
                onClick={(e) => {
                  e.stopPropagation()
                  removeFile(index)
                }}
                className="p-2 hover:bg-red-50 rounded-lg transition-colors"
              >
                <X className="w-5 h-5 text-gray-400 hover:text-red-500" />
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}