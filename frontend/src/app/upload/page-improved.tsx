'use client'

import { useState, useEffect } from 'react'
import DashboardLayout from '@/components/DashboardLayout'
import UploadZone from '@/components/UploadZone'
import { 
  AlertCircle, 
  CheckCircle2, 
  ArrowRight, 
  Loader2, 
  X,
  Sparkles,
  Zap,
  Shield
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
  
  const [selectedTemplate, setSelectedTemplate] = useState('simple')

  // Load user's preferred template on component mount
  useEffect(() => {
    const loadUserPreference = async () => {
      try {
        const { data: { user } } = await supabase.auth.getUser()
        if (user) {
          const savedTemplate = localStorage.getItem(`export_template_${user.id}`)
          if (savedTemplate && ['simple', 'accountant', 'analyst', 'compliance'].includes(savedTemplate)) {
            setSelectedTemplate(savedTemplate)
          }
        }
      } catch (error) {
        console.error('Error loading template preference:', error)
      }
    }
    loadUserPreference()
  }, [])

  // Save template preference when changed
  const handleTemplateChange = async (template: string) => {
    setSelectedTemplate(template)
    try {
      const { data: { user } } = await supabase.auth.getUser()
      if (user) {
        localStorage.setItem(`export_template_${user.id}`, template)
      }
    } catch (error) {
      console.error('Error saving template preference:', error)
    }
  }

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
            setUploadProgress(25)
            setProcessingStatus(`🧠 AI analyzing ${file.name}...`)
            
            const formData = new FormData()
            formData.append('file', file)
            
            const apiUrls = [
              'http://localhost:8000',
              process.env.NEXT_PUBLIC_API_URL || 'https://trulyinvoice-backend.onrender.com',
              'https://trulyinvoice-backend.onrender.com'
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
                })
                
                setUploadProgress(75)
                
                if (!response.ok) {
                  const errorText = await response.text()
                  throw new Error(`API Error ${response.status}: ${errorText}`)
                }
                
                const result = await response.json()
                console.log('✅ Anonymous processing completed:', result)
                setUploadProgress(100)
                
                showAnonymousPreview(result, file.name)
                processed = true
                
              } catch (apiError: any) {
                console.warn(`⚠️ API endpoint ${apiUrl} failed:`, apiError.message)
                lastError = apiError
                
                if (apiUrl !== apiUrls[apiUrls.length - 1]) {
                  continue
                }
              }
            }
            
            if (!processed) {
              throw new Error(`Unable to process invoice. Please try again later. (${lastError?.message || 'Service unavailable'})`)
            }
            
          } else {
            const fileName = `${user.id}/${Date.now()}_${file.name.replace(/[^a-zA-Z0-9.-]/g, '_')}`
            console.log(`🗂️ Storage path: ${fileName}`)
            
            const { data: uploadData, error: uploadError } = await supabase.storage
              .from('invoice-documents')
              .upload(fileName, file, {
                cacheControl: '3600',
                upsert: true
              })

            if (uploadError) {
              console.error('❌ Storage upload error:', uploadError)
              
              if (uploadError.message.includes('not found') || uploadError.message.includes('bucket')) {
                console.log('🪣 Trying to create bucket...')
                
                const { error: bucketError } = await supabase.storage.createBucket('invoice-documents', {
                  public: true
                })
                
                if (bucketError && !bucketError.message.includes('already exists')) {
                  console.error('❌ Bucket creation failed:', bucketError)
                  throw new Error(`Storage setup failed: ${bucketError.message}`)
                }
                
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

            const { data: { publicUrl } } = supabase.storage
              .from('invoice-documents')
              .getPublicUrl(fileName)

            console.log('🔗 Public URL generated:', publicUrl)
            setUploadProgress(50)

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
                    
                    await supabase
                      .from('documents')
                      .update({ status: 'upload_complete' })
                      .eq('id', docData.id)
                    
                    processed = true
                    setUploadProgress(100)
                  } else {
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
          }

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
        
        console.log('🔄 Redirecting to invoices page in 3 seconds...')
        setTimeout(() => {
          router.push('/invoices')
        }, 3000)
      } else {
        setIsUploading(false)
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
      <div className="relative min-h-screen">
        {/* Animated Background Gradient */}
        <div className="absolute inset-0 -z-10 overflow-hidden pointer-events-none">
          <div className="absolute top-0 left-0 w-96 h-96 bg-blue-300/20 rounded-full filter blur-3xl animate-blob"></div>
          <div className="absolute top-0 right-0 w-96 h-96 bg-purple-300/20 rounded-full filter blur-3xl animate-blob animation-delay-2000"></div>
          <div className="absolute bottom-0 left-1/2 w-96 h-96 bg-pink-300/20 rounded-full filter blur-3xl animate-blob animation-delay-4000"></div>
        </div>

        <div className="max-w-5xl mx-auto px-4 md:px-0 py-8">
          {/* Header - Enhanced with Animation */}
          <div className="text-center mb-8 md:mb-12 relative z-10 animate-in fade-in slide-in-from-top-4 duration-700">
            <div className="inline-block mb-4">
              <div className="px-4 py-2 bg-gradient-to-r from-blue-500/20 via-purple-500/20 to-pink-500/20 rounded-full border border-blue-200/50 dark:border-blue-800/50 backdrop-blur-sm hover:border-blue-300 dark:hover:border-blue-700 transition-colors">
                <span className="text-sm font-semibold bg-gradient-to-r from-blue-600 to-purple-600 dark:from-blue-400 dark:to-purple-400 bg-clip-text text-transparent flex items-center gap-2">
                  <Sparkles className="w-4 h-4" />
                  AI-Powered Invoice Processing
                </span>
              </div>
            </div>
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-gray-900 dark:text-white mb-3 tracking-tight leading-tight">
              Upload Your Invoices
            </h1>
            <p className="text-lg md:text-xl text-gray-600 dark:text-gray-400 max-w-2xl mx-auto font-light mb-8">
              Our advanced AI extracts all data automatically in seconds. No manual entry needed.
            </p>
            <div className="flex flex-wrap items-center justify-center gap-3 md:gap-4">
              <div className="inline-flex items-center gap-2 px-4 py-3 rounded-xl bg-white/40 dark:bg-gray-800/40 backdrop-blur-xl border border-white/20 dark:border-gray-700/20 hover:bg-white/60 dark:hover:bg-gray-800/60 transition-all duration-300 shadow-sm hover:shadow-md">
                <Zap className="w-4 h-4 text-green-500" />
                <span className="text-sm font-medium text-gray-700 dark:text-gray-300">PDF Support</span>
              </div>
              <div className="inline-flex items-center gap-2 px-4 py-3 rounded-xl bg-white/40 dark:bg-gray-800/40 backdrop-blur-xl border border-white/20 dark:border-gray-700/20 hover:bg-white/60 dark:hover:bg-gray-800/60 transition-all duration-300 shadow-sm hover:shadow-md">
                <Shield className="w-4 h-4 text-blue-500" />
                <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Image Recognition</span>
              </div>
              <div className="inline-flex items-center gap-2 px-4 py-3 rounded-xl bg-white/40 dark:bg-gray-800/40 backdrop-blur-xl border border-white/20 dark:border-gray-700/20 hover:bg-white/60 dark:hover:bg-gray-800/60 transition-all duration-300 shadow-sm hover:shadow-md">
                <Sparkles className="w-4 h-4 text-purple-500" />
                <span className="text-sm font-medium text-gray-700 dark:text-gray-300">60+ Fields</span>
              </div>
            </div>
          </div>

          {/* Export Template Selection - Enhanced */}
          <div className="relative mb-8 px-4 md:px-0 animate-in fade-in slide-in-from-top-4 duration-700 group" style={{ animationDelay: '100ms' }}>
            <div className="absolute inset-0 bg-gradient-to-r from-blue-500/10 via-purple-500/10 to-pink-500/10 rounded-3xl blur opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
            <div className="relative bg-white/80 dark:bg-gray-900/80 backdrop-blur-xl border border-gray-200/50 dark:border-gray-700/50 rounded-3xl p-6 md:p-8 shadow-xl hover:shadow-2xl transition-all duration-300">
              <div className="flex items-start gap-4 mb-6">
                <div className="flex-shrink-0">
                  <div className="w-12 h-12 bg-gradient-to-br from-blue-500 via-blue-600 to-purple-600 rounded-2xl flex items-center justify-center shadow-lg">
                    <span className="text-xl">📊</span>
                  </div>
                </div>
                <div className="flex-1">
                  <h3 className="font-bold text-gray-900 dark:text-white mb-1 text-lg md:text-xl">
                    Choose Export Format
                  </h3>
                  <p className="text-gray-600 dark:text-gray-400 text-sm">
                    Select how you want your invoice data exported later.
                  </p>
                </div>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                <label className={`relative cursor-pointer rounded-2xl border-2 p-4 transition-all duration-300 hover:shadow-md ${
                  selectedTemplate === 'simple' 
                    ? 'border-blue-500 bg-gradient-to-br from-blue-50 to-blue-100 dark:from-blue-900/30 dark:to-blue-800/30 shadow-md' 
                    : 'border-gray-200 dark:border-gray-700 hover:border-blue-300 dark:hover:border-blue-600 hover:bg-gray-50 dark:hover:bg-gray-800/30'
                }`}>
                  <input
                    type="radio"
                    name="template"
                    value="simple"
                    checked={selectedTemplate === 'simple'}
                    onChange={(e) => handleTemplateChange(e.target.value)}
                    className="sr-only"
                  />
                  <div className="flex items-start gap-3">
                    <div className={`w-5 h-5 rounded-full border-2 mt-0.5 flex items-center justify-center transition-all ${
                      selectedTemplate === 'simple' 
                        ? 'border-blue-500 bg-blue-500' 
                        : 'border-gray-300 dark:border-gray-600'
                    }`}>
                      {selectedTemplate === 'simple' && (
                        <div className="w-2 h-2 bg-white rounded-full"></div>
                      )}
                    </div>
                    <div>
                      <h4 className="font-semibold text-gray-900 dark:text-white">
                        Simple (2 sheets)
                      </h4>
                      <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                        Invoice Summary + Complete Data
                      </p>
                    </div>
                  </div>
                </label>

                <label className={`relative cursor-pointer rounded-2xl border-2 p-4 transition-all duration-300 hover:shadow-md ${
                  selectedTemplate === 'accountant' 
                    ? 'border-purple-500 bg-gradient-to-br from-purple-50 to-purple-100 dark:from-purple-900/30 dark:to-purple-800/30 shadow-md' 
                    : 'border-gray-200 dark:border-gray-700 hover:border-purple-300 dark:hover:border-purple-600 hover:bg-gray-50 dark:hover:bg-gray-800/30'
                }`}>
                  <input
                    type="radio"
                    name="template"
                    value="accountant"
                    checked={selectedTemplate === 'accountant'}
                    onChange={(e) => handleTemplateChange(e.target.value)}
                    className="sr-only"
                  />
                  <div className="flex items-start gap-3">
                    <div className={`w-5 h-5 rounded-full border-2 mt-0.5 flex items-center justify-center transition-all ${
                      selectedTemplate === 'accountant' 
                        ? 'border-purple-500 bg-purple-500' 
                        : 'border-gray-300 dark:border-gray-600'
                    }`}>
                      {selectedTemplate === 'accountant' && (
                        <div className="w-2 h-2 bg-white rounded-full"></div>
                      )}
                    </div>
                    <div>
                      <h4 className="font-semibold text-gray-900 dark:text-white">
                        Accountant (5 sheets)
                      </h4>
                      <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                        Summary, Line Items, GST, Vendor Analysis + Data
                      </p>
                    </div>
                  </div>
                </label>
              </div>
              
              <div className="p-3 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-xl">
                <p className="text-blue-800 dark:text-blue-200 text-sm">
                  <span className="font-semibold">💡 Tip:</span> Change anytime from the invoices page
                </p>
              </div>
            </div>
          </div>

          {/* Error Message - Enhanced */}
          {error && (
            <div className="mb-6 animate-in fade-in slide-in-from-top-2 duration-300 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-300 px-4 py-3 rounded-2xl flex items-center gap-3 shadow-md">
              <AlertCircle className="w-5 h-5 flex-shrink-0" />
              <div className="flex-1">
                <p className="font-semibold text-sm">Upload Failed</p>
                <p className="text-sm break-words">{error}</p>
              </div>
            </div>
          )}

          {/* Upload Zone - Compact */}
          <div className="bg-gradient-to-br from-purple-50/40 via-blue-50/40 to-pink-50/40 dark:from-purple-900/10 dark:via-blue-900/10 dark:to-pink-900/10 p-1 rounded-3xl mb-8 animate-in fade-in duration-700" style={{ animationDelay: '200ms' }}>
            <UploadZone onFileSelect={handleFileSelect} />
          </div>

          {/* Upload Progress - Enhanced */}
          {isUploading && (
            <div className="mb-8 animate-in fade-in slide-in-from-bottom-4 duration-500 bg-white dark:bg-gray-900 p-6 rounded-3xl border border-gray-200 dark:border-gray-800 shadow-xl">
              <div className="flex items-center gap-3 mb-4">
                <div className="relative">
                  <Loader2 className="w-5 h-5 text-blue-600 dark:text-blue-400 animate-spin" />
                </div>
                <span className="font-semibold text-gray-900 dark:text-white">
                  Processing your invoices...
                </span>
              </div>
              
              {/* Progress Bar */}
              <div className="relative w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3 overflow-hidden mb-3 shadow-inner">
                <div
                  className="bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 h-full rounded-full transition-all duration-500 ease-out shadow-lg"
                  style={{ width: `${uploadProgress}%` }}
                >
                  <div className="absolute inset-0 bg-white/20 animate-pulse"></div>
                </div>
              </div>
              
              <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-2">
                <p className="text-sm text-gray-600 dark:text-gray-400 font-semibold">
                  {uploadProgress}% complete
                </p>
                {processingStatus && (
                  <p className="text-sm text-blue-600 dark:text-blue-400 font-medium">
                    {processingStatus}
                  </p>
                )}
              </div>
            </div>
          )}

          {/* Upload Complete - Enhanced */}
          {uploadComplete && (
            <div className="mb-8 animate-in fade-in zoom-in-50 duration-500 bg-gradient-to-br from-green-50 to-emerald-50 dark:from-green-900/20 dark:to-emerald-900/20 border border-green-200 dark:border-green-800 p-6 rounded-3xl shadow-xl">
              <div className="flex items-start gap-4">
                <div className="flex-shrink-0">
                  <div className="flex items-center justify-center h-12 w-12 rounded-full bg-green-100 dark:bg-green-900/30">
                    <CheckCircle2 className="w-6 h-6 text-green-600 dark:text-green-400" />
                  </div>
                </div>
                <div className="flex-1">
                  <h3 className="font-bold text-green-900 dark:text-green-100 mb-1">
                    Upload Successful! 🎉
                  </h3>
                  <p className="text-green-700 dark:text-green-300 mb-4">
                    {files.length} invoice{files.length > 1 ? 's' : ''} processed successfully! Redirecting to your invoices...
                  </p>
                  <Link
                    href="/invoices"
                    className="inline-flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-green-600 to-emerald-600 dark:from-green-500 dark:to-emerald-500 text-white rounded-xl hover:shadow-lg transition-all font-semibold text-sm"
                  >
                    View Invoices <ArrowRight className="w-4 h-4" />
                  </Link>
                </div>
              </div>
            </div>
          )}

          {/* Upload Button - Enhanced */}
          {files.length > 0 && !isUploading && !uploadComplete && (
            <div className="mb-8 flex justify-center animate-in fade-in slide-in-from-bottom-4 duration-500">
              <button
                onClick={handleUpload}
                className="px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 dark:from-blue-500 dark:to-purple-500 text-white rounded-xl hover:shadow-2xl hover:scale-105 active:scale-95 transition-all font-bold text-lg flex items-center gap-2 shadow-xl"
              >
                <Sparkles className="w-5 h-5" />
                Process {files.length} Invoice{files.length > 1 ? 's' : ''}
                <ArrowRight className="w-5 h-5" />
              </button>
            </div>
          )}

          {/* Info Cards - Enhanced */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            {[
              { icon: '📄', title: 'Supported Formats', desc: 'PDF, JPG, PNG up to 10MB' },
              { icon: '🤖', title: 'AI Extraction', desc: 'Vendor, amounts, dates & GST' },
              { icon: '⚡', title: 'Fast Processing', desc: 'Results in under 10 seconds' }
            ].map((card, idx) => (
              <div 
                key={idx}
                className="group relative animate-in fade-in slide-in-from-bottom-4 duration-700 cursor-pointer"
                style={{ animationDelay: `${300 + idx * 100}ms` }}
              >
                <div className="absolute inset-0 bg-gradient-to-r from-blue-500/10 via-purple-500/10 to-pink-500/10 rounded-2xl blur opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
                <div className="relative p-6 bg-white/80 dark:bg-gray-900/80 backdrop-blur-xl rounded-2xl border border-gray-200/50 dark:border-gray-700/50 hover:shadow-lg transition-all duration-300 text-center">
                  <div className="text-4xl mb-3">{card.icon}</div>
                  <h3 className="font-bold text-gray-900 dark:text-white mb-2">{card.title}</h3>
                  <p className="text-gray-600 dark:text-gray-400 text-sm">{card.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
        
        {/* Anonymous Preview Modal - Enhanced */}
        {showAnonymousModal && anonymousResult && (
          <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4 animate-in fade-in duration-300">
            <div className="bg-white dark:bg-gray-800 rounded-3xl max-w-2xl w-full max-h-[80vh] overflow-y-auto shadow-2xl animate-in slide-in-from-bottom-8 duration-500">
              <div className="p-8">
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-2xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
                    <Sparkles className="w-6 h-6 text-purple-600" />
                    AI Analysis Complete!
                  </h2>
                  <button
                    onClick={() => setShowAnonymousModal(false)}
                    className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-xl transition-colors"
                  >
                    <X className="w-6 h-6" />
                  </button>
                </div>
                
                <div className="bg-gradient-to-r from-blue-50 to-blue-100 dark:from-blue-900/20 dark:to-blue-800/20 border border-blue-200 dark:border-blue-800 p-4 rounded-2xl mb-6">
                  <p className="text-blue-900 dark:text-blue-100 text-sm">
                    <span className="font-bold">File:</span> {anonymousResult.fileName}
                  </p>
                  <p className="text-blue-800 dark:text-blue-200 text-sm mt-2">
                    🤖 Our AI has successfully extracted all invoice data! Sign up to save and manage your invoices.
                  </p>
                </div>
                
                {/* Preview of extracted data */}
                <div className="space-y-4 mb-8">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {anonymousResult.vendor_name && (
                      <div className="p-4 bg-gray-50 dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-700">
                        <label className="block text-sm font-semibold text-gray-600 dark:text-gray-400 mb-2">
                          Vendor Name
                        </label>
                        <p className="text-gray-900 dark:text-white font-bold text-lg">
                          {anonymousResult.vendor_name}
                        </p>
                      </div>
                    )}
                    
                    {anonymousResult.invoice_number && (
                      <div className="p-4 bg-gray-50 dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-700">
                        <label className="block text-sm font-semibold text-gray-600 dark:text-gray-400 mb-2">
                          Invoice Number
                        </label>
                        <p className="text-gray-900 dark:text-white font-mono">
                          {anonymousResult.invoice_number}
                        </p>
                      </div>
                    )}
                    
                    {anonymousResult.total_amount && (
                      <div className="p-4 bg-gradient-to-br from-green-50 to-emerald-50 dark:from-green-900/20 dark:to-emerald-900/20 rounded-xl border border-green-200 dark:border-green-800">
                        <label className="block text-sm font-semibold text-green-700 dark:text-green-400 mb-2">
                          Total Amount
                        </label>
                        <p className="text-green-900 dark:text-green-100 font-bold text-2xl">
                          ₹{anonymousResult.total_amount.toLocaleString()}
                        </p>
                      </div>
                    )}
                    
                    {anonymousResult.invoice_date && (
                      <div className="p-4 bg-gray-50 dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-700">
                        <label className="block text-sm font-semibold text-gray-600 dark:text-gray-400 mb-2">
                          Invoice Date
                        </label>
                        <p className="text-gray-900 dark:text-white">
                          {anonymousResult.invoice_date}
                        </p>
                      </div>
                    )}
                  </div>
                  
                  <div className="bg-gradient-to-r from-amber-50 to-orange-50 dark:from-amber-900/20 dark:to-orange-900/20 border border-amber-200 dark:border-amber-800 p-5 rounded-2xl">
                    <p className="text-amber-900 dark:text-amber-100 font-bold text-sm mb-3">
                      ✨ This is just a preview! Sign up to:
                    </p>
                    <ul className="text-amber-900 dark:text-amber-200 text-sm space-y-2">
                      <li className="flex items-center gap-2">
                        <span className="w-1 h-1 bg-amber-600 dark:bg-amber-400 rounded-full"></span>
                        Save and manage all your invoices
                      </li>
                      <li className="flex items-center gap-2">
                        <span className="w-1 h-1 bg-amber-600 dark:bg-amber-400 rounded-full"></span>
                        Export to PDF, Excel, and CSV
                      </li>
                      <li className="flex items-center gap-2">
                        <span className="w-1 h-1 bg-amber-600 dark:bg-amber-400 rounded-full"></span>
                        Access advanced features and analytics
                      </li>
                      <li className="flex items-center gap-2">
                        <span className="w-1 h-1 bg-amber-600 dark:bg-amber-400 rounded-full"></span>
                        Process unlimited invoices
                      </li>
                    </ul>
                  </div>
                </div>
                
                <div className="flex flex-col sm:flex-row gap-3">
                  <button
                    onClick={handleSignUpRedirect}
                    className="flex-1 bg-gradient-to-r from-blue-600 to-purple-600 dark:from-blue-500 dark:to-purple-500 hover:shadow-xl text-white px-6 py-4 rounded-xl font-bold transition-all text-center"
                  >
                    🚀 Sign Up & Save This Invoice
                  </button>
                  <button
                    onClick={() => setShowAnonymousModal(false)}
                    className="px-6 py-4 border-2 border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 rounded-xl hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors font-semibold"
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
