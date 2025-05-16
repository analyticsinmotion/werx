from .werx import analysis as _analysis  # Rust binding

def analysis(
    ref: str | list[str],
    hyp: str | list[str],
    insertion_weight: float = 1.0,
    deletion_weight: float = 1.0,
    substitution_weight: float = 1.0
) -> list:
    """
    Perform detailed WER analysis with alignment and error tracking.

    Parameters
    ----------
    ref : str | list[str]
        Reference sentence(s). Single string or list of sentences.
    hyp : str | list[str]
        Hypothesis sentence(s). Single string or list of sentences.
    insertion_weight : float, default=1.0
        Weight for insertion errors.
    deletion_weight : float, default=1.0
        Weight for deletion errors.
    substitution_weight : float, default=1.0
        Weight for substitution errors.

    Returns
    -------
    list of WerAnalysisResult objects (Rust-backed class)

    Example
    -------
    >>> ref = ["this is a test"]
    >>> hyp = ["this was a test"]
    >>> results = analysis(ref, hyp)
    >>> print(results[0].wer)
    0.25
    """
    return _analysis(ref, hyp, insertion_weight, deletion_weight, substitution_weight)
