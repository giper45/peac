# Change Log
All notable changes to this project will be documented in this file.
 
The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).
 
## [Unreleased] - yyyy-mm-dd
 
Here we write upgrading notes for brands. It's a team effort to make them as
straightforward as possible.
 
### Added
- Excel XLSX provider support with sheet filtering
- Support for "sheets" option in XLSX files (instead of "pages")
- Dynamic GUI labels for Pages/Sheets based on file type
- bumpversion configuration for automated version management
- BUMPVERSION.md guide for version management workflow
 
### Changed
- GUI now displays appropriate labels (Pages for PDF/DOCX, Sheets for XLSX)
- Provider system enhanced to support multiple file types consistently
 
### Fixed
- Regex filtering now works correctly across all providers (PDF, DOCX, XLSX)

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
 
 