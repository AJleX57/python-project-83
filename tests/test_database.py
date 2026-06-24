from datetime import date
from unittest.mock import MagicMock, patch

from page_analyzer import database


def make_mock_conn(fetchone_value=None, fetchall_value=None):
    mock_cur = MagicMock()
    mock_cur.fetchone.return_value = fetchone_value
    mock_cur.fetchall.return_value = fetchall_value or []

    mock_conn = MagicMock()
    mock_conn.__enter__.return_value = mock_conn
    mock_conn.cursor.return_value.__enter__.return_value = mock_cur

    return mock_conn, mock_cur


@patch('page_analyzer.database.get_conn')
def test_find_url_by_name_found(mock_get_conn):
    mock_conn, mock_cur = make_mock_conn(fetchone_value=(1,))
    mock_get_conn.return_value = mock_conn

    result = database.find_url_by_name('https://example.com')

    assert result == (1,)
    mock_cur.execute.assert_called_once()


@patch('page_analyzer.database.get_conn')
def test_find_url_by_name_not_found(mock_get_conn):
    mock_conn, mock_cur = make_mock_conn(fetchone_value=None)
    mock_get_conn.return_value = mock_conn

    result = database.find_url_by_name('https://nope.com')

    assert result is None


@patch('page_analyzer.database.get_conn')
def test_create_url_returns_id(mock_get_conn):
    mock_conn, mock_cur = make_mock_conn(fetchone_value=(42,))
    mock_get_conn.return_value = mock_conn

    url_id = database.create_url('https://example.com', date.today())

    assert url_id == 42
    mock_cur.execute.assert_called_once()


@patch('page_analyzer.database.get_conn')
def test_get_all_urls(mock_get_conn):
    rows = [(1, 'https://example.com', date.today(), 200)]
    mock_conn, mock_cur = make_mock_conn(fetchall_value=rows)
    mock_get_conn.return_value = mock_conn

    result = database.get_all_urls()

    assert result == rows


@patch('page_analyzer.database.get_conn')
def test_get_url_by_id_found(mock_get_conn):
    row = (1, 'https://example.com', date.today())
    mock_conn, mock_cur = make_mock_conn(fetchone_value=row)
    mock_get_conn.return_value = mock_conn

    result = database.get_url_by_id(1)

    assert result == row


@patch('page_analyzer.database.get_conn')
def test_get_checks_by_url_id(mock_get_conn):
    rows = [(1, 200, 'h1', 'title', 'desc', date.today())]
    mock_conn, mock_cur = make_mock_conn(fetchall_value=rows)
    mock_get_conn.return_value = mock_conn

    result = database.get_checks_by_url_id(1)

    assert result == rows


@patch('page_analyzer.database.get_conn')
def test_create_check_executes_insert(mock_get_conn):
    mock_conn, mock_cur = make_mock_conn()
    mock_get_conn.return_value = mock_conn

    database.create_check(
        1, 200, 'h1 text', 'title text', 'desc text', date.today()
    )

    mock_cur.execute.assert_called_once()
