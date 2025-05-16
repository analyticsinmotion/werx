import werx
from werx.utils import to_polars, to_pandas

# ****************************
# Test 1 - Sentence-Level WER Analysis with Word-Level Errors
# ****************************

ref = [
    'it is consumed domestically and exported to other countries',
    'rufino street in makati right inside the makati central business district',
    'its estuary is considered to have abnormally low rates of dissolved oxygen',
    'he later cited his first wife anita as the inspiration for the song',
    'no one else could claim that'
]

hyp = [
    'it is consumed domestically and exported to other countries',
    'rofino street in mccauti right inside the macasi central business district',
    'its estiary is considered to have a normally low rates of dissolved oxygen',
    'he later sighted his first wife anita as the inspiration for the song',
    'no one else could claim that'
]

results = werx.analysis(ref, hyp)
print("===== Test 1: Full Analysis Results =====")
print(results)

# Inspect detailed word-level analysis for the second sentence (index 1)
first_result = results[1]

print("\n===== Test 1: Detailed Word-Level Errors for Sentence 2 =====")
print("Inserted Words   :", first_result.inserted_words)
print("Deleted Words    :", first_result.deleted_words)
print("Substituted Words:", first_result.substituted_words)


# ****************************
# Test 2 - Simple WER Calculation Example
# ****************************

ref2 = ["this is a test"]
hyp2 = ["this was a test"]
results = werx.analysis(ref2, hyp2)

print("\n===== Test 2: Simple WER Calculation =====")
print(f"WER: {results[0].wer}")

# ****************************
# Test 3 - Weighted WER Calculation Example
# ****************************

ref3 = ["i love cold pizza", "the sugar bear character was popular"]
hyp3 = ["i love pizza", "the sugar bare character was popular"]
results = werx.analysis(ref3, hyp3, insertion_weight=2, deletion_weight=2, substitution_weight=1)

print("\n===== Test 3: Weighted WER Calculation =====")
print(f"Weighted WER (wwer): {results[0].wwer}")

# ****************************
# Test 4 - Results with Polars Example
# ****************************

ref4 = ["i love cold pizza", "the sugar bear character was popular"]
hyp4 = ["i love pizza", "the sugar bare character was popular"]

results = werx.analysis(ref4, hyp4)

# Convert results to Polars DataFrame
df_polars = to_polars(results)

print("\n===== Test 4: Polars DataFrame Output =====")
print(df_polars)

# ****************************
# Test 5 - Weghted WER with Polars Example
# ****************************

results = werx.analysis(ref, hyp, insertion_weight=2, deletion_weight=2, substitution_weight=1)

# Convert results to Polars DataFrame
df_polars = to_polars(results)

print("\n===== Test 5: Polars DataFrame Output =====")
print(df_polars)

# ****************************
# Test 6 - Results with Pandas Example
# ****************************

ref6 = ["i love cold pizza", "the sugar bear character was popular"]
hyp6 = ["i love pizza", "the sugar bare character was popular"]

results = werx.analysis(ref6, hyp6)

# Convert results to Polars DataFrame
df_pandas = to_pandas(results)

print("\n===== Test 4: Pandas DataFrame Output =====")
print(df_pandas)

# ****************************
# Test 7 - Weghted WER with Pandas Example
# ****************************

results = werx.analysis(ref, hyp, insertion_weight=2, deletion_weight=2, substitution_weight=1)

# Convert results to Polars DataFrame
df_pandas = to_pandas(results)

print("\n===== Test 5: Pandas DataFrame Output =====")
print(df_pandas)
