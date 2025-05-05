import pytest
from werx import wer

# ----------------------------------------------------------------------
# Test 1
# Basic test with small candidate set (default sort path)
# ----------------------------------------------------------------------
def test_wer_example_1():
    assert wer("i love cold pizza", "i love pizza") == 0.25


# ----------------------------------------------------------------------
# Test 2
# Two-sentence input, moderate substitution test
# ----------------------------------------------------------------------
def test_wer_example_2():
    ref = ["i love cold pizza", "the sugar bear character was popular"]
    hyp = ["i love pizza", "the sugar bare character was popular"]
    expected_result = 0.2
    assert wer(ref, hyp) == expected_result


# ----------------------------------------------------------------------
# Test 3
# Larger corpus test with known substitutions, insertions, deletions
# ----------------------------------------------------------------------
def test_wer_example_3():
    ref = [
        "it is consumed domestically and exported to other countries",
        "the sugar bear character was popular enough to have occasional premium toys",
        "it is one of the most watched television networks in the country",
        "it could be carried and prepared by the individual soldier",
        "he was executed in a lubyanka prison cellar",
        "rufino street in makati right inside the makati central business district",
        "its estuary is considered to have abnormally low rates of dissolved oxygen",
        "he later cited his first wife anita as the inspiration for the song",
        "gadya is the nearest rural locality",
        "taxes are a tool in the adjustment of the economy",
    ]
    hyp = [
        "it is consumed domestically and exported to other countries",
        "the sugar bare character was popular enough to have occasional premium toys",
        "it is one of the most watched television networks in the country",
        "it could be carried and prepared by the individual soldier",
        "he was executed in alabianca prison seller",
        "rofino street in mccauti right inside the macasi central business district",
        "its estiary is considered to have a normally low rates of dissolved oxygen",
        "he later sighted his first wife anita as the inspiration for the song",
        "gadia is the nearest rural locality",
        "taxes are a tool in the adjustment of the economy",
    ]
    expected_result = 0.11650485436893204
    assert wer(ref, hyp) == expected_result


# ----------------------------------------------------------------------
# Test 4
# Invalid input type (numerical input), should raise exception
# ----------------------------------------------------------------------
def test_wer_numerical_input_returns_none():
    ref = [1, 2, 3, 4]
    hyp = [2, 3, 3, 3]
    with pytest.raises(Exception):
        wer(ref, hyp)


# ----------------------------------------------------------------------
# Test 5
# Edge case with empty input strings — should return WER of 0.0
# ----------------------------------------------------------------------
def test_wer_blank_input():
    ref = [""]
    hyp = [""]
    assert wer(ref, hyp) == 0.0

# ----------------------------------------------------------------------
# Test 6
# Mismatched lengths between ref and hyp should raise an exception
# ----------------------------------------------------------------------
def test_wer_mismatched_lengths():
    ref = ["hello world", "another sentence"]
    hyp = ["hello world"]  # shorter
    with pytest.raises(Exception):
        wer(ref, hyp)

# ----------------------------------------------------------------------
# Test 7
# None inputs should raise a TypeError or similar
# ----------------------------------------------------------------------
def test_wer_with_none_input():
    ref = None
    hyp = ["hello world"]
    with pytest.raises(Exception):
        wer(ref, hyp)

    ref = ["hello world"]
    hyp = None
    with pytest.raises(Exception):
        wer(ref, hyp)
