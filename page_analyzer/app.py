import os
from datetime import date

import requests
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for

from page_analyzer import database
from page_analyzer.parser import parse_page
from page_analyzer.url_normalizer import normalize_url, validate_url

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.get('/')
def index():
    return render_template('index.html')


@app.post('/urls')
def urls_post():
    url = request.form.get('url', '').strip()

    if not validate_url(url):
        flash('Некорректный URL', 'danger')
        return render_template('index.html', url=url), 422

    normalized = normalize_url(url)
    existing = database.find_url_by_name(normalized)

    if existing:
        flash('Страница уже существует', 'info')
        return redirect(url_for('url_get', id=existing[0]))

    url_id = database.create_url(normalized, date.today())

    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('url_get', id=url_id))


@app.get('/urls')
def urls_get():
    urls = database.get_all_urls()
    return render_template('urls.html', urls=urls)


@app.get('/urls/<int:id>')
def url_get(id):
    url = database.get_url_by_id(id)

    if not url:
        return 'Not Found', 404

    checks = database.get_checks_by_url_id(id)
    return render_template('url.html', url=url, checks=checks)


@app.post('/urls/<int:id>/checks')
def url_check(id):
    url = database.get_url_by_id(id)

    if not url:
        return 'Not Found', 404

    try:
        response = requests.get(url[1], timeout=10)
        response.raise_for_status()

        page_data = parse_page(response.text)

        database.create_check(
            id,
            response.status_code,
            page_data['h1'],
            page_data['title'],
            page_data['description'],
            date.today()
        )

        flash('Страница успешно проверена', 'success')

    except Exception:
        flash('Произошла ошибка при проверке', 'danger')

    return redirect(url_for('url_get', id=id))
