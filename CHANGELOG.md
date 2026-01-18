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

## [0.2.7] - 2026-01-14

### Added
- Dual RAG provider architecture with factory pattern (FastEmbed + FAISS)
- FastembedProvider: default, lightweight, JSON-based indexes, no PyTorch dependency
- FaissProvider: optional, scalable, binary indexes with multiple types (flat/ivf/hnsw)
- Provider field in YAML grammar to support dynamic provider selection
- Conditional FAISS installation via Makefile: `make install`, `make faiss-cpu`, `make faiss-gpu`
- Comprehensive test suite for RAG providers (22 tests, all passing)
- Cross-platform path handling tests (test_path_cross_platform.py and test_extends_cross_platform.py)
- 4 example YAML files: rag-simple, rag-fastembed, rag-faiss, rag-sample-docs
- Sample documentation folder (5 documents) for RAG testing
- RAG_EXAMPLES.md: comprehensive guide with provider comparison table
- RAG_PROVIDERS.md: technical architecture documentation
- EBNF grammar file in docs/
- Hierarchical extends regression tests and local-rules validation tests
- Coverage tests for all `examples/usecase/nutrizione-*` YAML prompts
- Integrated FastEmbed benchmark results into MANUSCRIPT_TEXT.md (50 runs on 100-document corpus); updated analysis to reflect single-provider reporting.

### Changed
- Refactored RagProvider to modular provider architecture
- Updated YAML parser to recognize `provider`, `index_path`, `provider_config` fields
- Backward compatibility maintained with `faiss_file` field
- GUI models updated to support new RAG fields
- Makefile enhanced with test targets: `make test`, `make test-rag`, `make test-all`
- Enhanced nutritional guidelines in usecase files with specific rules for meal planning

### Fixed
- Module naming conflict (rag.py renamed to rag_legacy.py)
- Import structure for RAG providers
- Path resolution in YAML examples
- Hierarchical extends merge now fully recursive (inherits grandparents)
- Cross-platform path handling in PathResolverService (Windows/macOS/Linux compatibility)
- Path separator handling for files created on different platforms
- Cross-platform extends in YAML files (handles both forward and backslashes in path references)
- find_path and PromptYaml now normalize path separators automatically (\ to /)
- Missing `source` in local rules now reported gracefully instead of KeyError

## [0.2.6] - 2026-01-12

### Added
- [Next features here]

### Changed
- [Changes here]

### Fixed
- [Fixes here]

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
 
 