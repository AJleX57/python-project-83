from bs4 import BeautifulSoup


def truncate(text, length=200):
    if text and len(text) > length:
        return text[:length] + '...'
    return text


def parse_page(html):
    soup = BeautifulSoup(html, 'html.parser')

    h1 = soup.find('h1')
    h1_text = truncate(h1.get_text(strip=True)) if h1 else ''

    title = soup.find('title')
    title_text = truncate(title.get_text(strip=True)) if title else ''

    meta_desc = soup.find('meta', attrs={'name': 'description'})
    desc_text = truncate(
        meta_desc.get('content', '') if meta_desc else ''
    )

    return {
        'h1': h1_text,
        'title': title_text,
        'description': desc_text,
    }
