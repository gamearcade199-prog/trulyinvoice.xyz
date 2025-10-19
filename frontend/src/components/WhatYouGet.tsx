'use client'

import { FileText, FileSpreadsheet, Files } from 'lucide-react'

const WhatYouGet = () => {
  return (
    <div className="bg-white dark:bg-gray-900 py-12 sm:py-16">
      <div className="mx-auto max-w-7xl px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 md:gap-12 items-center">
          <div className="text-center md:text-left">
            <h2 className="text-3xl font-bold tracking-tight text-gray-900 dark:text-white sm:text-4xl">
              You Give Us Any Invoice
            </h2>
            <p className="mt-6 text-lg leading-8 text-gray-600 dark:text-gray-300">
              PDFs, photos, or scans. We can handle them all.
            </p>
            <div className="mt-8 flex justify-center md:justify-start gap-4">
              <FileText className="w-12 h-12 text-blue-500" />
              <FileText className="w-12 h-12 text-red-500" />
              <FileText className="w-12 h-12 text-green-500" />
            </div>
          </div>
          <div className="text-center md:text-left">
            <h2 className="text-3xl font-bold tracking-tight text-gray-900 dark:text-white sm:text-4xl">
              We Give You Perfect Data
            </h2>
            <p className="mt-6 text-lg leading-8 text-gray-600 dark:text-gray-300">
              Clean, structured spreadsheets. Ready for your accounting software.
            </p>
            <div className="mt-8 flex justify-center md:justify-start gap-4">
              <FileSpreadsheet className="w-12 h-12 text-green-500" />
              <Files className="w-12 h-12 text-blue-500" />
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default WhatYouGet
