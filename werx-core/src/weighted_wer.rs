use pyo3::prelude::*;
use pyo3::types::PyAny;
use pyo3::Bound;
use rayon::prelude::*;
use crate::utils::extract_string_list;

/// Compute corpus-level **Weighted Word Error Rate (WER)** using weighted dynamic programming.
///
/// # Arguments
/// * `py_ref` - Reference sentences (string or list of strings)
/// * `py_hyp` - Hypothesis sentences (string or list of strings)
/// * `insertion_weight` - Weight assigned to insertion errors (default: 1.0)
/// * `deletion_weight` - Weight assigned to deletion errors (default: 1.0)
/// * `substitution_weight` - Weight assigned to substitution errors (default: 1.0)
///
/// # Returns
/// * Weighted Word Error Rate (WER) as a floating-point `f64`
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

    // Early exit optimization
    if refs == hyps {
        return Ok(0.0);
    }

    if refs.len() != hyps.len() {
        return Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(
            "Reference and hypothesis lists must be the same length",
        ));
    }

    let (total_weighted_cost, total_words) = refs
        .par_iter()
        .zip(hyps.par_iter())
        .map(|(r, h)| {
            let r_tokens: Vec<&str> = r.split_whitespace().collect();
            let h_tokens: Vec<&str> = h.split_whitespace().collect();

            let cost = weighted_cost_levenshtein(
                &r_tokens,
                &h_tokens,
                insertion_weight,
                deletion_weight,
                substitution_weight,
            );

            (cost, r_tokens.len())
        })
        .reduce(
            || (0.0f64, 0usize),
            |(c1, w1), (c2, w2)| (c1 + c2, w1 + w2),
        );

    Ok(total_weighted_cost / total_words.max(1) as f64)
}

/// Compute the **minimum weighted cost** between two tokenized sequences using 
/// the Weighted Levenshtein Distance algorithm.
///
/// This implementation calculates only the final weighted cost, avoiding the need to 
/// track or backtrack individual edit operations. It uses a rolling two-row dynamic 
/// programming (DP) array to minimize memory usage.
///
/// # Arguments
/// * `a` - Tokenized reference sequence (slice of string slices).
/// * `b` - Tokenized hypothesis sequence (slice of string slices).
/// * `ins_w` - Weight assigned to insertion errors.
/// * `del_w` - Weight assigned to deletion errors.
/// * `sub_w` - Weight assigned to substitution errors.
///
/// # Returns
/// * Final weighted cost as an `f64` representing the minimal cost to transform `a` into `b`.
///
fn weighted_cost_levenshtein(
    a: &[&str],
    b: &[&str],
    ins_w: f64,
    del_w: f64,
    sub_w: f64,
) -> f64 {
    let m = a.len();
    let n = b.len();

    if m == 0 {
        return n as f64 * ins_w;
    }
    if n == 0 {
        return m as f64 * del_w;
    }

    let mut prev = vec![0.0; n + 1];
    let mut curr = vec![0.0; n + 1];

    for j in 0..=n {
        prev[j] = j as f64 * ins_w;
    }

    for i in 1..=m {
        curr[0] = i as f64 * del_w;
        for j in 1..=n {
            if a[i - 1] == b[j - 1] {
                curr[j] = prev[j - 1]; // No cost for a match
            } else {
                let ins = curr[j - 1] + ins_w;
                let del = prev[j] + del_w;
                let sub = prev[j - 1] + sub_w;
                curr[j] = ins.min(del).min(sub);
            }
        }
        std::mem::swap(&mut prev, &mut curr);
    }

    prev[n] // Final weighted cost
}
