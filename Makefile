dev:
	uv run python3 manage.py runserver

build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi

.PHONY: install
install:
	@uv sync

lint:
	uv run ruff check .

fix:
	uv run ruff check --fix .

migrate:
	uv run python3 manage.py migrate

