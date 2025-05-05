from memory_profiler import memory_usage
import werpy
import werx
import jiwer
import pywer
from torchmetrics.text import WordErrorRate

# --- Test Data (Repeated 1000 times) ---
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

# Normalize using werpy (shared pre-processing)
ref = werpy.normalize(reference_translation)
hyp = werpy.normalize(hypothesis_translation)

# --- Function Definitions ---
def wer_werpy():
    return werpy.wer(ref, hyp)

def wer_werx():
    return werx.wer(ref, hyp)

def wer_jiwer():
    return jiwer.wer(ref, hyp)

def wer_pywer():
    return pywer.wer(ref, hyp)

def wer_torchmetrics():
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

def main():
    print(f"Running memory benchmark with {len(ref)} examples...\n")
    memory_results = {}

    for name, func in package_funcs.items():
        try:
            mem_usage = memory_usage((func,), max_iterations=1, retval=True)
            peak_mem = max(mem_usage[0])  # mem_usage[0] is the memory usage list
            wer_value = mem_usage[1]      # mem_usage[1] is the return value
            memory_results[name] = (peak_mem, wer_value)
            print(f"{name}.wer used peak memory: {peak_mem:.2f} MiB, WER: {wer_value:.4f}")
        except Exception as e:
            memory_results[name] = (None, None)
            print(f"{name} failed during memory profiling: {e}")

    # --- Relative Memory Usage Summary ---
    print("\n📈 Relative memory usage (MiB):")
    baseline_name = "werx"
    baseline_mem = memory_results.get(baseline_name, (None, None))[0]

    if baseline_mem is not None:
        for name, (mem, _) in memory_results.items():
            if mem is None:
                continue
            if name == baseline_name:
                print(f"{name}: baseline")
            else:
                ratio = mem / baseline_mem
                if ratio > 1:
                    print(f"{name}: ⚠️  {ratio:.2f}× more memory than {baseline_name}")
                else:
                    print(f"{name}: ✅ {1 / ratio:.2f}× less memory than {baseline_name}")
    else:
        print(f"Cannot calculate memory ratios: baseline package {baseline_name} failed.")

if __name__ == "__main__":
    main()
