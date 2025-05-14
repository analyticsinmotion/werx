use pyo3::prelude::*;
use pyo3::types::PyAny;
use pyo3::Bound;

/// Extracts a string or list of strings from Python into a Vec<String>
/// Optimized to inline for performance.
#[inline]
pub fn extract_string_list(obj: Bound<PyAny>) -> PyResult<Vec<String>> {
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
