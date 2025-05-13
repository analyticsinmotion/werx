from datasets import load_dataset
import werx
import timeit

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
references = [row["reference"] for row in filtered]
hypotheses = [row["hypothesis"] for row in filtered]

# --- WER tools ---
tools = {
    "WERX (Standard)": lambda r, h: werx.wer(r, h),
    "WERX (Weighted)": lambda r, h: werx.weighted_wer(
        r, h, insertion_weight=2.0, deletion_weight=2.0, substitution_weight=1.0
    ),
}

# --- Run + time each tool using timeit ---
results = []
n_repeats = 10  # Number of repeats for timeit

for name, func in tools.items():
    def stmt():
        return func(references, hypotheses)
    total_time = timeit.timeit(stmt, number=n_repeats)
    avg_time = total_time / n_repeats
    wer = func(references, hypotheses)
    results.append((name, wer, avg_time))

# --- Sort by fastest execution time ---
results.sort(key=lambda x: x[2])

# --- Print CLI-friendly table ---
print("\nWERX Benchmark: Standard vs Weighted WER (Ordered by Speed)\n")
print(f"{'Method':<18} {'WER':<8} {'WER (%)':<10} {'Time (s)':<12}")
print("-" * 60)
for name, wer, t in results:
    print(f"{name:<18} {wer:.4f}   {wer*100:6.2f}%   {t:.6f}")
