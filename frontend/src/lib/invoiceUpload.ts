// Invoice upload utility for non-authenticated users
import { supabase } from './supabase'

export class QuotaExceededError extends Error {
  status: number
  scansUsed: number
  scansLimit: number

  constructor(message: string, scansUsed?: number, scansLimit?: number) {
    super(message)
    this.name = 'QuotaExceededError'
    this.status = 429
    this.scansUsed = scansUsed || 0
    this.scansLimit = scansLimit || 0
  }
}

export interface TempInvoiceData {
  fileName: string
  fileSize: number
  fileType: string
  uploadedAt: string
  extractedData: {
    vendor_name?: string
    invoice_number?: string
    invoice_date?: string
    total_amount?: number
    tax_amount?: number
    currency?: string
  }
  documentId?: string
  storagePath?: string
}

const TEMP_INVOICE_KEY = 'truly_temp_invoices'

// Store invoice data temporarily in localStorage
export function storeTempInvoice(data: TempInvoiceData) {
  try {
    const existing = getTempInvoices()
    existing.push(data)
    localStorage.setItem(TEMP_INVOICE_KEY, JSON.stringify(existing))
    console.log('✅ Temp invoice stored:', data)
  } catch (error) {
    console.error('❌ Failed to store temp invoice:', error)
  }
}

// Get all temporary invoices
export function getTempInvoices(): TempInvoiceData[] {
  try {
    const stored = localStorage.getItem(TEMP_INVOICE_KEY)
    return stored ? JSON.parse(stored) : []
  } catch (error) {
    console.error('❌ Failed to get temp invoices:', error)
    return []
  }
}

// Clear temporary invoices
export function clearTempInvoices() {
  try {
    localStorage.removeItem(TEMP_INVOICE_KEY)
    console.log('✅ Temp invoices cleared')
  } catch (error) {
    console.error('❌ Failed to clear temp invoices:', error)
  }
}

// Link temporary invoices to user account after login/register
export async function linkTempInvoicesToUser(userId: string) {
  const tempInvoices = getTempInvoices()
  if (tempInvoices.length === 0) return

  console.log(`🔗 Linking ${tempInvoices.length} temp invoices to user:`, userId)
  
  for (const tempInvoice of tempInvoices) {
    try {
      if (tempInvoice.documentId) {
        // Update existing document with user ID
        const { error } = await supabase
          .from('documents')
          .update({ user_id: userId })
          .eq('id', tempInvoice.documentId)

        if (error) {
          console.error('❌ Failed to link document:', error)
        } else {
          console.log('✅ Document linked:', tempInvoice.documentId)
        }
      }
    } catch (error) {
      console.error('❌ Error linking invoice:', error)
    }
  }

  // Clear temp invoices after linking
  clearTempInvoices()
}

// Upload invoice (works for both authenticated and anonymous users)
export async function uploadInvoiceAnonymous(file: File) {
  try {
    // Check if user is logged in
    const { data: { user } } = await supabase.auth.getUser()
    const isAuthenticated = !!user
    
    console.log(isAuthenticated ? '📤 Uploading as authenticated user' : '📤 Uploading anonymously')
    
    // Get API URL
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
    console.log('🔗 API URL:', apiUrl)
    
    // Get session token for authenticated requests
    const { data: { session } } = await supabase.auth.getSession()
    const token = session?.access_token

    if (isAuthenticated) {
      console.log('🔐 Authenticated upload flow')
      // For authenticated users: Upload file to backend (handles storage + document creation + processing)
      const formData = new FormData()
      formData.append('file', file)

      const headers: HeadersInit = {}
      if (token) {
        headers['Authorization'] = `Bearer ${token}`
      }

      console.log('📤 POSTing to /api/documents/upload...')
      // Upload to backend API (handles everything: storage, DB, processing)
      const uploadResponse = await fetch(`${apiUrl}/api/documents/upload?user_id=${user.id}`, {
        method: 'POST',
        headers,
        body: formData
      })

      console.log('📥 Upload response status:', uploadResponse.status)

      if (!uploadResponse.ok) {
        const errorData = await uploadResponse.json().catch(() => ({ detail: 'Upload failed' }))
        console.error('❌ Upload error:', errorData)
        
        // Check for quota exceeded error (HTTP 429)
        if (uploadResponse.status === 429) {
          const match = errorData.detail?.match(/Used: (\d+)\/(\d+)/)
          if (match) {
            throw new QuotaExceededError(
              errorData.detail,
              parseInt(match[1], 10),
              parseInt(match[2], 10)
            )
          }
          throw new QuotaExceededError(errorData.detail || 'Monthly scan limit exceeded')
        }
        
        throw new Error(errorData.detail || `Upload failed: ${uploadResponse.statusText}`)
      }

      const uploadResult = await uploadResponse.json()
      const documentId = uploadResult.id || uploadResult.document_id
      console.log('✅ File uploaded, document ID:', documentId)

      if (!documentId) {
        throw new Error('No document ID returned from upload')
      }

      console.log('⚙️ Starting processing for document:', documentId)
      // Step 2: Process the document
      const processResponse = await fetch(`${apiUrl}/api/documents/${documentId}/process`, {
        method: 'POST',
        headers: token ? { 'Authorization': `Bearer ${token}` } : {}
      })

      console.log('📥 Process response status:', processResponse.status)

      if (!processResponse.ok) {
        const errorData = await processResponse.json().catch(() => ({ detail: 'Processing failed' }))
        console.error('❌ Processing error:', errorData)
        
        // Check for quota exceeded error
        if (processResponse.status === 429) {
          const match = errorData.detail?.match(/Used: (\d+)\/(\d+)/)
          if (match) {
            throw new QuotaExceededError(
              errorData.detail,
              parseInt(match[1], 10),
              parseInt(match[2], 10)
            )
          }
          throw new QuotaExceededError(errorData.detail || 'Monthly scan limit exceeded')
        }
        throw new Error(`Processing failed: ${processResponse.statusText}`)
      }

      const processedData = await processResponse.json()
      console.log('✅ Invoice processed successfully')

      return {
        success: true,
        data: processedData.data || processedData,
        documentId: documentId
      }
    } else {
      console.log('👤 Anonymous upload flow')
      // For anonymous users: Use the process-anonymous endpoint (all-in-one)
      const formData = new FormData()
      formData.append('file', file)

      console.log('📤 POSTing to /api/documents/process-anonymous...')
      const response = await fetch(`${apiUrl}/api/documents/process-anonymous`, {
        method: 'POST',
        body: formData
      })

      console.log('📥 Anonymous response status:', response.status)

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Processing failed' }))
        console.error('❌ Anonymous processing error:', errorData)
        
        // Check for quota exceeded error (HTTP 429)
        if (response.status === 429) {
          const match = errorData.detail?.match(/Used: (\d+)\/(\d+)/)
          if (match) {
            throw new QuotaExceededError(
              errorData.detail,
              parseInt(match[1], 10),
              parseInt(match[2], 10)
            )
          }
          throw new QuotaExceededError(errorData.detail || 'Monthly scan limit exceeded')
        }
        
        throw new Error(errorData.detail || `Processing failed: ${response.statusText}`)
      }

      const result = await response.json()
      console.log('✅ Anonymous processing completed:', result)

      // Store in localStorage for later linking
      const tempData: TempInvoiceData = {
        fileName: file.name,
        fileSize: file.size,
        fileType: file.type,
        uploadedAt: new Date().toISOString(),
        extractedData: result,
        documentId: 'anonymous',
        storagePath: 'anonymous'
      }
      storeTempInvoice(tempData)

      return {
        success: true,
        data: result,
        documentId: 'anonymous'
      }
    }
  } catch (error: any) {
    console.error('❌ Upload failed:', error)
    
    // Enhanced error reporting
    if (error.name === 'TypeError' && error.message.includes('fetch')) {
      return {
        success: false,
        error: `Cannot connect to server at ${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}. Please ensure the backend is running.`
      }
    }
    
    return {
      success: false,
      error: error.message || 'Upload failed'
    }
  }
}
