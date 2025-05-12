use pyo3::prelude::*;
use pyo3::types::PyAny;
use pyo3::Bound;
use rayon::prelude::*;
use crate::utils::extract_string_list;

/// Compute corpus-level Weighted Word Error Rate (WER)
///
/// # Arguments
/// - `py_ref`: Reference sentences (str or list of str).
/// - `py_hyp`: Hypothesis sentences (str or list of str).
/// - `insertion_weight`: Weight for insertion errors. Default = 1.0.
/// - `deletion_weight`: Weight for deletion errors. Default = 1.0.
/// - `substitution_weight`: Weight for substitution errors. Default = 1.0.
///
/// # Returns
/// - Weighted WER as `f64`.
/// 
#[pyfunction]
#[pyo3(signature = (py_ref, py_hyp, insertion_weight=1.0, deletion_weight=1.0, substitution_weight=1.0))]
pub fn weighted_wer<'py>(
    py_ref: Bound<'py, PyAny>,
    py_hyp: Bound<'py, PyAny>,
    insertion_weight: f64,
    deletion_weight: f64,
    substitution_weight: f64,
) -> PyResult<f64> {
    let refs = extract_string_list(py_ref)?;
    let hyps = extract_string_list(py_hyp)?;

    if refs.len() != hyps.len() {
        return Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(
            "Reference and hypothesis lists must be the same length",
        ));
    }

    let (total_weighted_distance, total_words) = refs
        .par_iter()
        .zip(hyps.par_iter())
        .map(|(r, h)| {
            let r_tokens: Vec<&str> = r.split_whitespace().collect();
            let h_tokens: Vec<&str> = h.split_whitespace().collect();
            let mut dp = Vec::new();
            let weighted_distance = weighted_levenshtein(
                &r_tokens,
                &h_tokens,
                &mut dp,
                insertion_weight,
                deletion_weight,
                substitution_weight,
            );
            (weighted_distance, r_tokens.len())
        })
        .reduce(
            || (0.0f64, 0usize),
            |(dist1, words1), (dist2, words2)| (dist1 + dist2, words1 + words2),
        );

    Ok(total_weighted_distance / total_words.max(1) as f64)
}

/// Weighted Levenshtein: returns total weighted cost as f64
fn weighted_levenshtein(
    a: &[&str],
    b: &[&str],
    dp: &mut Vec<Vec<f64>>,
    ins_w: f64,
    del_w: f64,
    sub_w: f64,
) -> f64 {
    let m = a.len();
    let n = b.len();

    dp.resize(m + 1, vec![0.0; n + 1]);
    for row in dp.iter_mut() {
        row.resize(n + 1, 0.0);
    }

    for i in 0..=m {
        dp[i][0] = i as f64 * del_w;
    }
    for j in 0..=n {
        dp[0][j] = j as f64 * ins_w;
    }

    for i in 1..=m {
        for j in 1..=n {
            let cost = if a[i - 1] == b[j - 1] { 0.0 } else { sub_w };
            dp[i][j] = (dp[i - 1][j] + del_w)
                .min(dp[i][j - 1] + ins_w)
                .min(dp[i - 1][j - 1] + cost);
        }
    }
    dp[m][n]
}
