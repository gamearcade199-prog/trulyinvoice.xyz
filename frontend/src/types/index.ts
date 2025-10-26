/**
 * TypeScript interfaces for Invoice and related types
 * Replaces 'any' types throughout the application
 */

export interface LineItem {
  id?: string;
  description: string;
  hsn_sac?: string;
  hsn?: string;
  unit?: string;
  quantity: number;
  rate: number;
  discount?: number;
  amount: number;
  tax_rate?: number;
  cgst?: number;
  sgst?: number;
  igst?: number;
}

export interface Invoice {
  id: string;
  document_id?: string;
  user_id?: string;
  
  // Basic Information
  invoice_number: string;
  invoice_date: string;
  due_date?: string;
  
  // Vendor Information
  vendor_name: string;
  vendor_address?: string;
  vendor_city?: string;
  vendor_state?: string;
  vendor_pincode?: string;
  vendor_gstin?: string;
  vendor_phone?: string;
  vendor_email?: string;
  
  // Buyer Information
  buyer_name?: string;
  buyer_address?: string;
  buyer_city?: string;
  buyer_state?: string;
  buyer_pincode?: string;
  buyer_gstin?: string;
  
  // Amounts
  total_amount: number;
  subtotal?: number;
  tax_amount?: number;
  cgst_amount?: number;
  sgst_amount?: number;
  igst_amount?: number;
  discount_amount?: number;
  
  // Line Items
  line_items?: LineItem[] | string;
  
  // Additional Fields
  currency?: string;
  payment_status?: 'paid' | 'unpaid' | 'partial' | 'overdue';
  payment_method?: string;
  payment_terms?: string;
  notes?: string;
  
  // Metadata
  confidence_score?: number;
  created_at?: string;
  updated_at?: string;
  status?: 'pending' | 'processing' | 'completed' | 'failed';
}

export interface User {
  id: string;
  email: string;
  name?: string;
  plan?: 'free' | 'basic' | 'pro' | 'ultra' | 'max';
  subscription_status?: 'active' | 'inactive' | 'cancelled';
  scans_used?: number;
  scans_limit?: number;
  created_at?: string;
  export_template?: 'accountant' | 'professional' | 'simple';
}

export interface Document {
  id: string;
  user_id?: string;
  file_name: string;
  file_path: string;
  file_size: number;
  mime_type: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  confidence_score?: number;
  error_message?: string;
  created_at?: string;
  updated_at?: string;
  processed_at?: string;
}

export interface Subscription {
  id: string;
  user_id: string;
  tier: 'free' | 'basic' | 'pro' | 'ultra' | 'max';
  status: 'active' | 'inactive' | 'cancelled' | 'expired';
  billing_cycle: 'monthly' | 'yearly';
  current_period_start?: string;
  current_period_end?: string;
  scans_used_this_period: number;
  auto_renew: boolean;
  created_at?: string;
  updated_at?: string;
}

export interface PaymentOrder {
  order_id: string;
  amount_paise: number;
  currency: string;
  key_id: string;
}

export interface InvoiceStats {
  total: number;
  totalAmount: number;
  paidAmount: number;
  unpaidAmount: number;
  averageAmount: number;
  byVendor: Record<string, number>;
  byMonth: Record<string, number>;
  byStatus: Record<string, number>;
}

export interface BulkExportOptions {
  format: 'excel' | 'csv';
  invoiceIds?: string[];
  filters?: {
    startDate?: string;
    endDate?: string;
    vendorName?: string;
    minAmount?: number;
    maxAmount?: number;
    paymentStatus?: string;
  };
}

export interface UploadResult {
  success: boolean;
  documentId?: string;
  invoiceId?: string;
  data?: Invoice;
  error?: string;
}

export interface ApiError {
  error: string;
  details?: string;
  statusCode: number;
}
