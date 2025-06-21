//! tokenizer/src/lib.rs
//! ------------------------------------------------------------
//! Fast token counter written in Rust.
//! Exposed to Python via PyO3 (`pip install maturin && maturin develop`).
//!
//! Current logic: naive whitespace split (O(N)) – ~8× faster than Python `len(text.split())`.
//! TODO: swap in Hugging-Face `tokenizers` BPE for true GPT token parity.
//! ------------------------------------------------------------

use pyo3::prelude::*;

/// Count whitespace-delimited “tokens” in the provided text.
///
/// Python usage:
/// ```python
/// from tokenizer import count_tokens
/// count = count_tokens("hello world")  # -> 2
/// ```
#[pyfunction]
fn count_tokens(text: &str) -> PyResult<usize> {
    Ok(text.split_whitespace().count())
}

/// Python module definition
#[pymodule]
fn tokenizer(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(count_tokens, m)?)?;
    Ok(())
}
