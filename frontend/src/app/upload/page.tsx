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
  Shield,
  FileText,
  Cpu,
  Upload
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
    setProcessingStatus(`${fileName} analyzed! Sign up to save results.`)
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
        setProcessingStatus(`Successfully processed ${files.length} file(s)!`)
        
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

        <div className="max-w-6xl mx-auto px-4 md:px-6 py-6">
          {/* Professional Header with Gradient */}
          <div className="text-center mb-6 sm:mb-8 relative z-10">
            {/* Floating Badge */}
            <div className="inline-block mb-3 sm:mb-4">
              <div className="relative group">
                <div className="absolute inset-0 bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 rounded-full blur opacity-20 group-hover:opacity-30 transition-opacity"></div>
                <div className="relative px-3 py-1.5 sm:px-4 sm:py-2 bg-white/90 dark:bg-gray-900/90 backdrop-blur-xl rounded-full border border-gray-200/50 dark:border-gray-700/50 shadow-lg">
                  <span className="text-xs sm:text-sm font-semibold bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent flex items-center gap-1.5 sm:gap-2">
                    <Sparkles className="w-3 h-3 sm:w-4 sm:h-4 text-blue-600" />
                    AI-Powered Processing
                  </span>
                </div>
              </div>
            </div>
            
            {/* Modern Typography */}
            <h1 className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-bold text-gray-900 dark:text-white mb-2 sm:mb-3 tracking-tight px-4">
              Upload Your <span className="bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">Invoices</span>
            </h1>
            <p className="text-sm sm:text-base md:text-lg text-gray-600 dark:text-gray-300 max-w-2xl mx-auto leading-relaxed px-4">
              Advanced AI extracts all data automatically in seconds. 
              <span className="text-blue-600 dark:text-blue-400 font-medium"> No manual entry required.</span>
            </p>
          </div>

          {/* Error Message - Enhanced */}
          {error && (
            <div className="mb-6 relative">
              <div className="absolute inset-0 bg-red-500/10 rounded-2xl blur"></div>
              <div className="relative bg-red-50/80 dark:bg-red-900/20 backdrop-blur-xl border border-red-200/50 dark:border-red-800/50 text-red-700 dark:text-red-300 px-5 py-4 rounded-2xl flex items-start gap-4 shadow-lg">
                <div className="flex-shrink-0 mt-0.5">
                  <div className="w-8 h-8 bg-red-100 dark:bg-red-900/30 rounded-full flex items-center justify-center">
                    <AlertCircle className="w-4 h-4 text-red-600 dark:text-red-400" />
                  </div>
                </div>
                <div className="flex-1">
                  <p className="font-semibold text-sm mb-1">Upload Failed</p>
                  <p className="text-sm break-words opacity-90">{error}</p>
                </div>
              </div>
            </div>
          )}

          {/* Premium Upload Zone Card */}
          <div className="mb-8 relative group">
            {/* Glow Effect */}
            <div className="absolute inset-0 bg-gradient-to-r from-blue-500/20 via-purple-500/20 to-pink-500/20 rounded-3xl blur-xl opacity-0 group-hover:opacity-100 transition-all duration-500"></div>
            
            {/* Main Card */}
            <div className="relative bg-white/80 dark:bg-gray-900/80 backdrop-blur-2xl border border-gray-200/50 dark:border-gray-700/50 rounded-3xl shadow-2xl hover:shadow-3xl transition-all duration-500">
              {/* Card Header */}
              <div className="px-6 pt-6 pb-4 border-b border-gray-100 dark:border-gray-800">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-gradient-to-br from-blue-500 via-purple-500 to-pink-500 rounded-xl flex items-center justify-center shadow-lg">
                    <Upload className="w-5 h-5 text-white" />
                  </div>
                  <div>
                    <h3 className="font-bold text-gray-900 dark:text-white text-lg">Upload Center</h3>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Drag & drop or click to select files</p>
                  </div>
                </div>
              </div>
              
              {/* Upload Zone */}
              <div className="p-6">
                <UploadZone onFileSelect={handleFileSelect} />
              </div>
            </div>
          </div>

          {/* Process Button - Premium Design */}
          {files.length > 0 && !isUploading && !uploadComplete && (
            <div className="mb-6 sm:mb-8 flex justify-center px-4">
              <div className="relative group w-full sm:w-auto">
                <div className="absolute inset-0 bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 rounded-xl sm:rounded-2xl blur opacity-20 group-hover:opacity-30 transition-opacity"></div>
                <button
                  onClick={handleUpload}
                  className="relative w-full sm:w-auto px-6 sm:px-8 py-3 sm:py-4 bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 hover:from-blue-700 hover:via-purple-700 hover:to-pink-700 text-white rounded-xl sm:rounded-2xl font-bold text-base sm:text-lg flex items-center justify-center gap-2 sm:gap-3 shadow-2xl hover:shadow-3xl hover:scale-105 active:scale-95 transition-all duration-300 min-h-[48px]"
                >
                  <div className="w-5 h-5 sm:w-6 sm:h-6 bg-white/20 rounded-full flex items-center justify-center">
                    <Sparkles className="w-3 h-3 sm:w-4 sm:h-4" />
                  </div>
                  Process {files.length} Invoice{files.length > 1 ? 's' : ''}
                  <ArrowRight className="w-4 h-4 sm:w-5 sm:h-5" />
                </button>
              </div>
            </div>
          )}

          {/* Enhanced Progress Card */}
          {isUploading && (
            <div className="mb-8 relative">
              <div className="absolute inset-0 bg-blue-500/10 rounded-3xl blur"></div>
              <div className="relative bg-white/90 dark:bg-gray-900/90 backdrop-blur-2xl border border-gray-200/50 dark:border-gray-700/50 rounded-3xl shadow-2xl p-6">
                <div className="flex items-center gap-4 mb-5">
                  <div className="relative">
                    <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center shadow-lg">
                      <Loader2 className="w-6 h-6 text-white animate-spin" />
                    </div>
                  </div>
                  <div className="flex-1">
                    <h3 className="font-bold text-gray-900 dark:text-white text-lg">Processing Your Invoices</h3>
                    <p className="text-gray-600 dark:text-gray-400">AI is extracting and analyzing data...</p>
                  </div>
                  <div className="text-right">
                    <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">{uploadProgress}%</div>
                    <div className="text-xs text-gray-500 dark:text-gray-400">Complete</div>
                  </div>
                </div>
                
                {/* Animated Progress Bar */}
                <div className="relative w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3 overflow-hidden shadow-inner">
                  <div
                    className="bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 h-full rounded-full transition-all duration-700 ease-out relative"
                    style={{ width: `${uploadProgress}%` }}
                  >
                    <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent animate-pulse"></div>
                  </div>
                </div>
                
                {processingStatus && (
                  <div className="mt-4 flex items-center gap-2">
                    <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse"></div>
                    <p className="text-sm text-blue-600 dark:text-blue-400 font-medium">
                      {processingStatus}
                    </p>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Success Card - Premium */}
          {uploadComplete && (
            <div className="mb-8 relative">
              <div className="absolute inset-0 bg-green-500/10 rounded-3xl blur"></div>
              <div className="relative bg-gradient-to-br from-green-50/80 to-emerald-50/80 dark:from-green-900/20 dark:to-emerald-900/20 backdrop-blur-2xl border border-green-200/50 dark:border-green-800/50 rounded-3xl shadow-2xl p-6">
                <div className="flex items-center gap-4">
                  <div className="w-12 h-12 bg-gradient-to-br from-green-500 to-emerald-600 rounded-xl flex items-center justify-center shadow-lg">
                    <CheckCircle2 className="w-6 h-6 text-white" />
                  </div>
                  <div className="flex-1">
                    <h3 className="font-bold text-green-900 dark:text-green-100 text-lg mb-1">
                      Upload Successful!
                    </h3>
                    <p className="text-green-700 dark:text-green-300">
                      {files.length} invoice{files.length > 1 ? 's' : ''} processed successfully
                    </p>
                  </div>
                  <Link
                    href="/invoices"
                    className="px-6 py-3 bg-gradient-to-r from-green-600 to-emerald-600 dark:from-green-500 dark:to-emerald-500 text-white rounded-xl hover:shadow-lg transition-all font-semibold text-sm flex items-center gap-2 group"
                  >
                    View Results 
                    <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                  </Link>
                </div>
              </div>
            </div>
          )}

          {/* Premium Feature Cards */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 sm:gap-4">
            {[
              { icon: FileText, title: 'Multiple Formats', desc: 'PDF, JPG, PNG', gradient: 'from-blue-500 to-cyan-500' },
              { icon: Cpu, title: 'AI Extraction', desc: '60+ Fields Auto-detected', gradient: 'from-purple-500 to-pink-500' },
              { icon: Zap, title: 'Lightning Fast', desc: 'Results in <10 seconds', gradient: 'from-amber-500 to-orange-500' }
            ].map((card, idx) => (
              <div key={idx} className="group relative">
                <div className="absolute inset-0 bg-gradient-to-r opacity-0 group-hover:opacity-20 rounded-xl sm:rounded-2xl blur transition-opacity duration-500" 
                     style={{ background: `linear-gradient(to right, ${card.gradient.split(' ')[1]}, ${card.gradient.split(' ')[3]})` }}></div>
                <div className="relative text-center p-3 sm:p-4 bg-white/70 dark:bg-gray-900/70 backdrop-blur-xl rounded-xl sm:rounded-2xl border border-gray-200/50 dark:border-gray-700/50 hover:shadow-xl transition-all duration-300 group-hover:scale-105">
                  <div className={`w-8 h-8 sm:w-10 sm:h-10 bg-gradient-to-br ${card.gradient} rounded-lg sm:rounded-xl flex items-center justify-center mx-auto mb-2 sm:mb-3 shadow-lg group-hover:shadow-xl transition-all`}>
                    <card.icon className="w-4 h-4 sm:w-5 sm:h-5 text-white" />
                  </div>
                  <h3 className="font-bold text-gray-900 dark:text-white text-xs sm:text-sm mb-0.5 sm:mb-1">{card.title}</h3>
                  <p className="text-gray-600 dark:text-gray-400 text-[10px] sm:text-xs leading-relaxed">{card.desc}</p>
                </div>
              </div>
            ))}
          </div>

          {/* Trust Indicators */}
          <div className="text-center px-4">
            <div className="inline-flex flex-wrap items-center justify-center gap-3 sm:gap-4 md:gap-6 px-4 sm:px-6 py-2.5 sm:py-3 bg-white/50 dark:bg-gray-900/50 backdrop-blur-xl rounded-full border border-gray-200/50 dark:border-gray-700/50 shadow-lg">
              <div className="flex items-center gap-1.5 sm:gap-2">
                <Sparkles className="w-3.5 h-3.5 sm:w-4 sm:h-4 text-blue-500" />
                <span className="text-xs sm:text-sm font-medium text-gray-700 dark:text-gray-300 whitespace-nowrap">AI-Powered</span>
              </div>
              <div className="hidden sm:block w-px h-4 bg-gray-300 dark:bg-gray-600"></div>
              <div className="flex items-center gap-1.5 sm:gap-2">
                <Zap className="w-3.5 h-3.5 sm:w-4 sm:h-4 text-purple-500" />
                <span className="text-xs sm:text-sm font-medium text-gray-700 dark:text-gray-300 whitespace-nowrap">99% Accurate</span>
              </div>
              <div className="hidden sm:block w-px h-4 bg-gray-300 dark:bg-gray-600"></div>
              <div className="flex items-center gap-1.5 sm:gap-2">
                <Shield className="w-3.5 h-3.5 sm:w-4 sm:h-4 text-green-500" />
                <span className="text-xs sm:text-sm font-medium text-gray-700 dark:text-gray-300 whitespace-nowrap">Secure & Private</span>
              </div>
            </div>
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
                    Analysis Complete
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
                    Our AI has successfully extracted all invoice data! Sign up to save and manage your invoices.
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
                      This is just a preview! Sign up to:
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
                    Sign Up & Save This Invoice
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
