.PHONY: gui gui-debug cli help

# Default target
help:
	@echo "PEaC - Makefile Commands"
	@echo "========================"
	@echo ""
	@echo "  make gui        - Launch the GUI application"
	@echo "  make gui-debug  - Launch the GUI with debug output"
	@echo "  make cli        - Run the CLI prompt command (requires yaml file argument)"
	@echo ""
	@echo "Examples:"
	@echo "  make gui"
	@echo "  make gui-debug"
	@echo "  make cli YAML=examples/academic.yaml"

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
