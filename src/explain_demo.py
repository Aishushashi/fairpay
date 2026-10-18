import pandas as pd
from src.peers import peer_benchmark
from src.explain import explain_flag, LABEL

df = pd.read_csv("data/payouts_synthetic.csv")
flags = pd.read_csv("data/flags.csv")
for kind in ["pay_rate_drop", "deduction_increase", "incentive_drop"]:
    row = flags[flags["flag_type"] == kind].iloc[0]
    peer = peer_benchmark(df, int(row["worker_id"]), row["slot"]) if kind == "pay_rate_drop" else None
    print("[" + kind + "] worker", int(row["worker_id"]), "| severity:", row["severity"])
    print(explain_flag(row, peer))
    print()
print(LABEL)
