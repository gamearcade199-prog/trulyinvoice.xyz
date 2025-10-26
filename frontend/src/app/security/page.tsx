'use client'

import Link from 'next/link'
import { 
  ArrowLeft, 
  FileText, 
  Shield, 
  Lock, 
  Eye, 
  Server,
  CheckCircle2,
  AlertTriangle,
  Users,
  Database,
  Zap,
  Award
} from 'lucide-react'

export default function SecurityPage() {
  const securityFeatures = [
    {
      icon: Lock,
      title: 'End-to-End Encryption',
      description: 'All data is encrypted in transit and at rest using industry-standard AES-256 encryption.',
      details: ['TLS 1.3 for data transmission', 'AES-256 encryption at rest', 'Zero-knowledge architecture']
    },
    {
      icon: Server,
      title: 'Secure Infrastructure',
      description: 'Hosted on enterprise-grade cloud infrastructure with multiple layers of security.',
      details: ['SOC 2 Type II certified data centers', 'Regular security audits', '99.9% uptime guarantee']
    },
    {
      icon: Eye,
      title: 'Privacy by Design',
      description: 'We collect only necessary data and never share it with third parties.',
      details: ['Minimal data collection', 'No data selling or sharing', 'GDPR and CCPA compliant']
    },
    {
      icon: Users,
      title: 'Access Control',
      description: 'Granular permissions and role-based access control for team members.',
      details: ['Multi-factor authentication', 'Role-based permissions', 'Session management']
    },
    {
      icon: Database,
      title: 'Data Backup & Recovery',
      description: 'Automated backups and disaster recovery procedures to protect your data.',
      details: ['Daily automated backups', 'Point-in-time recovery', 'Geographic redundancy']
    },
    {
      icon: Zap,
      title: 'Real-time Monitoring',
      description: '24/7 security monitoring and threat detection systems.',
      details: ['Intrusion detection systems', 'Automated threat response', 'Security incident logging']
    }
  ]

  const certifications = [
    {
      icon: Award,
      title: 'SOC 2 Type II',
      description: 'Certified for security, availability, and confidentiality'
    },
    {
      icon: Shield,
      title: 'ISO 27001',
      description: 'International standard for information security management'
    },
    {
      icon: Lock,
      title: 'GDPR Compliant',
      description: 'Full compliance with European data protection regulations'
    }
  ]

  return (
    <main className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors">
      {/* Navigation */}
      <nav className="bg-gray-50 dark:bg-gray-900 border-b border-gray-200 dark:border-gray-800 sticky top-0 z-50">
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-between h-16">
            <Link href="/" className="flex items-center gap-2">
              <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg flex items-center justify-center">
                <FileText className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold text-gray-900 dark:text-white">TrulyInvoice</span>
            </Link>
            <Link 
              href="/" 
              className="flex items-center gap-2 text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
            >
              <ArrowLeft className="w-4 h-4" />
              Back to Home
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="bg-gradient-to-br from-blue-50 to-purple-50 dark:from-gray-800 dark:to-gray-900 py-16">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center">
            <div className="w-16 h-16 bg-blue-100 dark:bg-blue-900/50 rounded-full flex items-center justify-center mx-auto mb-6">
              <Shield className="w-8 h-8 text-blue-600 dark:text-blue-400" />
            </div>
            <h1 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-4">
              Security & Privacy
            </h1>
            <p className="text-xl text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
              Your data security is our top priority. Learn how we protect your sensitive business information.
            </p>
          </div>
        </div>
      </section>

      {/* Trust Banner */}
      <section className="bg-green-50 dark:bg-green-900/20 border-y border-green-200 dark:border-green-800 py-8">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto">
            <div className="flex items-center justify-center gap-3 text-green-800 dark:text-green-200">
              <CheckCircle2 className="w-6 h-6" />
              <p className="font-semibold text-lg">
                Bank-level security trusted by 10,000+ businesses across India
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Security Features */}
      <section className="py-16">
        <div className="container mx-auto px-4">
          <div className="max-w-6xl mx-auto">
            <div className="text-center mb-12">
              <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">
                Enterprise-Grade Security
              </h2>
              <p className="text-lg text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
                Multiple layers of security protect your data at every step of the process
              </p>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
              {securityFeatures.map((feature, index) => {
                const Icon = feature.icon
                return (
                  <div 
                    key={index}
                    className="bg-gray-50 dark:bg-gray-900 rounded-xl p-6 border border-gray-200 dark:border-gray-800 hover:shadow-lg transition-all"
                  >
                    <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/50 rounded-lg flex items-center justify-center mb-4">
                      <Icon className="w-6 h-6 text-blue-600 dark:text-blue-400" />
                    </div>
                    
                    <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3">
                      {feature.title}
                    </h3>
                    
                    <p className="text-gray-600 dark:text-gray-400 mb-4">
                      {feature.description}
                    </p>
                    
                    <ul className="space-y-2">
                      {feature.details.map((detail, detailIndex) => (
                        <li key={detailIndex} className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400">
                          <CheckCircle2 className="w-4 h-4 text-green-500 flex-shrink-0" />
                          <span>{detail}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )
              })}
            </div>
          </div>
        </div>
      </section>

      {/* Certifications */}
      <section className="bg-gray-50 dark:bg-gray-900 py-16">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto">
            <div className="text-center mb-12">
              <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
                Security Certifications
              </h2>
              <p className="text-gray-600 dark:text-gray-400">
                Independently verified security standards and compliance
              </p>
            </div>

            <div className="grid md:grid-cols-3 gap-8">
              {certifications.map((cert, index) => {
                const Icon = cert.icon
                return (
                  <div key={index} className="text-center">
                    <div className="w-16 h-16 bg-blue-100 dark:bg-blue-900/50 rounded-full flex items-center justify-center mx-auto mb-4">
                      <Icon className="w-8 h-8 text-blue-600 dark:text-blue-400" />
                    </div>
                    <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-2">
                      {cert.title}
                    </h3>
                    <p className="text-gray-600 dark:text-gray-400 text-sm">
                      {cert.description}
                    </p>
                  </div>
                )
              })}
            </div>
          </div>
        </div>
      </section>

      {/* Security Practices */}
      <section className="py-16">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-8 text-center">
              Our Security Practices
            </h2>
            
            <div className="grid md:grid-cols-2 gap-8">
              <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-xl p-6">
                <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4">Data Protection</h3>
                <ul className="space-y-3 text-gray-700 dark:text-gray-300">
                  <li className="flex items-start gap-3">
                    <CheckCircle2 className="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" />
                    <span>All data encrypted with 256-bit SSL encryption</span>
                  </li>
                  <li className="flex items-start gap-3">
                    <CheckCircle2 className="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" />
                    <span>Regular automated backups with point-in-time recovery</span>
                  </li>
                  <li className="flex items-start gap-3">
                    <CheckCircle2 className="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" />
                    <span>Data residency compliance for Indian businesses</span>
                  </li>
                </ul>
              </div>
              
              <div className="bg-purple-50 dark:bg-purple-900/20 border border-purple-200 dark:border-purple-800 rounded-xl p-6">
                <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4">Access Security</h3>
                <ul className="space-y-3 text-gray-700 dark:text-gray-300">
                  <li className="flex items-start gap-3">
                    <CheckCircle2 className="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" />
                    <span>Multi-factor authentication (MFA) required</span>
                  </li>
                  <li className="flex items-start gap-3">
                    <CheckCircle2 className="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" />
                    <span>Role-based access control for team members</span>
                  </li>
                  <li className="flex items-start gap-3">
                    <CheckCircle2 className="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" />
                    <span>Automatic session timeout and secure logout</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Incident Response */}
      <section className="bg-orange-50 dark:bg-orange-900/20 py-12">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto">
            <div className="flex items-start gap-4">
              <AlertTriangle className="w-8 h-8 text-orange-600 dark:text-orange-400 flex-shrink-0 mt-1" />
              <div>
                <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">
                  Security Incident Response
                </h3>
                <p className="text-gray-700 dark:text-gray-300 mb-4">
                  In the unlikely event of a security incident, we have a comprehensive response plan:
                </p>
                <ul className="space-y-2 text-gray-600 dark:text-gray-400">
                  <li>• Immediate containment and assessment within 1 hour</li>
                  <li>• User notification within 24 hours if personal data is affected</li>
                  <li>• Full investigation and remediation report within 72 hours</li>
                  <li>• Coordination with relevant authorities and compliance bodies</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-gradient-to-r from-blue-600 to-purple-600 dark:from-blue-500 dark:to-purple-500 py-16">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center">
            <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
              Questions About Security?
            </h2>
            <p className="text-xl text-blue-100 dark:text-blue-200 mb-8">
              Our security team is here to help. Contact us for detailed security documentation.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                href="/contact"
                className="bg-white text-blue-600 hover:bg-gray-100 px-8 py-3 rounded-xl font-bold transition-all shadow-lg hover:shadow-xl hover:scale-105"
              >
                Contact Security Team
              </Link>
              <Link
                href="/register"
                className="bg-transparent border-2 border-white text-white hover:bg-white hover:text-blue-600 px-8 py-3 rounded-xl font-bold transition-all"
              >
                Start Free
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 dark:bg-gray-950 text-gray-400 py-8">
        <div className="container mx-auto px-4">
          <div className="text-center">
            <div className="flex items-center justify-center gap-2 mb-4">
              <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg flex items-center justify-center">
                <FileText className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold text-white">TrulyInvoice</span>
            </div>
            <p className="text-sm">
              © 2025 TrulyInvoice. All rights reserved. • <Link href="/privacy" className="hover:text-white">Privacy Policy</Link>
            </p>
          </div>
        </div>
      </footer>
    </main>
  )
}
