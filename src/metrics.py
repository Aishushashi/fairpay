"""FairPay core calculations. Every number shown to a worker comes from here."""
import numpy as np
import pandas as pd

REQUIRED_COLUMNS = [
    "worker_id", "platform", "date", "city", "time_slot", "trips_completed",
    "distance_km", "active_hours", "base_pay", "incentive", "deductions",
    "total_payout",
]
NUMERIC_COLUMNS = [
    "trips_completed", "distance_km", "active_hours", "base_pay",
    "incentive", "deductions", "total_payout",
]


def validate(df):
    """Return a list of plain-English problems. An empty list means the file is OK."""
    if df is None or len(df) == 0:
        return ["The file is empty."]
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        return ["Missing columns: " + ", ".join(missing)]
    problems = []
    for c in NUMERIC_COLUMNS:
        values = pd.to_numeric(df[c], errors="coerce")
        bad = int(values.isna().sum())
        if bad:
            problems.append(f"Column '{c}' has {bad} missing or non-numeric values.")
        elif (values < 0).any():
            problems.append(f"Column '{c}' has negative values.")
    bad_dates = int(pd.to_datetime(df["date"], errors="coerce").isna().sum())
    if bad_dates:
        problems.append(f"Column 'date' has {bad_dates} invalid dates.")
    return problems


def safe_divide(num, den):
    """Divide, returning NaN (not an error) when the denominator is zero."""
    num = np.asarray(num, dtype=float)
    den = np.asarray(den, dtype=float)
    out = np.full(np.broadcast(num, den).shape, np.nan)
    np.divide(num, den, out=out, where=(den != 0))
    return out


def pct_change(old, new):
    """Percentage change from old to new. NaN if it cannot be computed."""
    if old is None or new is None or np.isnan(old) or np.isnan(new) or old == 0:
        return float("nan")
    return (new - old) / old * 100.0


def summarize(df):
    """Totals and ratios for a set of rows (add up first, then divide)."""
    t = {c: float(pd.to_numeric(df[c], errors="coerce").sum()) for c in NUMERIC_COLUMNS}
    gross = t["base_pay"] + t["incentive"]
    return {
        "total_earnings": t["total_payout"],
        "trips": t["trips_completed"],
        "distance_km": t["distance_km"],
        "active_hours": t["active_hours"],
        "earnings_per_trip": float(safe_divide(t["total_payout"], t["trips_completed"])),
        "earnings_per_km": float(safe_divide(t["total_payout"], t["distance_km"])),
        "earnings_per_hour": float(safe_divide(t["total_payout"], t["active_hours"])),
        "incentive_share": float(safe_divide(t["incentive"], gross)),
        "deduction_share": float(safe_divide(t["deductions"], gross)),
    }
