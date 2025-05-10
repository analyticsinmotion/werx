from datasets import load_dataset
import werpy
import werx
import jiwer
from torchmetrics.text import WordErrorRate as TorchWER
import pywer
import evaluate
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
references = [werpy.normalize(row["reference"]) for row in filtered]
hypotheses = [werpy.normalize(row["hypothesis"]) for row in filtered]

# --- WER tools ---
wer_metric = evaluate.load("wer")
tools = {
    "WERX": werx.wer,
    "WERPY": werpy.wer,
    "JIWER": jiwer.wer,
    "TORCHMETRICS": lambda r, h: TorchWER()(r, h).item(),
    "PYWER": lambda r, h: pywer.wer(r, h) / 100.0,  # pywer returns percent
    "EVALUATE": lambda r, h: wer_metric.compute(predictions=h, references=r),
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

# --- Normalize by fastest average time ---
min_time = min(r[2] for r in results)
normalized_results = [
    (name, wer, t, t / min_time) for name, wer, t in results
]

# --- Print CLI-friendly table ---
print("\n Word Error Rate Benchmark:\n")
print(f"{'Tool':<15} {'WER':<8} {'WER (%)':<10} {'Time (s)':<12} {'Norm Time':<18}")
print("-" * 70)
for name, wer, t, norm in normalized_results:
    if name == "WERX":
        norm_str = "1.00× (baseline)"
    else:
        norm_str = f"{norm:.2f}× slower"
    print(f"{name:<15} {wer:.4f}   {wer*100:6.2f}%   {t:.6f}   {norm_str:<18}")
