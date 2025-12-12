from .werx import wer as _wer

def wer(ref: str | list[str], hyp: str | list[str]) -> float:
    """
    Calculate Word Error Rate (WER) between reference and hypothesis texts.

    WER is computed as (insertions + deletions + substitutions) / total_words_in_reference.
    Lower values indicate better accuracy, with 0.0 being a perfect match.

    Args:
        ref: Reference text(s). Can be a single string or list of strings.
        hyp: Hypothesis text(s). Can be a single string or list of strings.
             Must match the type and length of ref.

    Returns:
        float: Word Error Rate as a decimal (0.0 to infinity).
               - 0.0 = perfect match
               - 1.0 = 100% error rate
               - Values > 1.0 possible when insertions exceed reference length

    Raises:
        ValueError: If ref and hyp have different lengths (when lists).
        TypeError: If inputs are not strings or lists of strings.

    Examples:
        >>> import werx
        >>> werx.wer('i love cold pizza', 'i love pizza')
        0.25

        >>> ref = ['i love cold pizza', 'the cat sat']
        >>> hyp = ['i love pizza', 'the cat sat']
        >>> werx.wer(ref, hyp)
        0.14285714285714285
    """
    return _wer(ref, hyp)