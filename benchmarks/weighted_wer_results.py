from werx import weighted_wer

# ----------------------------------------------------------------------
# Test 1: Alias Consistency
# ----------------------------------------------------------------------
ref = ["i love cold pizza"]
hyp = ["i love pizza"]
test1 = weighted_wer(ref, hyp, insertion_weight=0.5, deletion_weight=0.5, substitution_weight=1.0)
print("Test 1 Result:", test1)

# ----------------------------------------------------------------------
# Test 2: Basic Weighted WER with Reduced Insertion and Deletion Weights
# ----------------------------------------------------------------------
ref = ["i love cold pizza"]
hyp = ["i love pizza"]
# 1 deletion, deletion weight = 0.5 → weighted cost = 0.5 / 4 = 0.125
expected_result = 0.125
test2 = weighted_wer(ref, hyp, insertion_weight=0.5, deletion_weight=0.5, substitution_weight=1.0)
print("Test 2 Result:", test2)

# ----------------------------------------------------------------------
# Test 3: Two-Sentence Input with Increased Substitution Weight
# ----------------------------------------------------------------------
ref = ["i love cold pizza", "the sugar bear character was popular"]
hyp = ["i love pizza", "the sugar bare character was popular"]
# 1 deletion, 1 substitution; deletion_weight = 0.5, substitution_weight = 2.0
expected_result = (0.5 + 2.0) / (4 + 6)  # Total words = 10
test3 = weighted_wer(ref, hyp, insertion_weight=0.5, deletion_weight=0.5, substitution_weight=2.0)
print("Test 3 Result:", test3)

# ----------------------------------------------------------------------
# Test 4: Edge Case with Zero Weights (Should Return 0 Regardless of Errors)
# ----------------------------------------------------------------------
ref = ["i love cold pizza"]
hyp = ["i love pizza"]
test4 = weighted_wer(ref, hyp, insertion_weight=0.0, deletion_weight=0.0, substitution_weight=0.0)
print("Test 4 Result:", test4)

# ----------------------------------------------------------------------
# Test 5: All Weights Set to 1 (Equivalent to Standard WER)
# ----------------------------------------------------------------------
ref = ["i love cold pizza"]
hyp = ["i love pizza"]
expected_result = 0.25  # 1 deletion / 4 words
test5 = weighted_wer(ref, hyp)
print("Test 5 Result:", test5)

# ----------------------------------------------------------------------
# Test 6: Invalid Input Types Should Raise Exceptions
# ----------------------------------------------------------------------
try:
    ref = [1, 2, 3]
    hyp = [2, 3, 4]
    test6 = weighted_wer(ref, hyp)
except Exception as e:
    print("Test 6 Result: Exception Raised -", e)

# ----------------------------------------------------------------------
# Test 7: Edge Case with Empty Input Strings — Should Return WER of 0.0
# ----------------------------------------------------------------------
ref = [""]
hyp = [""]
test7 = weighted_wer(ref, hyp)
print("Test 7 Result:", test7)

# ----------------------------------------------------------------------
# Test 8: Mismatched Reference and Hypothesis Lengths
# ----------------------------------------------------------------------
try:
    ref = ["hello world", "another sentence"]
    hyp = ["hello world"]
    test8 = weighted_wer(ref, hyp)
except Exception as e:
    print("Test 8 Result: Exception Raised -", e)

# ----------------------------------------------------------------------
# Test 9: None Inputs Should Raise an Exception
# ----------------------------------------------------------------------
try:
    ref = None
    hyp = ["hello world"]
    test9a = weighted_wer(ref, hyp)
except Exception as e:
    print("Test 9a Result: Exception Raised -", e)

try:
    ref = ["hello world"]
    hyp = None
    test9b = weighted_wer(ref, hyp)
except Exception as e:
    print("Test 9b Result: Exception Raised -", e)


# ----------------------------------------------------------------------
# Test 10: werpy comparison
# ----------------------------------------------------------------------
ref = ['it was beautiful and sunny today']
hyp = ['it was a beautiful and sunny day']
werp = weighted_wer(ref, hyp, insertion_weight=0.5, deletion_weight=0.5, substitution_weight=1)
print("Test 10 Result:", werp)


# ----------------------------------------------------------------------
# Test 11: Heavy Substitution Impact
# ----------------------------------------------------------------------
ref = ["the quick brown fox jumps over the lazy dog multiple times in the evening"]
hyp = ["the fast brown cat leaps across the sleepy dog several times at night"]
# Expect higher impact from substitutions due to synonym replacements
test11 = weighted_wer(ref, hyp, insertion_weight=1.0, deletion_weight=1.0, substitution_weight=3.0)
print("Test 11 (High Substitution Weight) Result:", test11)


# ----------------------------------------------------------------------
# Test 12: Heavy Substitution Impact
# ----------------------------------------------------------------------
ref = ["i love cold pizza", "the sugar bear character was popular"]
hyp = ["i love pizza", "the sugar bare character was popular"]
# 1 deletion, 1 substitution;
test12a = weighted_wer(ref, hyp, insertion_weight=.5, deletion_weight=.5, substitution_weight=2.0)
test12b = weighted_wer(ref, hyp, insertion_weight=1, deletion_weight=1, substitution_weight=1.0)
test12c = weighted_wer(ref, hyp, insertion_weight=2, deletion_weight=2, substitution_weight=1.0)
print("Test 12a Result:", test12a)
print("Test 12b Result:", test12b)
print("Test 12c Result:", test12c)

# ----------------------------------------------------------------------
# Test 13: Example in weighted_wer.py
# ----------------------------------------------------------------------
ref = ['it was beautiful and sunny today', 'tomorrow may not be as nice']
hyp = ['it was a beautiful and sunny day', 'tomorrow may not be as nice']
test13 = weighted_wer(ref, hyp, insertion_weight=0.5, deletion_weight=0.5, substitution_weight=1.0)
print("Test 13 Result:", test13)
