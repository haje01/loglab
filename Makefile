.PHONY: help install test coverage lint format security clean build all pre-commit test-python test-csharp test-cpp test-typescript test-java test-codegen

# Default target
help:
	@echo "LogLab Development Commands"
	@echo "=========================="
	@echo "install     - Install dependencies and setup development environment"
	@echo "test        - Run all tests"
	@echo "coverage    - Run tests with coverage report"
	@echo "lint        - Run linting checks"
	@echo "format      - Format code with black and isort"
	@echo "security    - Run security checks"
	@echo "clean       - Clean build artifacts and cache files"
	@echo "build       - Build standalone executable"
	@echo "pre-commit  - Install and run pre-commit hooks"
	@echo "all         - Run format, lint, test, and coverage"
	@echo ""
	@echo "Multi-language tests:"
	@echo "test-python     - Test Python code generation"
	@echo "test-csharp     - Test C# code generation"
	@echo "test-cpp        - Test C++ code generation"
	@echo "test-typescript - Test TypeScript code generation"
	@echo "test-java       - Test Java code generation"
	@echo "test-codegen    - Test all code generation"

# Install dependencies
install:
	uv pip install --upgrade pip || python -m pip install --upgrade pip || true
	uv pip install -e . || pip install -e . || true
	uv pip install -r requirements-dev.txt || pip install -r requirements-dev.txt || uv pip install pytest coverage tox black isort flake8 pre-commit safety bandit psutil
	pre-commit install || true

# Run all tests
test:
	pytest tests/ -v

# Run tests with coverage
coverage:
	coverage run --source loglab -m pytest tests/
	coverage report --show-missing
	coverage html

# Run linting checks
lint:
	@echo "Running flake8..."
	flake8 loglab tests
	@echo "Checking black formatting..."
	black --check loglab tests
	@echo "Checking isort imports..."
	isort --check-only loglab tests

# Format code
format:
	@echo "Formatting with black..."
	black loglab tests
	@echo "Sorting imports with isort..."
	isort loglab tests

# Security checks
security:
	@echo "Running safety check..."
	safety check || echo "Safety check completed with warnings"
	@echo "Running bandit security scan..."
	bandit -r loglab/ -f txt || echo "Bandit scan completed with warnings"

# Clean build artifacts
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/ dist/ .coverage htmlcov/ .pytest_cache/ .tox/
	rm -f *.html *.schema.json loglab_*.py loglab_*.cs loglab_*.h loglab_*.ts loglab_*.java
	cd tests && rm -f *.html *.schema.json loglab_*.py loglab_*.cs loglab_*.h
	cd tests/cpptest && rm -f loglab_*.h test_log_objects_cpp || true
	cd tests/tstest && rm -f loglab_*.ts loglab_*.js && rm -rf dist/ node_modules package-lock.json || true
	cd tests/javatest && mvn clean || true

# Build standalone executable
build: test
	./tools/build.sh

# Install and run pre-commit hooks
pre-commit:
	pre-commit install
	pre-commit run --all-files

# Test Python code generation
test-python:
	@echo "Testing Python code generation..."
	python -m loglab object example/foo.lab.json py -o tests/loglab_foo.py
	cd tests && python -m pytest test_log_objects_python.py -v

# Test C# code generation (requires .NET SDK)
test-csharp:
	@echo "Testing C# code generation..."
	python -m loglab object example/foo.lab.json cs -o tests/cstest/loglab_foo.cs
	cd tests/cstest && dotnet run

# Test C++ code generation (requires libgtest-dev)
test-cpp:
	@echo "Testing C++ code generation..."
	python -m loglab object example/foo.lab.json cpp -o tests/cpptest/loglab_foo.h
	cd tests/cpptest && g++ -std=c++17 -I. test_log_objects_cpp.cpp -lgtest -lgtest_main -lpthread -o test_log_objects_cpp && ./test_log_objects_cpp

# Test TypeScript code generation (requires Node.js)
test-typescript:
	@echo "Testing TypeScript code generation..."
	python -m loglab object example/foo.lab.json ts -o tests/tstest/loglab_foo.ts
	cd tests/tstest && npm install
	cd tests/tstest && npx tsc
	cd tests/tstest && node dist/test_log_objects_typescript.js

# Test Java code generation (requires Maven)
test-java:
	@echo "Testing Java code generation..."
	python -m loglab object example/foo.lab.json java -o tests/javatest/src/main/java/loglab_foo/LogLabFoo.java
	cd tests/javatest && mvn compile exec:java

# Test all code generation
test-codegen: test-python test-csharp test-cpp test-typescript test-java

# Run tox for multiple Python versions
test-tox:
	tox

# Full development workflow
all: format lint test coverage

# Development setup for new contributors
setup: install pre-commit
	@echo "Development environment setup complete!"
	@echo "Run 'make help' to see available commands."
