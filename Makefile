dev:
	python3 manage.py runserver

build:
	./build.sh

render-start:
	uv run gunicorn task_manager.wsgi

.PHONY: install
install:
	@uv sync