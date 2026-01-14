.PHONY: gui gui-debug cli help install test test-rag test-all build-cli-lite build-cli-full build-gui-lite build-gui-full

# Default target
help:
	@echo "PEaC - Makefile Commands"
	@echo "========================"
	@echo ""
	@echo "Setup:"
	@echo "  make install   - Install dependencies with Poetry"
	@echo ""
	@echo "Core Commands:"
	@echo "  make gui        - Launch the GUI application"
	@echo "  make gui-debug  - Launch the GUI with debug output"
	@echo "  make cli        - Run the CLI prompt command (requires yaml file argument)"
	@echo ""
	@echo "Build Commands (Windows only):"
	@echo "  make build-cli-lite      - Build CLI executable (lite: fastembed only)"
	@echo "  make build-cli-full      - Build CLI executable (full: FAISS + fastembed)"
	@echo "  make build-gui-lite      - Build GUI executable (lite: fastembed only)"
	@echo "  make build-gui-full      - Build GUI executable (full: FAISS + fastembed)"
	@echo ""
	@echo "  FAST builds (skip compression, ~2-3x faster):"
	@echo "  make build-cli-lite-fast - CLI lite (no UPX compression)"
	@echo "  make build-cli-full-fast - CLI full (no UPX compression)"
	@echo "  make build-gui-lite-fast - GUI lite (no UPX compression)"
	@echo "  make build-gui-full-fast - GUI full (no UPX compression)"
	@echo ""
	@echo "Testing:"
	@echo "  make test            - Run all tests"
	@echo "  make test-rag        - Run RAG-specific tests"
	@echo "  make test-core       - Run PEaC core module tests"
	@echo "  make test-performance - Run performance benchmarks (50 runs, ~10 min)"
	@echo "  make test-all        - Run all tests with verbose output"
	@echo ""
	@echo "Benchmarking:"
	@echo "  make benchmark       - Generate corpus and run full performance benchmarks"
	@echo "  make docker-build    - Build Docker container for reproducibility"
	@echo "  make docker-test     - Run tests in Docker container"
	@echo ""
	@echo "Examples:"
	@echo "  make install"
	@echo "  make gui"
	@echo "  make build-gui-lite"
	@echo "  make cli YAML=examples/academic.yaml"

# Install all dependencies with Poetry
install:
	@echo "Installing PEaC with Poetry..."
	poetry install
	@echo "✓ Installation complete"
	@echo ""
	@echo "Optional: Install FAISS support"
	@echo "  poetry install -E faiss-cpu   (Windows/Mac/Linux)"
	@echo "  poetry install -E faiss-gpu   (Linux with NVIDIA GPU)"

# Launch GUI
gui:
	@echo "Starting PEaC GUI..."
	poetry run peac gui

# Launch GUI with debug output
gui-debug:
	@echo "Starting PEaC GUI with debug output..."
	DEBUG=true poetry run peac gui

# Run CLI prompt command
# Usage: make cli YAML=path/to/file.yaml
cli:
	@if [ -z "$(YAML)" ]; then \
		echo "Error: YAML parameter required"; \
		echo "Usage: make cli YAML=path/to/file.yaml"; \
		echo "Example: make cli YAML=examples/academic.yaml"; \
		exit 1; \
	fi
	@echo "Running PEaC CLI with $(YAML)..."
	poetry run peac prompt $(YAML)

# Run all tests
test:
	@echo "Running test suite..."
	poetry run pytest tests/ -v

# Run RAG-specific tests
test-rag:
	@echo "Running RAG tests..."
	poetry run pytest tests/test_rag.py -v

# Run core module tests
test-core:
	@echo "Running PEaC core module tests..."
	poetry run pytest tests/test_peac_core.py -v

# Run all tests with detailed output
test-all:
	@echo "Running full test suite with detailed output..."
	poetry run pytest tests/ -vv -s

# Run performance benchmarks
test-performance:
	@echo "Running performance benchmarks (50 runs, ~10 minutes)..."
	poetry run pytest tests/test_performance.py -v -s

# Generate corpus and run benchmarks
benchmark:
	@echo "Running full benchmark suite with corpus generation..."
	poetry run python scripts/run_benchmarks.py

# Build Docker container
docker-build:
	@echo "Building PEaC reproducibility container..."
	docker-compose build

# Run tests in Docker
docker-test:
	@echo "Running tests in Docker container..."
	docker-compose run peac-tests

# Run benchmarks in Docker
docker-benchmark:
	@echo "Running benchmarks in Docker container..."
	docker-compose run peac-benchmarks

# Build CLI executable - LITE version (fastembed only)
build-cli-lite:
	@echo "Building CLI LITE executable..."
	@cmd.exe /c "cd build_scripts && build.bat cli lite"

# Build CLI executable - LITE version FAST (no compression)
build-cli-lite-fast:
	@echo "Building CLI LITE executable (FAST mode - no compression)..."
	@cmd.exe /c "cd build_scripts && build.bat cli lite fast"

# Build CLI executable - FULL version (FAISS + fastembed)
build-cli-full:
	@echo "Building CLI FULL executable..."
	@cmd.exe /c "cd build_scripts && build.bat cli full"

# Build CLI executable - FULL version FAST (no compression)
build-cli-full-fast:
	@echo "Building CLI FULL executable (FAST mode - no compression)..."
	@cmd.exe /c "cd build_scripts && build.bat cli full fast"

# Build GUI executable - LITE version (fastembed only)
build-gui-lite:
	@echo "Building GUI LITE executable..."
	@cmd.exe /c "cd build_scripts && build.bat gui lite"

# Build GUI executable - LITE version FAST (no compression)
build-gui-lite-fast:
	@echo "Building GUI LITE executable (FAST mode - no compression)..."
	@cmd.exe /c "cd build_scripts && build.bat gui lite fast"

# Build GUI executable - FULL version (FAISS + fastembed)
build-gui-full:
	@echo "Building GUI FULL executable..."
	@cmd.exe /c "cd build_scripts && build.bat gui full"

# Build GUI executable - FULL version FAST (no compression)
build-gui-full-fast:
	@echo "Building GUI FULL executable (FAST mode - no compression)..."
	@cmd.exe /c "cd build_scripts && build.bat gui full fast"
