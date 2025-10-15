'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { createBrowserClient } from '@supabase/ssr';
import DashboardLayout from '@/components/DashboardLayout';

interface Invoice {
  id: string;
  document_id: string;
  invoice_number: string;
  vendor_name: string;
  total_amount: number;
  payment_status: string;
  invoice_date: string;
  created_at: string;
  user_id?: string;
  raw_extracted_data?: any;
  documents?: {
    file_name: string;
    storage_path: string;
  };
}

export default function InvoiceDetailPage() {
  const params = useParams();
  const [invoice, setInvoice] = useState<Invoice | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  const supabase = createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  );

  useEffect(() => {
    async function fetchInvoice() {
      try {
        console.log('DEBUG: Trying to fetch invoice with ID:', params.id);
        console.log('DEBUG: ID type:', typeof params.id, 'ID length:', params.id?.length);
        
        const { data, error } = await supabase
          .from('invoices')
          .select(`
            *,
            documents:document_id (
              file_name,
              storage_path
            )
          `)
          .eq('id', params.id)
          .single();

        console.log('DEBUG: Supabase query result:', { data, error });

        if (error) {
          console.error('Error fetching invoice:', error);
          setError('Invoice not found');
          return;
        }

        setInvoice(data);
      } catch (err) {
        console.error('Error:', err);
        setError('Failed to load invoice');
      } finally {
        setLoading(false);
      }
    }

    if (params.id) {
      fetchInvoice();
    }
  }, [params.id, supabase]);

  if (loading) {
    return (
      <DashboardLayout>
        <div className="flex items-center justify-center min-h-[400px]">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        </div>
      </DashboardLayout>
    );
  }

  if (error || !invoice) {
    return (
      <DashboardLayout>
        <div className="max-w-4xl mx-auto p-6">
          <div className="bg-red-50 border border-red-200 rounded-lg p-4">
            <h1 className="text-xl font-bold text-red-800 mb-2">Invoice Not Found</h1>
            <p className="text-red-600">{error || 'The requested invoice could not be found.'}</p>
          </div>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div className="max-w-4xl mx-auto p-6">
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
          <div className="mb-6">
            <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
              Invoice Details
            </h1>
            <p className="text-gray-600 dark:text-gray-300">
              Invoice ID: {invoice.id}
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                Invoice Information
              </h2>
              <div className="space-y-3">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                    Invoice Number
                  </label>
                  <p className="text-gray-900 dark:text-white">{invoice.invoice_number || 'N/A'}</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                    Vendor Name
                  </label>
                  <p className="text-gray-900 dark:text-white">{invoice.vendor_name || 'N/A'}</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                    Total Amount
                  </label>
                  <p className="text-gray-900 dark:text-white font-bold">
                    ₹{invoice.total_amount?.toLocaleString() || '0'}
                  </p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                    Payment Status
                  </label>
                  <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                    invoice.payment_status === 'paid' 
                      ? 'bg-green-100 text-green-800' 
                      : 'bg-yellow-100 text-yellow-800'
                  }`}>
                    {invoice.payment_status || 'unpaid'}
                  </span>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                    Invoice Date
                  </label>
                  <p className="text-gray-900 dark:text-white">
                    {invoice.invoice_date ? new Date(invoice.invoice_date).toLocaleDateString() : 'N/A'}
                  </p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                    Document File
                  </label>
                  <p className="text-gray-900 dark:text-white">
                    {invoice.documents?.file_name || 'No document attached'}
                  </p>
                </div>
              </div>
            </div>

            <div>
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                Raw Extracted Data
              </h2>
              <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4 max-h-96 overflow-auto">
                <pre className="text-sm text-gray-800 dark:text-gray-200 whitespace-pre-wrap">
                  {invoice.raw_extracted_data 
                    ? JSON.stringify(invoice.raw_extracted_data, null, 2)
                    : 'No extracted data available'}
                </pre>
              </div>
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
