// Google Analytics and Tracking Setup for TrulyInvoice
// This file configures comprehensive analytics tracking for invoice-to-excel conversion

export const trackingConfig = {
  // Google Analytics 4 - Production ID
  googleAnalyticsId: 'G-WDF15FK02Z',

  // Google Tag Manager (optional)
  gtmId: 'GTM-XXXXXXX', // Replace with your GTM container ID

  // Microsoft Clarity (optional) - For user behavior analysis
  clarityId: 'YOUR_CLARITY_ID',

  // Facebook Pixel (optional) - For retargeting
  facebookPixelId: 'YOUR_PIXEL_ID',

  // LinkedIn Insight Tag (optional) - For B2B targeting
  linkedInPartnerId: 'YOUR_PARTNER_ID',

  // Hotjar (optional) - For user feedback and heatmaps
  hotjarId: 'YOUR_HOTJAR_ID',
}

// Event tracking configuration
export const events = {
  // Page views
  pageView: (url: string) => ({
    event: 'page_view',
    page_location: url,
    page_title: document.title,
  }),
  
  // User registration
  signUp: (method: string) => ({
    event: 'sign_up',
    method: method, // 'email', 'google', etc.
  }),
  
  // Login
  login: (method: string) => ({
    event: 'login',
    method: method,
  }),
  
  // Invoice upload
  invoiceUpload: () => ({
    event: 'invoice_upload',
    category: 'engagement',
    label: 'Invoice Upload',
  }),
  
  // Invoice export
  invoiceExport: (format: string) => ({
    event: 'invoice_export',
    export_format: format, // 'excel', 'csv', 'pdf'
  }),
  
  // Pricing page view
  viewPricing: () => ({
    event: 'view_pricing',
    category: 'engagement',
  }),
  
  // Plan upgrade click
  upgradeClick: (plan: string) => ({
    event: 'upgrade_click',
    plan_name: plan, // 'basic', 'pro', 'ultra'
    value: getPlanValue(plan),
    currency: 'INR',
  }),
  
  // Purchase
  purchase: (plan: string, value: number) => ({
    event: 'purchase',
    transaction_id: Date.now().toString(),
    value: value,
    currency: 'INR',
    items: [{
      item_id: plan,
      item_name: `${plan} Plan`,
      price: value,
      quantity: 1,
    }],
  }),
  
  // Search
  search: (searchTerm: string) => ({
    event: 'search',
    search_term: searchTerm,
  }),
  
  // Contact form submission
  contactSubmit: () => ({
    event: 'contact_submit',
    category: 'engagement',
  }),
  
  // Blog post view
  blogView: (title: string) => ({
    event: 'blog_view',
    blog_title: title,
  }),
  
  // Download
  download: (fileName: string) => ({
    event: 'download',
    file_name: fileName,
  }),
  
  // Video play
  videoPlay: (videoTitle: string) => ({
    event: 'video_play',
    video_title: videoTitle,
  }),
  
  // Share
  share: (method: string, contentType: string) => ({
    event: 'share',
    method: method, // 'facebook', 'twitter', 'whatsapp', 'linkedin'
    content_type: contentType,
  }),
  
  // Feature interaction
  featureInteraction: (featureName: string) => ({
    event: 'feature_interaction',
    feature_name: featureName,
  }),
}

// Helper function
function getPlanValue(plan: string): number {
  const values: { [key: string]: number } = {
    'free': 0,
    'basic': 149,
    'pro': 299,
    'ultra': 599,
    'max': 999,
  }
  return values[plan.toLowerCase()] || 0
}

// Enhanced E-commerce tracking
export const ecommerce = {
  // View item list (pricing page)
  viewItemList: (items: any[]) => ({
    event: 'view_item_list',
    ecommerce: {
      items: items.map((item, index) => ({
        item_id: item.id,
        item_name: item.name,
        price: item.price,
        item_category: 'Subscription',
        item_list_name: 'Pricing Plans',
        index: index,
      })),
    },
  }),
  
  // Select item (plan)
  selectItem: (item: any) => ({
    event: 'select_item',
    ecommerce: {
      items: [{
        item_id: item.id,
        item_name: item.name,
        price: item.price,
        item_category: 'Subscription',
      }],
    },
  }),
  
  // Begin checkout
  beginCheckout: (item: any) => ({
    event: 'begin_checkout',
    ecommerce: {
      items: [{
        item_id: item.id,
        item_name: item.name,
        price: item.price,
        quantity: 1,
      }],
      value: item.price,
      currency: 'INR',
    },
  }),
  
  // Add payment info
  addPaymentInfo: (paymentMethod: string) => ({
    event: 'add_payment_info',
    ecommerce: {
      payment_type: paymentMethod, // 'UPI', 'Card', 'Net Banking'
    },
  }),
}

// User properties for segmentation
export const userProperties = {
  setPlan: (plan: string) => ({
    user_properties: {
      plan_tier: plan,
    },
  }),
  
  setIndustry: (industry: string) => ({
    user_properties: {
      industry: industry,
    },
  }),
  
  setCity: (city: string) => ({
    user_properties: {
      city: city,
    },
  }),
  
  setCompanySize: (size: string) => ({
    user_properties: {
      company_size: size, // 'solo', 'small', 'medium', 'large'
    },
  }),
}

export default trackingConfig
