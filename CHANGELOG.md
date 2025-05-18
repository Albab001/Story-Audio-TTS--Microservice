# Changelog

All notable changes to the Story2Audio Microservice project will be documented in this file.

## [Unreleased]

### Added
- Configuration management module (`config.py`) for centralized settings control
- `.gitignore` file to exclude build artifacts and temporary files
- CHANGELOG.md for tracking project changes

### Changed
- Refactored `api/server.py` to use centralized configuration instead of hardcoded values
- Improved code maintainability by moving configuration to a dedicated module

### Fixed
- Configuration values are now easily adjustable via environment variables

## [2025-05-15]

### Added
- CHANGELOG.md file for better project documentation

## [2025-05-12]

### Changed
- Refactored server implementation to use Config class for all settings
- Server now reads port, workers, chunk size, and other parameters from config

## [2025-05-10]

### Added
- `config.py` module with Config class for managing application settings
- Support for environment variable overrides for all configuration parameters

## [2025-05-08]

### Added
- `.gitignore` file to prevent committing build artifacts, temporary files, and sensitive data
