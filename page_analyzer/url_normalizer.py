from urllib.parse import urlparse

import validators


def validate_url(url):
    if not url or len(url) > 255 or not validators.url(url):
        return False
    return True


def normalize_url(url):
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}"
