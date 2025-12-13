<!-- markdownlint-disable MD024 -->
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.3.1] - 2025-12-13

### Added

- Added official support for Python 3.14 across project metadata and CI pipelines.
- Added universal-edit-distance (v0.4.3) as an additional WER baseline in benchmarking scripts.
- Integrated `ued.word_error_rate(refs, hyps)` into `benchmarks/speed_comparison_librispeech_data.py` for runtime comparison.
- Integrated universal-edit-distance into `benchmarks/memory_comparison_synthetic_data.py` for peak memory usage comparison.
- Added an explicit `[profile.dev]` configuration to align optimization settings with release builds while retaining debug symbols.

### Changed

- Optimized standard WER calculation by replacing full O(m×n) matrix allocation with space-efficient rolling window approach, reducing memory usage from O(m×n) to O(n) and improving performance.
- Updated `pyproject.toml`, `CI.yml`, and `ci-check.yml` to test and build against Python 3.14.
- Updated Rust dependencies: pyo3 to 0.27.2 and rayon to 1.11.0.
- Updated PyO3 usage in `wer_analysis.rs` to replace deprecated `PyObject` with `Py<PyAny>`.
- Replaced deprecated `Python::with_gil` with `Python::attach` to align with PyO3 0.27.x APIs.
- Enabled symbol stripping in `[profile.release]` to reduce PyPI wheel size.
- Aligned LTO, codegen units, and optimization level across dev and release profiles for consistent performance characteristics.
- Updated development dependencies to latest versions, including maturin, pytest, mypy, and ruff.
- Updated dataframe dependencies to latest versions of polars and pandas.
- Updated benchmark dependencies to latest versions, including jiwer, evaluate, datasets, and related tooling.
- Temporarily disabled torchmetrics and universal-edit-distance benchmarks due to missing Python 3.14 wheels.
- Updated benchmark scripts to run cleanly on Python 3.14 without torch-based dependencies.
- Updated weighted WER test script to suppress static type checker errors for intentional invalid input test cases.
- Refactored `align_and_stats` function in `wer_analysis.rs` to return a named `AlignmentStats` struct instead of a complex 7-element tuple, improving code readability and resolving Clippy type complexity warnings with zero performance impact.
- Added `speed_comparison_librispeech_full.py` benchmark script to evaluate WERx performance across both LibriSpeech test-clean and test-other datasets (5,559 total utterances), providing comprehensive real-world performance metrics for README documentation.

### Fixed

- Removed PyO3 deprecation warnings during Rust extension compilation.

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
- Included instructions for converting analysis results to Pandas and Polars DataFrames using the `to_pandas()` and `to_polars()` utilities.

### Fixed

- Added type annotations to all public functions in `utils.py`, resolving Pylance warnings about unknown or missing types.
- Improved docstrings and code comments for better clarity and maintainability.

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
