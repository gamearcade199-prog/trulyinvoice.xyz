import { PDFDocument } from 'pdf-lib'

/**
 * Get the number of pages in a file (PDF or image)
 * @param file - The file to analyze (PDF or image)
 * @returns Promise<number> - Number of pages (1 for images, actual count for PDFs)
 * @throws Error if file is not supported or is corrupted
 */
export async function getPdfPageCount(file: File): Promise<number> {
  // Check if it's an image file
  const imageTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp', 'image/heic', 'image/heif']
  const imageExtensions = ['.jpg', '.jpeg', '.png', '.webp', '.heic', '.heif']
  
  const isImage = imageTypes.includes(file.type) || 
                  imageExtensions.some(ext => file.name.toLowerCase().endsWith(ext))
  
  if (isImage) {
    // Images are always 1 page
    return 1
  }
  
  // Check if it's a PDF
  const isPdf = file.type.includes('pdf') || file.name.toLowerCase().endsWith('.pdf')
  
  if (!isPdf) {
    throw new Error(`${file.name} is not a supported file type. Supported: PDF, JPG, PNG, WebP, HEIC`)
  }
  
  try {
    const arrayBuffer = await file.arrayBuffer()
    const pdfDoc = await PDFDocument.load(arrayBuffer)
    const pageCount = pdfDoc.getPageCount()
    
    // Sanity check for page count
    if (pageCount <= 0 || pageCount > 10000) {
      throw new Error(`Invalid page count (${pageCount}) in ${file.name}. File may be corrupted.`)
    }
    
    return pageCount
  } catch (error: any) {
    console.error('Error counting PDF pages:', error)
    
    // Provide specific error message
    if (error.message.includes('not a supported file')) {
      throw error
    } else if (error.message.includes('Invalid page count')) {
      throw error
    } else {
      throw new Error(`Failed to read ${file.name}. File may be corrupted or password-protected.`)
    }
  }
}

/**
 * Get page counts for multiple files
 * @param files - Array of files to analyze
 * @returns Promise<{file: File, pageCount: number, fileName: string}[]>
 * @throws Error if any file is invalid
 */
export async function getMultipleFilePageCounts(
  files: File[]
): Promise<{ file: File; pageCount: number; fileName: string }[]> {
  const results = await Promise.all(
    files.map(async (file) => {
      const pageCount = await getPdfPageCount(file)
      return {
        file,
        fileName: file.name,
        pageCount,
      }
    })
  )
  return results
}

/**
 * Calculate total pages across all files
 * @param files - Array of files
 * @returns Promise<number> - Total page count
 */
export async function getTotalPageCount(files: File[]): Promise<number> {
  const pageCounts = await Promise.all(files.map(getPdfPageCount))
  return pageCounts.reduce((sum, count) => sum + count, 0)
}
