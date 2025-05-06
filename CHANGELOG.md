# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
<!-- Add new features here -->

### Changed
<!-- Add changed behavior here -->

### Fixed
<!-- Add bug fixes here -->

### Removed
<!-- Add removals/deprecations here -->

---

## [0.1.0] - 2025-05-05

### Added
- Project scaffolding, maturin integration, and core Python/Rust interface.
- Initial public release of **WERx**: a high-performance Word Error Rate library.
- Pure-Rust backed corpus-level WER computation via PyO3.
- Python wrapper ('wer.py') supporting string and list input formats.
- Benchmarks comparing speed and memory against other python packages.
- Memory benchmark script using 'memory-profiler' with relative usage summary.
- Performance benchmark script using 'time' and 'timeit', including relative speed ratio outputs.
- Test suite using 'pytest', with coverage of valid, blank, and invalid input cases.
- Linting configuration with 'ruff'; type checking setup with 'mypy'.
- Type annotations for the 'wer()' Python API wrapper, improving type checking with 'mypy'.
- Optional dependency groups for 'dev' and 'benchmarks' in 'pyproject.toml'.
- Updated 'README.md' with project description, installation and usage examples.
- 'CHANGELOG.md' formatted to support automation via CI release tooling.
- Introduced a parallel GitHub Actions workflow to validate wheel and sdist builds across Linux, Windows, and macOS without uploading to PyPI. This mirrors the logic and structure of ci.yml, excluding trusted publishing. Useful for testing build artifacts prior to official release.
