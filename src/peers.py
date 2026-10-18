"""FairPay peer benchmark: aggregated comparison with small-group suppression."""
import pandas as pd
from src.metrics import pct_change, safe_divide
from src.detect import split_periods

K_MIN = 20   # minimum number of OTHER workers in a peer group


def peer_benchmark(df, worker_id, slot):
    me = df[df["worker_id"] == worker_id]
    if me.empty:
        return {"available": False, "reason": "Worker not found."}
    city, platform = me["city"].iloc[0], me["platform"].iloc[0]
    d = df.copy()
    d["_period"] = split_periods(d)
    g = d[(d["city"] == city) & (d["platform"] == platform)
          & (d["time_slot"] == slot) & (d["worker_id"] != worker_id)]
    n = int(g["worker_id"].nunique())
    if n < K_MIN:
        return {"available": False, "n_peers": n,
                "reason": f"Peer group too small (under {K_MIN} workers); hidden for privacy."}
    e = g[g["_period"] == "earlier"]
    r = g[g["_period"] == "recent"]
    old = float(safe_divide(e["base_pay"].sum(), e["distance_km"].sum()))
    new = float(safe_divide(r["base_pay"].sum(), r["distance_km"].sum()))
    return {"available": True, "n_peers": n,
            "group": f"{city} / {platform} / {slot}",
            "peer_pct_change": pct_change(old, new)}
