'use client'

import { Briefcase } from 'lucide-react'

const logos = [
  { name: 'YourStory', icon: Briefcase },
  { name: 'IIM Bangalore', icon: Briefcase },
  { name: 'Startup India', icon: Briefcase },
  { name: 'NASSCOM', icon: Briefcase },
  { name: 'TiE', icon: Briefcase },
]

export default function TrustedBy() {
  return (
    <div className="bg-gray-50 dark:bg-gray-950 py-8 sm:py-12">
      <div className="mx-auto max-w-7xl px-6 lg:px-8">
        <h2 className="text-center text-lg font-semibold leading-8 text-gray-900 dark:text-white">
          Trusted by the most innovative companies in India
        </h2>
        <div className="mx-auto mt-10 grid max-w-lg grid-cols-2 items-center gap-x-8 gap-y-10 sm:max-w-xl sm:grid-cols-3 lg:mx-0 lg:max-w-none lg:grid-cols-5">
          {logos.map((logo) => {
            const Icon = logo.icon
            return (
              <div key={logo.name} className="flex items-center justify-center gap-2">
                <Icon className="h-8 w-8 text-gray-400" />
                <span className="text-gray-400 font-semibold">{logo.name}</span>
              </div>
            )
          })}
        </div>
      </div>
    </div>
  )
}
