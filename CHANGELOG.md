# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.2.8] - 2025-01-15

### Added
- Enhanced local environment with security controls and command tracking
- Token usage monitoring and cost tracking system
- Comprehensive project documentation
- EditorConfig for consistent code style
- Improved error handling and timeout management

### Changed
- Updated project metadata and package configuration
- Enhanced environment configuration with resource limits
- Improved logging system with structured output

### Security
- Added command blocking for dangerous operations (rm -rf, format, etc.)
- Implemented output size limits to prevent memory issues
- Added timeout handling for long-running commands

### Performance
- Command execution history tracking
- Statistics collection for optimization
- Caching support for repeated operations

## [2.2.7] - 2024-12-20

### Fixed
- Fixed issue with credential storage on Windows
- Improved Docker container cleanup

### Changed
- Updated LiteLLM dependency requirements

## [2.2.6] - 2024-12-01

### Added
- Support for new model providers
- Batch processing improvements

### Fixed
- Memory leak in trajectory browser
