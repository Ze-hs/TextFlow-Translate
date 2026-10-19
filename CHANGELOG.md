# Changelog

All notable changes to this project will be documented in this file.

## [0.0.2]

- Added CLI argument parsing with argparse.
- Added SQLite database support for translation jobs and chunks.
- Added job and chunk status tracking.
- Added commands for preparing, translating, listing, checking, exporting, and deleting jobs.
- Added support for resuming unfinished translation jobs.
- Added error handling for failed translation chunks.

### Changed
- Updated the translation workflow to use stored jobs and chunks.

## [0.0.1]

### Added

- Initial version of the translation application.
- Basic text chunking and translation through OpenRouter.
- Configuration and logging support.