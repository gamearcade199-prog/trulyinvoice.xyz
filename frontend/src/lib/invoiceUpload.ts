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
    
    // Step 1: Upload to storage (different paths for auth vs anonymous)
    let fileName: string
    if (isAuthenticated) {
      // Authenticated: use user_id/filename
      fileName = `${user.id}/${Date.now()}_${file.name.replace(/[^a-zA-Z0-9.-]/g, '_')}`
      console.log('📤 Uploading authenticated file:', fileName)
    } else {
      // Anonymous: use anonymous/anon_timestamp_filename
      const anonymousId = `anon_${Date.now()}`
      fileName = `anonymous/${anonymousId}_${file.name.replace(/[^a-zA-Z0-9.-]/g, '_')}`
      console.log('📤 Uploading anonymous file:', fileName)
    }
    
    const { data: uploadData, error: uploadError } = await supabase.storage
      .from('invoice-documents')
      .upload(fileName, file, {
        cacheControl: '3600',
        upsert: true
      })

    if (uploadError) {
      throw uploadError
    }

    // Step 2: Get public URL
    const { data: { publicUrl } } = supabase.storage
      .from('invoice-documents')
      .getPublicUrl(fileName)

    // Step 3: Create document record (with user_id if authenticated)
    const documentData: any = {
      file_name: file.name,
      file_size: file.size,
      file_type: file.type,
      storage_path: fileName,
      file_url: publicUrl,
      status: 'uploaded',
      uploaded_at: new Date().toISOString()
    }
    
    // Add user_id only if authenticated
    if (isAuthenticated) {
      documentData.user_id = user.id
    }

    const { data: docData, error: docError } = await supabase
      .from('documents')
      .insert(documentData)
      .select()
      .single()

    if (docError) {
      console.error('❌ Document creation error:', docError)
      throw docError
    }

    console.log(isAuthenticated ? '✅ Authenticated document created:' : '✅ Anonymous document created:', docData.id)

    // Step 4: Process the document
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    
    // Get the session token to authorize the request
    const { data: { session } } = await supabase.auth.getSession();
    const token = session?.access_token;

    const headers: HeadersInit = {
      'Content-Type': 'application/json',
    };
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(`${apiUrl}/api/documents/${docData.id}/process`, {
      method: 'POST',
      headers,
    });

    if (!response.ok) {
      // Check for quota exceeded error (HTTP 429)
      if (response.status === 429) {
        const errorData = await response.json()
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
      throw new Error(`Processing failed: ${response.statusText}`)
    }

    const processedData = await response.json()
    console.log('✅ Invoice processed:', processedData)

    // Step 5: Store in localStorage for later linking
    const tempData: TempInvoiceData = {
      fileName: file.name,
      fileSize: file.size,
      fileType: file.type,
      uploadedAt: new Date().toISOString(),
      extractedData: processedData.data || processedData,
      documentId: docData.id,
      storagePath: fileName
    }

    storeTempInvoice(tempData)

    return {
      success: true,
      data: processedData.data || processedData,
      documentId: docData.id
    }
  } catch (error: any) {
    console.error('❌ Upload failed:', error)
    return {
      success: false,
      error: error.message || 'Upload failed'
    }
  }
}
