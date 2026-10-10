PORT ?= 8000

setup: install build-css

install:
	uv sync
	npm ci

build-css:
	npm run build:css

dev:
	uv run flask --debug --app page_analyzer:app run

start:
	uv run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

build:
	./build.sh

render-start:
	gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

lint:
	uv run ruff check page_analyzer

.PHONY: setup install build-css dev start build render-start lint
