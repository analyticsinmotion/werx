import time
import timeit
import werpy
import werx
import jiwer
import pywer
from torchmetrics.text import WordErrorRate

# --- Test Data (Repeated 10,000 times) ---
reference_translation = [
    '     It is consumed domestically           and exported to other countries.     ',
    'The Sugar Bear character was popular enough to have occasional premium toys.',
    'It is one of the most watched television networks in the country.',
    'It could be carried and prepared by the individual soldier.',
    'He was executed in a Lubyanka prison cellar.',
    'Rufino Street in Makati, right inside the Makati Central Business District.',
    'Its estuary is considered to have abnormally low rates of dissolved oxygen.',
    'He later cited his first wife Anita as the inspiration for the song.',
    'Gadya is the nearest rural locality.',
    'Taxes are a tool in the adjustment of the economy.'
] * 10000

hypothesis_translation = [
    'it is consumed domestically and exported to other countries ',
    'the sugar bare character was popular enough to have occasional premium toys ',
    'it is one of the most watched television networks in the country ',
    'it could be carried and prepared by the individual soldier ',
    'he was executed in alabianca prison seller ',
    'rofino street in mccauti right inside the macasi central business district ',
    "it's estiary is considered to have a normally low rates of dissolved oxygen ",
    'he later sighted his first wife anita as the inspiration for the song ',
    'gadia is the nearest rural locality ',
    'taxes are a tool in the adjustment of the economy '
] * 10000

# Normalize using werpy (as common preprocessing)
ref = werpy.normalize(reference_translation)
hyp = werpy.normalize(hypothesis_translation)

# --- Function Definitions ---
def wer_werpy(ref, hyp):
    return werpy.wer(ref, hyp)

def wer_werx(ref, hyp):
    return werx.wer(ref, hyp)

def wer_jiwer(ref, hyp):
    return jiwer.wer(ref, hyp)

def wer_pywer(ref, hyp):
    return pywer.wer(ref, hyp)

def wer_torchmetrics(ref, hyp):
    metric = WordErrorRate()
    score = metric(ref, hyp)
    return score.item()

package_funcs = {
    "werpy": wer_werpy,
    "werx": wer_werx,
    "jiwer": wer_jiwer,
    "pywer": wer_pywer,
    "torchmetrics": wer_torchmetrics,
}

# --- Benchmarks ---
results_perf = {}
results_timeit = {}

print(f"Running benchmark with {len(ref)} examples...\n")

print("⏱ perf_counter() timings:")
for name, func in package_funcs.items():
    try:
        start = time.perf_counter()
        wer = func(ref, hyp)
        end = time.perf_counter()
        duration = end - start
        results_perf[name] = (duration, wer)
        print(f"{name}.wer took: {duration:.4f} seconds, WER: {wer:.4f}")
    except Exception as e:
        print(f"{name} failed during perf_counter timing: {e}")
        results_perf[name] = (None, None)

print("\n📊 timeit comparisons:")
for name, func in package_funcs.items():
    try:
        t = timeit.timeit(lambda: func(ref, hyp), number=1)
        results_timeit[name] = t
        print(f"{name}.wer took: {t:.4f} seconds")
    except Exception as e:
        print(f"{name} failed during timeit timing: {e}")
        results_timeit[name] = None

# --- Relative Speed Summary ---
print("\n📈 Relative performance (based on timeit):")
baseline_name = "werx"
baseline_time = results_timeit.get(baseline_name)

if baseline_time is not None:
    for name, t in results_timeit.items():
        if t is None:
            continue
        if name == baseline_name:
            print(f"{name}: baseline")
        else:
            ratio = t / baseline_time
            if ratio > 1:
                print(f"{name}: ⚠️  {ratio:.2f}× slower than {baseline_name}")
            else:
                print(f"{name}: ✅ {1 / ratio:.2f}× faster than {baseline_name}")
else:
    print(f"Cannot calculate ratios: baseline package {baseline_name} failed.")
