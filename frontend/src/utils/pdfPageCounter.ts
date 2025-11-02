import { PDFDocument } from 'pdf-lib'

/**
 * Get the number of pages in a PDF file
 * @param file - The PDF file to analyze
 * @returns Promise<number> - Number of pages in the PDF
 * @throws Error if file is not a PDF or is corrupted
 */
export async function getPdfPageCount(file: File): Promise<number> {
  // Validate file type
  if (!file.type.includes('pdf') && !file.name.toLowerCase().endsWith('.pdf')) {
    throw new Error(`${file.name} is not a PDF file. Only PDF files are supported.`)
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
    if (error.message.includes('not a PDF')) {
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
