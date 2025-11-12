.PHONY: install run test test-cov lint format clean help

help:
	@echo "Available commands:"
	@echo "  make install    - Install dependencies"
	@echo "  make run        - Run the development server"
	@echo "  make test       - Run tests"
	@echo "  make test-cov   - Run tests with coverage"
	@echo "  make clean      - Clean cache and build files"

install:
	pip install -r requirements.txt

run:
	python3 run.py

test:
	python3 -m pytest

test-cov:
	python3 -m pytest --cov=app --cov-report=html --cov-report=term

lint:
	@echo "Linting not configured. Consider adding flake8, black, or ruff."

format:
	@echo "Formatting not configured. Consider adding black or ruff."

clean:
	find . -type d -name __pycache__ -exec rm -r {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} + 2>/dev/null || true
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf dist
	rm -rf build

