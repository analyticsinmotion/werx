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

<br/>

## 📄 License

This project is licensed under the Apache License 2.0.



