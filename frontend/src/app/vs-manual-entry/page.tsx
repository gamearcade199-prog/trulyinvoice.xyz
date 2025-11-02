import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'TrulyInvoice vs Manual Data Entry - Comparison & ROI Analysis',
  description: 'Compare TrulyInvoice AI automation vs manual invoice data entry. See time savings, accuracy improvements, and ROI calculations for your business.',
  keywords: ['invoice automation vs manual', 'data entry vs OCR', 'invoice processing comparison', 'accounting automation ROI'],
  openGraph: {
    title: 'TrulyInvoice vs Manual Data Entry',
    description: 'See how AI automation outperforms manual invoice processing',
    images: ['/og-image-india.jpg'],
  },
}

export default function VsManualEntryPage() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50 dark:from-gray-900 dark:via-gray-900 dark:to-gray-800">
      <div className="container mx-auto px-4 py-12">
        <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
          TrulyInvoice vs Manual Data Entry: Complete Comparison
        </h1>
        <p className="text-xl text-gray-600 dark:text-gray-300 mb-8">
          Stop wasting time on manual invoice data entry. See exactly how AI automation saves time, improves accuracy, and boosts your bottom line.
        </p>

        {/* Comparison Table */}
        <section className="mb-12 overflow-x-auto">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">Head-to-Head Comparison</h2>
          <table className="w-full border-collapse">
            <thead>
              <tr className="bg-gray-100 dark:bg-gray-700">
                <th className="border border-gray-300 dark:border-gray-600 p-4 text-left font-bold text-gray-900 dark:text-white">Factor</th>
                <th className="border border-gray-300 dark:border-gray-600 p-4 text-center text-gray-900 dark:text-white">Manual Entry</th>
                <th className="border border-gray-300 dark:border-gray-600 p-4 text-center text-gray-900 dark:text-white">TrulyInvoice</th>
              </tr>
            </thead>
            <tbody>
              <tr className="hover:bg-gray-50 dark:hover:bg-gray-800">
                <td className="border border-gray-300 dark:border-gray-600 p-4 font-bold text-gray-900 dark:text-white">Time per Invoice</td>
                <td className="border border-gray-300 dark:border-gray-600 p-4 text-center text-gray-700 dark:text-gray-300">5-10 minutes</td>
                <td className="border border-gray-300 dark:border-gray-600 p-4 text-center bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-400 font-bold">30 seconds</td>
              </tr>
              <tr className="hover:bg-gray-50 dark:hover:bg-gray-800">
                <td className="border border-gray-300 dark:border-gray-600 p-4 font-bold text-gray-900 dark:text-white">Processing Speed (100 invoices)</td>
                <td className="border border-gray-300 dark:border-gray-600 p-4 text-center text-gray-700 dark:text-gray-300">8-16 hours</td>
                <td className="border border-gray-300 dark:border-gray-600 p-4 text-center bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-400 font-bold">2-5 minutes</td>
              </tr>
              <tr className="hover:bg-gray-50 dark:hover:bg-gray-800">
                <td className="border border-gray-300 dark:border-gray-600 p-4 font-bold text-gray-900 dark:text-white">Data Accuracy</td>
                <td className="border border-gray-300 dark:border-gray-600 p-4 text-center text-gray-700 dark:text-gray-300">95-98%</td>
                <td className="border border-gray-300 dark:border-gray-600 p-4 text-center bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-400 font-bold">98-99%</td>
              </tr>
              <tr className="hover:bg-gray-50 dark:hover:bg-gray-800">
                <td className="border border-gray-300 dark:border-gray-600 p-4 font-bold text-gray-900 dark:text-white">Error Rate</td>
                <td className="border border-gray-300 dark:border-gray-600 p-4 text-center text-gray-700 dark:text-gray-300">2-5% (mistakes)</td>
                <td className="border border-gray-300 dark:border-gray-600 p-4 text-center bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-400 font-bold">0.5-1% (requires review)</td>
              </tr>
              <tr className="hover:bg-gray-50 dark:hover:bg-gray-800">
                <td className="border border-gray-300 dark:border-gray-600 p-4 font-bold text-gray-900 dark:text-white">Monthly Cost (500 invoices)</td>
                <td className="border border-gray-300 dark:border-gray-600 p-4 text-center text-gray-700 dark:text-gray-300">₹15,000-25,000 labor</td>
                <td className="border border-gray-300 dark:border-gray-600 p-4 text-center bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-400 font-bold">₹299-799/month</td>
              </tr>
              <tr className="hover:bg-gray-50 dark:hover:bg-gray-800">
                <td className="border border-gray-300 dark:border-gray-600 p-4 font-bold text-gray-900 dark:text-white">Setup Time</td>
                <td className="border border-gray-300 dark:border-gray-600 p-4 text-center text-gray-700 dark:text-gray-300">Immediate</td>
                <td className="border border-gray-300 dark:border-gray-600 p-4 text-center bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-400 font-bold">2 minutes</td>
              </tr>
              <tr className="hover:bg-gray-50 dark:hover:bg-gray-800">
                <td className="border border-gray-300 dark:border-gray-600 p-4 font-bold text-gray-900 dark:text-white">Staff Training Required</td>
                <td className="border border-gray-300 dark:border-gray-600 p-4 text-center text-gray-700 dark:text-gray-300">Ongoing</td>
                <td className="border border-gray-300 dark:border-gray-600 p-4 text-center bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-400 font-bold">None (intuitive UI)</td>
              </tr>
              <tr className="hover:bg-gray-50 dark:hover:bg-gray-800">
                <td className="border border-gray-300 dark:border-gray-600 p-4 font-bold text-gray-900 dark:text-white">Scalability</td>
                <td className="border border-gray-300 dark:border-gray-600 p-4 text-center text-gray-700 dark:text-gray-300">Limited (hire more staff)</td>
                <td className="border border-gray-300 dark:border-gray-600 p-4 text-center bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-400 font-bold">Unlimited</td>
              </tr>
              <tr className="hover:bg-gray-50 dark:hover:bg-gray-800">
                <td className="border border-gray-300 dark:border-gray-600 p-4 font-bold text-gray-900 dark:text-white">GST Compliance</td>
                <td className="border border-gray-300 dark:border-gray-600 p-4 text-center text-gray-700 dark:text-gray-300">Manual validation needed</td>
                <td className="border border-gray-300 dark:border-gray-600 p-4 text-center bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-400 font-bold">Automatic validation</td>
              </tr>
              <tr className="hover:bg-gray-50 dark:hover:bg-gray-800">
                <td className="border border-gray-300 dark:border-gray-600 p-4 font-bold text-gray-900 dark:text-white">GSTIN Extraction</td>
                <td className="border border-gray-300 dark:border-gray-600 p-4 text-center text-gray-700 dark:text-gray-300">Manual entry</td>
                <td className="border border-gray-300 dark:border-gray-600 p-4 text-center bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-400 font-bold">Automatic (99% accurate)</td>
              </tr>
            </tbody>
          </table>
        </section>

        {/* Time Savings Visual */}
        <section className="mb-12 bg-blue-50 dark:bg-blue-900/20 p-8 rounded-lg">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">Real-World Time Savings Example</h2>
          <p className="text-gray-700 dark:text-gray-300 mb-6">Processing 100 invoices - The difference is dramatic:</p>
          <div className="grid md:grid-cols-3 gap-6">
            <div className="bg-white dark:bg-gray-800 p-6 rounded-lg border-l-4 border-red-500">
              <div className="text-3xl font-bold text-red-500 mb-2">16 hours</div>
              <p className="text-sm text-gray-900 dark:text-white"><strong>Manual Entry</strong> at 10 min/invoice</p>
              <p className="text-xs text-gray-500 dark:text-gray-400 mt-2">Need 2 staff members working full day</p>
            </div>
            <div className="bg-white dark:bg-gray-800 p-6 rounded-lg border-l-4 border-orange-500">
              <div className="text-3xl font-bold text-orange-500 mb-2">3 hours</div>
              <p className="text-sm text-gray-900 dark:text-white"><strong>With Basic OCR</strong> + manual fix</p>
              <p className="text-xs text-gray-500 dark:text-gray-400 mt-2">Lower accuracy = more corrections</p>
            </div>
            <div className="bg-white dark:bg-gray-800 p-6 rounded-lg border-l-4 border-green-500">
              <div className="text-3xl font-bold text-green-500 mb-2">5 minutes</div>
              <p className="text-sm text-gray-900 dark:text-white"><strong>TrulyInvoice</strong> bulk processing</p>
              <p className="text-xs text-gray-500 dark:text-gray-400 mt-2">98% accuracy, ready to export</p>
            </div>
          </div>
        </section>

        {/* Cost Analysis */}
        <section className="mb-12">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">Cost Comparison for Indian Businesses</h2>
          <div className="grid md:grid-cols-2 gap-6">
            <div className="border border-gray-300 dark:border-gray-600 rounded-lg p-6 bg-white dark:bg-gray-800">
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4">Manual Entry (Monthly)</h3>
              <ul className="space-y-2 mb-4">
                <li className="flex justify-between text-gray-700 dark:text-gray-300">
                  <span>Staff cost (50 hrs @ ₹300/hr):</span>
                  <span className="font-bold">₹15,000</span>
                </li>
                <li className="flex justify-between text-gray-700 dark:text-gray-300">
                  <span>Supervisor oversight (10 hrs):</span>
                  <span className="font-bold">₹3,000</span>
                </li>
                <li className="flex justify-between text-gray-700 dark:text-gray-300">
                  <span>Error correction (5%):</span>
                  <span className="font-bold">₹2,000</span>
                </li>
                <li className="flex justify-between text-gray-700 dark:text-gray-300">
                  <span>Software (Excel, basic):</span>
                  <span className="font-bold">₹500</span>
                </li>
              </ul>
              <div className="border-t border-gray-300 dark:border-gray-600 pt-3">
                <div className="flex justify-between font-bold text-lg text-gray-900 dark:text-white">
                  <span>Total:</span>
                  <span>₹20,500/month</span>
                </div>
              </div>
            </div>
            <div className="border border-gray-300 dark:border-gray-600 rounded-lg p-6 bg-green-50 dark:bg-green-900/20">
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4">TrulyInvoice (Monthly)</h3>
              <ul className="space-y-2 mb-4">
                <li className="flex justify-between text-gray-700 dark:text-gray-300">
                  <span>Professional Plan:</span>
                  <span className="font-bold">₹799</span>
                </li>
                <li className="flex justify-between text-gray-700 dark:text-gray-300">
                  <span>Spot checks (2 hrs):</span>
                  <span className="font-bold">₹600</span>
                </li>
                <li className="flex justify-between text-gray-700 dark:text-gray-300">
                  <span>Training & support:</span>
                  <span className="font-bold">₹0 (included)</span>
                </li>
                <li className="flex justify-between text-gray-700 dark:text-gray-300">
                  <span>Error corrections:</span>
                  <span className="font-bold">≈₹100</span>
                </li>
              </ul>
              <div className="border-t border-gray-300 dark:border-gray-600 pt-3">
                <div className="flex justify-between font-bold text-lg text-green-600 dark:text-green-400">
                  <span>Total:</span>
                  <span>₹1,499/month</span>
                </div>
              </div>
            </div>
          </div>
          <div className="mt-6 bg-yellow-50 dark:bg-yellow-900/20 p-6 rounded-lg border-l-4 border-yellow-500">
            <p className="font-bold text-lg text-gray-900 dark:text-white">💰 Monthly Savings: ₹19,001</p>
            <p className="text-sm text-gray-700 dark:text-gray-300 mt-2">Annual Savings: ₹2,28,012 with a single plan upgrade!</p>
          </div>
        </section>

        {/* ROI Calculator */}
        <section className="mb-12 bg-gradient-to-r from-purple-50 to-pink-50 dark:from-purple-900/20 dark:to-pink-900/20 p-8 rounded-lg">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">ROI Breakdown</h2>
          <div className="space-y-4">
            <div className="bg-white dark:bg-gray-800 p-4 rounded border border-gray-200 dark:border-gray-700">
              <p className="font-bold text-gray-900 dark:text-white">Payback Period: <span className="text-green-600 dark:text-green-400">Less than 1 week</span></p>
              <p className="text-sm text-gray-600 dark:text-gray-400">One month of manual labor savings covers an entire year of TrulyInvoice subscription</p>
            </div>
            <div className="bg-white dark:bg-gray-800 p-4 rounded border border-gray-200 dark:border-gray-700">
              <p className="font-bold text-gray-900 dark:text-white">12-Month ROI: <span className="text-green-600 dark:text-green-400">1,520%</span></p>
              <p className="text-sm text-gray-600 dark:text-gray-400">₹9,600 investment returns ₹2,28,012 in savings</p>
            </div>
            <div className="bg-white dark:bg-gray-800 p-4 rounded border border-gray-200 dark:border-gray-700">
              <p className="font-bold text-gray-900 dark:text-white">5-Year Value: <span className="text-green-600 dark:text-green-400">₹11,40,060</span></p>
              <p className="text-sm text-gray-600 dark:text-gray-400">Cumulative savings over 5 years of using TrulyInvoice</p>
            </div>
          </div>
        </section>

        {/* Quality Improvements */}
        <section className="mb-12">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">Beyond Cost: Quality & Compliance Benefits</h2>
          <div className="grid md:grid-cols-2 gap-6">
            <div className="bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg p-6">
              <h3 className="font-bold text-gray-900 dark:text-white mb-4">Manual Entry Issues:</h3>
              <ul className="space-y-2 list-disc pl-5 text-gray-700 dark:text-gray-300">
                <li>Typos in GSTIN lead to compliance issues</li>
                <li>Missed line items cause accounting discrepancies</li>
                <li>Tax calculation errors result in GST audit flags</li>
                <li>Duplicate entries create reconciliation nightmares</li>
                <li>Staff fatigue leads to quality decline</li>
              </ul>
            </div>
            <div className="bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg p-6">
              <h3 className="font-bold text-gray-900 dark:text-white mb-4">TrulyInvoice Advantages:</h3>
              <ul className="space-y-2 list-disc pl-5 text-gray-700 dark:text-gray-300">
                <li>Automatic GSTIN validation (99% accuracy)</li>
                <li>Zero missed line items (AI captures all data)</li>
                <li>Tax calculations always correct</li>
                <li>Duplicate detection prevents errors</li>
                <li>Consistent quality 24/7, no staff fatigue</li>
              </ul>
            </div>
          </div>
        </section>

        {/* Risk Analysis */}
        <section className="mb-12 bg-red-50 dark:bg-red-900/20 p-8 rounded-lg border-l-4 border-red-500">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Risks of Manual Data Entry</h2>
          <ul className="space-y-3">
            <li className="flex items-start">
              <span className="text-red-600 font-bold mr-3">⚠</span>
              <span className="text-gray-700 dark:text-gray-300"><strong>GST Audit Risk:</strong> Typos in GSTIN and incorrect tax entries can trigger GST audits</span>
            </li>
            <li className="flex items-start">
              <span className="text-red-600 font-bold mr-3">⚠</span>
              <span className="text-gray-700 dark:text-gray-300"><strong>Financial Misstatement:</strong> Manual errors accumulate and distort financial reports</span>
            </li>
            <li className="flex items-start">
              <span className="text-red-600 font-bold mr-3">⚠</span>
              <span className="text-gray-700 dark:text-gray-300"><strong>Staff Burnout:</strong> Repetitive data entry leads to high staff turnover and hiring costs</span>
            </li>
            <li className="flex items-start">
              <span className="text-red-600 font-bold mr-3">⚠</span>
              <span className="text-gray-700 dark:text-gray-300"><strong>Lost Productivity:</strong> Time spent on data entry could be spent on value-added advisory work</span>
            </li>
          </ul>
        </section>

        {/* Call to Action */}
        <section className="bg-gradient-to-r from-blue-600 to-blue-800 text-white p-12 rounded-lg text-center">
          <h2 className="text-3xl font-bold mb-4">Ready to Stop Manual Data Entry?</h2>
          <p className="text-lg mb-6">Join hundreds of businesses that have automated their invoice processing with TrulyInvoice.</p>
          <div className="flex justify-center gap-4 flex-wrap">
            <a href="/signup" className="bg-white text-blue-600 px-8 py-3 rounded-lg font-bold hover:bg-gray-100">
              Start Free Trial
            </a>
            <a href="/contact" className="border-2 border-white text-white px-8 py-3 rounded-lg font-bold hover:bg-blue-700">
              Schedule Demo
            </a>
          </div>
          <p className="text-sm mt-4">10 free invoices • No credit card required • Cancel anytime</p>
        </section>
      </div>
    </main>
  )
}
