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

## [0.3.0] - 2025-05-16

### Added
- `wer_analysis` module for detailed WER analytics and word-level error breakdown
- New utilities: `to_pandas()` and `to_polars()` for converting analysis results into Pandas and Polars DataFrames.

### Changed
- Added minimum version requirements for all packages in [project.optional-dependencies] in pyproject.toml. This improves dependency management and reduces risk of incompatibility with older package versions.
- Updated `__init__.py` to expose analysis, to_pandas, and to_polars at the top level for easier access.
- Updated README.md to include detailed user guide and instructions for using the analysis() function.
- Documented optional dependency installation steps for Pandas and Polars.
- Included  instructions for converting analysis results to Pandas and Polars DataFrames using the `to_pandas()` and `to_polars()` utilities.

### Fixed
- Added type annotations to all public functions in `utils.py`, resolving Pylance warnings about unknown or missing types.
- Improved docstrings and code comments for better clarity and maintainability.

### Removed
<!-- Add removals/deprecations here -->

---

## [0.2.0] - 2025-05-14

### Added
- Implemented `weighted_wer` functionality to calculate Weighted Word Error Rate with customizable weights for insertion, deletion, and substitution errors.
- Introduced Python API alias `wwer` for convenience alongside `weighted_wer`.
- Created `utils.rs` module containing the shared `extract_string_list` utility function, marked as `pub` and `#[inline]` for performance.
- Added detailed Rust doc comments and Python docstrings, including usage examples and parameter descriptions.
- Introduced `test_weighted_wer.py` with comprehensive unit tests for the `weighted_wer` function.
- Verified correct handling of default and custom weight configurations.
- Added tests for edge cases including zero weights, empty inputs, mismatched lengths, and invalid input types.
- Benchmark script to compare execution speed between `werx.wer` (standard WER) and `werx.weighted_wer` (weighted WER). 
- `weighted_wer_results.py` script to visualize weighted WER results and validate benchmark outputs.

### Changed
- Extracted the `extract_string_list` utility function from `wer.rs` and moved it to a new `utils.rs` module for shared usage.
- Marked `extract_string_list` as `pub` and `#[inline]` for performance and cross-module access.
- Updated `wer.rs` to import `extract_string_list` from `utils.rs`.
- Updated Python `__init__.py` to expose the new `weighted_wer` and `wwer` functions.

---

## [0.1.3] - 2025-05-11

### Added
- Added '[project.urls]' to 'pyproject.toml' for Github repository and issue tracker links.
- Introduced 'keywords' field in 'pyproject.toml' to improve PyPI discoverability.
- Support for the 'evaluate' package in the WER benchmarking script.
- New benchmarking script `benchmarks_librispeech.py` that evaluates and compares the performance and speed of several Word Error Rate (WER) tools using real LibriSpeech evaluation data.
- Results table includes normalized timing, with WERX as the baseline for comparison.

### Changed
- Expanded 'classifiers' in 'pyproject.toml' to show supported python versions and operating systems.

### Fixed
- Fixed a type error in `benchmarks_memory.py` by passing the benchmark function directly to `memory_usage`, ensuring accurate memory profiling for all WER packages.

---

## [0.1.2] - 2025-05-07

### Added
- Explicit inclusion of LICENSE, NOTICE, and README.md files in build artifacts via '[tool.maturin]' include directive to ensure compliance and completeness during packaging.

### Changed
- Renamed Rust crate from 'werx_rust' to 'werx' to align with Python module name
- Simplified module integration by using a unified 'werx' namespace for both Rust and Python.

### Fixed
- PyO3 import warnings about missing 'PyInit_werx_rust'
- Source distribution upload error due to mismatched symbol name

### Removed
- Remove memory-profiler from dependencies in pyproject.toml. This is used only for benchmarking and is an optional dependency.
- Removed '[tool.setuptools]' block from 'pyproject.toml' as it is unused and irrelevant when using 'maturin'. This simplifies the configuration and avoids confusion for future maintainers.

---

## [0.1.1] - 2025-05-07

### Added
- MANIFEST.in to include LICENSE, NOTICE, and key source files in the source distribution (sdist).
- Validation steps in the CI workflow to check .whl and .tar.gz artifacts using zipfile, file, and sha256sum before upload.
- CI logic for verifying the presence of all distribution files prior to publishing.

### Changed
- GitHub Actions CI workflow to use merge-multiple: true for consolidating build artifacts.

### Fixed
- ImportError caused by mismatched Rust module export function (PyInit_werx_rust missing).
- Publishing issues caused by file reuse and broken wheels due to structure mismatches.

### Removed
- Platform suffixes from wheel filenames to ensure compatibility with PyPI’s strict filename parsing and attestation requirements.

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
