#from .werx_rust import wer as _wer
from .werx import wer as _wer

def wer(ref: str | list[str], hyp: str | list[str]) -> float:
    return _wer(ref, hyp)