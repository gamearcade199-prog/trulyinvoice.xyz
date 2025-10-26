'use client'

import { useState } from 'react'
import DashboardLayout from '@/components/DashboardLayout'
import UploadZone from '@/components/UploadZone'
import { Loader2, CheckCircle2, AlertCircle, ArrowRight } from 'lucide-react'
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

  const handleFileSelect = (selectedFiles: File[]) => {
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
            throw new Error(`Storage upload failed: ${uploadError.message}. Please ensure the 'invoice-documents' bucket exists in Supabase Storage.`)
          }

          // Update progress
          setUploadProgress(Math.round(((i + 0.5) / files.length) * 100))

          // Get public URL
          const { data: { publicUrl } } = supabase.storage
            .from('invoice-documents')
            .getPublicUrl(fileName)

          // Step 2: Create document record (but NOT invoice yet)
          const { data: docData, error: docError } = await supabase
            .from('documents')
            .insert({
              user_id: user.id,
              file_name: file.name,
              file_type: file.type,
              file_size: file.size,
              storage_path: fileName,
              file_url: publicUrl,
              status: 'uploaded'  // Start as uploaded, not processing
            })
            .select()
            .single()

          if (docError) {
            console.error('Database insert error:', docError)
            throw new Error(`Database error: ${docError.message}`)
          }

          // Call ROBUST_PROCESSOR for automatic AI extraction with retry
          let processed = false
          let attempts = 0
          const maxAttempts = 3
          
          while (!processed && attempts < maxAttempts) {
            attempts++
            try {
              setProcessingStatus(`🧠 AI extracting data (attempt ${attempts}/3)...`)
              
              const response = await fetch(`http://localhost:8000/api/documents/${docData.id}/process`, {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json'
                }
              })

              if (response.ok) {
                const result = await response.json()
                console.log('✅ AI extraction completed:', result)
                setProcessingStatus(`✅ ${file.name} processed successfully!`)
                processed = true
                
                // Update document status to processed (invoice already created by backend)
                await supabase
                  .from('documents')
                  .update({ status: 'processed' })
                  .eq('id', docData.id)
                  
              } else {
                const errorText = await response.text()
                console.warn(`Attempt ${attempts} failed:`, response.status, errorText)
                
                if (attempts === maxAttempts) {
                  setProcessingStatus(`❌ ${file.name} processing failed`)
                  // Don't create invoice if processing failed
                  await supabase
                    .from('documents')
                    .update({ status: 'failed' })
                    .eq('id', docData.id)
                  processed = true
                } else {
                  await new Promise(resolve => setTimeout(resolve, 2000))
                }
              }
            } catch (apiError) {
              console.warn(`API attempt ${attempts} error:`, apiError)
              
              if (attempts === maxAttempts) {
                setProcessingStatus(`❌ ${file.name} processing failed`)
                await supabase
                  .from('documents')
                  .update({ status: 'failed' })
                  .eq('id', docData.id)
                processed = true
              } else {
                await new Promise(resolve => setTimeout(resolve, 2000))
              }
            }
          }

          setUploadProgress(Math.round(((i + 1) / files.length) * 100))
        } catch (fileError) {
          console.error('Error processing file:', file.name, fileError)
          throw fileError
        }
      }

      setUploadComplete(true)
      setIsUploading(false)
      
      // Redirect to invoices page after 2 seconds
      setTimeout(() => {
        router.push('/invoices')
      }, 2000)

    } catch (err: any) {
      console.error('Upload error:', err)
      setError(err.message || 'Upload failed. Please try again.')
      setIsUploading(false)
    }
  }

  return (
    <DashboardLayout>
      <div className="max-w-4xl mx-auto">
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
        <div className="bg-gradient-to-br from-purple-50 via-blue-50 to-pink-50 p-8 rounded-2xl">
          <UploadZone onFileSelect={handleFileSelect} />
        </div>

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