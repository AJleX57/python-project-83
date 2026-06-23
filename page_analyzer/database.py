import os

import psycopg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')


def get_conn():
    return psycopg.connect(DATABASE_URL)


def find_url_by_name(name):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT id FROM urls WHERE name = %s', (name,))
            return cur.fetchone()


def create_url(name, created_at):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                'INSERT INTO urls (name, created_at)'
                ' VALUES (%s, %s) RETURNING id',
                (name, created_at)
            )
            return cur.fetchone()[0]


def get_all_urls():
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
            return cur.fetchall()


def get_url_by_id(id):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                'SELECT id, name, created_at FROM urls WHERE id = %s', (id,)
            )
            return cur.fetchone()


def get_checks_by_url_id(id):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                SELECT id, status_code, h1, title, description, created_at
                FROM url_checks
                WHERE url_id = %s
                ORDER BY id DESC
            ''', (id,))
            return cur.fetchall()


def create_check(url_id, status_code, h1, title, description, created_at):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                '''INSERT INTO url_checks
                (url_id, status_code, h1, title, description, created_at)
                VALUES (%s, %s, %s, %s, %s, %s)''',
                (url_id, status_code, h1, title, description, created_at)
            )
