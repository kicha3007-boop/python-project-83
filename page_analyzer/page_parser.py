from bs4 import BeautifulSoup


def get_text(tag):
    return tag.get_text(strip=True) if tag else ''


def parse_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    description = soup.find('meta', attrs={'name': 'description'})
    return {
        'h1': get_text(soup.h1),
        'title': get_text(soup.title),
        'description': description.get('content', '') if description else '',
    }
