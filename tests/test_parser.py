from page_analyzer.parser import parse_page, truncate


def test_parse_page_full():
    html = '''
        <html>
            <head>
                <title>My Title</title>
                <meta name="description" content="My description">
            </head>
            <body>
                <h1>My Header</h1>
            </body>
        </html>
    '''
    result = parse_page(html)
    assert result['h1'] == 'My Header'
    assert result['title'] == 'My Title'
    assert result['description'] == 'My description'


def test_parse_page_missing_tags():
    html = '<html><body><p>no tags here</p></body></html>'
    result = parse_page(html)
    assert result['h1'] == ''
    assert result['title'] == ''
    assert result['description'] == ''


def test_truncate_short_text():
    assert truncate('short text') == 'short text'


def test_truncate_long_text():
    long_text = 'a' * 250
    result = truncate(long_text)
    assert result.endswith('...')
    assert len(result) == 203


def test_truncate_empty():
    assert truncate('') == ''
    assert truncate(None) is None
