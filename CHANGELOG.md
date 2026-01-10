# Change Log
All notable changes to this project will be documented in this file.
 
The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).
 
## [Unreleased] - yyyy-mm-dd
 
Here we write upgrading notes for brands. It's a team effort to make them as
straightforward as possible.
 
### Added
- [Next features here]
 
### Changed
- [Changes here]
 
### Fixed
- [Fixes here]

## [0.2.3] - 2026-01-10
 
### Added
- Section header option for instruction blocks in GUI
- Comprehensive example configurations and test files
- Makefile for common development tasks
 
### Changed
- Enhanced GUI main app with improved instruction section handling
- Updated build scripts for Linux, macOS, and Windows with better error handling
- Improved architecture diagrams (modules, integration, and use case sequences)
- Updated copilot instructions for better development workflow
 
### Fixed
- Instruction section now fully parsed and included in prompt output
- GUI launcher initialization issues
- Dependency management improvements in poetry.lock

## [0.2.2] - 2025-09-18
 
### Added
- Architecture documentation with accurate implementation diagrams
- PlantUML and Draw.io architecture diagrams with modular design
- Comprehensive prompt engineering templates collection (12+ strategies)
- Academic paper descriptions following Elsevier CAS-SC guidelines
- RAG integration verification and code structure analysis
- Module documentation with actual vs. theoretical implementation mapping
 
### Changed
- Updated architecture diagrams to reflect actual codebase implementation
- Improved diagram styling with clean black/white theme for publications
- Enhanced PlantUML diagrams with straight lines and readable fonts
- Reorganized draw.io components for easier modification
 
### Fixed
- Copy function now includes Instruction section in prompt generation
- Architecture diagram accuracy - removed theoretical components
- Provider module documentation now matches actual implementation
- Component relationship mapping corrected in architectural diagrams

## [0.2.1] - 2024-12-12
  
### Added
- Support for PDF provider with page range filtering
- Support for DOCX provider with paragraph filtering
- GUI components for provider options
- Template examples for PDF/DOCX usage
 
### Changed
- Provider system architecture to support specialized file handlers
- Template updated with provider-specific examples
  
### Fixed
- Filter regex functionality for specialized providers

## [0.2.0] - 2024-12-12
 
 Added the local directory parsing with regex features
 
### Added
- `local` also parses directories, with filter and recursive options.

### Changed
- the preamble is attached to the first line. The file separator becomes ``` in order to match the GPT markdown parsing syntax.
 
 