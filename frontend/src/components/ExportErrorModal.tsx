import { XCircle, AlertTriangle, X } from 'lucide-react'

interface ExportErrorModalProps {
  title: string
  errors: string[]
  type: 'validation' | 'noSelection'
  onClose: () => void
}

export default function ExportErrorModal({ title, errors, type, onClose }: ExportErrorModalProps) {
  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div className="bg-white dark:bg-gray-900 rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-hidden border border-gray-200 dark:border-gray-700 animate-fadeIn">
        {/* Header - Consistent Theme */}
        <div className="bg-gradient-to-r from-blue-600 to-indigo-600 p-6 relative">
          <button
            onClick={onClose}
            className="absolute top-4 right-4 text-white/80 hover:text-white transition-colors"
            aria-label="Close"
          >
            <X className="w-6 h-6" />
          </button>
          <div className="flex items-center gap-3 text-white">
            {type === 'validation' ? (
              <XCircle className="w-10 h-10" />
            ) : (
              <AlertTriangle className="w-10 h-10" />
            )}
            <div>
              <h2 className="text-2xl font-bold">{title}</h2>
              <p className="text-blue-100 text-sm">
                {type === 'validation' 
                  ? 'Please fix these issues before exporting' 
                  : 'Select at least one invoice to continue'}
              </p>
            </div>
          </div>
        </div>

        {/* Content */}
        <div className="p-6 overflow-y-auto max-h-[calc(90vh-180px)]">
          {type === 'noSelection' ? (
            <div className="text-center py-8">
              <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-blue-100 dark:bg-blue-900/20 mb-4">
                <AlertTriangle className="w-10 h-10 text-blue-600 dark:text-blue-400" />
              </div>
              <p className="text-lg text-gray-700 dark:text-gray-300 mb-4">
                No invoices selected for export
              </p>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Please select at least one invoice from the list and try again.
              </p>
            </div>
          ) : (
            <>
              <div className="mb-4">
                <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
                  Found <span className="font-bold text-blue-600 dark:text-blue-400">{errors.length}</span> {errors.length === 1 ? 'error' : 'errors'} that must be fixed:
                </p>
              </div>

              {/* Error List */}
              <div className="space-y-2 mb-6">
                {errors.slice(0, 10).map((error, index) => (
                  <div
                    key={index}
                    className="flex items-start gap-3 p-3 bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg"
                  >
                    <XCircle className="w-5 h-5 text-blue-600 dark:text-blue-400 flex-shrink-0 mt-0.5" />
                    <span className="text-sm text-gray-900 dark:text-gray-100">{error}</span>
                  </div>
                ))}
                
                {errors.length > 10 && (
                  <div className="text-center py-3 text-sm text-gray-600 dark:text-gray-400">
                    ... and <span className="font-bold">{errors.length - 10}</span> more {errors.length - 10 === 1 ? 'error' : 'errors'}
                  </div>
                )}
              </div>

              {/* Help Text */}
              <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
                <p className="text-sm text-blue-900 dark:text-blue-200">
                  <span className="font-semibold">💡 Quick Fix:</span> Click on each invoice to edit and fill in the missing required fields. All fields must be completed before export.
                </p>
              </div>
            </>
          )}
        </div>

        {/* Footer */}
        <div className="border-t border-gray-200 dark:border-gray-700 p-4 bg-gray-50 dark:bg-gray-800/50">
          <button
            onClick={onClose}
            className="w-full py-3 px-4 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-semibold rounded-lg transition-colors shadow-lg"
          >
            {type === 'validation' ? 'Fix Issues' : 'Select Invoices'}
          </button>
        </div>
      </div>
    </div>
  )
}
