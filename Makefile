.PHONY: gui gui-debug cli help install faiss-cpu faiss-gpu faiss-install test test-rag test-all

# Default target
help:
	@echo "PEaC - Makefile Commands"
	@echo "========================"
	@echo ""
	@echo "Setup:"
	@echo "  make install   - Install dependencies and optionally configure RAG (FAISS)"
	@echo ""
	@echo "Core Commands:"
	@echo "  make gui        - Launch the GUI application"
	@echo "  make gui-debug  - Launch the GUI with debug output"
	@echo "  make cli        - Run the CLI prompt command (requires yaml file argument)"
	@echo ""
	@echo "Testing:"
	@echo "  make test       - Run all tests"
	@echo "  make test-rag   - Run RAG-specific tests"
	@echo "  make test-core  - Run PEaC core module tests"
	@echo "  make test-all   - Run all tests with verbose output"
	@echo ""
	@echo "RAG Dependencies:"
	@echo "  make faiss-cpu  - Install FAISS with CPU support (macOS/Linux/Windows)"
	@echo "  make faiss-gpu  - Install FAISS with CUDA GPU support (Linux only)"
	@echo "  make faiss-install - Interactive FAISS installation (auto-detect OS/GPU)"
	@echo ""
	@echo "Examples:"
	@echo "  make install"
	@echo "  make gui"
	@echo "  make gui-debug"
	@echo "  make cli YAML=examples/academic.yaml"
	@echo "  make faiss-cpu"

# Install all dependencies and optionally configure RAG
install:
	@echo "PEaC Installation"
	@echo "================="
	@echo ""
	@echo "Step 1/2: Installing base dependencies with Poetry..."
	poetry install
	@echo "✓ Base dependencies installed"
	@echo ""
	@echo "Step 2/2: Configuring RAG provider (optional)..."
	@echo ""
	$(MAKE) faiss-install

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

# Alternative CLI target with section headers disabled
cli-no-headers:
	@if [ -z "$(YAML)" ]; then \
		echo "Error: YAML parameter required"; \
		echo "Usage: make cli-no-headers YAML=path/to/file.yaml"; \
		exit 1; \
	fi
	@echo "Running PEaC CLI (no headers) with $(YAML)..."
	poetry run peac prompt $(YAML) --no-section-headers

# Install FAISS with CPU support (all platforms)
faiss-cpu:
	@echo "Installing FAISS with CPU support..."
	poetry install -E faiss-cpu
	@echo "✓ FAISS CPU installation complete"
	@echo "  Usage: make cli YAML=examples/rag-faiss.yaml"

# Install FAISS with GPU support (CUDA, Linux only)
faiss-gpu:
	@if [ "$$(uname)" != "Linux" ]; then \
		echo "Error: FAISS GPU (CUDA) is only available on Linux"; \
		echo "For macOS/Windows, use: make faiss-cpu"; \
		exit 1; \
	fi
	@echo "Installing FAISS with CUDA GPU support..."
	poetry install -E faiss-gpu
	@echo "✓ FAISS GPU installation complete"
	@echo "  Usage: make cli YAML=examples/rag-faiss.yaml"

# Interactive FAISS installation (auto-detect OS/GPU)
faiss-install:
	@echo "PEaC FAISS Installation Helper"
	@echo "==============================="
	@echo ""
	@uname_output=$$(uname); \
	if [ "$$uname_output" = "Darwin" ]; then \
		echo "macOS detected → Installing FAISS CPU support..."; \
		poetry install -E faiss-cpu; \
	elif [ "$$uname_output" = "Linux" ]; then \
		echo "Linux detected"; \
		if command -v nvidia-smi > /dev/null 2>&1; then \
			echo "NVIDIA GPU detected → Install FAISS GPU (CUDA)? [y/n]"; \
			read -r response; \
			if [ "$$response" = "y" ] || [ "$$response" = "Y" ]; then \
				poetry install -E faiss-gpu; \
			else \
				poetry install -E faiss-cpu; \
			fi; \
		else \
			echo "No NVIDIA GPU detected → Installing FAISS CPU support..."; \
			poetry install -E faiss-cpu; \
		fi; \
	else \
		echo "Windows detected → Installing FAISS CPU support..."; \
		poetry install -E faiss-cpu; \
	fi
	@echo ""
	@echo "✓ FAISS installation complete"
	@echo "  Test it: make cli YAML=examples/rag-faiss.yaml"

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