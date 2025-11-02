# Dark Mode Batch Fix Guide for Blog Articles

## Files Needing Fixes
1. `/blog/how-to-extract-data-from-gst-invoices/page.tsx` (1516 lines)
2. `/blog/bulk-csv-export-for-accounting-software/page.tsx` 

## Common Pattern Replacements

### Background Classes
```
bg-white → bg-white dark:bg-gray-800
bg-gray-50 → bg-gray-50 dark:bg-gray-900
bg-gray-100 → bg-gray-100 dark:bg-gray-700
bg-blue-50 → bg-blue-50 dark:bg-blue-900/20
bg-blue-100 → bg-blue-100 dark:bg-blue-900/30
bg-green-50 → bg-green-50 dark:bg-green-900/20
bg-green-100 → bg-green-100 dark:bg-green-900/30
```

### Text Classes
```
text-gray-900 → text-gray-900 dark:text-white
text-gray-800 → text-gray-800 dark:text-gray-200
text-gray-700 → text-gray-700 dark:text-gray-300
text-gray-600 → text-gray-600 dark:text-gray-400
text-blue-800 → text-blue-800 dark:text-blue-300
text-green-800 → text-green-800 dark:text-green-300
```

### Border Classes
```
border-gray-200 → border-gray-200 dark:border-gray-700
border-gray-300 → border-gray-300 dark:border-gray-600
border-blue-200 → border-blue-200 dark:border-blue-700
```

##Strategy: Use Find & Replace in VS Code

1. Open file in VS Code
2. Press Ctrl+H (Find & Replace)
3. Apply each replacement pattern above
4. Validate no errors with TypeScript

OR: Since the files are too large, recommend user to:
- Open both blog files
- Use VS Code's Multi-cursor (Ctrl+D) to select and replace patterns
- Use Regex Find & Replace for efficiency

## Time Estimate
- Each file: 10 minutes with Find & Replace
- Total: 20 minutes for 2 blog articles
