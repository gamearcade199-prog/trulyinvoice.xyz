'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { createClientComponentClient } from '@supabase/auth-helpers-nextjs';
import DashboardLayout from '@/components/DashboardLayout';

interface Invoice {
  id: string;
  filename: string;
  extracted_data: any;
  status: string;
  created_at: string;
  user_id?: string;
}

export default function InvoiceDetailPage() {
  const params = useParams();
  const [invoice, setInvoice] = useState<Invoice | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const supabase = createClientComponentClient();

  useEffect(() => {
    async function fetchInvoice() {
      try {
        const { data, error } = await supabase
          .from('invoices')
          .select('*')
          .eq('id', params.id)
          .single();

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
                Basic Information
              </h2>
              <div className="space-y-3">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                    Filename
                  </label>
                  <p className="text-gray-900 dark:text-white">{invoice.filename}</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                    Status
                  </label>
                  <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                    invoice.status === 'completed' 
                      ? 'bg-green-100 text-green-800' 
                      : 'bg-yellow-100 text-yellow-800'
                  }`}>
                    {invoice.status}
                  </span>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                    Created At
                  </label>
                  <p className="text-gray-900 dark:text-white">
                    {new Date(invoice.created_at).toLocaleString()}
                  </p>
                </div>
              </div>
            </div>

            <div>
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                Extracted Data
              </h2>
              <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
                <pre className="text-sm text-gray-800 dark:text-gray-200 whitespace-pre-wrap overflow-auto">
                  {invoice.extracted_data 
                    ? JSON.stringify(invoice.extracted_data, null, 2)
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
