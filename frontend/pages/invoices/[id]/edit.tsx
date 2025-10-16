"""
Frontend React/TypeScript page for invoice editing
Located at: frontend/pages/invoices/[id]/edit.tsx

This file demonstrates the Next.js structure and component hierarchy.
It should be compiled by the Next.js framework with proper TypeScript support.
"""

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import { useSupabaseClient, useUser } from '@supabase/auth-helpers-react';
import Link from 'next/link';
import Head from 'next/head';


interface InvoiceField {
  label: string;
  value: string | number;
  confidence?: number;
  required?: boolean;
  editable?: boolean;
  type?: string;
}


interface Invoice {
  id: string;
  user_id: string;
  file_id: string;
  file_name: string;
  invoice_number?: string;
  invoice_date?: string;
  due_date?: string;
  vendor_name?: string;
  vendor_email?: string;
  vendor_phone?: string;
  vendor_address?: string;
  vendor_gstin?: string;
  amount_total?: number;
  tax_amount?: number;
  amount_net?: number;
  payment_status?: string;
  payment_status_confidence?: number;
  currency?: string;
  line_items?: any[];
  extracted_data?: Record<string, any>;
  created_at: string;
  updated_at: string;
}


export default function InvoiceEditPage() {
  const router = useRouter();
  const { id } = router.query;
  const user = useUser();
  const supabase = useSupabaseClient();

  const [invoice, setInvoice] = useState<Invoice | null>(null);
  const [editedFields, setEditedFields] = useState<Record<string, any>>({});
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);


  // Load invoice data on mount
  useEffect(() => {
    if (!id || !user) return;
    loadInvoice();
  }, [id, user]);


  const loadInvoice = async () => {
    try {
      setLoading(true);
      setError(null);

      const { data, error: fetchError } = await supabase
        .from('documents')
        .select('*')
        .eq('id', id)
        .eq('user_id', user?.id)
        .single();

      if (fetchError) throw fetchError;
      if (!data) {
        setError('Invoice not found');
        return;
      }

      setInvoice(data as Invoice);
      setEditedFields({});
    } catch (err) {
      console.error('Error loading invoice:', err);
      setError(err instanceof Error ? err.message : 'Failed to load invoice');
    } finally {
      setLoading(false);
    }
  };


  const handleFieldChange = (fieldName: string, newValue: any) => {
    setEditedFields(prev => ({
      ...prev,
      [fieldName]: newValue
    }));
  };


  const handleSave = async () => {
    if (!invoice) return;

    try {
      setSaving(true);
      setError(null);
      setSuccessMessage(null);

      // Merge edited fields with original data
      const updatedData = {
        ...invoice,
        ...editedFields,
        updated_at: new Date().toISOString()
      };

      const { error: updateError } = await supabase
        .from('documents')
        .update({
          invoice_number: updatedData.invoice_number,
          invoice_date: updatedData.invoice_date,
          due_date: updatedData.due_date,
          vendor_name: updatedData.vendor_name,
          vendor_email: updatedData.vendor_email,
          vendor_phone: updatedData.vendor_phone,
          vendor_address: updatedData.vendor_address,
          vendor_gstin: updatedData.vendor_gstin,
          amount_total: updatedData.amount_total,
          tax_amount: updatedData.tax_amount,
          amount_net: updatedData.amount_net,
          payment_status: updatedData.payment_status,
          currency: updatedData.currency,
          extracted_data: updatedData.extracted_data,
          updated_at: updatedData.updated_at
        })
        .eq('id', invoice.id);

      if (updateError) throw updateError;

      setInvoice(updatedData);
      setEditedFields({});
      setSuccessMessage('✅ Invoice updated successfully!');

      // Auto-hide success message
      setTimeout(() => setSuccessMessage(null), 3000);
    } catch (err) {
      console.error('Error saving invoice:', err);
      setError(err instanceof Error ? err.message : 'Failed to save invoice');
    } finally {
      setSaving(false);
    }
  };


  const handleReset = () => {
    setEditedFields({});
    setError(null);
  };


  const handleDelete = async () => {
    if (!invoice) return;
    if (!confirm('Are you sure? This action cannot be undone.')) return;

    try {
      setSaving(true);
      setError(null);

      const { error: deleteError } = await supabase
        .from('documents')
        .delete()
        .eq('id', invoice.id);

      if (deleteError) throw deleteError;

      setSuccessMessage('Invoice deleted successfully');
      setTimeout(() => router.push('/invoices'), 2000);
    } catch (err) {
      console.error('Error deleting invoice:', err);
      setError(err instanceof Error ? err.message : 'Failed to delete invoice');
    } finally {
      setSaving(false);
    }
  };


  if (!router.isReady) return <div className="p-8">Loading...</div>;
  if (!user) return <div className="p-8">Please log in</div>;
  if (loading) return <div className="p-8">Loading invoice...</div>;
  if (!invoice) return <div className="p-8 text-red-600">Invoice not found</div>;


  return (
    <>
      <Head>
        <title>Edit Invoice - TrulyInvoice</title>
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
        <div className="max-w-4xl mx-auto">
          {/* Header */}
          <div className="flex justify-between items-center mb-8">
            <div>
              <h1 className="text-3xl font-bold text-gray-800">Edit Invoice</h1>
              <p className="text-gray-600 mt-2">{invoice.file_name}</p>
            </div>
            <Link href={`/invoices/${id}`}>
              <button className="px-4 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 transition">
                ← Back to View
              </button>
            </Link>
          </div>

          {/* Messages */}
          {error && (
            <div className="mb-6 p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg">
              {error}
            </div>
          )}
          {successMessage && (
            <div className="mb-6 p-4 bg-green-100 border border-green-400 text-green-700 rounded-lg">
              {successMessage}
            </div>
          )}

          {/* Invoice Data Form */}
          <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
              {/* Basic Information */}
              <section>
                <h2 className="text-xl font-bold mb-4 text-gray-800">📋 Basic Information</h2>

                <EditableField
                  label="Invoice Number"
                  value={editedFields.invoice_number ?? invoice.invoice_number ?? ''}
                  confidence={invoice.extracted_data?.invoice_number_confidence}
                  onChange={(val) => handleFieldChange('invoice_number', val)}
                />

                <EditableField
                  label="Invoice Date"
                  value={editedFields.invoice_date ?? invoice.invoice_date ?? ''}
                  type="date"
                  confidence={invoice.extracted_data?.invoice_date_confidence}
                  onChange={(val) => handleFieldChange('invoice_date', val)}
                />

                <EditableField
                  label="Due Date"
                  value={editedFields.due_date ?? invoice.due_date ?? ''}
                  type="date"
                  confidence={invoice.extracted_data?.due_date_confidence}
                  onChange={(val) => handleFieldChange('due_date', val)}
                />

                <EditableField
                  label="Currency"
                  value={editedFields.currency ?? invoice.currency ?? 'INR'}
                  confidence={invoice.extracted_data?.currency_confidence}
                  onChange={(val) => handleFieldChange('currency', val)}
                />
              </section>

              {/* Vendor Information */}
              <section>
                <h2 className="text-xl font-bold mb-4 text-gray-800">🏢 Vendor Information</h2>

                <EditableField
                  label="Vendor Name"
                  value={editedFields.vendor_name ?? invoice.vendor_name ?? ''}
                  confidence={invoice.extracted_data?.vendor_name_confidence}
                  onChange={(val) => handleFieldChange('vendor_name', val)}
                />

                <EditableField
                  label="Email"
                  value={editedFields.vendor_email ?? invoice.vendor_email ?? ''}
                  type="email"
                  confidence={invoice.extracted_data?.vendor_email_confidence}
                  onChange={(val) => handleFieldChange('vendor_email', val)}
                />

                <EditableField
                  label="Phone"
                  value={editedFields.vendor_phone ?? invoice.vendor_phone ?? ''}
                  type="tel"
                  confidence={invoice.extracted_data?.vendor_phone_confidence}
                  onChange={(val) => handleFieldChange('vendor_phone', val)}
                />

                <EditableField
                  label="GSTIN"
                  value={editedFields.vendor_gstin ?? invoice.vendor_gstin ?? ''}
                  confidence={invoice.extracted_data?.vendor_gstin_confidence}
                  onChange={(val) => handleFieldChange('vendor_gstin', val)}
                />
              </section>
            </div>

            {/* Address Information */}
            <section className="mb-8">
              <h2 className="text-xl font-bold mb-4 text-gray-800">📍 Vendor Address</h2>
              <textarea
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                rows={3}
                value={editedFields.vendor_address ?? invoice.vendor_address ?? ''}
                onChange={(e) => handleFieldChange('vendor_address', e.target.value)}
                placeholder="Enter vendor address..."
              />
            </section>

            {/* Financial Information */}
            <section className="mb-8">
              <h2 className="text-xl font-bold mb-4 text-gray-800">💰 Financial Information</h2>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <EditableField
                  label="Net Amount"
                  value={editedFields.amount_net ?? invoice.amount_net ?? 0}
                  type="number"
                  confidence={invoice.extracted_data?.amount_net_confidence}
                  onChange={(val) => handleFieldChange('amount_net', parseFloat(val) || 0)}
                />

                <EditableField
                  label="Tax Amount"
                  value={editedFields.tax_amount ?? invoice.tax_amount ?? 0}
                  type="number"
                  confidence={invoice.extracted_data?.tax_amount_confidence}
                  onChange={(val) => handleFieldChange('tax_amount', parseFloat(val) || 0)}
                />

                <EditableField
                  label="Total Amount"
                  value={editedFields.amount_total ?? invoice.amount_total ?? 0}
                  type="number"
                  confidence={invoice.extracted_data?.amount_total_confidence}
                  onChange={(val) => handleFieldChange('amount_total', parseFloat(val) || 0)}
                />
              </div>
            </section>

            {/* Payment Status */}
            <section className="mb-8">
              <h2 className="text-xl font-bold mb-4 text-gray-800">💳 Payment Status</h2>

              <div className="flex items-center gap-4">
                <select
                  className="flex-1 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                  value={editedFields.payment_status ?? invoice.payment_status ?? 'pending'}
                  onChange={(e) => handleFieldChange('payment_status', e.target.value)}
                >
                  <option value="pending">Pending</option>
                  <option value="paid">Paid</option>
                  <option value="unpaid">Unpaid</option>
                  <option value="overdue">Overdue</option>
                  <option value="partially_paid">Partially Paid</option>
                </select>

                {(invoice.payment_status_confidence !== undefined) && (
                  <div className="text-right">
                    <div className="text-sm text-gray-600">Confidence</div>
                    <div className="text-lg font-bold">
                      {(invoice.payment_status_confidence * 100).toFixed(0)}%
                    </div>
                  </div>
                )}
              </div>
            </section>

            {/* Action Buttons */}
            <div className="flex gap-4 justify-between pt-8 border-t border-gray-200">
              <div className="flex gap-4">
                <button
                  onClick={handleSave}
                  disabled={saving || Object.keys(editedFields).length === 0}
                  className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition"
                >
                  {saving ? 'Saving...' : '💾 Save Changes'}
                </button>

                <button
                  onClick={handleReset}
                  disabled={Object.keys(editedFields).length === 0}
                  className="px-6 py-2 bg-gray-400 text-white rounded-lg hover:bg-gray-500 disabled:opacity-50 disabled:cursor-not-allowed transition"
                >
                  🔄 Reset
                </button>
              </div>

              <button
                onClick={handleDelete}
                disabled={saving}
                className="px-6 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:opacity-50 disabled:cursor-not-allowed transition"
              >
                🗑️ Delete
              </button>
            </div>

            {Object.keys(editedFields).length > 0 && (
              <div className="mt-4 p-3 bg-blue-50 border border-blue-200 rounded-lg text-sm text-blue-700">
                💡 {Object.keys(editedFields).length} field(s) modified. Click "Save Changes" to persist.
              </div>
            )}
          </div>

          {/* Summary */}
          <div className="bg-white rounded-lg shadow-lg p-8">
            <h2 className="text-xl font-bold mb-4 text-gray-800">📊 Summary</h2>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
              <div className="p-4 bg-blue-50 rounded-lg">
                <div className="text-gray-600 text-sm">Created</div>
                <div className="font-bold text-gray-800">
                  {new Date(invoice.created_at).toLocaleDateString()}
                </div>
              </div>
              <div className="p-4 bg-green-50 rounded-lg">
                <div className="text-gray-600 text-sm">Status</div>
                <div className="font-bold text-gray-800 capitalize">
                  {editedFields.payment_status ?? invoice.payment_status ?? 'pending'}
                </div>
              </div>
              <div className="p-4 bg-purple-50 rounded-lg">
                <div className="text-gray-600 text-sm">Total Amount</div>
                <div className="font-bold text-gray-800">
                  ₹{(editedFields.amount_total ?? invoice.amount_total ?? 0).toFixed(2)}
                </div>
              </div>
              <div className="p-4 bg-orange-50 rounded-lg">
                <div className="text-gray-600 text-sm">Modified</div>
                <div className="font-bold text-gray-800">
                  {new Date(invoice.updated_at).toLocaleDateString()}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}


/**
 * Reusable editable field component with confidence indicator
 */
function EditableField({
  label,
  value,
  type = 'text',
  confidence,
  onChange
}: {
  label: string;
  value: string | number;
  type?: string;
  confidence?: number;
  onChange: (value: string) => void;
}) {
  const getConfidenceColor = (conf?: number) => {
    if (conf === undefined) return 'gray';
    if (conf >= 0.9) return 'green';
    if (conf >= 0.7) return 'yellow';
    if (conf >= 0.5) return 'orange';
    return 'red';
  };

  const color = getConfidenceColor(confidence);
  const colorClasses = {
    green: 'text-green-600',
    yellow: 'text-yellow-600',
    orange: 'text-orange-600',
    red: 'text-red-600',
    gray: 'text-gray-400'
  };

  return (
    <div className="mb-4">
      <div className="flex justify-between items-center mb-1">
        <label className="block text-sm font-medium text-gray-700">{label}</label>
        {confidence !== undefined && (
          <span className={`text-xs font-bold ${colorClasses[color as keyof typeof colorClasses]}`}>
            📊 {(confidence * 100).toFixed(0)}%
          </span>
        )}
      </div>
      <input
        type={type}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
        placeholder={`Enter ${label.toLowerCase()}...`}
      />
    </div>
  );
}
