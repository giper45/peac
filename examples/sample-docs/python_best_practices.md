# Python Best Practices Guide

## Code Organization

### Module Structure
Organize your Python project with clear module boundaries:
- Use `__init__.py` files to mark directories as packages
- Group related functionality into modules
- Separate business logic from presentation logic

### Naming Conventions
- Classes: PascalCase (e.g., `UserManager`, `DataProcessor`)
- Functions and variables: snake_case (e.g., `get_user_data`, `total_count`)
- Constants: UPPER_SNAKE_CASE (e.g., `MAX_CONNECTIONS`, `API_KEY`)
- Private members: prefix with underscore (e.g., `_internal_method`)

## Error Handling

Always use specific exception types:
```python
try:
    result = risky_operation()
except FileNotFoundError:
    logger.error("File not found")
except PermissionError:
    logger.error("Permission denied")
```

## Type Hints

Use type hints for better code documentation and IDE support:
```python
def process_data(items: list[str], threshold: int = 10) -> dict[str, int]:
    return {item: len(item) for item in items if len(item) > threshold}
```

## Testing

Write comprehensive unit tests using pytest:
- Test edge cases and error conditions
- Use fixtures for test data
- Mock external dependencies
- Aim for high code coverage
