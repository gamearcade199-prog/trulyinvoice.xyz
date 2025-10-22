'use client'

import { useState } from 'react'
import DashboardLayout from '@/components/DashboardLayout'
import { 
  MessageCircle, 
  Mail, 
  Phone, 
  MapPin, 
  Send,
  HelpCircle,
  Book,
  Video,
  Clock,
  CheckCircle
} from 'lucide-react'

export default function SupportPage() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    subject: '',
    message: ''
  })
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [submitSuccess, setSubmitSuccess] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsSubmitting(true)
    
    // Simulate form submission
    setTimeout(() => {
      setIsSubmitting(false)
      setSubmitSuccess(true)
      setFormData({ name: '', email: '', subject: '', message: '' })
      
      setTimeout(() => setSubmitSuccess(false), 5000)
    }, 1500)
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  return (
    <DashboardLayout>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            Support Center - Invoice Processing Help & Documentation
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Get help with TrulyInvoice - we're here to assist you
          </p>
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Contact Information - Left Sidebar */}
          <div className="lg:col-span-1 space-y-6">
            {/* Quick Contact Cards */}
            <div className="bg-gray-50 dark:bg-gray-900 rounded-xl shadow-sm border border-gray-200 dark:border-gray-800 p-6">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
                <Phone className="w-5 h-5 text-blue-500" />
                Quick Contact
              </h2>
              
              <div className="space-y-4">
                {/* WhatsApp Support */}
                <a 
                  href="https://wa.me/919101361482" 
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-start gap-3 p-4 rounded-lg bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 hover:bg-green-100 dark:hover:bg-green-900/30 transition-colors group"
                >
                  <MessageCircle className="w-5 h-5 text-green-600 dark:text-green-400 mt-0.5" />
                  <div className="flex-1">
                    <div className="font-medium text-gray-900 dark:text-white group-hover:text-green-600 dark:group-hover:text-green-400">
                      WhatsApp Support
                    </div>
                    <div className="text-sm text-gray-600 dark:text-gray-400">
                      +91 9101361482
                    </div>
                    <div className="text-xs text-green-600 dark:text-green-400 mt-1">
                      Available 24/7
                    </div>
                  </div>
                </a>

                {/* Email Support */}
                <a 
                  href="mailto:infotrulybot@gmail.com"
                  className="flex items-start gap-3 p-4 rounded-lg bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 hover:bg-blue-100 dark:hover:bg-blue-900/30 transition-colors group"
                >
                  <Mail className="w-5 h-5 text-blue-600 dark:text-blue-400 mt-0.5" />
                  <div className="flex-1">
                    <div className="font-medium text-gray-900 dark:text-white group-hover:text-blue-600 dark:group-hover:text-blue-400">
                      Email Support
                    </div>
                    <div className="text-sm text-gray-600 dark:text-gray-400 break-all">
                      infotrulybot@gmail.com
                    </div>
                    <div className="text-xs text-blue-600 dark:text-blue-400 mt-1">
                      Response within 24 hours
                    </div>
                  </div>
                </a>

                {/* Office Address */}
                <div className="flex items-start gap-3 p-4 rounded-lg bg-purple-50 dark:bg-purple-900/20 border border-purple-200 dark:border-purple-800">
                  <MapPin className="w-5 h-5 text-purple-600 dark:text-purple-400 mt-0.5" />
                  <div className="flex-1">
                    <div className="font-medium text-gray-900 dark:text-white mb-1">
                      Office Address
                    </div>
                    <div className="text-sm text-gray-600 dark:text-gray-400">
                      GS Road, Ganeshguri<br />
                      Assam - 781005<br />
                      India
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Business Hours */}
            <div className="bg-gradient-to-br from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20 rounded-xl shadow-sm border border-blue-200 dark:border-blue-800 p-6">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
                <Clock className="w-5 h-5 text-blue-500" />
                Business Hours
              </h3>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between text-gray-700 dark:text-gray-300">
                  <span>Monday - Friday</span>
                  <span className="font-medium">9:00 AM - 6:00 PM</span>
                </div>
                <div className="flex justify-between text-gray-700 dark:text-gray-300">
                  <span>Saturday</span>
                  <span className="font-medium">10:00 AM - 4:00 PM</span>
                </div>
                <div className="flex justify-between text-gray-700 dark:text-gray-300">
                  <span>Sunday</span>
                  <span className="font-medium">Closed</span>
                </div>
                <div className="mt-3 pt-3 border-t border-blue-200 dark:border-blue-800 text-green-600 dark:text-green-400 font-medium">
                  WhatsApp Support: 24/7
                </div>
              </div>
            </div>

            {/* Quick Links */}
            <div className="bg-gray-50 dark:bg-gray-900 rounded-xl shadow-sm border border-gray-200 dark:border-gray-800 p-6">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
                <Book className="w-5 h-5 text-blue-500" />
                Resources
              </h3>
              <div className="space-y-2">
                <a href="#faq" className="flex items-center gap-2 text-blue-600 dark:text-blue-400 hover:underline text-sm">
                  <HelpCircle className="w-4 h-4" />
                  FAQs
                </a>
                <a href="#guides" className="flex items-center gap-2 text-blue-600 dark:text-blue-400 hover:underline text-sm">
                  <Book className="w-4 h-4" />
                  User Guides
                </a>
                <a href="#videos" className="flex items-center gap-2 text-blue-600 dark:text-blue-400 hover:underline text-sm">
                  <Video className="w-4 h-4" />
                  Video Tutorials
                </a>
              </div>
            </div>
          </div>

          {/* Contact Form - Right Side */}
          <div className="lg:col-span-2">
            <div className="bg-gray-50 dark:bg-gray-900 rounded-xl shadow-sm border border-gray-200 dark:border-gray-800 p-8">
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
                Send us a Message
              </h2>
              <p className="text-gray-600 dark:text-gray-400 mb-6">
                Fill out the form below and we'll get back to you as soon as possible
              </p>

              {submitSuccess && (
                <div className="mb-6 p-4 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg flex items-center gap-3">
                  <CheckCircle className="w-5 h-5 text-green-600 dark:text-green-400" />
                  <div className="text-green-800 dark:text-green-200">
                    <strong>Message sent successfully!</strong> We'll respond within 24 hours.
                  </div>
                </div>
              )}

              <form onSubmit={handleSubmit} className="space-y-6">
                {/* Name */}
                <div>
                  <label htmlFor="name" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Your Name *
                  </label>
                  <input
                    type="text"
                    id="name"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    required
                    className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 focus:border-transparent transition-all"
                    placeholder="John Doe"
                  />
                </div>

                {/* Email */}
                <div>
                  <label htmlFor="email" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Email Address *
                  </label>
                  <input
                    type="email"
                    id="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    required
                    className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 focus:border-transparent transition-all"
                    placeholder="john@example.com"
                  />
                </div>

                {/* Subject */}
                <div>
                  <label htmlFor="subject" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Subject *
                  </label>
                  <select
                    id="subject"
                    name="subject"
                    value={formData.subject}
                    onChange={handleChange}
                    required
                    className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 focus:border-transparent transition-all"
                  >
                    <option value="">Select a subject</option>
                    <option value="technical">Technical Support</option>
                    <option value="billing">Billing & Subscription</option>
                    <option value="feature">Feature Request</option>
                    <option value="bug">Report a Bug</option>
                    <option value="general">General Inquiry</option>
                    <option value="other">Other</option>
                  </select>
                </div>

                {/* Message */}
                <div>
                  <label htmlFor="message" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Message *
                  </label>
                  <textarea
                    id="message"
                    name="message"
                    value={formData.message}
                    onChange={handleChange}
                    required
                    rows={6}
                    className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 focus:border-transparent transition-all resize-none"
                    placeholder="Describe your issue or question in detail..."
                  />
                </div>

                {/* Submit Button */}
                <div className="flex items-center gap-4">
                  <button
                    type="submit"
                    disabled={isSubmitting}
                    className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 disabled:from-gray-400 disabled:to-gray-500 text-white font-medium rounded-lg shadow-lg shadow-blue-500/30 hover:shadow-blue-600/40 dark:shadow-blue-500/20 dark:hover:shadow-blue-600/30 transition-all disabled:cursor-not-allowed"
                  >
                    {isSubmitting ? (
                      <>
                        <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                        Sending...
                      </>
                    ) : (
                      <>
                        <Send className="w-5 h-5" />
                        Send Message
                      </>
                    )}
                  </button>
                  <span className="text-sm text-gray-500 dark:text-gray-400">
                    * Required fields
                  </span>
                </div>
              </form>
            </div>

            {/* FAQ Section */}
            <div id="faq" className="mt-8 bg-gray-50 dark:bg-gray-900 rounded-xl shadow-sm border border-gray-200 dark:border-gray-800 p-8">
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
                Frequently Asked Questions
              </h2>
              
              <div className="space-y-6">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                    How do I upload an invoice?
                  </h3>
                  <p className="text-gray-600 dark:text-gray-400">
                    Navigate to the Upload page from the sidebar, drag and drop your invoice PDF or image, and our AI will automatically extract all the information.
                  </p>
                </div>

                <div>
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                    What file formats are supported?
                  </h3>
                  <p className="text-gray-600 dark:text-gray-400">
                    We support PDF, JPEG, JPG, and PNG formats. Files should be clear and readable for best results.
                  </p>
                </div>

                <div>
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                    How accurate is the AI extraction?
                  </h3>
                  <p className="text-gray-600 dark:text-gray-400">
                    Our AI achieves 95%+ accuracy on standard invoices. You can always review and edit the extracted data before saving.
                  </p>
                </div>

                <div>
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                    Is my data secure?
                  </h3>
                  <p className="text-gray-600 dark:text-gray-400">
                    Yes! All data is encrypted in transit and at rest. We use enterprise-grade security powered by Supabase.
                  </p>
                </div>

                <div>
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                    Can I export my invoices?
                  </h3>
                  <p className="text-gray-600 dark:text-gray-400">
                    Absolutely! You can export all your invoices to CSV format from the Invoices page.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  )
}

