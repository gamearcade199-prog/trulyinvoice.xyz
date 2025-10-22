/**
 * Environment variable validation utility
 * Fails fast if required variables are missing
 */

export class EnvError extends Error {
  constructor(variable: string) {
    super(`Missing required environment variable: ${variable}`);
    this.name = 'EnvError';
  }
}

/**
 * Get required environment variable
 * Throws error if not found
 */
export function getRequiredEnv(key: string): string {
  const value = process.env[key];
  if (!value || value === '') {
    throw new EnvError(key);
  }
  return value;
}

/**
 * Get optional environment variable with default
 */
export function getOptionalEnv(key: string, defaultValue: string): string {
  return process.env[key] || defaultValue;
}

/**
 * Validate all required environment variables on app start
 */
export function validateEnvironment() {
  const required = [
    'NEXT_PUBLIC_SUPABASE_URL',
    'NEXT_PUBLIC_SUPABASE_ANON_KEY',
  ];

  const missing: string[] = [];

  for (const key of required) {
    if (!process.env[key]) {
      missing.push(key);
    }
  }

  if (missing.length > 0) {
    throw new Error(
      `Missing required environment variables:\n${missing.map(k => `  - ${k}`).join('\n')}`
    );
  }

  return true;
}

/**
 * Get validated environment variables
 */
export const env = {
  supabase: {
    url: getRequiredEnv('NEXT_PUBLIC_SUPABASE_URL'),
    anonKey: getRequiredEnv('NEXT_PUBLIC_SUPABASE_ANON_KEY'),
  },
  api: {
    url: getOptionalEnv('NEXT_PUBLIC_API_URL', 'http://localhost:8000'),
  },
  razorpay: {
    keyId: getOptionalEnv('NEXT_PUBLIC_RAZORPAY_KEY_ID', ''),
  },
  isDevelopment: process.env.NODE_ENV === 'development',
  isProduction: process.env.NODE_ENV === 'production',
} as const;
