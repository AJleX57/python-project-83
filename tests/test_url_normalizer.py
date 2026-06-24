from page_analyzer.url_normalizer import normalize_url, validate_url


def test_validate_url_valid():
    assert validate_url('https://example.com') is True


def test_validate_url_invalid_scheme():
    assert validate_url('httpsss://abcabca@test.ru') is False


def test_validate_url_empty():
    assert validate_url('') is False


def test_validate_url_too_long():
    long_url = 'https://example.com/' + 'a' * 250
    assert validate_url(long_url) is False


def test_normalize_url_strips_path():
    assert normalize_url('https://example.com/page/1') == \
        'https://example.com'


def test_normalize_url_strips_query():
    assert normalize_url('https://example.com?q=1') == \
        'https://example.com'


def test_normalize_url_keeps_scheme_and_host():
    assert normalize_url('http://example.com') == 'http://example.com'
