import os
import time
import secrets
from PIL import Image
from werkzeug.utils import secure_filename
from flask import current_app


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def validate_image_file(file_stream):
    """
    Validate image file using PIL (not just extension).
    Returns the actual image format or None if invalid.

    Args:
        file_stream: File stream to validate

    Returns:
        str: Image format (e.g., 'JPEG', 'PNG') or None if invalid
    """
    # Save current position
    pos = file_stream.tell()

    try:
        # Try to open with PIL
        img = Image.open(file_stream)
        file_format = img.format

        # Reset position
        file_stream.seek(pos)

        # Map PIL formats to our allowed types
        allowed_formats = {'JPEG', 'PNG', 'GIF', 'WEBP'}

        return file_format.lower() if file_format in allowed_formats else None

    except Exception:
        # Reset position even on error
        file_stream.seek(pos)
        return None


def validate_file_size(file_stream, max_size_mb=5):
    """
    Validate file size before processing.

    Args:
        file_stream: File stream to validate
        max_size_mb: Maximum file size in megabytes

    Returns:
        bool: True if file size is acceptable
    """
    pos = file_stream.tell()
    file_stream.seek(0, os.SEEK_END)
    size = file_stream.tell()
    file_stream.seek(pos)  # Reset position

    max_size_bytes = max_size_mb * 1024 * 1024
    return size <= max_size_bytes


def save_cover_image(file, post_id):
    """
    Save and optimize uploaded cover image with enhanced security validation.

    Args:
        file: FileStorage object from form upload
        post_id: Post ID for filename generation

    Returns:
        str: Generated filename or None if validation fails
    """
    if not file or not file.filename:
        return None

    # Validate file extension
    if not allowed_file(file.filename):
        current_app.logger.warning(f'Invalid file extension for upload: {file.filename}')
        return None

    # Validate file size (5MB max)
    if not validate_file_size(file.stream, max_size_mb=5):
        current_app.logger.warning(f'File size exceeds limit: {file.filename}')
        return None

    # Validate file type using magic bytes
    actual_type = validate_image_file(file.stream)
    if not actual_type:
        current_app.logger.warning(f'Invalid image file (magic bytes check failed): {file.filename}')
        return None

    try:
        # Open and optimize image
        img = Image.open(file.stream)

        # Verify it's actually an image by trying to load it
        img.verify()

        # Re-open after verify (verify closes the file)
        file.stream.seek(0)
        img = Image.open(file.stream)

        # Convert RGBA to RGB if needed
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background

        # Resize if too large
        img.thumbnail((1200, 800), Image.Resampling.LANCZOS)

        # Generate secure random filename (not predictable)
        random_string = secrets.token_hex(8)
        ext = actual_type if actual_type != 'jpeg' else 'jpg'
        filename = f"post_{post_id}_{random_string}.{ext}"

        # Save optimized image
        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        filepath = os.path.join(upload_folder, filename)

        # Save with appropriate format
        if ext in ['jpg', 'jpeg']:
            img.save(filepath, 'JPEG', quality=85, optimize=True)
        elif ext == 'png':
            img.save(filepath, 'PNG', optimize=True)
        elif ext == 'webp':
            img.save(filepath, 'WEBP', quality=85)
        elif ext == 'gif':
            img.save(filepath, 'GIF', optimize=True)
        else:
            img.save(filepath)

        current_app.logger.info(f'Saved cover image: {filename} for post {post_id}')
        return filename

    except Exception as e:
        current_app.logger.error(f'Error processing image upload: {str(e)}', exc_info=True)
        return None


def delete_cover_image(filename):
    """Delete cover image file from filesystem"""
    if filename:
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(filepath):
            os.remove(filepath)
