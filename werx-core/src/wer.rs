use pyo3::prelude::*;
use pyo3::types::PyAny;
use pyo3::Bound;
use rayon::prelude::*;
use crate::utils::extract_string_list;

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
            let distance = levenshtein_distance(&r_tokens, &h_tokens);
            (distance, r_tokens.len())
        })
        .reduce(
            || (0usize, 0usize), // Identity value for reduction
            |(dist1, words1), (dist2, words2)| (dist1 + dist2, words1 + words2), // Combine results
        );

    Ok(total_distance as f64 / total_words.max(1) as f64) // Avoid divide-by-zero; returns 0.0 if ref is empty
}

/// Levenshtein distance using space-optimized rolling window dynamic programming.
/// Maintains only two rows (previous and current) to minimize memory allocations.
fn levenshtein_distance(a: &[&str], b: &[&str]) -> usize {
    let m = a.len();
    let n = b.len();
    
    if m == 0 { return n; }
    if n == 0 { return m; }
    
    let mut prev = vec![0usize; n + 1];
    let mut curr = vec![0usize; n + 1];
    
    for j in 0..=n {
        prev[j] = j;
    }
    
    for i in 1..=m {
        curr[0] = i;
        for j in 1..=n {
            if a[i - 1] == b[j - 1] {
                curr[j] = prev[j - 1];
            } else {
                curr[j] = prev[j].min(curr[j - 1]).min(prev[j - 1]) + 1;
            }
        }
        std::mem::swap(&mut prev, &mut curr);
    }
    
    prev[n]
}
