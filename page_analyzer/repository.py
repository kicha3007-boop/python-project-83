from contextlib import contextmanager

import psycopg
from psycopg.rows import dict_row


@contextmanager
def get_cursor(database_url):
    with psycopg.connect(database_url, row_factory=dict_row) as connection:
        with connection.cursor() as cursor:
            yield cursor


def find_url(database_url, url_id):
    with get_cursor(database_url) as cursor:
        cursor.execute('SELECT * FROM urls WHERE id = %s', (url_id,))
        return cursor.fetchone()


def find_url_by_name(database_url, name):
    with get_cursor(database_url) as cursor:
        cursor.execute('SELECT * FROM urls WHERE name = %s', (name,))
        return cursor.fetchone()


def add_url(database_url, name):
    with get_cursor(database_url) as cursor:
        cursor.execute(
            'INSERT INTO urls (name) VALUES (%s) RETURNING id',
            (name,),
        )
        return cursor.fetchone()['id']


def get_urls_with_last_check(database_url):
    query = '''
        SELECT DISTINCT ON (urls.id)
            urls.id,
            urls.name,
            url_checks.created_at AS last_check_at,
            url_checks.status_code
        FROM urls
        LEFT JOIN url_checks ON url_checks.url_id = urls.id
        ORDER BY urls.id DESC, url_checks.id DESC
    '''
    with get_cursor(database_url) as cursor:
        cursor.execute(query)
        return cursor.fetchall()


def get_checks(database_url, url_id):
    with get_cursor(database_url) as cursor:
        cursor.execute(
            'SELECT * FROM url_checks WHERE url_id = %s ORDER BY id DESC',
            (url_id,),
        )
        return cursor.fetchall()


def add_check(database_url, url_id, status_code, seo):
    query = '''
        INSERT INTO url_checks (url_id, status_code, h1, title, description)
        VALUES (%s, %s, %s, %s, %s)
    '''
    with get_cursor(database_url) as cursor:
        cursor.execute(query, (
            url_id,
            status_code,
            seo['h1'],
            seo['title'],
            seo['description'],
        ))
