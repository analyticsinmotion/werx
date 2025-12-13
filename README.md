<!-- markdownlint-disable MD033 MD041 -->
![logo-werx](https://github.com/user-attachments/assets/26701780-4809-433d-9920-38c221bd016b)

<h1 align="center">⚡Lightning fast Word Error Rate Calculations</h1>

<!-- badges: start -->

<div align="center">
  <table>
    <tr>
      <td><strong>Meta</strong></td>
      <td>
        <a href="https://pypi.org/project/werx/"><img src="https://img.shields.io/pypi/v/werx?label=PyPI&color=blue" alt="PyPI version"></a>&nbsp;
        <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.10%7C3.11%7C3.12%7C3.13%7C3.14-blue?logo=python&logoColor=ffdd54" alt="Supports Python 3.10-3.14"></a>&nbsp;
        <a href="https://github.com/analyticsinmotion/werx/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-Apache_2.0-blue.svg" alt="Apache 2.0 License"></a>&nbsp;
        <a href="https://github.com/astral-sh/uv"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json" alt="uv"></a>&nbsp;
        <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff"></a>&nbsp;
        <a href="https://www.rust-lang.org"><img src="https://img.shields.io/badge/Powered%20by-Rust-black?logo=rust&logoColor=white" alt="Powered by Rust"></a>&nbsp;
        <a href="https://github.com/analyticsinmotion"><img src="https://raw.githubusercontent.com/analyticsinmotion/.github/main/assets/images/analytics-in-motion-github-badge-rounded.svg" alt="Analytics in Motion"></a>
        <!-- &nbsp;
        <a href="https://pypi.org/project/werx/"><img src="https://img.shields.io/pypi/dm/werx?label=PyPI%20downloads"></a>&nbsp;
        <a href="https://pepy.tech/project/werx"><img src="https://static.pepy.tech/badge/werx"></a>
        -->
      </td>
    </tr>
  </table>
</div>

<!-- badges: end -->

## What is WERx?

**WERx** is a high-performance Python package for calculating Word Error Rate (WER), built with Rust for unmatched speed, memory efficiency, and stability. WERx delivers accurate results with exceptional performance, making it ideal for large-scale evaluation tasks.

<br/>

## 🚀 Why Use WERx?

⚡ **Blazing Fast:** Rust-powered core delivers outstanding performance, optimized for large datasets<br>

🧩 **Robust:** Designed to handle edge cases gracefully, including empty strings and mismatched sequences<br>

📐 **Insightful:** Provides rich word-level error breakdowns, including substitutions, insertions, deletions, and weighted error rates<br>

🛡️ **Production-Ready:** Minimal dependencies, memory-efficient, and engineered for stability<br>

<br/>

## ⚙️ Installation

You can install WERx either with 'uv' or 'pip'.

### Using uv (recommended)

```bash
uv pip install werx
```

### Using pip

```bash
pip install werx
```

<br/>

## ✨ Usage

### Import the WERx package

*Python Code:*

```python
import werx
```

### Examples

### 1. Single sentence comparison

*Python Code:*

```python
wer = werx.wer('i love cold pizza', 'i love pizza')
print(wer)
```

*Results Output:*

```text
0.25
```

<br/>

### 2. Corpus level Word Error Rate Calculation

*Python Code:*

```python
ref = ['i love cold pizza','the sugar bear character was popular']
hyp = ['i love pizza','the sugar bare character was popular']
wer = werx.wer(ref, hyp)
print(wer)
```

*Results Output:*

```text
0.2
```

<br/>

### 3. Weighted Word Error Rate Calculation

*Python Code:*

```python
ref = ['i love cold pizza', 'the sugar bear character was popular']
hyp = ['i love pizza', 'the sugar bare character was popular']

# Apply lower weight to insertions and deletions, standard weight for substitutions
wer = werx.weighted_wer(
    ref, 
    hyp, 
    insertion_weight=0.5, 
    deletion_weight=0.5, 
    substitution_weight=1.0
)
print(wer)
```

*Results Output:*

```text
0.15
```

<br/>

### 4. Complete Word Error Rate Breakdown

The `analysis()` function provides a complete breakdown of word error rates, supporting both standard WER and weighted WER calculations.

It delivers detailed, per-sentence metrics—including insertions, deletions, substitutions, and word-level error tracking, with the flexibility to customize error weights.

Results are easily accessible through standard Python objects or can be conveniently converted into Pandas and Polars DataFrames for further analysis and reporting.

#### 4a. Getting Started

*Python Code:*

```python
ref = ["the quick brown fox"]
hyp = ["the quick brown dog"]

results = werx.analysis(ref, hyp)

print("Inserted:", results[0].inserted_words)
print("Deleted:", results[0].deleted_words)
print("Substituted:", results[0].substituted_words)

```

*Results Output:*

```text
Inserted Words   : []
Deleted Words    : []
Substituted Words: [('fox', 'dog')]
```

<br/>

#### 4b. Converting Analysis Results to a DataFrame

*Note:* To use this module, you must have either `pandas` or `polars` (or both) installed.

#### Install Pandas / Polars for DataFrame Conversion

```python
uv pip install pandas
uv pip install polars
```

*Python Code:*

```python
ref = ["i love cold pizza", "the sugar bear character was popular"]
hyp = ["i love pizza", "the sugar bare character was popular"]
results = werx.analysis(
    ref, hyp,
    insertion_weight=2,
    deletion_weight=2,
    substitution_weight=1
)
```

We have created a special utility to make working with DataFrames seamless.
Just import the following helper:

```python
import werx
from werx.utils import to_polars, to_pandas
```

You can then easily convert analysis results to get output using **Polars**:

```python
# Convert to Polars DataFrame
df_polars = to_polars(results)
print(df_polars)
```

Alternatively, you can also use **Pandas** depending on your preference:

```python
# Convert to Pandas DataFrame
df_pandas = to_pandas(results)
print(df_pandas)
```

*Results Output:*

| wer    | wwer   | ld  | n_ref | insertions | deletions | substitutions | inserted_words | deleted_words | substituted_words   |
|--------|--------|-----|-------|------------|-----------|---------------|----------------|----------------|---------------------|
| 0.25   | 0.50   | 1   | 4     | 0          | 1         | 0             | []             | ['cold']       | []                  |
| 0.1667 | 0.1667 | 1   | 6     | 0          | 0         | 1             | []             | []             | [('bear', 'bare')]   |

<br/>

## 🚀 Performance Benchmarks

WERx was benchmarked on the **LibriSpeech test sets** (industry-standard ASR benchmark) evaluating OpenAI Whisper-base transcriptions:

| Dataset | Utterances | Total Time (ms) | Throughput |
|---------|------------|-----------------|------------|
| test-clean | 2,620 | 3.35 | 781,791 utt/s |
| test-other | 2,939 | 2.78 | 1,057,194 utt/s |
| **Combined** | **5,559** | **6.13** | **~907,000 utt/s** |

### What This Means in Practice

**Evaluating ASR at scale (WER computation only):**

- 1 million utterances: **~1.1 seconds** at ~907,000 utt/s
- 1-hour podcast (~3,000 utterances): **~3.3 ms** of WER computation
- Large corpora (millions of utterances): **seconds, not hours**

### Technical Performance

**Memory Efficiency:**

- Effective space complexity: **O(n)** per sequence vs O(m×n) traditional implementations
- Rolling window algorithm reduces memory by 5-50× for typical sentence lengths (10-40 tokens)

**Parallelization:**

- Rayon-based automatic multi-core scaling
- Near-linear speedup with CPU cores

### Running Benchmarks Yourself

```bash
# Install with benchmark dependencies
uv pip install werx[benchmarks]

# Run full LibriSpeech benchmark
uv run benchmarks/speed_comparison_librispeech_full.py
```

See the [`benchmarks/`](benchmarks/) directory for all benchmark scripts.

> 📊 **Benchmark Details**: [LibriSpeech](https://www.openslr.org/12/) test-clean + test-other (5,559 utterances), OpenAI Whisper-base (v20240930), Python 3.14.2, averaged over 10 runs
>
> **Environment**: 16-core (24 threads) CPU, 64 GB RAM, NVMe SSD; single process, all data in RAM. Results are CPU-bound; no GPU is used for WER.

<br/>

## 📄 License

This project is licensed under the Apache License 2.0.
