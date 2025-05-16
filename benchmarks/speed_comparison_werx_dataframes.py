from datasets import load_dataset
import werx
import werpy
import timeit
from werx.utils import to_pandas, to_polars

# Load the consolidated CSV from the Hugging Face Hub
dataset = load_dataset(
    "analyticsinmotion/librispeech-eval",
    data_files="all_splits.csv",
    split="train"
)

# Specify which split and model/version to evaluate
split = "test-clean"
model_name = "whisper-base"
model_version = "v20240930"

# Filter references and hypotheses for the chosen split/model/version
filtered = dataset.filter(
    lambda x: x["split"] == split and
              x["model_name"] == model_name and
              x["model_version"] == model_version
)

filtered = list(filtered)
references = [str(werpy.normalize(row["reference"])) for row in filtered]
hypotheses = [str(werpy.normalize(row["hypothesis"])) for row in filtered]

# --- Run werx.analysis once for Standard and Weighted ---
results_standard = werx.analysis(references, hypotheses)
results_weighted = werx.analysis(references, hypotheses, insertion_weight=2, deletion_weight=2, substitution_weight=1)

# --- DataFrame conversion tools ---
df_tools = {
    "Pandas (Standard)": lambda: to_pandas(results_standard),
    "Polars (Standard)": lambda: to_polars(results_standard),
    "Pandas (Weighted)": lambda: to_pandas(results_weighted),
    "Polars (Weighted)": lambda: to_polars(results_weighted),
}

# --- Run + time each DataFrame conversion using timeit ---
df_results = []
n_repeats = 10

for name, func in df_tools.items():
    total_time = timeit.timeit(func, number=n_repeats)
    avg_time = total_time / n_repeats
    # Actually create the DataFrame once for display
    df = func()
    df_results.append((name, df, avg_time))

# --- Sort by fastest execution time ---
df_results.sort(key=lambda x: x[2])

# --- Print CLI-friendly table ---
print("\nWERX Analysis: DataFrame Conversion Benchmark (Ordered by Speed)\n")
print(f"{'Method':<20} {'Rows':<8} {'Cols':<6} {'Time (s)':<12}")
print("-" * 50)
for name, df, t in df_results:
    n_rows = len(df)
    n_cols = len(df.columns)
    print(f"{name:<20} {n_rows:<8} {n_cols:<6} {t:.6f}")

# --- Optionally, show a preview of each DataFrame ---
for name, df, _ in df_results:
    print(f"\n{name} DataFrame preview:")
    print(df.head())
