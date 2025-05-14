from .werx import weighted_wer as _weighted_wer

def weighted_wer(
    ref: str | list[str],
    hyp: str | list[str],
    insertion_weight: float = 1.0,
    deletion_weight: float = 1.0,
    substitution_weight: float = 1.0
) -> float:
    """
    Compute the Weighted Word Error Rate (WER).

    Parameters:
    ----------
    ref : str | list[str]
        Reference text(s). Can be a single string or a list of sentences.
    hyp : str | list[str]
        Hypothesis text(s). Can be a single string or a list of sentences.
    insertion_weight : float, default=1.0
        Weight assigned to insertion errors.
    deletion_weight : float, default=1.0
        Weight assigned to deletion errors.
    substitution_weight : float, default=1.0
        Weight assigned to substitution errors.

    Returns:
    -------
    float
        Weighted Word Error Rate (WER) score.

    Example:
    --------
    >>> ref = ['it was beautiful and sunny today', 'tomorrow may not be as nice']
    >>> hyp = ['it was a beautiful and sunny day', 'tomorrow may not be as nice']
    >>> weighted_wer(ref, hyp, insertion_weight=0.5, deletion_weight=0.5, substitution_weight=1.0)
    0.125
    """
    return _weighted_wer(ref, hyp, insertion_weight, deletion_weight, substitution_weight)

# Alias
wwer = weighted_wer
