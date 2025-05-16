use pyo3::prelude::*;
use pyo3::types::PyAny;
use pyo3::Bound;
use rayon::prelude::*;
use crate::utils::extract_string_list;

/// Alignment operation
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum Op {
    Match,
    Sub,
    Ins,
    Del,
}

#[pyclass]
pub struct WerAnalysisResult {
    #[pyo3(get)]
    pub wer: f64,
    #[pyo3(get)]
    pub wwer: f64,
    #[pyo3(get)]
    pub ld: usize,
    #[pyo3(get)]
    pub n_ref: usize,
    #[pyo3(get)]
    pub insertions: usize,
    #[pyo3(get)]
    pub deletions: usize,
    #[pyo3(get)]
    pub substitutions: usize,
    #[pyo3(get)]
    pub inserted_words: Vec<String>,
    #[pyo3(get)]
    pub deleted_words: Vec<String>,
    #[pyo3(get)]
    pub substituted_words: Vec<(String, String)>,
}

#[pymethods]
impl WerAnalysisResult {
    pub fn to_dict(&self) -> PyResult<PyObject> {
        Python::with_gil(|py| {
            let dict = pyo3::types::PyDict::new(py);
            dict.set_item("wer", self.wer)?;
            dict.set_item("wwer", self.wwer)?;
            dict.set_item("ld", self.ld)?;
            dict.set_item("n_ref", self.n_ref)?;
            dict.set_item("insertions", self.insertions)?;
            dict.set_item("deletions", self.deletions)?;
            dict.set_item("substitutions", self.substitutions)?;
            dict.set_item("inserted_words", self.inserted_words.clone())?;
            dict.set_item("deleted_words", self.deleted_words.clone())?;
            dict.set_item("substituted_words", self.substituted_words.clone())?;
            Ok(dict.into())
        })
    }
}

#[pyfunction]
#[pyo3(signature = (
    py_ref,
    py_hyp,
    insertion_weight = 1.0,
    deletion_weight = 1.0,
    substitution_weight = 1.0
))]
pub fn analysis<'py>(
    py_ref: Bound<'py, PyAny>,
    py_hyp: Bound<'py, PyAny>,
    insertion_weight: f64,
    deletion_weight: f64,
    substitution_weight: f64,
) -> PyResult<Vec<WerAnalysisResult>> {
    let refs = extract_string_list(py_ref)?;
    let hyps = extract_string_list(py_hyp)?;

    if refs.len() != hyps.len() {
        return Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(
            "Reference and hypothesis lists must be the same length",
        ));
    }

    // Parallelized with Rayon
    let results: Vec<WerAnalysisResult> = refs
        .par_iter()
        .zip(hyps.par_iter())
        .map(|(r, h)| {
            let (ld, ins, dels, subs, ins_words, del_words, sub_words) = align_and_stats(r, h);
            let n_ref = r.split_whitespace().count();
            let wer = ld as f64 / n_ref.max(1) as f64;
            let wwer = (
                insertion_weight * ins as f64 +
                deletion_weight * dels as f64 +
                substitution_weight * subs as f64
            ) / n_ref.max(1) as f64;

            WerAnalysisResult {
                wer,
                wwer,
                ld,
                n_ref,
                insertions: ins,
                deletions: dels,
                substitutions: subs,
                inserted_words: ins_words,
                deleted_words: del_words,
                substituted_words: sub_words,
            }
        })
        .collect();

    Ok(results)
}

/// Returns (levenshtein_distance, insertions, deletions, substitutions, inserted_words, deleted_words, substituted_pairs)
fn align_and_stats(
    ref_str: &str,
    hyp_str: &str,
) -> (usize, usize, usize, usize, Vec<String>, Vec<String>, Vec<(String, String)>) {
    let r_tokens: Vec<&str> = ref_str.split_whitespace().collect();
    let h_tokens: Vec<&str> = hyp_str.split_whitespace().collect();
    let m = r_tokens.len();
    let n = h_tokens.len();

    // DP matrix for distances
    let mut dp = vec![vec![0usize; n + 1]; m + 1];
    // DP matrix for backtrace
    let mut bt = vec![vec![Op::Match; n + 1]; m + 1];

    for i in 0..=m {
        dp[i][0] = i;
        if i > 0 {
            bt[i][0] = Op::Del;
        }
    }
    for j in 0..=n {
        dp[0][j] = j;
        if j > 0 {
            bt[0][j] = Op::Ins;
        }
    }

    for i in 1..=m {
        for j in 1..=n {
            if r_tokens[i - 1] == h_tokens[j - 1] {
                dp[i][j] = dp[i - 1][j - 1];
                bt[i][j] = Op::Match;
            } else {
                let sub = dp[i - 1][j - 1] + 1;
                let ins = dp[i][j - 1] + 1;
                let del = dp[i - 1][j] + 1;
                let min = sub.min(ins.min(del));
                dp[i][j] = min;
                if min == sub {
                    bt[i][j] = Op::Sub;
                } else if min == ins {
                    bt[i][j] = Op::Ins;
                } else {
                    bt[i][j] = Op::Del;
                }
            }
        }
    }

    // Traceback
    let mut i = m;
    let mut j = n;
    let mut insertions = 0;
    let mut deletions = 0;
    let mut substitutions = 0;
    let mut inserted_words = Vec::new();
    let mut deleted_words = Vec::new();
    let mut substituted_words = Vec::new();

    while i > 0 || j > 0 {
        match bt[i][j] {
            Op::Match => {
                i -= 1;
                j -= 1;
            }
            Op::Sub => {
                substitutions += 1;
                substituted_words.push((r_tokens[i - 1].to_string(), h_tokens[j - 1].to_string()));
                i -= 1;
                j -= 1;
            }
            Op::Ins => {
                insertions += 1;
                inserted_words.push(h_tokens[j - 1].to_string());
                j -= 1;
            }
            Op::Del => {
                deletions += 1;
                deleted_words.push(r_tokens[i - 1].to_string());
                i -= 1;
            }
        }
    }

    inserted_words.reverse();
    deleted_words.reverse();
    substituted_words.reverse();

    (
        dp[m][n],
        insertions,
        deletions,
        substitutions,
        inserted_words,
        deleted_words,
        substituted_words,
    )
}
