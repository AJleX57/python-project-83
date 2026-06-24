from datetime import date
from unittest.mock import MagicMock, patch


def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert 'Анализатор страниц'.encode() in response.data


def test_urls_post_invalid_url(client):
    response = client.post('/urls', data={'url': 'not-a-url'})
    assert response.status_code == 422
    assert 'Некорректный URL'.encode() in response.data


@patch('page_analyzer.app.database')
def test_urls_post_new_url(mock_db, client):
    mock_db.find_url_by_name.return_value = None
    mock_db.create_url.return_value = 1

    response = client.post(
        '/urls', data={'url': 'https://example.com'}, follow_redirects=True
    )

    assert response.status_code == 200
    assert 'Страница успешно добавлена'.encode() in response.data
    mock_db.create_url.assert_called_once()


@patch('page_analyzer.app.database')
def test_urls_post_existing_url(mock_db, client):
    mock_db.find_url_by_name.return_value = (1,)

    response = client.post(
        '/urls', data={'url': 'https://example.com'}, follow_redirects=True
    )

    assert response.status_code == 200
    assert 'Страница уже существует'.encode() in response.data
    mock_db.create_url.assert_not_called()


@patch('page_analyzer.app.database')
def test_urls_get_list(mock_db, client):
    mock_db.get_all_urls.return_value = [
        (1, 'https://example.com', date.today(), 200),
    ]

    response = client.get('/urls')

    assert response.status_code == 200
    assert 'https://example.com'.encode() in response.data


@patch('page_analyzer.app.database')
def test_url_get_not_found(mock_db, client):
    mock_db.get_url_by_id.return_value = None

    response = client.get('/urls/999')

    assert response.status_code == 404


@patch('page_analyzer.app.database')
def test_url_get_existing(mock_db, client):
    mock_db.get_url_by_id.return_value = (
        1, 'https://example.com', date.today()
    )
    mock_db.get_checks_by_url_id.return_value = []

    response = client.get('/urls/1')

    assert response.status_code == 200
    assert 'https://example.com'.encode() in response.data


@patch('page_analyzer.app.database')
@patch('page_analyzer.app.requests')
def test_url_check_success(mock_requests, mock_db, client):
    mock_db.get_url_by_id.return_value = (1, 'https://example.com')

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = '<html><body><h1>Hi</h1></body></html>'
    mock_response.raise_for_status.return_value = None
    mock_requests.get.return_value = mock_response

    response = client.post('/urls/1/checks', follow_redirects=True)

    assert response.status_code == 200
    assert 'Страница успешно проверена'.encode() in response.data
    mock_db.create_check.assert_called_once()


@patch('page_analyzer.app.database')
@patch('page_analyzer.app.requests')
def test_url_check_failure(mock_requests, mock_db, client):
    mock_db.get_url_by_id.return_value = (1, 'https://wrong.test')
    mock_requests.get.side_effect = Exception('Connection error')

    response = client.post('/urls/1/checks', follow_redirects=True)

    assert response.status_code == 200
    assert 'Произошла ошибка при проверке'.encode() in response.data
    mock_db.create_check.assert_not_called()


@patch('page_analyzer.app.database')
def test_url_check_url_not_found(mock_db, client):
    mock_db.get_url_by_id.return_value = None

    response = client.post('/urls/999/checks')

    assert response.status_code == 404
