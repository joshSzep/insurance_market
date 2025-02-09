# List available recipes
default:
    @just --list

# Install backend dependencies using uv
install-backend:
    cd backend && uv sync --all-extras --all-groups --all-packages --upgrade

# Install frontend dependencies
install-frontend:
    cd frontend && npm install

# Install all dependencies
install: install-backend install-frontend

# Format backend code with ruff
fmt-backend:
    cd backend && ruff format .

# Format frontend code with prettier
fmt-frontend:
    cd frontend && npm run format

# Format all code
fmt: fmt-backend fmt-frontend

# Lint backend code with ruff
lint-backend:
    cd backend && ruff check . --fix

# Lint frontend code
lint-frontend:
    cd frontend && npm run lint

# Run all linters
lint: lint-backend lint-frontend

# Type check backend code with pyright
typecheck-backend:
    cd backend && pyright

# Type check frontend code
typecheck-frontend:
    cd frontend && npm run typecheck

# Run all type checks
typecheck: typecheck-backend typecheck-frontend

# Run backend tests
test-backend:
    cd backend && uv run pytest

# Run frontend tests
test-frontend:
    cd frontend && npm test

# Run all tests
test: test-backend test-frontend

# Run backend tests with coverage
test-backend-cov:
    cd backend && uv run pytest --cov=insurance_market --cov-report=term-missing .

# Run Django development server
serve-backend:
    cd backend && uv run python manage.py runserver

# Run Next.js development server
serve-frontend:
    cd frontend && npm run dev

# Run database migrations
migrate:
    cd backend && uv run python manage.py migrate

# Make database migrations
makemigrations:
    cd backend && uv run python manage.py makemigrations

# Create a superuser
createsuperuser:
    cd backend && uv run python manage.py createsuperuser

# Clean Python cache files
clean-backend:
    cd backend && find . -type d -name "__pycache__" -exec rm -r {} +
    cd backend && find . -type f -name "*.pyc" -delete
    cd backend && find . -type f -name "*.pyo" -delete
    cd backend && find . -type f -name "*.pyd" -delete
    cd backend && find . -type d -name "*.egg-info" -exec rm -r {} +
    cd backend && find . -type d -name "*.egg" -exec rm -r {} +
    cd backend && find . -type d -name ".pytest_cache" -exec rm -r {} +
    cd backend && find . -type d -name ".coverage" -delete
    cd backend && find . -type d -name "htmlcov" -exec rm -r {} +

# Clean frontend build artifacts
clean-frontend:
    cd frontend && rm -rf .next node_modules

# Clean all build artifacts
clean: clean-backend clean-frontend

# Check all (format, lint, typecheck, test)
check: fmt lint typecheck test

# Run pre-commit hooks on all files
pre-commit:
    cd backend && uv run pre-commit run --all-files
