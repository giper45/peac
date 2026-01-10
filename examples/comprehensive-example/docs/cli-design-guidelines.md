# CLI Design Guidelines

## Introduction

Command-line interfaces (CLI) are powerful tools for developers and power users. Well-designed CLIs follow consistent patterns and conventions that make them intuitive and efficient to use.

## Core Principles

### 1. Be Predictable
Users should be able to guess how your CLI works based on common conventions:
- Use standard flags: `-h` or `--help`, `-v` or `--version`
- Follow POSIX conventions for flag syntax
- Use consistent naming patterns across commands

### 2. Be Helpful
Provide clear, actionable help:
- Display help when no arguments are given
- Show context-sensitive help for subcommands
- Include examples in help text
- Suggest corrections for typos

### 3. Be Composable
Design for integration with other tools:
- Accept input from stdin
- Write output to stdout
- Use stderr for errors and diagnostics
- Return meaningful exit codes

### 4. Be Consistent
Maintain consistency throughout your CLI:
- Use the same terminology everywhere
- Apply uniform formatting to output
- Standardize flag naming conventions

## Command Structure

### Hierarchical Commands
Organize complex CLIs with subcommands:
```
app <command> [<subcommand>] [options] [arguments]
```

Example:
```bash
peac gui config.yaml              # Simple command
peac parse --format json input.md # Command with options
```

### Flags and Options

#### Short vs Long Flags
- Short: `-f`, `-v`, `-h` (single dash, single letter)
- Long: `--file`, `--verbose`, `--help` (double dash, full word)
- Support both when possible

#### Flag Conventions
```bash
# Boolean flags (no argument)
--verbose, --quiet, --force

# Value flags (require argument)
--output <file>, --config <path>
--format json, --format=json

# Multiple values
--tag python --tag cli
--tags python,cli,tools
```

## Input and Output

### Input Sources
Support multiple input methods:
```python
# From file
peac process input.txt

# From stdin
cat input.txt | peac process

# From argument
peac process --text "inline text"
```

### Output Formatting
Provide multiple output formats:
- Human-readable (default)
- JSON (for machine processing)
- Quiet mode (minimal output)
- Verbose mode (detailed output)

### Color and Styling
Use colors meaningfully:
- **Green**: Success messages
- **Yellow**: Warnings
- **Red**: Errors
- **Blue**: Information
- **Gray**: Secondary information

Always provide a `--no-color` option and respect `NO_COLOR` environment variable.

## Error Handling

### Error Messages
Craft helpful error messages:
```
# Bad
Error: Invalid input

# Good
Error: Could not read file 'config.yaml'
  File not found at path: /home/user/config.yaml
  
  Did you mean:
    - config.yml (in current directory)
    - config-example.yaml (in current directory)
```

### Exit Codes
Use standard exit codes:
- `0`: Success
- `1`: General errors
- `2`: Misuse of shell command
- `126`: Command cannot execute
- `127`: Command not found
- `128+N`: Fatal error signal N

## Progress and Feedback

### Progress Indicators
Show progress for long-running operations:
- Spinner for indefinite operations
- Progress bar for operations with known duration
- Percentage completion
- ETA estimates

### Interactive Mode
Provide interactive prompts when appropriate:
```python
# Confirmation prompts
"Are you sure you want to delete all files? (y/N)"

# Selection prompts
"Select provider: [1] OpenAI [2] Anthropic [3] Local"

# Input prompts
"Enter API key: "
```

## Configuration

### Configuration Sources
Support multiple configuration methods (in order of precedence):
1. Command-line flags (highest priority)
2. Environment variables
3. Configuration files
4. Default values (lowest priority)

### Configuration Files
```yaml
# Support standard locations
~/.config/app/config.yaml
~/.app.yaml
./.app.yaml (project-specific)

# Use common formats
YAML, JSON, TOML, INI
```

### Environment Variables
```bash
# Use consistent naming
APP_API_KEY=xxx
APP_MODEL=gpt-4
APP_VERBOSE=true

# Prefix with app name to avoid conflicts
PEAC_PROVIDER=openai
PEAC_OUTPUT_DIR=./output
```

## Documentation

### Help Text Structure
```
Usage: peac [OPTIONS] COMMAND [ARGS]...

  PEaC - Prompt Engineering as Code
  
  Structure and manage LLM prompts using YAML configurations.

Options:
  -v, --version          Show version and exit
  -h, --help            Show this message and exit
  --config PATH         Configuration file path
  --verbose             Enable verbose output

Commands:
  gui      Launch GUI interface
  parse    Parse YAML and generate prompt
  validate Validate YAML configuration
  
Examples:
  # Launch GUI with configuration
  peac gui config.yaml
  
  # Generate prompt from YAML
  peac parse --output prompt.txt config.yaml
  
  # Validate configuration
  peac validate config.yaml

For more information, visit: https://github.com/user/peac
```

### Command-Specific Help
```bash
peac gui --help  # Show help for 'gui' command
peac parse -h    # Short form works too
```

## Performance

### Startup Time
Optimize for fast startup:
- Lazy load modules
- Minimize initial imports
- Cache expensive operations
- Use compiled extensions for heavy lifting

### Resource Usage
Be mindful of resources:
- Stream large files instead of loading entirely
- Provide options to limit memory usage
- Clean up temporary files
- Cancel operations on SIGINT (Ctrl+C)

## Testing CLIs

### Test Coverage
Test different aspects:
- Unit tests for business logic
- Integration tests for command flow
- E2E tests for complete workflows
- Help text and documentation tests

### Automated Testing
```python
# Use click.testing.CliRunner or similar
from click.testing import CliRunner

def test_cli():
    runner = CliRunner()
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert 'Usage:' in result.output
```

## Accessibility

### Screen Reader Support
- Use semantic output structure
- Avoid ASCII art for essential information
- Provide text alternatives for visual elements

### Keyboard Navigation
- Support standard navigation keys
- Provide keyboard shortcuts
- Allow Tab completion where possible

## Best Practices Summary

1. **Follow conventions**: Use standard patterns users expect
2. **Provide help**: Make help easy to discover and understand
3. **Be forgiving**: Accept flexible input, suggest corrections
4. **Give feedback**: Show progress, confirm actions
5. **Support automation**: Design for scripting and integration
6. **Document thoroughly**: Include examples and common use cases
7. **Test extensively**: Validate behavior across platforms
8. **Version carefully**: Use semantic versioning, maintain compatibility

## Tools and Libraries

### Python CLI Frameworks
- **Click**: Composable command-line interface toolkit
- **Typer**: Modern CLI framework with type hints
- **argparse**: Standard library option parser
- **Rich**: Beautiful terminal formatting
- **Questionary**: Interactive prompts

### Testing Tools
- **pytest**: Testing framework
- **click.testing**: CLI testing utilities
- **pexpect**: Automation for interactive programs

## Conclusion

A well-designed CLI is a joy to use and integrates seamlessly into workflows. Follow these guidelines to create CLIs that users will love.
