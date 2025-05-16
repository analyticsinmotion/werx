"""
Utility conversion functions for WERX results.

Available Functions:
- to_polars(results): Convert analysis results to a Polars DataFrame.
- to_pandas(results): Convert analysis results to a Pandas DataFrame.
"""
def _asdict(r):
    try:
        return r.to_dict()
    except AttributeError:
        if isinstance(r, dict):
            return r
        raise TypeError(f"Object of type {type(r)} is not convertible to dict")

def to_polars(results):
    """
    Convert analysis results to a Polars DataFrame.
    Requires Polars to be installed: pip install polars
    """
    try:
        import polars as pl
    except ImportError as e:
        raise ImportError("Polars is not installed. Install it using 'pip install polars'.") from e

    return pl.DataFrame([_asdict(r) for r in results])


def to_pandas(results):
    """
    Convert analysis results to a Pandas DataFrame.
    Requires Pandas to be installed: pip install pandas
    """
    try:
        import pandas as pd
    except ImportError as e:
        raise ImportError("Pandas is not installed. Install it using 'pip install pandas'.") from e

    return pd.DataFrame([_asdict(r) for r in results])
