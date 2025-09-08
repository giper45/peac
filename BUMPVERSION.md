# Bumpversion Usage Guide

This project is configured with `bump-my-version` for automated version management.

## Installation

The dependency is already included in the dev dependencies. To install:

```bash
poetry install
```

## Basic Usage

### Show current version and possible bumps
```bash
poetry run bump-my-version show-bump
```

### Bump version types

#### Patch version (0.2.1 → 0.2.2)
```bash
poetry run bump-my-version bump patch
```

#### Minor version (0.2.1 → 0.3.0)
```bash
poetry run bump-my-version bump minor
```

#### Major version (0.2.1 → 1.0.0)
```bash
poetry run bump-my-version bump major
```

### Dry run (preview changes without applying them)
```bash
poetry run bump-my-version bump patch --dry-run
```

### Allow dirty working directory (for testing)
```bash
poetry run bump-my-version bump patch --allow-dirty
```

## Configuration

The bumpversion configuration is in `pyproject.toml` under `[tool.bumpversion]`.

It automatically:
- Updates the version in `pyproject.toml`
- Updates the `CHANGELOG.md` with a new version section
- Creates a git commit with the version change
- Creates a git tag for the new version

## Files Updated

- `pyproject.toml` - Updates the version field
- `CHANGELOG.md` - Adds a new version section and moves unreleased items

## CHANGELOG.md Format

The changelog follows [Keep a Changelog](https://keepachangelog.com/) format.

When you bump a version, it will:
1. Create a new `[Unreleased]` section
2. Move current unreleased items to a dated version section
3. Add empty subsections (Added, Changed, Fixed) for future changes

## Workflow

1. Make your changes
2. Update `CHANGELOG.md` in the `[Unreleased]` section with your changes
3. Commit your changes
4. Run `poetry run bump-my-version bump [patch|minor|major]`
5. Push the commit and tags: `git push && git push --tags`
