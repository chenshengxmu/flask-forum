import os
import time
from PIL import Image
from werkzeug.utils import secure_filename
from flask import current_app


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def save_cover_image(file, post_id):
    """Save and optimize uploaded cover image"""
    if file and allowed_file(file.filename):
        # Open and optimize image
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

        # Generate filename
        ext = file.filename.rsplit('.', 1)[1].lower()
        timestamp = int(time.time())
        filename = f"post_{post_id}_{timestamp}.{ext}"

        # Save optimized image
        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        filepath = os.path.join(upload_folder, filename)

        if ext in ['jpg', 'jpeg']:
            img.save(filepath, 'JPEG', quality=85, optimize=True)
        elif ext == 'png':
            img.save(filepath, 'PNG', optimize=True)
        elif ext == 'webp':
            img.save(filepath, 'WEBP', quality=85)
        else:
            img.save(filepath)

        return filename
    return None


def delete_cover_image(filename):
    """Delete cover image file from filesystem"""
    if filename:
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(filepath):
            os.remove(filepath)
