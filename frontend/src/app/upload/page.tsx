'use client'

import { useState } from 'react'
import DashboardLayout from '@/components/DashboardLayout'
import UploadZone from '@/components/UploadZone'
import { Loader2, CheckCircle2, AlertCircle, ArrowRight } from 'lucide-react'
import Link from 'next/link'
import { supabase } from '@/lib/supabase'
import { useRouter } from 'next/navigation'

export default function UploadPageRobust() {
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
    setProcessingStatus('')
  }

  const handleUpload = async () => {
    if (files.length === 0) return

    setIsUploading(true)
    setUploadProgress(0)
    setError('')
    setProcessingStatus('Starting upload...')

    try {
      // Get current user
      const { data: { user } } = await supabase.auth.getUser()
      if (!user) {
        throw new Error('You must be logged in to upload files')
      }

      console.log('👤 User authenticated:', user.id)
      
      for (let i = 0; i < files.length; i++) {
        const file = files[i]
        setProcessingStatus(`📤 Uploading ${file.name}...`)
        console.log(`📤 Starting upload for: ${file.name}`)
        
        try {
          // Step 1: Upload to Supabase Storage with error handling
          const fileName = `${user.id}/${Date.now()}_${file.name.replace(/[^a-zA-Z0-9.-]/g, '_')}`
          console.log(`🗂️ Storage path: ${fileName}`)
          
          const { data: uploadData, error: uploadError } = await supabase.storage
            .from('invoice-documents')
            .upload(fileName, file, {
              cacheControl: '3600',
              upsert: true  // Allow overwrite if exists
            })

          if (uploadError) {
            console.error('❌ Storage upload error:', uploadError)
            
            // Try to create bucket if it doesn't exist
            if (uploadError.message.includes('not found') || uploadError.message.includes('bucket')) {
              console.log('🪣 Trying to create bucket...')
              
              // Create public bucket
              const { error: bucketError } = await supabase.storage.createBucket('invoice-documents', {
                public: true
              })
              
              if (bucketError && !bucketError.message.includes('already exists')) {
                console.error('❌ Bucket creation failed:', bucketError)
                throw new Error(`Storage setup failed: ${bucketError.message}`)
              }
              
              // Retry upload
              const { data: retryData, error: retryError } = await supabase.storage
                .from('invoice-documents')
                .upload(fileName, file, { upsert: true })
                
              if (retryError) {
                throw new Error(`Storage upload failed: ${retryError.message}`)
              }
            } else {
              throw new Error(`Storage upload failed: ${uploadError.message}`)
            }
          }

          console.log('✅ File uploaded to storage')
          setUploadProgress(25)

          // Step 2: Get public URL
          const { data: { publicUrl } } = supabase.storage
            .from('invoice-documents')
            .getPublicUrl(fileName)

          console.log('🔗 Public URL generated:', publicUrl)
          setUploadProgress(50)

          // Step 3: Create document record
          setProcessingStatus(`💾 Creating document record...`)
          
          const { data: docData, error: docError } = await supabase
            .from('documents')
            .insert({
              user_id: user.id,
              file_name: file.name,
              file_type: file.type,
              file_size: file.size,
              storage_path: fileName,
              file_url: publicUrl,
              status: 'uploaded'
            })
            .select()
            .single()

          if (docError) {
            console.error('❌ Database insert error:', docError)
            throw new Error(`Database error: ${docError.message}`)
          }

          console.log('✅ Document record created:', docData.id)
          setUploadProgress(75)

          // Step 4: Process with AI (with comprehensive retry)
          setProcessingStatus(`🧠 AI processing ${file.name}...`)
          let processed = false
          let attempts = 0
          const maxAttempts = 3

          while (!processed && attempts < maxAttempts) {
            attempts++
            console.log(`🔄 AI processing attempt ${attempts}/${maxAttempts}`)
            
            try {
              const response = await fetch(`http://localhost:8000/api/documents/${docData.id}/process`, {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json'
                }
              })

              console.log(`🔍 API response: ${response.status}`)

              if (response.ok) {
                const result = await response.json()
                console.log('✅ AI processing completed:', result)
                setProcessingStatus(`✅ ${file.name} processed successfully!`)
                processed = true
                
                // Update document status
                await supabase
                  .from('documents')
                  .update({ status: 'processed' })
                  .eq('id', docData.id)
                  
                setUploadProgress(100)
                
              } else {
                const errorText = await response.text()
                console.warn(`⚠️ Attempt ${attempts} failed: ${response.status} - ${errorText}`)
                
                if (attempts === maxAttempts) {
                  console.log('❌ All AI processing attempts failed')
                  setProcessingStatus(`⚠️ ${file.name} uploaded but AI processing failed`)
                  
                  // Still mark as uploaded so user can retry later
                  await supabase
                    .from('documents')
                    .update({ status: 'upload_complete' })
                    .eq('id', docData.id)
                  
                  processed = true
                  setUploadProgress(100)
                } else {
                  // Wait before retry
                  console.log(`⏳ Waiting 3 seconds before retry...`)
                  await new Promise(resolve => setTimeout(resolve, 3000))
                }
              }
            } catch (apiError) {
              console.warn(`⚠️ API attempt ${attempts} error:`, apiError)
              
              if (attempts === maxAttempts) {
                console.log('❌ All API attempts failed')
                setProcessingStatus(`⚠️ ${file.name} uploaded but processing unavailable`)
                
                await supabase
                  .from('documents')
                  .update({ status: 'upload_complete' })
                  .eq('id', docData.id)
                
                processed = true
                setUploadProgress(100)
              } else {
                await new Promise(resolve => setTimeout(resolve, 3000))
              }
            }
          }

        } catch (fileError: unknown) {
          console.error(`❌ Error processing file ${file.name}:`, fileError)
          const errorMessage = fileError instanceof Error ? fileError.message : 'Unknown error'
          setProcessingStatus(`❌ Failed to process ${file.name}: ${errorMessage}`)
          throw fileError
        }
      }

      setUploadComplete(true)
      setIsUploading(false)
      setProcessingStatus(`🎉 Successfully processed ${files.length} file(s)!`)
      
      // Auto-redirect to invoices page after 3 seconds
      console.log('🔄 Redirecting to invoices page in 3 seconds...')
      setTimeout(() => {
        router.push('/invoices')
      }, 3000)

    } catch (err: any) {
      console.error('💥 Upload process failed:', err)
      setError(err.message || 'Upload failed. Please try again.')
      setIsUploading(false)
      setProcessingStatus('')
    }
  }

  return (
    <DashboardLayout>
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-3">
            Upload Your Invoices
          </h1>
          <p className="text-lg text-gray-600 dark:text-gray-400">
            Our AI will extract all the data automatically in seconds
          </p>
        </div>

        {/* Error Message */}
        {error && (
          <div className="mb-6 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-300 px-4 py-3 rounded-lg flex items-center gap-2">
            <AlertCircle className="w-5 h-5" />
            <div>
              <p className="font-semibold">Upload Failed</p>
              <p className="text-sm">{error}</p>
            </div>
          </div>
        )}

        {/* Upload Zone */}
        <div className="bg-gradient-to-br from-purple-50 via-blue-50 to-pink-50 dark:from-purple-900/20 dark:via-blue-900/20 dark:to-pink-900/20 p-8 rounded-2xl">
          <UploadZone onFileSelect={handleFileSelect} />
        </div>

        {/* Upload Progress */}
        {isUploading && (
          <div className="mt-8 bg-gray-50 dark:bg-gray-900 p-6 rounded-xl border border-gray-200 dark:border-gray-800">
            <div className="flex items-center gap-3 mb-4">
              <Loader2 className="w-6 h-6 text-blue-600 dark:text-blue-400 animate-spin" />
              <span className="font-semibold text-gray-900 dark:text-white">Processing your invoices...</span>
            </div>
            <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3 overflow-hidden">
              <div
                className="bg-gradient-to-r from-blue-500 to-blue-600 h-full rounded-full transition-all duration-300"
                style={{ width: `${uploadProgress}%` }}
              />
            </div>
            <div className="flex justify-between items-center mt-2">
              <p className="text-sm text-gray-600 dark:text-gray-400">{uploadProgress}% complete</p>
              {processingStatus && (
                <p className="text-sm text-blue-600 dark:text-blue-400 font-medium">{processingStatus}</p>
              )}
            </div>
          </div>
        )}

        {/* Upload Complete */}
        {uploadComplete && (
          <div className="mt-8 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 p-6 rounded-xl">
            <div className="flex items-start gap-4">
              <div className="flex-shrink-0">
                <CheckCircle2 className="w-8 h-8 text-green-600 dark:text-green-400" />
              </div>
              <div className="flex-1">
                <h3 className="font-semibold text-green-900 dark:text-green-100 text-lg mb-2">
                  Upload Successful!
                </h3>
                <p className="text-green-700 dark:text-green-300 mb-4">
                  {files.length} invoice{files.length > 1 ? 's' : ''} processed successfully! 
                  🤖 Redirecting to your invoices...
                </p>
                <Link
                  href="/invoices"
                  className="inline-flex items-center gap-2 px-4 py-2 bg-green-600 dark:bg-green-500 text-white rounded-lg hover:bg-green-700 dark:hover:bg-green-600 transition-colors font-semibold"
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
              className="px-8 py-4 bg-blue-600 dark:bg-blue-500 text-white rounded-xl hover:bg-blue-700 dark:hover:bg-blue-600 transition-all font-semibold text-lg shadow-lg hover:shadow-xl flex items-center gap-2"
            >
              Process {files.length} Invoice{files.length > 1 ? 's' : ''}
              <ArrowRight className="w-5 h-5" />
            </button>
          </div>
        )}

        {/* Info Cards */}
        <div className="mt-12 grid md:grid-cols-3 gap-6">
          <div className="text-center p-6 bg-gray-50 dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800">
            <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/50 rounded-lg flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl">📄</span>
            </div>
            <h3 className="font-semibold text-gray-900 dark:text-white mb-2">Supported Formats</h3>
            <p className="text-gray-600 dark:text-gray-400 text-sm">PDF, JPG, PNG up to 10MB</p>
          </div>
          
          <div className="text-center p-6 bg-gray-50 dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800">
            <div className="w-12 h-12 bg-green-100 dark:bg-green-900/50 rounded-lg flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl">🤖</span>
            </div>
            <h3 className="font-semibold text-gray-900 dark:text-white mb-2">AI Extraction</h3>
            <p className="text-gray-600 dark:text-gray-400 text-sm">Vendor, amounts, dates & GST</p>
          </div>
          
          <div className="text-center p-6 bg-gray-50 dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800">
            <div className="w-12 h-12 bg-purple-100 dark:bg-purple-900/50 rounded-lg flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl">⚡</span>
            </div>
            <h3 className="font-semibold text-gray-900 dark:text-white mb-2">Fast Processing</h3>
            <p className="text-gray-600 dark:text-gray-400 text-sm">Results in under 10 seconds</p>
          </div>
        </div>
      </div>
    </DashboardLayout>
  )
}
