import pandas as pd
from src.peers import peer_benchmark

df = pd.read_csv("data/payouts_synthetic.csv")
flags = pd.read_csv("data/flags.csv")
row = flags[flags["flag_type"] == "pay_rate_drop"].iloc[0]
wid, slot = int(row["worker_id"]), row["slot"]
print("Worker", wid, "| slot", slot, "| own change: %.1f%%" % row["pct_change"])
print("Peer result:", peer_benchmark(df, wid, slot))
small = df[df["worker_id"] <= 10]
print("Small-group test:", peer_benchmark(small, 1, "evening"))
