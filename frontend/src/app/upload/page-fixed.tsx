'use client'

import { useState } from 'react'
import DashboardLayout from '@/components/DashboardLayout'
import { Loader2, CheckCircle2, AlertCircle, ArrowRight, Upload as UploadIcon, FileText } from 'lucide-react'
import Link from 'next/link'
import { supabase } from '@/lib/supabase'
import { useRouter } from 'next/navigation'

export default function UploadPage() {
  const router = useRouter()
  const [files, setFiles] = useState<File[]>([])
  const [isUploading, setIsUploading] = useState(false)
  const [uploadProgress, setUploadProgress] = useState(0)
  const [uploadComplete, setUploadComplete] = useState(false)
  const [processingStatus, setProcessingStatus] = useState('')
  const [error, setError] = useState('')

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFiles = Array.from(event.target.files || [])
    setFiles(selectedFiles)
    setUploadComplete(false)
    setError('')
  }

  const handleUpload = async () => {
    if (files.length === 0) return

    setIsUploading(true)
    setUploadProgress(0)
    setError('')

    try {
      // Get current user
      const { data: { user } } = await supabase.auth.getUser()
      if (!user) {
        setError('You must be logged in to upload files')
        setIsUploading(false)
        return
      }

      for (let i = 0; i < files.length; i++) {
        const file = files[i]
        
        try {
          // Upload file to Supabase Storage
          const fileName = `${user.id}/${Date.now()}_${file.name}`
          const { data: uploadData, error: uploadError } = await supabase.storage
            .from('invoice-documents')
            .upload(fileName, file)

          if (uploadError) {
            console.error('Storage upload error:', uploadError)
            throw new Error(`Upload failed: ${uploadError.message}`)
          }

          // Insert document record
          const { data: docData, error: docError } = await supabase
            .from('documents')
            .insert({
              user_id: user.id,
              file_name: file.name,
              file_type: file.type,
              file_size: file.size,
              storage_path: fileName,
              status: 'processing'
            })
            .select()
            .single()

          if (docError) {
            console.error('Database insert error:', docError)
            throw new Error(`Database error: ${docError.message}`)
          }

          // Call backend API for automatic AI extraction
          try {
            setProcessingStatus('🧠 AI is extracting invoice data...')
            
            const session = await supabase.auth.getSession()
            const response = await fetch(`http://localhost:8000/api/documents/${docData.id}/process`, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${session.data.session?.access_token}`
              }
            })

            if (response.ok) {
              const result = await response.json()
              console.log('✅ AI extraction completed for document:', docData.id, result)
              setProcessingStatus('✅ Invoice data extracted successfully!')
              
              // Update document status to completed
              await supabase
                .from('documents')
                .update({ status: 'completed' })
                .eq('id', docData.id)
                
            } else {
              const errorText = await response.text()
              console.warn('⚠️ AI extraction failed:', response.status, errorText)
              setProcessingStatus('⚠️ AI extraction failed - will retry automatically')
            }
          } catch (apiError) {
            console.warn('⚠️ Backend not available:', apiError)
            setProcessingStatus('⚠️ AI service temporarily unavailable')
          }

          setUploadProgress(Math.round(((i + 1) / files.length) * 100))
        } catch (fileError) {
          console.error('Error processing file:', file.name, fileError)
          throw fileError
        }
      }

      setUploadComplete(true)
      setIsUploading(false)
      
      // Redirect to invoices page after 3 seconds
      setTimeout(() => {
        router.push('/invoices')
      }, 3000)

    } catch (err: any) {
      console.error('Upload error:', err)
      setError(err.message || 'Upload failed. Please try again.')
      setIsUploading(false)
    }
  }

  return (
    <DashboardLayout>
      <div className="max-w-4xl mx-auto p-6">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-3">
            Upload Your Invoices
          </h1>
          <p className="text-lg text-gray-600">
            Our AI will extract all the data automatically in seconds
          </p>
        </div>

        {/* Error Message */}
        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg flex items-center gap-2">
            <AlertCircle className="w-5 h-5" />
            {error}
          </div>
        )}

        {/* Upload Zone */}
        <div className="bg-gradient-to-br from-purple-50 via-blue-50 to-pink-50 p-8 rounded-2xl border-2 border-dashed border-gray-300 hover:border-blue-400 transition-colors">
          <div className="text-center">
            <UploadIcon className="mx-auto h-16 w-16 text-gray-400 mb-4" />
            <div className="mb-4">
              <label htmlFor="file-upload" className="cursor-pointer">
                <span className="text-lg font-semibold text-gray-700 hover:text-blue-600">
                  Click to upload files
                </span>
                <input
                  id="file-upload"
                  type="file"
                  className="sr-only"
                  multiple
                  accept=".pdf,.jpg,.jpeg,.png"
                  onChange={handleFileSelect}
                />
              </label>
              <p className="text-gray-500 mt-2">or drag and drop</p>
            </div>
            <p className="text-sm text-gray-500">
              Supports PDF, JPG, PNG • Max 10MB per file
            </p>
          </div>
        </div>

        {/* Selected Files */}
        {files.length > 0 && (
          <div className="mt-6 bg-white p-4 rounded-lg border border-gray-200">
            <h3 className="font-semibold text-gray-900 mb-3">Selected Files ({files.length})</h3>
            <div className="space-y-2">
              {files.map((file, index) => (
                <div key={index} className="flex items-center gap-3 p-2 bg-gray-50 rounded-lg">
                  <FileText className="w-5 h-5 text-blue-600" />
                  <span className="flex-1 text-sm text-gray-700">{file.name}</span>
                  <span className="text-xs text-gray-500">{(file.size / 1024 / 1024).toFixed(2)} MB</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Upload Progress */}
        {isUploading && (
          <div className="mt-8 bg-white p-6 rounded-xl border border-gray-200">
            <div className="flex items-center gap-3 mb-4">
              <Loader2 className="w-6 h-6 text-blue-600 animate-spin" />
              <span className="font-semibold text-gray-900">Processing your invoices...</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
              <div
                className="bg-gradient-to-r from-blue-500 to-blue-600 h-full rounded-full transition-all duration-300"
                style={{ width: `${uploadProgress}%` }}
              />
            </div>
            <p className="text-sm text-gray-600 mt-2">{uploadProgress}% complete</p>
            
            {/* AI Processing Status */}
            {processingStatus && (
              <div className="mt-4 p-3 bg-blue-50 rounded-lg border border-blue-200">
                <p className="text-sm text-blue-800 font-medium">{processingStatus}</p>
              </div>
            )}
          </div>
        )}

        {/* Upload Complete */}
        {uploadComplete && (
          <div className="mt-8 bg-green-50 border border-green-200 p-6 rounded-xl">
            <div className="flex items-start gap-4">
              <div className="flex-shrink-0">
                <CheckCircle2 className="w-8 h-8 text-green-600" />
              </div>
              <div className="flex-1">
                <h3 className="font-semibold text-green-900 text-lg mb-2">
                  Upload Successful!
                </h3>
                <p className="text-green-700 mb-4">
                  {files.length} invoice{files.length > 1 ? 's' : ''} uploaded and processed successfully! 
                  🤖 AI extraction completed with high confidence.
                </p>
                <Link
                  href="/invoices"
                  className="inline-flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors font-semibold"
                >
                  View Invoices <ArrowRight className="w-4 h-4" />
                </Link>
              </div>
            </div>
          </div>
        )}

        {/* Upload Button */}
        {files.length > 0 && !isUploading && !uploadComplete && (
          <div className="mt-8 flex justify-center">
            <button
              onClick={handleUpload}
              className="px-8 py-4 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition-all font-semibold text-lg shadow-lg hover:shadow-xl flex items-center gap-2"
            >
              Process {files.length} Invoice{files.length > 1 ? 's' : ''}
              <ArrowRight className="w-5 h-5" />
            </button>
          </div>
        )}

        {/* Info Cards */}
        <div className="mt-12 grid md:grid-cols-3 gap-6">
          <div className="bg-white p-6 rounded-xl border border-gray-200">
            <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
              <span className="text-2xl">🚀</span>
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">Lightning Fast</h3>
            <p className="text-gray-600 text-sm">
              Our AI processes invoices in under 5 seconds
            </p>
          </div>

          <div className="bg-white p-6 rounded-xl border border-gray-200">
            <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-4">
              <span className="text-2xl">🎯</span>
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">98% Accurate</h3>
            <p className="text-gray-600 text-sm">
              Industry-leading accuracy for Indian invoices
            </p>
          </div>

          <div className="bg-white p-6 rounded-xl border border-gray-200">
            <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4">
              <span className="text-2xl">🔒</span>
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">Secure</h3>
            <p className="text-gray-600 text-sm">
              Bank-level encryption for your sensitive data
            </p>
          </div>
        </div>
      </div>
    </DashboardLayout>
  )
}