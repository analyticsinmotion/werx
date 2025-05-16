![logo-werx](https://github.com/user-attachments/assets/26701780-4809-433d-9920-38c221bd016b)

<h1 align="center">⚡Lightning fast Word Error Rate Calculations</h1>


<!-- badges: start -->

<div align="center">
  <table>
    <tr>
      <td><strong>Meta</strong></td>
      <td>
        <a href="https://pypi.org/project/werx/"><img src="https://img.shields.io/pypi/v/werx?label=PyPI&color=blue"></a>&nbsp;
        <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.10%7C3.11%7C3.12%7C3.13-blue?logo=python&logoColor=ffdd54"></a>&nbsp;
        <a href="https://github.com/analyticsinmotion/werx/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-Apache_2.0-blue.svg"></a>&nbsp;
        <a href="https://github.com/astral-sh/uv"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json" alt="uv"></a>&nbsp;
        <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff"></a>&nbsp;
        <a href="https://www.rust-lang.org"><img src="https://img.shields.io/badge/Powered%20by-Rust-black?logo=rust&logoColor=white" alt="Powered by Rust"></a>&nbsp;
        <a href="https://www.analyticsinmotion.com"><img src="https://raw.githubusercontent.com/analyticsinmotion/.github/main/assets/images/analytics-in-motion-github-badge-rounded.svg" alt="Analytics in Motion"></a>
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

📐 **Accurate:** Carefully tested to ensure consistent and reliable results<br>

🛡️ **Production-Ready:** Minimal dependencies, memory-efficient, and engineered for stability<br> 

<br/>

## ⚙️ Installation

You can install WERx either with 'uv' or 'pip'.

### Using uv (recommended):
```bash
uv pip install werx
```

### Using pip:
```bash
pip install werx
```

<br/>

## ✨ Usage
**Import the WERx package**

*Python Code:*
```python
import werx
```

### Examples:

#### 1. Single sentence comparison

*Python Code:*
```python
wer = werx.wer('i love cold pizza', 'i love pizza')
print(wer)
```

*Results Output:*
```
0.25
```

#### 2. Corpus level Word Error Rate Calculation

*Python Code:*
```python
ref = ['i love cold pizza','the sugar bear character was popular']
hyp = ['i love pizza','the sugar bare character was popular']
wer = werx.wer(ref, hyp)
print(wer)
```

*Results Output:*
```
0.2
```

#### 3. Weighted Word Error Rate Calculation

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
```
0.15
```

#### 4. Complete Word Error Rate Breakdown

The `analysis()` function provides a complete breakdown and detailed, per-sentence metrics.

#### Basic Example

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
```
Inserted Words   : []
Deleted Words    : []
Substituted Words: [('fox', 'dog')]
```

#### View full dataframe Example

**Note:** To use this module, you must have either `pandas` or `polars` (or both) installed.

#### Install Pandas / Polars for DataFrame Conversion

```python
uv pip install pandas
uv pip install polars
```

*Python Code:*
```python
results = werx.analysis(
    ref, hyp,
    insertion_weight=2,
    deletion_weight=2,
    substitution_weight=1
)
```

Get ouput dataframe using Polars
```python
# Convert to Polars DataFrame
df_polars = werx.to_polars(results)
print(df_polars)
```

Alternatively, get ouput dataframe using Polars
```python
# Convert to Pandas DataFrame
df_pandas = werx.to_pandas(results)
print(df_pandas)
```

#### Example Output (DataFrame)

| wer   | wwer  | ld  | n_ref | insertions | deletions | substitutions | inserted_words | deleted_words | substituted_words          |
|-------|-------|-----|-------|------------|-----------|---------------|----------------|----------------|----------------------------|
| 0.25  | 0.50  | 1   | 4     | 0          | 0         | 1             | []             | []             | [('brown', 'dog')]          |
| 0.33  | 0.66  | 2   | 6     | 1          | 0         | 1             | ['cold']       | []             | [('bear', 'bare')]          |

---

<br/>

## 📄 License

This project is licensed under the Apache License 2.0.



