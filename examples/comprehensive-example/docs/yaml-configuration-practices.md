# YAML Configuration Best Practices

## Introduction

YAML (YAML Ain't Markup Language) is a human-friendly data serialization format commonly used for configuration files. This guide covers best practices for designing and using YAML configurations.

## Structure and Organization

### Keep It Simple
YAML should be easy to read and understand:
```yaml
# Good: Clear and simple
database:
  host: localhost
  port: 5432
  name: myapp

# Avoid: Overly complex nesting
configuration:
  settings:
    database:
      connection:
        parameters:
          host: localhost
```

### Use Meaningful Keys
Choose descriptive, consistent key names:
```yaml
# Good: Clear intent
max_retry_attempts: 3
connection_timeout: 30
enable_logging: true

# Avoid: Unclear abbreviations
max_ret: 3
conn_to: 30
log: true
```

### Group Related Settings
Organize configuration logically:
```yaml
# Group by functionality
server:
  host: 0.0.0.0
  port: 8080
  workers: 4

database:
  host: localhost
  port: 5432
  pool_size: 10

logging:
  level: INFO
  format: json
  output: stdout
```

## Data Types

### Strings
```yaml
# Plain strings (no quotes needed)
name: John Doe
message: Hello world

# Quoted strings (when needed)
special_chars: "Line 1\nLine 2"
with_colon: "Key: Value"

# Multi-line strings
description: |
  This is a multi-line
  description that preserves
  line breaks.

folded_text: >
  This is folded text
  that will be combined
  into a single line.
```

### Numbers
```yaml
# Integers
count: 42
negative: -10

# Floats
temperature: 98.6
scientific: 1.23e-4

# Preserve as string if needed
version: "1.0"  # Not 1.0 float
zip_code: "00123"  # Not 123 integer
```

### Booleans
```yaml
# Various ways to express boolean
enabled: true
disabled: false
flag_yes: yes
flag_no: no
on_switch: on
off_switch: off

# Recommended: Use true/false for clarity
is_active: true
is_public: false
```

### Lists
```yaml
# Inline list
tags: [python, yaml, config]

# Block list (preferred for readability)
features:
  - authentication
  - authorization
  - logging
  - monitoring

# List of objects
users:
  - name: Alice
    role: admin
  - name: Bob
    role: user
```

### Dictionaries
```yaml
# Inline dictionary
metadata: {version: 1.0, author: John}

# Block dictionary (preferred)
metadata:
  version: 1.0
  author: John
  created: 2026-01-09
```

## Advanced Features

### Anchors and Aliases
Reuse configuration blocks:
```yaml
# Define anchor with &
defaults: &defaults
  timeout: 30
  retries: 3
  logging: true

# Reference with *
development:
  <<: *defaults
  debug: true

production:
  <<: *defaults
  debug: false
  timeout: 60  # Override specific value
```

### Multiple Documents
Separate multiple configurations in one file:
```yaml
# Document 1
---
name: Config 1
setting: value1

# Document 2
---
name: Config 2
setting: value2
```

### Comments
Use comments liberally:
```yaml
# Main configuration section
server:
  host: localhost  # Listen on local interface
  port: 8080       # Default HTTP port
  
  # Worker configuration
  workers: 4  # Number of parallel workers
```

## Validation and Schema

### Define Expected Structure
Document your configuration schema:
```yaml
# config.schema.yaml
type: object
properties:
  server:
    type: object
    required: [host, port]
    properties:
      host:
        type: string
      port:
        type: integer
        minimum: 1
        maximum: 65535
```

### Provide Defaults
Include sensible defaults:
```yaml
# Default configuration
defaults:
  server:
    host: localhost
    port: 8080
    workers: 4
  
  logging:
    level: INFO
    format: text

# User only needs to override what's different
```

### Validate Early
Check configuration at startup:
```python
import yaml
from schema import Schema, And, Use

# Define schema
config_schema = Schema({
    'server': {
        'host': str,
        'port': And(int, lambda n: 1 <= n <= 65535)
    }
})

# Validate
config = yaml.safe_load(open('config.yaml'))
config_schema.validate(config)
```

## Security Considerations

### Sensitive Data
Don't store secrets in YAML:
```yaml
# Bad: Secrets in config
database:
  password: supersecret123

# Good: Reference environment variables
database:
  password: ${DB_PASSWORD}
  
# Or use external secrets management
database:
  password_from_vault: /secret/db/password
```

### Safe Loading
Always use safe_load:
```python
import yaml

# Safe: Only load basic types
with open('config.yaml') as f:
    config = yaml.safe_load(f)

# Unsafe: Can execute arbitrary Python code
# config = yaml.load(f)  # DON'T DO THIS
```

## File Organization

### Split Large Configs
Break down large configurations:
```
config/
├── base.yaml          # Base configuration
├── development.yaml   # Dev overrides
├── production.yaml    # Prod overrides
└── secrets.yaml.example  # Template for secrets
```

### Use Inheritance
Extend configurations:
```yaml
# base.yaml
server:
  host: localhost
  port: 8080

# production.yaml
extends: base.yaml
server:
  host: 0.0.0.0
  workers: 8
```

## Common Patterns

### Feature Flags
```yaml
features:
  new_ui: true
  beta_api: false
  experimental_mode: false
```

### Environment-Specific Config
```yaml
# Pattern 1: Separate sections
development:
  debug: true
  database: dev.db

production:
  debug: false
  database: prod.db

# Pattern 2: Separate files
# config/development.yaml
# config/production.yaml
```

### Plugin Configuration
```yaml
plugins:
  - name: authentication
    enabled: true
    config:
      method: oauth2
      provider: google
  
  - name: caching
    enabled: true
    config:
      backend: redis
      ttl: 3600
```

## Documentation

### Self-Documenting Config
```yaml
# Application Configuration
# Version: 1.0
# Last updated: 2026-01-09

# Server Settings
# Configure the web server behavior
server:
  # Hostname or IP address to bind to
  # Use 0.0.0.0 to listen on all interfaces
  host: localhost
  
  # Port number (1-65535)
  # Standard HTTP port is 80, HTTPS is 443
  port: 8080
  
  # Number of worker processes
  # Recommended: 2 * CPU_CORES
  workers: 4
```

### Include Examples
Provide example configurations:
```yaml
# Example: Basic configuration
# Copy this to config.yaml and customize

# Minimal required settings
required_setting: value

# Optional settings with defaults shown
# optional_setting: default_value

# Advanced options (uncomment to use)
# advanced:
#   option1: value1
#   option2: value2
```

## Testing Configurations

### Validation Tests
```python
def test_config_valid():
    config = yaml.safe_load(open('config.yaml'))
    assert 'server' in config
    assert config['server']['port'] > 0

def test_config_has_required_keys():
    config = yaml.safe_load(open('config.yaml'))
    required = ['server', 'database', 'logging']
    for key in required:
        assert key in config
```

### Environment Testing
Test configs for each environment:
```python
def test_production_config():
    config = yaml.safe_load(open('config/production.yaml'))
    assert config['debug'] is False
    assert config['server']['workers'] >= 4
```

## Tools and Libraries

### Python Libraries
- **PyYAML**: Standard YAML parser
- **ruamel.yaml**: Preserves formatting and comments
- **pydantic**: Validation with type hints
- **python-dotenv**: Environment variable management

### Validation Tools
- **yamllint**: YAML file linter
- **jsonschema**: Schema validation
- **cerberus**: Data validation

### IDEs and Editors
- VS Code: YAML extension with validation
- PyCharm: Built-in YAML support
- Vim: yaml-vim plugin

## Common Pitfalls

### Avoid
1. **Deep nesting**: Keep structure flat when possible
2. **Inconsistent formatting**: Use consistent indentation (2 or 4 spaces)
3. **Complex anchors**: Use sparingly, prefer explicit values
4. **Ambiguous types**: Quote strings that look like numbers/booleans
5. **Large files**: Split into multiple files for maintainability

### Remember
1. **Indentation matters**: YAML is whitespace-sensitive
2. **No tabs**: Use spaces only
3. **Quote special characters**: Especially `:`, `{`, `[`, `]`, `&`, `*`
4. **Version your schema**: Track changes to configuration structure
5. **Validate on load**: Catch errors early

## Conclusion

Well-structured YAML configurations make applications easier to deploy, configure, and maintain. Follow these best practices to create robust, maintainable configuration files.
