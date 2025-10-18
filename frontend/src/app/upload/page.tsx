'use client'

import { useState } from 'react'
import DashboardLayout from '@/components/DashboardLayout'
import UploadZone from '@/components/UploadZone'
import { 
  AlertCircle, 
  CheckCircle2, 
  ArrowRight, 
  Loader2, 
  X 
} from 'lucide-react'
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

  const [anonymousResult, setAnonymousResult] = useState<any>(null)
  const [showAnonymousModal, setShowAnonymousModal] = useState(false)

  const handleFileSelect = (selectedFiles: File[]) => {
    setFiles(selectedFiles)
    setUploadComplete(false)
    setError('')
    setProcessingStatus('')
    setAnonymousResult(null)
    setShowAnonymousModal(false)
  }

  const showAnonymousPreview = (result: any, fileName: string) => {
    setAnonymousResult({ ...result, fileName })
    setShowAnonymousModal(true)
    setProcessingStatus(`🎉 ${fileName} analyzed! Sign up to save results.`)
  }

  const handleSignUpRedirect = () => {
    router.push('/auth?mode=signup&redirect=/upload')
  }

  const handleUpload = async () => {
    if (files.length === 0) return

    setIsUploading(true)
    setUploadProgress(0)
    setError('')
    setProcessingStatus('Starting upload...')

    try {
      // Get current user (may be null for anonymous users)
      const { data: { user } } = await supabase.auth.getUser()
      const isAnonymous = !user
      
      if (isAnonymous) {
        console.log('👻 Anonymous user detected - enabling preview mode')
        setProcessingStatus('🎯 Processing anonymously for preview...')
      } else {
        console.log('👤 User authenticated:', user.id)
      }
      
      for (let i = 0; i < files.length; i++) {
        const file = files[i]
        setProcessingStatus(`📤 Processing ${file.name}...`)
        console.log(`📤 Starting processing for: ${file.name}`)
        
        try {
          if (isAnonymous) {
            // Anonymous processing flow - direct to backend without storage
            setUploadProgress(25)
            setProcessingStatus(`🧠 AI analyzing ${file.name}...`)
            
            const formData = new FormData()
            formData.append('file', file)
            
            // Try multiple API URLs for better reliability
            const apiUrls = [
              'http://localhost:8000', // Local development
              process.env.NEXT_PUBLIC_API_URL || 'https://trulyinvoice-backend.onrender.com', // Production
              'https://trulyinvoice-backend.onrender.com' // Fallback
            ]
            
            let processed = false
            let lastError = null
            
            for (const apiUrl of apiUrls) {
              if (processed) break
              
              try {
                console.log(`🔄 Trying API endpoint: ${apiUrl}`)
                setProcessingStatus(`🔄 Connecting to AI service...`)
                
                const response = await fetch(`${apiUrl}/api/documents/process-anonymous`, {
                  method: 'POST',
                  body: formData,
                  // Remove Content-Type header to let browser set it with boundary for FormData
                })
                
                setUploadProgress(75)
                
                if (!response.ok) {
                  const errorText = await response.text()
                  throw new Error(`API Error ${response.status}: ${errorText}`)
                }
                
                const result = await response.json()
                console.log('✅ Anonymous processing completed:', result)
                setUploadProgress(100)
                
                // Show preview popup with extracted data
                showAnonymousPreview(result, file.name)
                processed = true
                
              } catch (apiError: any) {
                console.warn(`⚠️ API endpoint ${apiUrl} failed:`, apiError.message)
                lastError = apiError
                
                // If this is not the last URL, continue to next
                if (apiUrl !== apiUrls[apiUrls.length - 1]) {
                  continue
                }
              }
            }
            
            if (!processed) {
              // All API endpoints failed, show user-friendly error
              throw new Error(`Unable to process invoice. Please try again later. (${lastError?.message || 'Service unavailable'})`)
            }
            
          } else {
            // Authenticated user flow - existing logic
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
              const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
              const response = await fetch(`${apiUrl}/api/documents/${docData.id}/process`, {
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
          
          } // End of authenticated user flow

        } catch (fileError: unknown) {
          console.error(`❌ Error processing file ${file.name}:`, fileError)
          const errorMessage = fileError instanceof Error ? fileError.message : 'Unknown error'
          setProcessingStatus(`❌ Failed to process ${file.name}: ${errorMessage}`)
          throw fileError
        }
      }

      if (!isAnonymous) {
        setUploadComplete(true)
        setIsUploading(false)
        setProcessingStatus(`🎉 Successfully processed ${files.length} file(s)!`)
        
        // Auto-redirect to invoices page after 3 seconds
        console.log('🔄 Redirecting to invoices page in 3 seconds...')
        setTimeout(() => {
          router.push('/invoices')
        }, 3000)
      } else {
        setIsUploading(false)
        // Anonymous users see preview modal instead of redirect
      }

    } catch (err: any) {
      console.error('💥 Upload process failed:', err)
      setError(err.message || 'Upload failed. Please try again.')
      setIsUploading(false)
      setProcessingStatus('')
    }
  }

  return (
    <DashboardLayout>
      <div className="max-w-6xl mx-auto px-4 md:px-0">
        {/* Header - Desktop Enhanced */}
        <div className="text-center mb-6 md:mb-8">
          <h1 className="text-2xl md:text-4xl lg:text-5xl font-bold text-gray-900 dark:text-white mb-2 md:mb-3">
            Upload Your Invoices
          </h1>
          <p className="text-base md:text-lg lg:text-xl text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
            Our AI will extract all the data automatically in seconds
          </p>
          <div className="flex items-center justify-center gap-4 mt-4 text-sm text-gray-500 dark:text-gray-400">
            <span className="flex items-center gap-1">
              <span className="w-2 h-2 bg-green-500 rounded-full"></span>
              PDF Support
            </span>
            <span className="flex items-center gap-1">
              <span className="w-2 h-2 bg-blue-500 rounded-full"></span>
              Image Recognition
            </span>
            <span className="flex items-center gap-1">
              <span className="w-2 h-2 bg-purple-500 rounded-full"></span>
              60+ Fields Extracted
            </span>
          </div>
        </div>

        {/* Error Message - Mobile Optimized */}
        {error && (
          <div className="mb-4 md:mb-6 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-300 px-3 md:px-4 py-3 rounded-lg flex items-center gap-2 mx-4 md:mx-0">
            <AlertCircle className="w-4 h-4 md:w-5 md:h-5 flex-shrink-0" />
            <div className="min-w-0">
              <p className="font-semibold text-sm md:text-base">Upload Failed</p>
              <p className="text-xs md:text-sm break-words">{error}</p>
            </div>
          </div>
        )}

        {/* Upload Zone - Desktop Enhanced */}
        <div className="bg-gradient-to-br from-purple-50 via-blue-50 to-pink-50 dark:from-purple-900/20 dark:via-blue-900/20 dark:to-pink-900/20 p-4 md:p-8 lg:p-12 rounded-2xl mx-4 md:mx-0 lg:rounded-3xl">
          <UploadZone onFileSelect={handleFileSelect} />
        </div>

        {/* Upload Progress - Desktop Enhanced */}
        {isUploading && (
          <div className="mt-4 md:mt-8 bg-white dark:bg-gray-900 p-4 md:p-6 lg:p-8 rounded-xl lg:rounded-2xl border border-gray-200 dark:border-gray-800 shadow-lg md:shadow-xl sticky top-4 z-10 mx-4 md:mx-0">
            <div className="flex items-center gap-3 mb-4">
              <Loader2 className="w-5 h-5 md:w-6 md:h-6 lg:w-8 lg:h-8 text-blue-600 dark:text-blue-400 animate-spin" />
              <span className="font-semibold text-gray-900 dark:text-white text-sm md:text-base lg:text-lg">
                Processing your invoices...
              </span>
            </div>
            
            {/* Sleek Progress Bar - Desktop Enhanced */}
            <div className="relative w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3 md:h-4 lg:h-6 overflow-hidden">
              <div
                className="bg-gradient-to-r from-blue-500 via-purple-500 to-blue-600 h-full rounded-full transition-all duration-500 ease-out shadow-lg"
                style={{ width: `${uploadProgress}%` }}
              >
                {/* Animated shimmer effect */}
                <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/30 to-transparent animate-pulse"></div>
                {/* Progress percentage on desktop */}
                <div className="hidden lg:flex absolute inset-0 items-center justify-center">
                  <span className="text-white text-sm font-bold drop-shadow-lg">
                    {uploadProgress}%
                  </span>
                </div>
              </div>
            </div>
            
            <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center mt-3 gap-2 sm:gap-0">
              <p className="text-xs md:text-sm lg:text-base text-gray-600 dark:text-gray-400 font-medium">
                {uploadProgress}% complete
              </p>
              {processingStatus && (
                <p className="text-xs md:text-sm lg:text-base text-blue-600 dark:text-blue-400 font-medium break-words">
                  {processingStatus}
                </p>
              )}
            </div>
          </div>
        )}

        {/* Upload Complete - Mobile Optimized */}
        {uploadComplete && (
          <div className="mt-4 md:mt-8 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 p-4 md:p-6 rounded-xl mx-4 md:mx-0">
            <div className="flex items-start gap-3 md:gap-4">
              <div className="flex-shrink-0">
                <CheckCircle2 className="w-6 h-6 md:w-8 md:h-8 text-green-600 dark:text-green-400" />
              </div>
              <div className="flex-1 min-w-0">
                <h3 className="font-semibold text-green-900 dark:text-green-100 text-base md:text-lg mb-2">
                  Upload Successful!
                </h3>
                <p className="text-green-700 dark:text-green-300 mb-4 text-sm md:text-base">
                  {files.length} invoice{files.length > 1 ? 's' : ''} processed successfully! 
                  🤖 Redirecting to your invoices...
                </p>
                <Link
                  href="/invoices"
                  className="inline-flex items-center gap-2 px-3 md:px-4 py-2 bg-green-600 dark:bg-green-500 text-white rounded-lg hover:bg-green-700 dark:hover:bg-green-600 transition-colors font-semibold text-sm md:text-base"
                >
                  View Invoices <ArrowRight className="w-4 h-4" />
                </Link>
              </div>
            </div>
          </div>
        )}

        {/* Upload Button - Mobile Optimized */}
        {files.length > 0 && !isUploading && !uploadComplete && (
          <div className="mt-6 md:mt-8 flex justify-center px-4 md:px-0">
            <button
              onClick={handleUpload}
              className="w-full md:w-auto px-6 md:px-8 py-3 md:py-4 bg-blue-600 dark:bg-blue-500 text-white rounded-xl hover:bg-blue-700 dark:hover:bg-blue-600 transition-all font-semibold text-base md:text-lg shadow-lg hover:shadow-xl flex items-center justify-center gap-2"
            >
              Process {files.length} Invoice{files.length > 1 ? 's' : ''}
              <ArrowRight className="w-4 h-4 md:w-5 md:h-5" />
            </button>
          </div>
        )}

        {/* Info Cards - Desktop Enhanced */}
        <div className="mt-8 md:mt-12 lg:mt-16 grid grid-cols-1 md:grid-cols-3 lg:grid-cols-3 gap-4 md:gap-6 lg:gap-8 px-4 md:px-0">
          <div className="text-center p-4 md:p-6 lg:p-8 bg-gray-50 dark:bg-gray-900 rounded-xl lg:rounded-2xl border border-gray-200 dark:border-gray-800 hover:shadow-lg lg:hover:shadow-xl transition-all duration-300">
            <div className="w-12 h-12 md:w-14 md:h-14 lg:w-16 lg:h-16 bg-blue-100 dark:bg-blue-900/50 rounded-lg lg:rounded-xl flex items-center justify-center mx-auto mb-3 md:mb-4 lg:mb-6">
              <span className="text-xl md:text-2xl lg:text-3xl">📄</span>
            </div>
            <h3 className="font-semibold text-gray-900 dark:text-white mb-2 text-sm md:text-base lg:text-lg">Supported Formats</h3>
            <p className="text-gray-600 dark:text-gray-400 text-xs md:text-sm lg:text-base">PDF, JPG, PNG up to 10MB</p>
            <div className="hidden lg:block mt-3 text-xs text-gray-500 dark:text-gray-500">
              Drag & drop multiple files at once
            </div>
          </div>
          
          <div className="text-center p-4 md:p-6 lg:p-8 bg-gray-50 dark:bg-gray-900 rounded-xl lg:rounded-2xl border border-gray-200 dark:border-gray-800 hover:shadow-lg lg:hover:shadow-xl transition-all duration-300">
            <div className="w-12 h-12 md:w-14 md:h-14 lg:w-16 lg:h-16 bg-green-100 dark:bg-green-900/50 rounded-lg lg:rounded-xl flex items-center justify-center mx-auto mb-3 md:mb-4 lg:mb-6">
              <span className="text-xl md:text-2xl lg:text-3xl">🤖</span>
            </div>
            <h3 className="font-semibold text-gray-900 dark:text-white mb-2 text-sm md:text-base lg:text-lg">AI Extraction</h3>
            <p className="text-gray-600 dark:text-gray-400 text-xs md:text-sm lg:text-base">Vendor, amounts, dates & GST</p>
            <div className="hidden lg:block mt-3 text-xs text-gray-500 dark:text-gray-500">
              60+ fields extracted automatically
            </div>
          </div>
          
          <div className="text-center p-4 md:p-6 lg:p-8 bg-gray-50 dark:bg-gray-900 rounded-xl lg:rounded-2xl border border-gray-200 dark:border-gray-800 hover:shadow-lg lg:hover:shadow-xl transition-all duration-300">
            <div className="w-12 h-12 md:w-14 md:h-14 lg:w-16 lg:h-16 bg-purple-100 dark:bg-purple-900/50 rounded-lg lg:rounded-xl flex items-center justify-center mx-auto mb-3 md:mb-4 lg:mb-6">
              <span className="text-xl md:text-2xl lg:text-3xl">⚡</span>
            </div>
            <h3 className="font-semibold text-gray-900 dark:text-white mb-2 text-sm md:text-base lg:text-lg">Fast Processing</h3>
            <p className="text-gray-600 dark:text-gray-400 text-xs md:text-sm lg:text-base">Results in under 10 seconds</p>
            <div className="hidden lg:block mt-3 text-xs text-gray-500 dark:text-gray-500">
              Export to PDF, Excel & CSV
            </div>
          </div>
        </div>
        
        {/* Anonymous Preview Modal */}
        {showAnonymousModal && anonymousResult && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div className="bg-white dark:bg-gray-800 rounded-xl max-w-2xl w-full max-h-[80vh] overflow-y-auto">
              <div className="p-6">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
                    🎉 AI Analysis Complete!
                  </h2>
                  <button
                    onClick={() => setShowAnonymousModal(false)}
                    className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                  >
                    <X className="w-6 h-6" />
                  </button>
                </div>
                
                <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 p-4 rounded-lg mb-6">
                  <p className="text-blue-800 dark:text-blue-200 text-sm">
                    <strong>File:</strong> {anonymousResult.fileName}
                  </p>
                  <p className="text-blue-700 dark:text-blue-300 text-sm mt-1">
                    🤖 Our AI has successfully extracted all invoice data! Sign up to save and manage your invoices.
                  </p>
                </div>
                
                {/* Preview of extracted data */}
                <div className="space-y-4 mb-6">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {anonymousResult.vendor_name && (
                      <div>
                        <label className="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">
                          Vendor Name
                        </label>
                        <p className="text-gray-900 dark:text-white font-medium">
                          {anonymousResult.vendor_name}
                        </p>
                      </div>
                    )}
                    
                    {anonymousResult.invoice_number && (
                      <div>
                        <label className="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">
                          Invoice Number
                        </label>
                        <p className="text-gray-900 dark:text-white">
                          {anonymousResult.invoice_number}
                        </p>
                      </div>
                    )}
                    
                    {anonymousResult.total_amount && (
                      <div>
                        <label className="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">
                          Total Amount
                        </label>
                        <p className="text-gray-900 dark:text-white font-bold text-lg">
                          ₹{anonymousResult.total_amount.toLocaleString()}
                        </p>
                      </div>
                    )}
                    
                    {anonymousResult.invoice_date && (
                      <div>
                        <label className="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">
                          Invoice Date
                        </label>
                        <p className="text-gray-900 dark:text-white">
                          {anonymousResult.invoice_date}
                        </p>
                      </div>
                    )}
                  </div>
                  
                  <div className="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 p-4 rounded-lg">
                    <p className="text-yellow-800 dark:text-yellow-200 text-sm font-medium">
                      ✨ This is just a preview! Sign up to:
                    </p>
                    <ul className="text-yellow-700 dark:text-yellow-300 text-sm mt-2 space-y-1">
                      <li>• Save and manage all your invoices</li>
                      <li>• Export to PDF, Excel, and CSV</li>
                      <li>• Access advanced features and analytics</li>
                      <li>• Process unlimited invoices</li>
                    </ul>
                  </div>
                </div>
                
                <div className="flex flex-col sm:flex-row gap-3">
                  <button
                    onClick={handleSignUpRedirect}
                    className="flex-1 bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-semibold transition-colors"
                  >
                    🚀 Sign Up & Save This Invoice
                  </button>
                  <button
                    onClick={() => setShowAnonymousModal(false)}
                    className="px-6 py-3 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
                  >
                    Try Another Invoice
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </DashboardLayout>
  )
}
