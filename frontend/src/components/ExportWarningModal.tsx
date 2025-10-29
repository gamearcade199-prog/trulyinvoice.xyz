'use client'

import { AlertTriangle, CheckCircle, XCircle } from 'lucide-react'

interface ExportWarningModalProps {
  warnings: string[]
  onConfirm: () => void
  onCancel: () => void
}

export default function ExportWarningModal({ warnings, onConfirm, onCancel }: ExportWarningModalProps) {
  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-2xl max-w-2xl w-full max-h-[80vh] overflow-hidden animate-in fade-in zoom-in duration-200">
        {/* Header - Consistent Theme */}
        <div className="bg-gradient-to-r from-blue-600 to-indigo-600 p-6 text-white">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-white/20 rounded-lg backdrop-blur-sm">
              <AlertTriangle className="w-6 h-6" />
            </div>
            <div>
              <h3 className="text-xl font-bold">Export Validation Warnings</h3>
              <p className="text-sm text-blue-100 mt-1">
                {warnings.length} {warnings.length === 1 ? 'issue' : 'issues'} found in your invoices
              </p>
            </div>
          </div>
        </div>

        {/* Content */}
        <div className="p-6 max-h-96 overflow-y-auto">
          <p className="text-gray-700 dark:text-gray-300 mb-4">
            The following fields are missing and will use default values during export:
          </p>
          
          <div className="space-y-2">
            {warnings.slice(0, 10).map((warning, index) => (
              <div 
                key={index}
                className="flex items-start gap-3 p-3 bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 rounded-lg"
              >
                <AlertTriangle className="w-5 h-5 text-amber-600 dark:text-amber-400 flex-shrink-0 mt-0.5" />
                <p className="text-sm text-gray-700 dark:text-gray-300 flex-1">{warning}</p>
              </div>
            ))}
            
            {warnings.length > 10 && (
              <div className="p-3 bg-gray-100 dark:bg-gray-700 rounded-lg text-center">
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  ... and {warnings.length - 10} more {warnings.length - 10 === 1 ? 'warning' : 'warnings'}
                </p>
              </div>
            )}
          </div>

          <div className="mt-6 p-4 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg">
            <p className="text-sm text-blue-800 dark:text-blue-200">
              <strong>Note:</strong> These warnings won't prevent export. Default values will be applied automatically.
            </p>
          </div>
        </div>

        {/* Footer */}
        <div className="bg-gray-50 dark:bg-gray-900 px-6 py-4 flex items-center justify-end gap-3 border-t border-gray-200 dark:border-gray-700">
          <button
            onClick={onCancel}
            className="px-6 py-2.5 rounded-lg font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 hover:bg-gray-50 dark:hover:bg-gray-700 transition-all duration-200 flex items-center gap-2 shadow-sm"
          >
            <XCircle className="w-4 h-4" />
            Cancel & Review
          </button>
          <button
            onClick={onConfirm}
            className="px-6 py-2.5 rounded-lg font-medium text-white bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 transition-all duration-200 flex items-center gap-2 shadow-lg hover:shadow-xl"
          >
            <CheckCircle className="w-4 h-4" />
            Export with Defaults
          </button>
        </div>
      </div>
    </div>
  )
}
