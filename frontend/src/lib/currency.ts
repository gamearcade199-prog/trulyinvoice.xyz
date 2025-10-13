// Currency utility functions

export interface CurrencyConfig {
  symbol: string
  code: string
  name: string
}

export const CURRENCIES: Record<string, CurrencyConfig> = {
  INR: { symbol: '₹', code: 'INR', name: 'Indian Rupee' },
  USD: { symbol: '$', code: 'USD', name: 'US Dollar' },
  EUR: { symbol: '€', code: 'EUR', name: 'Euro' },
  GBP: { symbol: '£', code: 'GBP', name: 'British Pound' },
  JPY: { symbol: '¥', code: 'JPY', name: 'Japanese Yen' },
  AUD: { symbol: 'A$', code: 'AUD', name: 'Australian Dollar' },
  CAD: { symbol: 'C$', code: 'CAD', name: 'Canadian Dollar' },
  SGD: { symbol: 'S$', code: 'SGD', name: 'Singapore Dollar' },
  AED: { symbol: 'د.إ', code: 'AED', name: 'UAE Dirham' },
}

/**
 * Get currency symbol from currency code
 */
export function getCurrencySymbol(currencyCode?: string): string {
  if (!currencyCode) return '₹' // Default to INR
  const currency = CURRENCIES[currencyCode.toUpperCase()]
  return currency ? currency.symbol : currencyCode
}

/**
 * Format amount with currency symbol
 */
export function formatCurrency(amount: number, currencyCode?: string): string {
  const symbol = getCurrencySymbol(currencyCode)
  const formattedAmount = amount.toLocaleString('en-IN', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })
  
  // For symbols like $, €, £ - place before amount
  // For ₹ and other symbols - place before amount (common practice)
  return `${symbol}${formattedAmount}`
}

/**
 * Get currency configuration
 */
export function getCurrency(currencyCode?: string): CurrencyConfig {
  if (!currencyCode) return CURRENCIES.INR
  return CURRENCIES[currencyCode.toUpperCase()] || CURRENCIES.INR
}
