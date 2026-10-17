"""Compares detector flags with the planted answer key (SYNTHETIC data only)."""
import pandas as pd
from src.metrics import validate
from src.detect import detect_all

df = pd.read_csv("data/payouts_synthetic.csv")
truth = pd.read_csv("data/ground_truth.csv").set_index("worker_id")["planted_problem"]
print("Validation problems:", validate(df))

flags = detect_all(df)
flags.to_csv("data/flags.csv", index=False)
print("Total flags raised:", len(flags))
print()

MATCH = {"pay_rate_drop": "evening_cut",
         "deduction_increase": "deduction_spike",
         "incentive_drop": "incentive_drop"}

for ftype, planted in MATCH.items():
    f = flags[flags.flag_type == ftype]
    is_planted = f.worker_id.map(truth) == planted
    if ftype == "pay_rate_drop":
        correct = f[is_planted & (f.slot == "evening")]
    else:
        correct = f[is_planted]
    n_planted = int((truth == planted).sum())
    found = correct.worker_id.nunique()
    precision = len(correct) / len(f) if len(f) else float("nan")
    print(f"{ftype:19s} planted={n_planted:3d} found={found:3d} "
          f"recall={found / n_planted:4.0%}  flags={len(f):3d} "
          f"correct={len(correct):3d} precision={precision:4.0%}")

normal = truth[truth == "normal"].index
wrong = flags[flags.worker_id.isin(normal)].worker_id.nunique()
print()
print(f"Normal workers wrongly flagged: {wrong} of {len(normal)}")
print("NOTE: thresholds were set knowing the planted effect sizes, so these")
print("numbers test the pipeline on SYNTHETIC data, not real-world accuracy.")
