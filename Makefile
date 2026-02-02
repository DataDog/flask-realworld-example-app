.PHONY: help install test lint format clean run docker-up docker-down migrate

help:
	@echo "Available commands:"
	@echo "  make install       Install dependencies with hatch"
	@echo "  make test          Run tests"
	@echo "  make test-cov      Run tests with coverage"
	@echo "  make lint          Run linters"
	@echo "  make format        Format code with black"
	@echo "  make clean         Clean up cache and build files"
	@echo "  make run           Run development server"
	@echo "  make docker-up     Start Docker containers"
	@echo "  make docker-down   Stop Docker containers"
	@echo "  make migrate       Run database migrations"
	@echo "  make db-init       Initialize database"
	@echo "  make hooks         Install pre-commit hooks"

install:
	pip install hatch
	hatch env create

test:
	hatch run unit_tests:test

test-cov:
	hatch run unit_tests:cov

lint:
	hatch run lint:all

format:
	hatch run lint:fmt

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache .coverage htmlcov dist build
	rm -f dev.db

run:
	export FLASK_APP=autoapp.py && export FLASK_DEBUG=1 && flask run --with-threads

run-dd:
	export FLASK_APP=autoapp.py && export FLASK_DEBUG=1 && \
	export DD_SERVICE=flask-realworld-app && export DD_ENV=development && \
	ddtrace-run flask run --with-threads

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f app

migrate:
	flask db upgrade

db-init:
	flask db init
	flask db migrate
	flask db upgrade

hooks:
	bash hooks/autohook.sh install

# Development tasks
dev-setup: install hooks db-init
	@echo "Development environment ready!"

# CI simulation
ci: lint test
	@echo "CI checks passed!"
