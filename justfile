# Justfile for Excelence project

# Default recipe - show available commands
default:
    @just --list

# Start both frontend and backend in parallel
dev:
    @echo "Starting frontend and backend..."
    @just dev-backend & just dev-frontend

# Start backend server
dev-backend:
    @echo "Starting backend server on port 8000..."
    cd excelence/backend && uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Start frontend dev server
dev-frontend:
    @echo "Starting frontend dev server on port 5173..."
    cd excelence/frontend && npm run dev

# Install all dependencies
install:
    @echo "Installing dependencies..."
    @just install-backend
    @just install-frontend

# Install backend dependencies
install-backend:
    @echo "Installing backend dependencies..."
    cd excelence/backend && uv pip install -e ".[dev]"

# Install frontend dependencies
install-frontend:
    @echo "Installing frontend dependencies..."
    cd excelence/frontend && npm install

# Run backend tests
test-backend:
    @echo "Running backend tests..."
    cd excelence/backend && uv run pytest

# Run frontend tests
test-frontend:
    @echo "Running frontend tests..."
    cd excelence/frontend && npm test

# Run all tests
test:
    @just test-backend
    @just test-frontend

# Lint backend code
lint-backend:
    @echo "Linting backend code..."
    cd excelence/backend && uv run ruff check .

# Lint frontend code
lint-frontend:
    @echo "Linting frontend code..."
    cd excelence/frontend && npm run lint

# Lint all code
lint:
    @just lint-backend
    @just lint-frontend

# Format backend code
format-backend:
    @echo "Formatting backend code..."
    cd excelence/backend && uv run ruff format .

# Format frontend code
format-frontend:
    @echo "Formatting frontend code..."
    cd excelence/frontend && npm run format

# Format all code
format:
    @just format-backend
    @just format-frontend

# Clean build artifacts
clean:
    @echo "Cleaning build artifacts..."
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -type d -name "node_modules" -exec rm -rf {} + 2>/dev/null || true
    find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
    find . -type d -name "dist" -exec rm -rf {} + 2>/dev/null || true
