"""
HTML sanitization utilities for user-generated content.
Prevents XSS attacks while allowing basic formatting.
"""
import bleach
from markupsafe import Markup


# Allowed HTML tags for post and reply content
ALLOWED_TAGS = [
    'p', 'br', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'blockquote', 'code', 'pre', 'ul', 'ol', 'li', 'a', 'img'
]

# Allowed attributes for specific tags
ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title', 'rel'],
    'img': ['src', 'alt', 'title', 'width', 'height'],
}

# Allowed URL protocols
ALLOWED_PROTOCOLS = ['http', 'https', 'mailto']


def sanitize_html(content, strip=False):
    """
    Sanitize HTML content to prevent XSS attacks.

    Args:
        content (str): Raw HTML content from user input
        strip (bool): If True, strip all HTML tags. If False, allow safe tags.

    Returns:
        str: Sanitized HTML content safe for rendering
    """
    if not content:
        return ''

    if strip:
        # Strip all HTML tags, leaving only text
        return bleach.clean(content, tags=[], strip=True)

    # Clean HTML, allowing only safe tags and attributes
    cleaned = bleach.clean(
        content,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        protocols=ALLOWED_PROTOCOLS,
        strip=True  # Strip disallowed tags instead of escaping them
    )

    # Linkify URLs (convert plain text URLs to clickable links)
    cleaned = bleach.linkify(
        cleaned,
        callbacks=[bleach.callbacks.nofollow, bleach.callbacks.target_blank]
    )

    return cleaned


def sanitize_and_mark_safe(content):
    """
    Sanitize HTML content and mark it as safe for Jinja2 rendering.

    Args:
        content (str): Raw HTML content from user input

    Returns:
        Markup: Sanitized content marked as safe for rendering
    """
    return Markup(sanitize_html(content))


def strip_tags(content):
    """
    Remove all HTML tags from content, leaving only plain text.
    Useful for previews, search indexing, etc.

    Args:
        content (str): HTML content

    Returns:
        str: Plain text with all HTML tags removed
    """
    return sanitize_html(content, strip=True)
