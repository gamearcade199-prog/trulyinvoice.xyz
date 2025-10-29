import { CheckCircle2, Download, FileText, Users, DollarSign, X } from 'lucide-react'

interface ExportSuccessModalProps {
  exportType: 'tally' | 'quickbooks' | 'zoho' | 'csv'
  stats: {
    invoiceCount: number
    partyLedgers?: number
    gstLedgers?: number
    expenseLedgers?: number
    lineItems?: number
    warningCount?: number
  }
  onClose: () => void
}

export default function ExportSuccessModal({ exportType, stats, onClose }: ExportSuccessModalProps) {
  const titles = {
    tally: 'Tally XML Export Successful!',
    quickbooks: 'QuickBooks Export Successful!',
    zoho: 'Zoho Books Export Successful!',
    csv: 'CSV Export Successful!'
  }

  const importSteps = {
    tally: [
      'Backup your Tally company first!',
      'Gateway of Tally → Import Data → XML',
      'Select the downloaded XML file',
      'Check import log for any errors',
      'Verify vouchers: Display → Vouchers',
      'Check ledgers: Display → Ledgers'
    ],
    quickbooks: [
      'Backup your QuickBooks company first!',
      'File → Utilities → Import → IIF Files',
      'Select the downloaded .iif file',
      'Review import log for errors',
      'Verify bills: Vendors → Vendor Center',
      'Check accounts: Lists → Chart of Accounts'
    ],
    zoho: [
      'Login to Zoho Books',
      'Sales → Invoices → ⋮ → Import Invoices',
      'Upload CSV file',
      'Map fields (most will auto-detect)',
      'Preview and validate data',
      'Confirm import',
      'Check invoices list for new entries'
    ],
    csv: [
      'Open the downloaded CSV file',
      'Verify all data is correct',
      'Import into your accounting software',
      'Follow software-specific import steps'
    ]
  }

  const tips = {
    tally: 'If ledger already exists with different name case (e.g., "ABC INDUSTRIES" vs "Abc Industries"), Tally will create duplicate. You can merge ledgers later using Alter → Ledger.',
    quickbooks: 'IIF files import directly without field mapping. Review the imported data immediately after import to catch any issues early.',
    zoho: 'Zoho Books supports automatic customer creation during import. Map the "Customer Name" field correctly to avoid duplicates.',
    csv: 'Keep the CSV file as a backup. You can re-import if needed or use it for reconciliation.'
  }

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
            <CheckCircle2 className="w-10 h-10" />
            <div>
              <h2 className="text-2xl font-bold">{titles[exportType]}</h2>
              <p className="text-blue-100 text-sm">Your export is ready for import</p>
            </div>
          </div>
        </div>

        {/* Content */}
        <div className="p-6 overflow-y-auto max-h-[calc(90vh-180px)]">
          {/* Export Summary */}
          <div className="bg-gray-50 dark:bg-gray-800 rounded-xl p-5 mb-6">
            <h3 className="font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
              <Download className="w-5 h-5 text-blue-600" />
              Export Summary
            </h3>
            <div className="grid grid-cols-2 gap-4">
              <div className="flex items-center gap-3">
                <FileText className="w-5 h-5 text-blue-600" />
                <div>
                  <p className="text-sm text-gray-600 dark:text-gray-400">Invoices</p>
                  <p className="text-lg font-bold text-gray-900 dark:text-white">{stats.invoiceCount}</p>
                </div>
              </div>
              
              {stats.partyLedgers !== undefined && (
                <div className="flex items-center gap-3">
                  <Users className="w-5 h-5 text-purple-600" />
                  <div>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Party Ledgers</p>
                    <p className="text-lg font-bold text-gray-900 dark:text-white">{stats.partyLedgers}</p>
                  </div>
                </div>
              )}
              
              {stats.gstLedgers !== undefined && (
                <div className="flex items-center gap-3">
                  <DollarSign className="w-5 h-5 text-green-600" />
                  <div>
                    <p className="text-sm text-gray-600 dark:text-gray-400">GST Ledgers</p>
                    <p className="text-lg font-bold text-gray-900 dark:text-white">{stats.gstLedgers}</p>
                  </div>
                </div>
              )}
              
              {stats.expenseLedgers !== undefined && (
                <div className="flex items-center gap-3">
                  <FileText className="w-5 h-5 text-orange-600" />
                  <div>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Expense Ledgers</p>
                    <p className="text-lg font-bold text-gray-900 dark:text-white">{stats.expenseLedgers}</p>
                  </div>
                </div>
              )}
              
              {stats.lineItems !== undefined && (
                <div className="flex items-center gap-3">
                  <FileText className="w-5 h-5 text-indigo-600" />
                  <div>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Line Items</p>
                    <p className="text-lg font-bold text-gray-900 dark:text-white">{stats.lineItems}</p>
                  </div>
                </div>
              )}
            </div>
            
            {stats.warningCount && stats.warningCount > 0 && (
              <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
                <p className="text-sm text-amber-600 dark:text-amber-400">
                  ⚠️ {stats.warningCount} warning(s) - default values were used
                </p>
              </div>
            )}
          </div>

          {/* Import Checklist */}
          <div className="mb-6">
            <h3 className="font-semibold text-gray-900 dark:text-white mb-3">
              📋 Import Checklist
            </h3>
            <ol className="space-y-2">
              {importSteps[exportType].map((step, index) => (
                <li key={index} className="flex items-start gap-3">
                  <span className="flex-shrink-0 w-6 h-6 rounded-full bg-blue-100 dark:bg-blue-900 text-blue-600 dark:text-blue-400 text-sm font-bold flex items-center justify-center">
                    {index + 1}
                  </span>
                  <span className="text-gray-700 dark:text-gray-300 text-sm pt-0.5">{step}</span>
                </li>
              ))}
            </ol>
          </div>

          {/* Pro Tip */}
          <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
            <p className="text-sm text-blue-900 dark:text-blue-200">
              <span className="font-semibold">💡 Pro Tip:</span> {tips[exportType]}
            </p>
          </div>
        </div>

        {/* Footer */}
        <div className="border-t border-gray-200 dark:border-gray-700 p-4 bg-gray-50 dark:bg-gray-800/50">
          <button
            onClick={onClose}
            className="w-full py-3 px-4 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-semibold rounded-lg transition-colors shadow-lg"
          >
            Got it, thanks!
          </button>
        </div>
      </div>
    </div>
  )
}
