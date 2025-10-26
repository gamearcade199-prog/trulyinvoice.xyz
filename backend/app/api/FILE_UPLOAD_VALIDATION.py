"""
🔒 FILE UPLOAD VALIDATION & SECURITY
====================================
Add to backend/app/api/documents.py
"""

from fastapi import HTTPException, UploadFile
import os
import magic  # pip install python-magic-bin (Windows) or python-magic (Linux/Mac)
from typing import Optional
import hashlib

# =====================================================
# CONSTANTS
# =====================================================

# File upload limits
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
MAX_FILES_PER_USER_PER_DAY = 100
MAX_ANONYMOUS_UPLOADS_PER_IP_PER_HOUR = 5

# Allowed file types with magic numbers (prevents renamed .exe files)
ALLOWED_MIME_TYPES = {
    'application/pdf': {
        'extensions': ['.pdf'],
        'magic_bytes': b'%PDF',  # PDF files start with this
        'description': 'PDF Document'
    },
    'image/jpeg': {
        'extensions': ['.jpg', '.jpeg'],
        'magic_bytes': b'\xff\xd8\xff',  # JPEG magic number
        'description': 'JPEG Image'
    },
    'image/png': {
        'extensions': ['.png'],
        'magic_bytes': b'\x89PNG',  # PNG magic number
        'description': 'PNG Image'
    }
}

# Malicious file patterns to reject
MALICIOUS_PATTERNS = [
    b'<script',  # JavaScript
    b'<?php',    # PHP code
    b'<iframe',  # Embedded content
    b'eval(',    # Code execution
    b'exec(',    # Code execution
]

# =====================================================
# VALIDATION FUNCTIONS
# =====================================================

def validate_file_size(file: UploadFile) -> None:
    """Validate file size is within limits"""
    if file.size and file.size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size: {MAX_FILE_SIZE / 1024 / 1024:.0f}MB. Your file: {file.size / 1024 / 1024:.1f}MB"
        )


def validate_file_type(file: UploadFile) -> str:
    """
    Validate file type by content (magic bytes), not just extension
    Returns: validated MIME type
    """
    # Check declared content type
    if file.content_type not in ALLOWED_MIME_TYPES:
        allowed_types = ', '.join([v['description'] for v in ALLOWED_MIME_TYPES.values()])
        raise HTTPException(
            status_code=415,
            detail=f"Invalid file type '{file.content_type}'. Allowed: {allowed_types}"
        )
    
    # Check file extension matches content type
    file_ext = os.path.splitext(file.filename)[1].lower()
    allowed_extensions = ALLOWED_MIME_TYPES[file.content_type]['extensions']
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=415,
            detail=f"File extension '{file_ext}' doesn't match content type '{file.content_type}'"
        )
    
    return file.content_type


async def validate_file_content(file: UploadFile, content_type: str) -> None:
    """
    Validate file content by checking magic bytes
    Prevents renamed malicious files (e.g., virus.exe renamed to invoice.pdf)
    """
    # Read first 512 bytes to check magic number
    file_header = await file.read(512)
    await file.seek(0)  # Reset file pointer
    
    # Check magic bytes match expected type
    expected_magic = ALLOWED_MIME_TYPES[content_type]['magic_bytes']
    if not file_header.startswith(expected_magic):
        raise HTTPException(
            status_code=415,
            detail=f"File content doesn't match declared type. File may be corrupted or renamed."
        )
    
    # Check for malicious patterns
    for pattern in MALICIOUS_PATTERNS:
        if pattern in file_header:
            raise HTTPException(
                status_code=400,
                detail="Malicious content detected in file. Upload rejected for security."
            )


def validate_filename(filename: str) -> str:
    """
    Sanitize filename to prevent directory traversal attacks
    """
    # Remove any path components
    filename = os.path.basename(filename)
    
    # Remove dangerous characters
    dangerous_chars = ['..', '/', '\\', '<', '>', ':', '"', '|', '?', '*']
    for char in dangerous_chars:
        filename = filename.replace(char, '_')
    
    # Limit filename length
    if len(filename) > 255:
        name, ext = os.path.splitext(filename)
        filename = name[:250] + ext
    
    # Ensure filename is not empty
    if not filename or filename == '.':
        filename = f"unnamed_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    return filename


async def check_rate_limit_anonymous(ip_address: str) -> None:
    """
    Check rate limit for anonymous uploads
    Uses Supabase function created in RLS policies
    """
    try:
        # Call Supabase function to check rate limit
        result = supabase.rpc('check_anonymous_rate_limit', {'ip_addr': ip_address}).execute()
        
        if not result.data:
            raise HTTPException(
                status_code=429,
                detail=f"Rate limit exceeded. Maximum {MAX_ANONYMOUS_UPLOADS_PER_IP_PER_HOUR} uploads per hour for anonymous users. Please sign up for unlimited uploads."
            )
    except Exception as e:
        # Log but don't block if rate limiting fails
        print(f"⚠️ Rate limit check failed: {e}")


async def check_rate_limit_authenticated(user_id: str) -> None:
    """
    Check rate limit for authenticated users
    """
    # Count uploads today
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    result = supabase.table('documents').select('id', count='exact').eq('user_id', user_id).gte('created_at', today_start.isoformat()).execute()
    
    upload_count = result.count or 0
    
    if upload_count >= MAX_FILES_PER_USER_PER_DAY:
        raise HTTPException(
            status_code=429,
            detail=f"Daily upload limit reached. Maximum {MAX_FILES_PER_USER_PER_DAY} uploads per day. Upgrade your plan for higher limits."
        )


def calculate_file_hash(file_content: bytes) -> str:
    """
    Calculate SHA-256 hash of file content
    Used for duplicate detection
    """
    return hashlib.sha256(file_content).hexdigest()


async def check_duplicate_file(user_id: str, file_hash: str) -> Optional[str]:
    """
    Check if file was already uploaded by this user
    Returns: document_id if duplicate found, None otherwise
    """
    result = supabase.table('documents').select('id').eq('user_id', user_id).eq('file_hash', file_hash).execute()
    
    if result.data and len(result.data) > 0:
        return result.data[0]['id']
    
    return None


# =====================================================
# MAIN VALIDATION FUNCTION
# =====================================================

async def validate_upload(
    file: UploadFile,
    user_id: Optional[str] = None,
    ip_address: Optional[str] = None
) -> Dict[str, Any]:
    """
    Comprehensive file upload validation
    
    Args:
        file: Uploaded file
        user_id: User ID if authenticated, None if anonymous
        ip_address: Client IP address for rate limiting
        
    Returns:
        Dictionary with validated file info
        
    Raises:
        HTTPException: If validation fails
    """
    # Step 1: Validate file size
    validate_file_size(file)
    
    # Step 2: Validate file type (extension and content-type)
    content_type = validate_file_type(file)
    
    # Step 3: Sanitize filename
    safe_filename = validate_filename(file.filename)
    
    # Step 4: Validate file content (magic bytes)
    await validate_file_content(file, content_type)
    
    # Step 5: Rate limiting
    if user_id:
        await check_rate_limit_authenticated(user_id)
    else:
        if ip_address:
            await check_rate_limit_anonymous(ip_address)
        else:
            raise HTTPException(
                status_code=400,
                detail="Anonymous uploads require IP address for rate limiting"
            )
    
    # Step 6: Calculate file hash for duplicate detection
    file_content = await file.read()
    await file.seek(0)  # Reset file pointer
    file_hash = calculate_file_hash(file_content)
    
    # Step 7: Check for duplicates (authenticated users only)
    duplicate_id = None
    if user_id:
        duplicate_id = await check_duplicate_file(user_id, file_hash)
        if duplicate_id:
            print(f"⚠️ Duplicate file detected. Previous document ID: {duplicate_id}")
            # Don't raise error, but log it
    
    return {
        'validated': True,
        'safe_filename': safe_filename,
        'content_type': content_type,
        'file_size': file.size,
        'file_hash': file_hash,
        'duplicate_of': duplicate_id
    }


# =====================================================
# USAGE EXAMPLE
# =====================================================

"""
Update your upload endpoint in documents.py:

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    request: Request,
    current_user_id: str = Depends(get_current_user_optional)
):
    try:
        # Get client IP address
        ip_address = request.client.host
        
        # Validate upload
        validation_result = await validate_upload(
            file=file,
            user_id=current_user_id,
            ip_address=ip_address
        )
        
        # Check if duplicate
        if validation_result['duplicate_of']:
            return {
                'status': 'duplicate',
                'message': 'This file was already uploaded',
                'document_id': validation_result['duplicate_of']
            }
        
        # Proceed with upload using validated data
        safe_filename = validation_result['safe_filename']
        file_hash = validation_result['file_hash']
        
        # ... rest of upload logic ...
        
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"❌ Upload validation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
"""
