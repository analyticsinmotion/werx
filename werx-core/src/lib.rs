/// werx core library
/// Binds Rust functions to Python module using PyO3.
mod wer;
mod weighted_wer;
mod utils;

use pyo3::prelude::*;
use pyo3::wrap_pyfunction; // Import wrap_pyfunction manually

/// Python module definition
#[pymodule]
fn werx(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(wer::wer, m)?)?;
    m.add_function(wrap_pyfunction!(weighted_wer::weighted_wer, m)?)?;
    Ok(())
}
