use pyo3::prelude::*;
use pyo3::types::PyAny;
use pyo3::Bound;
use rayon::prelude::*; // Import Rayon for parallel iteration

/// Compute corpus-level Word Error Rate (WER)
#[pyfunction]
pub fn wer<'py>(py_ref: Bound<'py, PyAny>, py_hyp: Bound<'py, PyAny>) -> PyResult<f64> {
    let refs = extract_string_list(py_ref)?;
    let hyps = extract_string_list(py_hyp)?;

    if refs.len() != hyps.len() {
        return Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(
            "Reference and hypothesis lists must be the same length",
        ));
    }

    // Use Rayon to parallelize the computation
    let (total_distance, total_words) = refs
        .par_iter()
        .zip(hyps.par_iter())
        .map(|(r, h)| {
            let r_tokens: Vec<&str> = r.split_whitespace().collect();
            let h_tokens: Vec<&str> = h.split_whitespace().collect();
            let mut dp = Vec::new(); // Thread-local dp matrix
            let distance = levenshtein_distance(&r_tokens, &h_tokens, &mut dp);
            (distance, r_tokens.len())
        })
        .reduce(
            || (0usize, 0usize), // Identity value for reduction
            |(dist1, words1), (dist2, words2)| (dist1 + dist2, words1 + words2), // Combine results
        );

    Ok(total_distance as f64 / total_words.max(1) as f64) // Avoid divide-by-zero; returns 0.0 if ref is empty
}

/// Levenshtein distance function using dynamic programming
/// Reuses the `dp` matrix to avoid repeated allocations.
#[inline]
fn levenshtein_distance(a: &[&str], b: &[&str], dp: &mut Vec<Vec<usize>>) -> usize {
    let m = a.len();
    let n = b.len();

    // Resize the dp matrix if necessary
    dp.resize(m + 1, vec![0; n + 1]);
    for row in dp.iter_mut() {
        row.resize(n + 1, 0);
    }

    for i in 0..=m {
        dp[i][0] = i;
    }
    for j in 0..=n {
        dp[0][j] = j;
    }

    for i in 1..=m {
        for j in 1..=n {
            let cost = if a[i - 1] == b[j - 1] { 0 } else { 1 };
            dp[i][j] = std::cmp::min(
                std::cmp::min(dp[i - 1][j] + 1, dp[i][j - 1] + 1),
                dp[i - 1][j - 1] + cost,
            );
        }
    }

    dp[m][n]
}

/// Extracts a string or list of strings from Python into a Vec<String>
/// Optimized to inline for performance.
#[inline]
fn extract_string_list(obj: Bound<PyAny>) -> PyResult<Vec<String>> {
    if let Ok(s) = obj.extract::<String>() {
        Ok(vec![s])
    } else if let Ok(vs) = obj.extract::<Vec<String>>() {
        Ok(vs)
    } else {
        Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(
            "Input must be a string or list of strings",
        ))
    }
}
