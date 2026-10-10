from urllib.parse import urlparse

import validators

MAX_URL_LENGTH = 255
INVALID_URL_MESSAGE = 'Некорректный URL'


def normalize_url(raw_url):
    parsed = urlparse(raw_url.strip())
    return f'{parsed.scheme.lower()}://{parsed.netloc.lower()}'


def is_valid_url(url):
    if not url or len(url) > MAX_URL_LENGTH:
        return False
    return bool(validators.url(url, simple_host=True))


def validate_url(raw_url):
    return None if is_valid_url(raw_url.strip()) else INVALID_URL_MESSAGE
