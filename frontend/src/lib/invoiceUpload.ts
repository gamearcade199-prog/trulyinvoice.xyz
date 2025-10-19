// Invoice upload utility for non-authenticated users
import { supabase } from './supabase'

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

// Upload invoice without authentication (creates anonymous document)
export async function uploadInvoiceAnonymous(file: File) {
  try {
    // Step 1: Upload to storage with anonymous path
    const anonymousId = `anon_${Date.now()}`
    const fileName = `anonymous/${anonymousId}_${file.name.replace(/[^a-zA-Z0-9.-]/g, '_')}`
    
    console.log('📤 Uploading anonymous file:', fileName)
    
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

    // Step 3: Create document record (without user_id)
    const { data: docData, error: docError } = await supabase
      .from('documents')
      .insert({
        file_name: file.name,
        file_size: file.size,
        file_type: file.type,
        storage_path: fileName,
        file_url: publicUrl,
        status: 'uploaded',
        uploaded_at: new Date().toISOString()
      })
      .select()
      .single()

    if (docError) {
      console.error('❌ Document creation error:', docError)
      throw docError
    }

    console.log('✅ Anonymous document created:', docData.id)

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
