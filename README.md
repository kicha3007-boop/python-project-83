# Анализатор страниц (Python Flask)

[![hexlet-check](https://github.com/kicha3007-boop/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/kicha3007-boop/python-project-83/actions)
[![Python CI](https://github.com/kicha3007-boop/python-project-83/actions/workflows/pyci.yml/badge.svg)](https://github.com/kicha3007-boop/python-project-83/actions/workflows/pyci.yml)

Page Analyzer — сайт, который проверяет страницы на SEO-пригодность: пользователь добавляет адрес,
запускает проверку и видит код ответа, `h1`, `title` и `description` страницы.

## Стек

Python, Flask, PostgreSQL (psycopg), Jinja2, Tailwind CSS, gunicorn.

## Требования

- Python 3.10+, [uv](https://docs.astral.sh/uv/)
- Node.js и npm — только для сборки стилей
- PostgreSQL

## Установка и запуск

```bash
git clone https://github.com/kicha3007-boop/python-project-83.git
cd python-project-83
cp .env.example .env          # заполнить DATABASE_URL и SECRET_KEY
psql -d "$DATABASE_URL" -f database.sql
make setup                    # зависимости Python и npm, сборка CSS
make dev                      # режим разработки, http://localhost:5000
make start                    # продакшен (gunicorn), http://localhost:8000
```

Переменные окружения:

- `DATABASE_URL` — строка подключения, `postgresql://user:password@localhost:5432/page_analyzer`
- `SECRET_KEY` — ключ подписи сессии для flash-сообщений

Деплой на render.com: команда сборки `make build`, запуска — `make render-start`.

## Разработка

```bash
make lint       # ruff
make build-css  # пересобрать стили после правки шаблонов
```

---

<details>
<summary>Автоматические тесты Хекслета</summary>

Тесты запускаются на каждый коммит. За запуск отвечает файл `.github/workflows/hexlet-check.yml` — не удаляйте и не переименовывайте ни его, ни репозиторий.

</details>
