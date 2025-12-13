"""
Comprehensive tests for the analysis() function and related utilities.

This module tests:
- Basic analysis functionality
- Word-level error tracking (insertions, deletions, substitutions)
- Weighted WER in analysis results
- DataFrame conversion utilities (to_polars, to_pandas)
- Edge cases and error handling
"""

import pytest
import werx
from werx.utils import to_polars, to_pandas


class TestBasicAnalysis:
    """Test basic analysis() functionality."""

    # ----------------------------------------------------------------------
    # Test 1
    # Single word substitution - verify WER calculation and word tracking
    # ----------------------------------------------------------------------
    def test_analysis_single_substitution(self):
        """Test analysis with a single word substitution."""
        ref = ["the quick brown fox"]
        hyp = ["the quick brown dog"]

        results = werx.analysis(ref, hyp)

        assert len(results) == 1
        assert results[0].wer == 0.25  # 1 error out of 4 words
        assert results[0].insertions == 0
        assert results[0].deletions == 0
        assert results[0].substitutions == 1
        assert results[0].inserted_words == []
        assert results[0].deleted_words == []
        assert results[0].substituted_words == [("fox", "dog")]

    # ----------------------------------------------------------------------
    # Test 2
    # Single word deletion - verify WER calculation and word tracking
    # ----------------------------------------------------------------------
    def test_analysis_single_deletion(self):
        """Test analysis with a single word deletion."""
        ref = ["i love cold pizza"]
        hyp = ["i love pizza"]

        results = werx.analysis(ref, hyp)

        assert len(results) == 1
        assert results[0].wer == 0.25  # 1 error out of 4 words
        assert results[0].insertions == 0
        assert results[0].deletions == 1
        assert results[0].substitutions == 0
        assert results[0].inserted_words == []
        assert results[0].deleted_words == ["cold"]
        assert results[0].substituted_words == []

    # ----------------------------------------------------------------------
    # Test 3
    # Single word insertion - verify WER calculation and word tracking
    # ----------------------------------------------------------------------
    def test_analysis_single_insertion(self):
        """Test analysis with a single word insertion."""
        ref = ["hello world"]
        hyp = ["hello beautiful world"]

        results = werx.analysis(ref, hyp)

        assert len(results) == 1
        assert results[0].wer == 0.5  # 1 insertion out of 2 reference words
        assert results[0].insertions == 1
        assert results[0].deletions == 0
        assert results[0].substitutions == 0
        assert results[0].inserted_words == ["beautiful"]
        assert results[0].deleted_words == []
        assert results[0].substituted_words == []

    # ----------------------------------------------------------------------
    # Test 4
    # Perfect match - verify zero error rate
    # ----------------------------------------------------------------------
    def test_analysis_perfect_match(self):
        """Test analysis when reference and hypothesis match perfectly."""
        ref = ["the cat sat on the mat"]
        hyp = ["the cat sat on the mat"]

        results = werx.analysis(ref, hyp)

        assert len(results) == 1
        assert results[0].wer == 0.0
        assert results[0].insertions == 0
        assert results[0].deletions == 0
        assert results[0].substitutions == 0
        assert results[0].inserted_words == []
        assert results[0].deleted_words == []
        assert results[0].substituted_words == []

    # ----------------------------------------------------------------------
    # Test 5
    # Multiple errors in single sentence
    # ----------------------------------------------------------------------
    def test_analysis_multiple_errors(self):
        """Test analysis with multiple types of errors."""
        ref = ["the sugar bear character was popular"]
        hyp = ["the sugar bare character was popular"]

        results = werx.analysis(ref, hyp)

        assert len(results) == 1
        assert results[0].substitutions == 1
        assert results[0].substituted_words == [("bear", "bare")]


class TestCorpusAnalysis:
    """Test analysis() with multiple sentences."""

    # ----------------------------------------------------------------------
    # Test 6
    # Multiple sentences with different error types
    # ----------------------------------------------------------------------
    def test_analysis_multiple_sentences(self):
        """Test analysis with a corpus of multiple sentences."""
        ref = [
            "i love cold pizza",
            "the sugar bear character was popular"
        ]
        hyp = [
            "i love pizza",
            "the sugar bare character was popular"
        ]

        results = werx.analysis(ref, hyp)

        assert len(results) == 2

        # First sentence: 1 deletion
        assert results[0].wer == 0.25
        assert results[0].deletions == 1
        assert results[0].deleted_words == ["cold"]

        # Second sentence: 1 substitution
        assert results[1].wer == pytest.approx(0.1667, rel=1e-3)
        assert results[1].substitutions == 1
        assert results[1].substituted_words == [("bear", "bare")]


class TestWeightedAnalysis:
    """Test weighted WER functionality in analysis()."""

    # ----------------------------------------------------------------------
    # Test 7
    # Custom weights - deletion weight higher than others
    # ----------------------------------------------------------------------
    def test_analysis_with_custom_weights(self):
        """Test analysis with custom error weights."""
        ref = ["i love cold pizza"]
        hyp = ["i love pizza"]

        # Deletion weight = 2.0, others = 1.0
        results = werx.analysis(
            ref, hyp,
            insertion_weight=1.0,
            deletion_weight=2.0,
            substitution_weight=1.0
        )

        assert len(results) == 1
        assert results[0].wer == 0.25  # Standard WER
        assert results[0].wwer == 0.5   # Weighted WER (1 deletion * 2.0 / 4)

    # ----------------------------------------------------------------------
    # Test 8
    # Higher insertion weight
    # ----------------------------------------------------------------------
    def test_analysis_weighted_insertion(self):
        """Test analysis with higher insertion weight."""
        ref = ["hello world"]
        hyp = ["hello beautiful world"]

        results = werx.analysis(
            ref, hyp,
            insertion_weight=3.0,
            deletion_weight=1.0,
            substitution_weight=1.0
        )

        assert len(results) == 1
        assert results[0].wer == 0.5     # Standard WER
        assert results[0].wwer == 1.5    # Weighted WER (1 insertion * 3.0 / 2)

    # ----------------------------------------------------------------------
    # Test 9
    # Equal weights should produce same WER and WWER
    # ----------------------------------------------------------------------
    def test_analysis_all_equal_weights(self):
        """Test that equal weights produce same WER and WWER."""
        ref = ["the quick brown fox"]
        hyp = ["the quick brown dog"]

        results = werx.analysis(
            ref, hyp,
            insertion_weight=1.0,
            deletion_weight=1.0,
            substitution_weight=1.0
        )

        assert len(results) == 1
        assert results[0].wer == results[0].wwer


class TestAnalysisResultObject:
    """Test WerAnalysisResult object and its methods."""

    # ----------------------------------------------------------------------
    # Test 10
    # Verify all result object attributes exist
    # ----------------------------------------------------------------------
    def test_analysis_result_attributes(self):
        """Test that WerAnalysisResult has all expected attributes."""
        ref = ["the quick brown fox"]
        hyp = ["the quick brown dog"]

        result = werx.analysis(ref, hyp)[0]

        # Check all attributes exist
        assert hasattr(result, "wer")
        assert hasattr(result, "wwer")
        assert hasattr(result, "ld")
        assert hasattr(result, "n_ref")
        assert hasattr(result, "insertions")
        assert hasattr(result, "deletions")
        assert hasattr(result, "substitutions")
        assert hasattr(result, "inserted_words")
        assert hasattr(result, "deleted_words")
        assert hasattr(result, "substituted_words")

    # ----------------------------------------------------------------------
    # Test 11
    # Verify to_dict() method works correctly
    # ----------------------------------------------------------------------
    def test_analysis_result_to_dict(self):
        """Test converting WerAnalysisResult to dictionary."""
        ref = ["the quick brown fox"]
        hyp = ["the quick brown dog"]

        result = werx.analysis(ref, hyp)[0]
        result_dict = result.to_dict()

        assert isinstance(result_dict, dict)
        assert "wer" in result_dict
        assert "wwer" in result_dict
        assert "ld" in result_dict
        assert "n_ref" in result_dict
        assert "insertions" in result_dict
        assert "deletions" in result_dict
        assert "substitutions" in result_dict
        assert "inserted_words" in result_dict
        assert "deleted_words" in result_dict
        assert "substituted_words" in result_dict

        # Check values
        assert result_dict["wer"] == 0.25
        assert result_dict["substitutions"] == 1


class TestDataFrameConversion:
    """Test DataFrame conversion utilities."""

    # ----------------------------------------------------------------------
    # Test 12
    # Convert single result to Polars DataFrame
    # ----------------------------------------------------------------------
    def test_to_polars_basic(self):
        """Test converting analysis results to Polars DataFrame."""
        polars = pytest.importorskip("polars")

        ref = ["i love cold pizza"]
        hyp = ["i love pizza"]

        results = werx.analysis(ref, hyp)
        df = to_polars(results)

        assert isinstance(df, polars.DataFrame)
        assert len(df) == 1
        assert "wer" in df.columns
        assert "deletions" in df.columns
        assert df["deletions"][0] == 1

    # ----------------------------------------------------------------------
    # Test 13
    # Convert single result to Pandas DataFrame
    # ----------------------------------------------------------------------
    def test_to_pandas_basic(self):
        """Test converting analysis results to Pandas DataFrame."""
        pd = pytest.importorskip("pandas")

        ref = ["i love cold pizza"]
        hyp = ["i love pizza"]

        results = werx.analysis(ref, hyp)
        df = to_pandas(results)

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 1
        assert "wer" in df.columns
        assert "deletions" in df.columns
        assert df.loc[0, "deletions"] == 1

    # ----------------------------------------------------------------------
    # Test 14
    # Convert multiple results to Polars DataFrame
    # ----------------------------------------------------------------------
    def test_to_polars_multiple_rows(self):
        """Test Polars conversion with multiple sentences."""
        polars = pytest.importorskip("polars")

        ref = ["i love cold pizza", "the sugar bear character was popular"]
        hyp = ["i love pizza", "the sugar bare character was popular"]

        results = werx.analysis(ref, hyp)
        df = to_polars(results)

        assert isinstance(df, polars.DataFrame)
        assert len(df) == 2
        assert df["deletions"][0] == 1
        assert df["substitutions"][1] == 1

    # ----------------------------------------------------------------------
    # Test 15
    # Convert multiple results to Pandas DataFrame
    # ----------------------------------------------------------------------
    def test_to_pandas_multiple_rows(self):
        """Test Pandas conversion with multiple sentences."""
        pd = pytest.importorskip("pandas")

        ref = ["i love cold pizza", "the sugar bear character was popular"]
        hyp = ["i love pizza", "the sugar bare character was popular"]

        results = werx.analysis(ref, hyp)
        df = to_pandas(results)

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert df.loc[0, "deletions"] == 1
        assert df.loc[1, "substitutions"] == 1

    # ----------------------------------------------------------------------
    # Test 16
    # Verify Polars DataFrame includes weighted WER column
    # ----------------------------------------------------------------------
    def test_to_polars_with_weights(self):
        """Test Polars conversion includes weighted WER."""
        pytest.importorskip("polars")

        ref = ["i love cold pizza"]
        hyp = ["i love pizza"]

        results = werx.analysis(
            ref, hyp,
            insertion_weight=2,
            deletion_weight=2,
            substitution_weight=1
        )
        df = to_polars(results)

        assert "wwer" in df.columns
        assert df["wer"][0] == 0.25
        assert df["wwer"][0] == 0.5

    # ----------------------------------------------------------------------
    # Test 17
    # Verify Pandas DataFrame includes weighted WER column
    # ----------------------------------------------------------------------
    def test_to_pandas_with_weights(self):
        """Test Pandas conversion includes weighted WER."""
        pytest.importorskip("pandas")

        ref = ["i love cold pizza"]
        hyp = ["i love pizza"]

        results = werx.analysis(
            ref, hyp,
            insertion_weight=2,
            deletion_weight=2,
            substitution_weight=1
        )
        df = to_pandas(results)

        assert "wwer" in df.columns
        assert df.loc[0, "wer"] == 0.25
        assert df.loc[0, "wwer"] == 0.5


class TestEdgeCases:
    """Test edge cases for analysis()."""

    # ----------------------------------------------------------------------
    # Test 18
    # Empty strings should produce zero error rate
    # ----------------------------------------------------------------------
    def test_analysis_empty_strings(self):
        """Test analysis with empty strings."""
        ref = [""]
        hyp = [""]

        results = werx.analysis(ref, hyp)

        assert len(results) == 1
        assert results[0].wer == 0.0
        assert results[0].insertions == 0
        assert results[0].deletions == 0
        assert results[0].substitutions == 0

    # ----------------------------------------------------------------------
    # Test 19
    # Empty hypothesis should produce 100% error (all deletions)
    # ----------------------------------------------------------------------
    def test_analysis_empty_hypothesis(self):
        """Test analysis when hypothesis is empty."""
        ref = ["hello world"]
        hyp = [""]

        results = werx.analysis(ref, hyp)

        assert len(results) == 1
        assert results[0].wer == 1.0  # 100% error (all deletions)
        assert results[0].deletions == 2

    # ----------------------------------------------------------------------
    # Test 20
    # Empty reference with non-empty hypothesis
    # ----------------------------------------------------------------------
    def test_analysis_empty_reference(self):
        """Test analysis when reference is empty."""
        ref = [""]
        hyp = ["hello world"]

        results = werx.analysis(ref, hyp)

        # When reference is empty, WER is undefined (typically infinity or special handling)
        # This tests current behavior - adjust if implementation changes
        assert len(results) == 1

    # ----------------------------------------------------------------------
    # Test 21
    # Mismatched list lengths should raise ValueError
    # ----------------------------------------------------------------------
    def test_analysis_mismatched_lengths(self):
        """Test that analysis raises error for mismatched list lengths."""
        ref = ["sentence one", "sentence two"]
        hyp = ["sentence one"]

        with pytest.raises(ValueError, match="must be the same length"):
            werx.analysis(ref, hyp)

    # ----------------------------------------------------------------------
    # Test 22
    # Invalid input type should raise TypeError or ValueError
    # ----------------------------------------------------------------------
    def test_analysis_invalid_input_type(self):
        """Test that analysis raises error for invalid input types."""
        ref = [12345]  # Invalid: numeric instead of string
        hyp = ["text"]

        with pytest.raises((ValueError, TypeError)):
            werx.analysis(ref, hyp) # type: ignore[arg-type]

    # ----------------------------------------------------------------------
    # Test 23
    # None inputs should raise TypeError or ValueError
    # ----------------------------------------------------------------------
    def test_analysis_none_input(self):
        """Test that analysis raises error for None inputs."""
        with pytest.raises((ValueError, TypeError)):
            werx.analysis(None, ["text"])  # type: ignore[arg-type]

        with pytest.raises((ValueError, TypeError)):
            werx.analysis(["text"], None)  # type: ignore[arg-type]
