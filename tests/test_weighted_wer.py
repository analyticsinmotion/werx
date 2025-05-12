import pytest
from werx import weighted_wer, wwer

# Alias tests: Ensure both weighted_wer and wwer produce the same results
def test_weighted_wer_alias_consistency():
    ref = ["i love cold pizza"]
    hyp = ["i love pizza"]
    result_full = weighted_wer(ref, hyp, insertion_weight=0.5, deletion_weight=0.5, substitution_weight=1.0)
    result_alias = wwer(ref, hyp, insertion_weight=0.5, deletion_weight=0.5, substitution_weight=1.0)
    assert result_full == result_alias


# ----------------------------------------------------------------------
# Test 1: Basic Weighted WER with Reduced Insertion and Deletion Weights
# ----------------------------------------------------------------------
def test_weighted_wer_basic_weights():
    ref = ["i love cold pizza"]
    hyp = ["i love pizza"]
    # 1 deletion, deletion weight = 0.5 → weighted cost = 0.5 / 4 = 0.125
    expected_result = 0.125
    assert weighted_wer(ref, hyp, insertion_weight=0.5, deletion_weight=0.5, substitution_weight=1.0) == expected_result


# ----------------------------------------------------------------------
# Test 2: Two-Sentence Input with Increased Substitution Weight
# ----------------------------------------------------------------------
def test_weighted_wer_high_substitution_weight():
    ref = ["i love cold pizza", "the sugar bear character was popular"]
    hyp = ["i love pizza", "the sugar bare character was popular"]
    # 1 deletion, 1 substitution; deletion_weight = 0.5, substitution_weight = 2.0
    expected_result = (0.5 + 2.0) / (4 + 6)  # Total words = 10
    assert weighted_wer(ref, hyp, insertion_weight=0.5, deletion_weight=0.5, substitution_weight=2.0) == expected_result


# ----------------------------------------------------------------------
# Test 3: Edge Case with Zero Weights (Should Return 0 Regardless of Errors)
# ----------------------------------------------------------------------
def test_weighted_wer_zero_weights():
    ref = ["i love cold pizza"]
    hyp = ["i love pizza"]
    assert weighted_wer(ref, hyp, insertion_weight=0.0, deletion_weight=0.0, substitution_weight=0.0) == 0.0


# ----------------------------------------------------------------------
# Test 4: All Weights Set to 1 (Equivalent to Standard WER)
# ----------------------------------------------------------------------
def test_weighted_wer_equivalent_to_standard_wer():
    ref = ["i love cold pizza"]
    hyp = ["i love pizza"]
    expected_result = 0.25  # 1 deletion / 4 words
    assert weighted_wer(ref, hyp) == expected_result


# ----------------------------------------------------------------------
# Test 5: Invalid Input Types Should Raise Exceptions
# ----------------------------------------------------------------------
def test_weighted_wer_invalid_input_types():
    ref = [1, 2, 3]
    hyp = [2, 3, 4]
    with pytest.raises(Exception):
        weighted_wer(ref, hyp)


# ----------------------------------------------------------------------
# Test 6: Edge Case with Empty Input Strings — Should Return WER of 0.0
# ----------------------------------------------------------------------
def test_weighted_wer_blank_input():
    ref = [""]
    hyp = [""]
    assert weighted_wer(ref, hyp) == 0.0


# ----------------------------------------------------------------------
# Test 7: Mismatched Reference and Hypothesis Lengths
# ----------------------------------------------------------------------
def test_weighted_wer_mismatched_lengths():
    ref = ["hello world", "another sentence"]
    hyp = ["hello world"]
    with pytest.raises(Exception):
        weighted_wer(ref, hyp)


# ----------------------------------------------------------------------
# Test 8: None Inputs Should Raise an Exception
# ----------------------------------------------------------------------
def test_weighted_wer_with_none_input():
    ref = None
    hyp = ["hello world"]
    with pytest.raises(Exception):
        weighted_wer(ref, hyp)

    ref = ["hello world"]
    hyp = None
    with pytest.raises(Exception):
        weighted_wer(ref, hyp)

