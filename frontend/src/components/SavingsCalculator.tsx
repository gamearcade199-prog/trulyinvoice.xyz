'use client'

import { useState } from 'react'

const SavingsCalculator = () => {
  const [invoices, setInvoices] = useState(100)
  const hoursSaved = (invoices * 5) / 60
  const moneySaved = hoursSaved * 500 // Assuming an hourly rate of ₹500

  return (
    <div className="bg-white dark:bg-gray-900 py-12 sm:py-16">
      <div className="mx-auto max-w-7xl px-6 lg:px-8">
        <div className="mx-auto max-w-2xl text-center">
          <h2 className="text-3xl font-bold tracking-tight text-gray-900 dark:text-white sm:text-4xl">
            Calculate Your Savings
          </h2>
          <p className="mt-6 text-lg leading-8 text-gray-600 dark:text-gray-300">
            See how much time and money you can save with TrulyInvoice.
          </p>
        </div>
        <div className="mx-auto mt-16 max-w-2xl rounded-3xl ring-1 ring-gray-200 dark:ring-gray-700 p-8">
          <div className="flex flex-col items-center gap-y-8">
            <div className="w-full">
              <label htmlFor="invoices" className="block text-sm font-medium leading-6 text-gray-900 dark:text-white">
                How many invoices do you process per month?
              </label>
              <input
                id="invoices"
                type="range"
                min="10"
                max="1000"
                step="10"
                value={invoices}
                onChange={(e) => setInvoices(Number(e.target.value))}
                className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer dark:bg-gray-700"
              />
              <div className="text-center text-lg font-semibold text-gray-900 dark:text-white mt-2">
                {invoices} invoices
              </div>
            </div>
            <div className="grid grid-cols-1 gap-8 sm:grid-cols-2">
              <div className="text-center">
                <div className="text-4xl font-bold tracking-tight text-gray-900 dark:text-white">
                  {hoursSaved.toFixed(1)}
                </div>
                <div className="mt-2 text-base leading-7 text-gray-600 dark:text-gray-300">
                  Hours saved per month
                </div>
              </div>
              <div className="text-center">
                <div className="text-4xl font-bold tracking-tight text-gray-900 dark:text-white">
                  ₹{moneySaved.toFixed(2)}
                </div>
                <div className="mt-2 text-base leading-7 text-gray-600 dark:text-gray-300">
                  Money saved per month
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default SavingsCalculator
