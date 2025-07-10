.PHONY: help install test lint format clean run docker-build docker-run

help:
	@echo "Story2Audio Microservice - Makefile"
	@echo ""
	@echo "Available commands:"
	@echo "  make install      - Install dependencies"
	@echo "  make test         - Run tests"
	@echo "  make lint         - Run linters"
	@echo "  make format       - Format code with black"
	@echo "  make clean        - Clean temporary files"
	@echo "  make run          - Run the gRPC server"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-run   - Run Docker container"

install:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

test:
	pytest Tests/ -v --cov=src --cov=api

lint:
	flake8 .
	mypy src api --ignore-missing-imports

format:
	black src api Tests examples

clean:
	find . -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .mypy_cache .coverage htmlcov dist build *.egg-info

run:
	python api/server.py

docker-build:
	docker build -t story2audio:latest .

docker-run:
	docker run -p 50051:50051 story2audio:latest
