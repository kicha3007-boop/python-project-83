import os

import requests
from dotenv import load_dotenv
from flask import (
    Flask,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from page_analyzer import repository
from page_analyzer.formatting import format_date, truncate_text
from page_analyzer.page_parser import parse_page
from page_analyzer.url_validator import normalize_url, validate_url

load_dotenv()

REQUEST_TIMEOUT = 10

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')
app.add_template_filter(truncate_text, 'truncate_text')
app.add_template_filter(format_date, 'format_date')


def get_database_url():
    return app.config['DATABASE_URL']


@app.get('/')
def index():
    return render_template('index.html', url='')


@app.post('/urls')
def urls_create():
    raw_url = request.form.get('url', '')
    error = validate_url(raw_url)
    if error:
        flash(error, 'danger')
        return render_template('index.html', url=raw_url), 422

    name = normalize_url(raw_url)
    existing = repository.find_url_by_name(get_database_url(), name)
    if existing:
        flash('Страница уже существует', 'info')
        return redirect(url_for('urls_show', id=existing['id']))

    url_id = repository.add_url(get_database_url(), name)
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('urls_show', id=url_id))


@app.get('/urls')
def urls_index():
    urls = repository.get_urls_with_last_check(get_database_url())
    return render_template('urls/index.html', urls=urls)


@app.get('/urls/<int:id>')
def urls_show(id):
    url = repository.find_url(get_database_url(), id)
    if url is None:
        abort(404)
    checks = repository.get_checks(get_database_url(), id)
    return render_template('urls/show.html', url=url, checks=checks)


@app.post('/urls/<int:id>/checks')
def url_checks_create(id):
    url = repository.find_url(get_database_url(), id)
    if url is None:
        abort(404)

    try:
        response = requests.get(url['name'], timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
    except requests.RequestException as error:
        app.logger.warning('Check of %s failed: %s', url['name'], error)
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('urls_show', id=id))

    seo = parse_page(response.text)
    repository.add_check(get_database_url(), id, response.status_code, seo)
    flash('Страница успешно проверена', 'success')
    return redirect(url_for('urls_show', id=id))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500
