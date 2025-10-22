import { createClient } from '@supabase/supabase-js'

// Handle missing environment variables during build time
const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || 'https://placeholder.supabase.co'
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || 'placeholder-anon-key'

// Session timeout configuration (in minutes)
export const SESSION_TIMEOUT_MINUTES = 30
export const SESSION_WARNING_MINUTES = 25
export const INACTIVITY_CHECK_INTERVAL_MS = 60000 // Check every minute

// Session activity tracking
let lastActivityTime = Date.now()
let sessionTimeoutTimer: NodeJS.Timeout | null = null
let inactivityCheckInterval: NodeJS.Timeout | null = null
let onSessionTimeoutCallback: (() => void) | null = null

/**
 * Reset the activity timer when user interacts
 * Called on: mouse move, key press, click, scroll, touch
 */
export function resetActivityTimer() {
  lastActivityTime = Date.now()
  
  // Clear existing timeout
  if (sessionTimeoutTimer) {
    clearTimeout(sessionTimeoutTimer)
  }
  
  // Set new timeout for session expiry
  const timeoutMs = SESSION_TIMEOUT_MINUTES * 60 * 1000
  sessionTimeoutTimer = setTimeout(() => {
    handleSessionTimeout()
  }, timeoutMs)
}

/**
 * Get time remaining in current session (in seconds)
 */
export function getSessionTimeRemaining(): number {
  const now = Date.now()
  const timeoutMs = SESSION_TIMEOUT_MINUTES * 60 * 1000
  const elapsed = now - lastActivityTime
  const remaining = Math.max(0, timeoutMs - elapsed)
  return Math.floor(remaining / 1000)
}

/**
 * Check if session is about to timeout (within warning window)
 */
export function isSessionAboutToTimeout(): boolean {
  const remaining = getSessionTimeRemaining()
  const warningSeconds = SESSION_WARNING_MINUTES * 60
  return remaining < warningSeconds && remaining > 0
}

/**
 * Check if session has already expired
 */
export function isSessionExpired(): boolean {
  return getSessionTimeRemaining() <= 0
}

/**
 * Handle session timeout - logout user
 */
async function handleSessionTimeout() {
  console.warn('🔒 Session timeout - logging out user')
  
  // Clear timers
  if (sessionTimeoutTimer) {
    clearTimeout(sessionTimeoutTimer)
    sessionTimeoutTimer = null
  }
  
  if (inactivityCheckInterval) {
    clearInterval(inactivityCheckInterval)
    inactivityCheckInterval = null
  }
  
  // Sign out
  try {
    await supabase.auth.signOut()
  } catch (error) {
    console.error('Error signing out:', error)
  }
  
  // Call callback if set
  if (onSessionTimeoutCallback) {
    onSessionTimeoutCallback()
  }
}

/**
 * Set callback to be called when session times out
 */
export function onSessionTimeout(callback: () => void) {
  onSessionTimeoutCallback = callback
}

/**
 * Start monitoring session activity
 * Should be called when user logs in
 */
export function startSessionMonitoring() {
  console.log('✅ Session monitoring started')
  
  // Reset timer immediately
  resetActivityTimer()
  
  // Start periodic check for inactivity
  inactivityCheckInterval = setInterval(() => {
    if (isSessionExpired()) {
      handleSessionTimeout()
    }
  }, INACTIVITY_CHECK_INTERVAL_MS)
  
  // Add activity listeners
  addActivityListeners()
}

/**
 * Stop monitoring session activity
 * Should be called when user logs out
 */
export function stopSessionMonitoring() {
  console.log('✅ Session monitoring stopped')
  
  if (sessionTimeoutTimer) {
    clearTimeout(sessionTimeoutTimer)
    sessionTimeoutTimer = null
  }
  
  if (inactivityCheckInterval) {
    clearInterval(inactivityCheckInterval)
    inactivityCheckInterval = null
  }
  
  removeActivityListeners()
}

/**
 * Add event listeners for user activity
 */
function addActivityListeners() {
  if (typeof window === 'undefined') return
  
  const events = ['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart', 'click']
  
  events.forEach(event => {
    window.addEventListener(event, resetActivityTimer, { passive: true })
  })
}

/**
 * Remove event listeners for user activity
 */
function removeActivityListeners() {
  if (typeof window === 'undefined') return
  
  const events = ['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart', 'click']
  
  events.forEach(event => {
    window.removeEventListener(event, resetActivityTimer)
  })
}

export const supabase = createClient(supabaseUrl, supabaseAnonKey, {
  auth: {
    persistSession: true
  },
  global: {
    headers: {
      'X-Client-Info': 'trulyinvoice-web',
    },
  },
})
