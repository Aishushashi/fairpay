"""FairPay rule-based detector. Compares each worker's earlier weeks with recent weeks."""
import numpy as np
import pandas as pd
from src.metrics import summarize, pct_change, safe_divide

# Thresholds (named so they are easy to explain and change)
PAY_DROP_PCT = -10.0          # flag if base pay per km falls 10% or more in a time slot
DEDUCTION_RATIO = 1.5         # flag if deduction share becomes 1.5x the earlier share ...
DEDUCTION_MIN_RISE = 0.01     # ... and rises by at least 1 percentage point
INCENTIVE_DROP_PCT = -40.0    # flag if incentive share falls 40% or more
MIN_ROWS = 5                  # need at least 5 records in each period to compare
MIN_INCENTIVE_SHARE = 0.01    # skip incentive check if earlier share was under 1%

COLS = ["worker_id", "flag_type", "slot", "metric", "earlier", "recent",
        "pct_change", "severity"]


def severity(change_pct):
    """Size of the change only. It is NOT proof of wrongdoing."""
    return "high" if abs(change_pct) >= 25 else "medium"


def split_periods(df):
    """Label each row 'earlier' or 'recent' using the midpoint of the date range."""
    d = pd.to_datetime(df["date"])
    mid = d.min() + (d.max() - d.min()) / 2
    return np.where(d <= mid, "earlier", "recent")


def base_per_km(frame):
    return float(safe_divide(frame["base_pay"].sum(), frame["distance_km"].sum()))


def detect_all(df):
    """Return a table of flags (one row per flagged change)."""
    df = df.copy()
    df["_period"] = split_periods(df)
    flags = []
    for wid, w in df.groupby("worker_id"):
        e = w[w["_period"] == "earlier"]
        r = w[w["_period"] == "recent"]
        # Rule 1: base pay per km, checked separately for each time slot
        for slot in sorted(w["time_slot"].unique()):
            es = e[e["time_slot"] == slot]
            rs = r[r["time_slot"] == slot]
            if len(es) < MIN_ROWS or len(rs) < MIN_ROWS:
                continue
            old, new = base_per_km(es), base_per_km(rs)
            ch = pct_change(old, new)
            if not np.isnan(ch) and ch <= PAY_DROP_PCT:
                flags.append((wid, "pay_rate_drop", slot, "base_pay_per_km",
                              old, new, ch, severity(ch)))
        if len(e) < MIN_ROWS or len(r) < MIN_ROWS:
            continue
        se, sr = summarize(e), summarize(r)
        # Rule 2: deductions taking a bigger share of gross pay
        od, nd = se["deduction_share"], sr["deduction_share"]
        if not (np.isnan(od) or np.isnan(nd)):
            if nd >= od * DEDUCTION_RATIO and (nd - od) >= DEDUCTION_MIN_RISE:
                ch = pct_change(od, nd)
                flags.append((wid, "deduction_increase", "all", "deduction_share",
                              od, nd, ch, severity(ch)))
        # Rule 3: incentive share shrinking
        oi, ni = se["incentive_share"], sr["incentive_share"]
        if not (np.isnan(oi) or np.isnan(ni)) and oi >= MIN_INCENTIVE_SHARE:
            ch = pct_change(oi, ni)
            if not np.isnan(ch) and ch <= INCENTIVE_DROP_PCT:
                flags.append((wid, "incentive_drop", "all", "incentive_share",
                              oi, ni, ch, severity(ch)))
    return pd.DataFrame(flags, columns=COLS)
