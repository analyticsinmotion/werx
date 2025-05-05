# WERx

## What is WERx?

**WERx** is a high-performance Python package for calculating the Word Error Rate (WER), backed by a Rust core. Designed for speed, safety, and production-grade robustness, it supports both corpus-level and sentence-level WER, as well as weighted variations and diagnostic summaries.

## 🚀 Why Use WERx?

- ⚡ **Fast:** Rust-powered core outperforms many pure Python implementations  
- 🧪 **Accurate:** Deterministic and tested across thousands of examples  
- 🔒 **Safe:** Handles edge cases gracefully (empty strings, mismatched lengths, etc.)  
- 🔧 **Flexible:** Supports weighted insertions, deletions, substitutions  
- 📊 **Insightful:** Sentence-level breakdowns and alignment diagnostics available

## 🧩 Installation

You can install WERx either with 'uv' or 'pip'.

### Using 'uv' (recommended for modern workflows):
```bash
uv pip install werx
```

### Using pip:
```bash
pip install werx
```

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


## 📄 License

This project is licensed under the Apache License 2.0.



