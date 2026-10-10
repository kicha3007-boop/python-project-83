MAX_TEXT_LENGTH = 200
DATE_FORMAT = '%Y-%m-%d'


def truncate_text(text):
    if not text:
        return ''
    if len(text) <= MAX_TEXT_LENGTH:
        return text
    return f'{text[:MAX_TEXT_LENGTH]}...'


def format_date(value):
    return value.strftime(DATE_FORMAT) if value else ''
