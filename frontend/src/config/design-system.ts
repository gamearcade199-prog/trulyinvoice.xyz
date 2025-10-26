// =====================================================
// 🎨 DESIGN SYSTEM - Colors, Spacing, Typography
// =====================================================
// Add to: frontend/src/config/design-system.ts

export const designSystem = {
  // =====================================================
  // COLORS
  // =====================================================
  colors: {
    // Primary (Blue) - Main brand color
    primary: {
      50: '#EFF6FF',
      100: '#DBEAFE',
      200: '#BFDBFE',
      300: '#93C5FD',
      400: '#60A5FA',
      500: '#3B82F6',  // Main primary
      600: '#2563EB',
      700: '#1D4ED8',
      800: '#1E40AF',
      900: '#1E3A8A',
    },

    // Success (Green)
    success: {
      50: '#F0FDF4',
      100: '#DCFCE7',
      200: '#BBF7D0',
      300: '#86EFAC',
      400: '#4ADE80',
      500: '#22C55E',  // Main success
      600: '#16A34A',
      700: '#15803D',
      800: '#166534',
      900: '#14532D',
    },

    // Warning (Yellow)
    warning: {
      50: '#FFFBEB',
      100: '#FEF3C7',
      200: '#FDE68A',
      300: '#FCD34D',
      400: '#FBBF24',
      500: '#F59E0B',  // Main warning
      600: '#D97706',
      700: '#B45309',
      800: '#92400E',
      900: '#78350F',
    },

    // Error (Red)
    error: {
      50: '#FEF2F2',
      100: '#FEE2E2',
      200: '#FECACA',
      300: '#FCA5A5',
      400: '#F87171',
      500: '#EF4444',  // Main error
      600: '#DC2626',
      700: '#B91C1C',
      800: '#991B1B',
      900: '#7F1D1D',
    },

    // Gray (Neutral)
    gray: {
      50: '#F9FAFB',
      100: '#F3F4F6',
      200: '#E5E7EB',
      300: '#D1D5DB',
      400: '#9CA3AF',
      500: '#6B7280',
      600: '#4B5563',  // Main gray
      700: '#374151',
      800: '#1F2937',
      900: '#111827',
    },
  },

  // =====================================================
  // SPACING (based on 4px grid)
  // =====================================================
  spacing: {
    0: '0',
    1: '0.25rem',   // 4px
    2: '0.5rem',    // 8px
    3: '0.75rem',   // 12px
    4: '1rem',      // 16px
    5: '1.25rem',   // 20px
    6: '1.5rem',    // 24px
    8: '2rem',      // 32px
    10: '2.5rem',   // 40px
    12: '3rem',     // 48px
    16: '4rem',     // 64px
    20: '5rem',     // 80px
    24: '6rem',     // 96px
  },

  // =====================================================
  // TYPOGRAPHY
  // =====================================================
  typography: {
    // Font families
    fontFamily: {
      sans: ['Inter', 'system-ui', 'sans-serif'],
      mono: ['JetBrains Mono', 'Courier New', 'monospace'],
    },

    // Font sizes (with line heights)
    fontSize: {
      xs: { size: '0.75rem', lineHeight: '1rem' },      // 12px/16px
      sm: { size: '0.875rem', lineHeight: '1.25rem' },  // 14px/20px
      base: { size: '1rem', lineHeight: '1.5rem' },     // 16px/24px
      lg: { size: '1.125rem', lineHeight: '1.75rem' },  // 18px/28px
      xl: { size: '1.25rem', lineHeight: '1.75rem' },   // 20px/28px
      '2xl': { size: '1.5rem', lineHeight: '2rem' },    // 24px/32px
      '3xl': { size: '1.875rem', lineHeight: '2.25rem' }, // 30px/36px
      '4xl': { size: '2.25rem', lineHeight: '2.5rem' }, // 36px/40px
      '5xl': { size: '3rem', lineHeight: '1' },         // 48px
    },

    // Font weights
    fontWeight: {
      normal: 400,
      medium: 500,
      semibold: 600,
      bold: 700,
    },
  },

  // =====================================================
  // BORDER RADIUS
  // =====================================================
  borderRadius: {
    none: '0',
    sm: '0.125rem',   // 2px
    md: '0.375rem',   // 6px
    lg: '0.5rem',     // 8px
    xl: '0.75rem',    // 12px
    '2xl': '1rem',    // 16px
    full: '9999px',
  },

  // =====================================================
  // SHADOWS
  // =====================================================
  shadows: {
    sm: '0 1px 2px 0 rgb(0 0 0 / 0.05)',
    md: '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)',
    lg: '0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)',
    xl: '0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)',
    '2xl': '0 25px 50px -12px rgb(0 0 0 / 0.25)',
  },

  // =====================================================
  // TRANSITIONS
  // =====================================================
  transitions: {
    fast: '150ms cubic-bezier(0.4, 0, 0.2, 1)',
    base: '200ms cubic-bezier(0.4, 0, 0.2, 1)',
    slow: '300ms cubic-bezier(0.4, 0, 0.2, 1)',
  },

  // =====================================================
  // BREAKPOINTS
  // =====================================================
  breakpoints: {
    sm: '640px',
    md: '768px',
    lg: '1024px',
    xl: '1280px',
    '2xl': '1536px',
  },

  // =====================================================
  // Z-INDEX
  // =====================================================
  zIndex: {
    dropdown: 1000,
    sticky: 1020,
    fixed: 1030,
    modalBackdrop: 1040,
    modal: 1050,
    popover: 1060,
    tooltip: 1070,
  },

  // =====================================================
  // COMPONENT PRESETS
  // =====================================================
  components: {
    // Button sizes
    button: {
      sm: {
        padding: '0.5rem 1rem',      // 8px 16px
        fontSize: '0.875rem',        // 14px
        minHeight: '2rem',           // 32px
      },
      md: {
        padding: '0.625rem 1.25rem', // 10px 20px
        fontSize: '1rem',            // 16px
        minHeight: '2.5rem',         // 40px
      },
      lg: {
        padding: '0.75rem 1.5rem',   // 12px 24px
        fontSize: '1.125rem',        // 18px
        minHeight: '3rem',           // 48px
      },
    },

    // Input sizes
    input: {
      sm: {
        padding: '0.5rem 0.75rem',
        fontSize: '0.875rem',
        height: '2rem',
      },
      md: {
        padding: '0.625rem 1rem',
        fontSize: '1rem',
        height: '2.5rem',
      },
      lg: {
        padding: '0.75rem 1.25rem',
        fontSize: '1.125rem',
        height: '3rem',
      },
    },

    // Card styles
    card: {
      padding: '1.5rem',           // 24px
      borderRadius: '0.5rem',      // 8px
      shadow: '0 1px 3px 0 rgb(0 0 0 / 0.1)',
    },
  },
}

// =====================================================
// UTILITY FUNCTIONS
// =====================================================

export function getColor(colorPath: string): string {
  const parts = colorPath.split('.')
  let value: any = designSystem.colors
  
  for (const part of parts) {
    value = value[part]
    if (value === undefined) return ''
  }
  
  return value
}

export function getSpacing(key: string | number): string {
  return designSystem.spacing[key as keyof typeof designSystem.spacing] || '0'
}

// =====================================================
// EXPORT FOR TAILWIND CONFIG
// =====================================================

export const tailwindTheme = {
  colors: designSystem.colors,
  spacing: designSystem.spacing,
  borderRadius: designSystem.borderRadius,
  boxShadow: designSystem.shadows,
  fontFamily: designSystem.typography.fontFamily,
  fontSize: designSystem.typography.fontSize,
  fontWeight: designSystem.typography.fontWeight,
  screens: designSystem.breakpoints,
  transitionDuration: {
    fast: '150ms',
    DEFAULT: '200ms',
    slow: '300ms',
  },
}
