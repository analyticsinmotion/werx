__version__ = "0.2.0"
from .wer import wer
from .weighted_wer import weighted_wer, wwer

__all__ = ["wer", "weighted_wer", "wwer"]