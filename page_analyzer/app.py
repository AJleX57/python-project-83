import os
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
import psycopg
import validators
from urllib.parse import urlparse
from datetime import date

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

DATABASE_URL = os.getenv('DATABASE_URL')


def get_conn():
    return psycopg.connect(DATABASE_URL)


def truncate(text, length=200):
    if text and len(text) > length:
        return text[:length] + '...'
    return text


@app.route('/')
def index():
    return render_template('index.html')


@app.post('/urls')
def urls_post():
    url = request.form.get('url', '').strip()

    if not url or len(url) > 255 or not validators.url(url):
        flash('Некорректный URL', 'danger')
        return render_template('index.html', url=url), 422

    parsed = urlparse(url)
    normalized = f"{parsed.scheme}://{parsed.netloc}"

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT id FROM urls WHERE name = %s', (normalized,))
            existing = cur.fetchone()

            if existing:
                flash('Страница уже существует', 'info')
                return redirect(url_for('url_get', id=existing[0]))

            cur.execute(
                'INSERT INTO urls (name, created_at)'
                'VALUES (%s, %s) RETURNING id',
                (normalized, date.today())
            )
            url_id = cur.fetchone()[0]

    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('url_get', id=url_id))


@app.get('/urls')
def urls_get():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                SELECT
                    urls.id,
                    urls.name,
                    url_checks.created_at AS last_check,
                    url_checks.status_code
                FROM urls
                LEFT JOIN url_checks ON url_checks.id = (
                    SELECT id FROM url_checks
                    WHERE url_id = urls.id
                    ORDER BY id DESC
                    LIMIT 1
                )
                ORDER BY urls.id DESC
            ''')
            urls = cur.fetchall()
    return render_template('urls.html', urls=urls)


@app.get('/urls/<int:id>')
def url_get(id):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                'SELECT id, name, created_at FROM urls WHERE id = %s', (id,)
            )
            url = cur.fetchone()

            cur.execute('''
                SELECT id, status_code, h1, title, description, created_at
                FROM url_checks
                WHERE url_id = %s
                ORDER BY id DESC
            ''', (id,))
            checks = cur.fetchall()

    if not url:
        return 'Not Found', 404

    return render_template('url.html', url=url, checks=checks)


@app.post('/urls/<int:id>/checks')
def url_check(id):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT name FROM urls WHERE id = %s', (id,))
            url = cur.fetchone()

    if not url:
        return 'Not Found', 404

    try:
        response = requests.get(url[0], timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        h1 = soup.find('h1')
        h1_text = truncate(h1.get_text(strip=True)) if h1 else ''

        title = soup.find('title')
        title_text = truncate(title.get_text(strip=True)) if title else ''

        meta_desc = soup.find('meta', attrs={'name': 'description'})
        desc_text = truncate(
            meta_desc.get('content', '') if meta_desc else ''
        )

        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    '''INSERT INTO url_checks
                    (url_id, status_code, h1, title, description, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s)''',
                    (id, response.status_code, h1_text,
                     title_text, desc_text, date.today())
                )

        flash('Страница успешно проверена', 'success')

    except Exception:
        flash('Произошла ошибка при проверке', 'danger')

    return redirect(url_for('url_get', id=id))
