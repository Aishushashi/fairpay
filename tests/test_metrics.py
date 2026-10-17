import math
import pandas as pd
from src.metrics import validate, summarize, pct_change, REQUIRED_COLUMNS


def make_df():
    return pd.DataFrame({
        "worker_id": [1, 1], "platform": ["A", "A"],
        "date": ["2026-09-01", "2026-09-02"], "city": ["X", "X"],
        "time_slot": ["morning", "evening"],
        "trips_completed": [2, 4], "distance_km": [10, 20],
        "active_hours": [1, 3], "base_pay": [100, 200],
        "incentive": [10, 0], "deductions": [5, 10],
        "total_payout": [105, 190],
    })


def test_known_numbers():
    s = summarize(make_df())
    assert abs(s["total_earnings"] - 295) < 1e-9
    assert abs(s["earnings_per_trip"] - 295 / 6) < 1e-9
    assert abs(s["earnings_per_km"] - 295 / 30) < 1e-9
    assert abs(s["earnings_per_hour"] - 73.75) < 1e-9
    assert abs(s["incentive_share"] - 10 / 310) < 1e-9
    assert abs(s["deduction_share"] - 15 / 310) < 1e-9


def test_zero_trips_does_not_crash():
    df = make_df()
    df["trips_completed"] = 0
    df["distance_km"] = 0
    s = summarize(df)
    assert math.isnan(s["earnings_per_trip"])
    assert math.isnan(s["earnings_per_km"])


def test_validate_ok_and_missing_column():
    assert validate(make_df()) == []
    problems = validate(make_df().drop(columns=["deductions"]))
    assert len(problems) == 1 and "deductions" in problems[0]


def test_validate_empty_and_bad_numbers():
    assert validate(pd.DataFrame(columns=REQUIRED_COLUMNS)) == ["The file is empty."]
    df = make_df()
    df["base_pay"] = ["abc", 200]
    assert any("base_pay" in p for p in validate(df))


def test_pct_change():
    assert abs(pct_change(100, 82) + 18) < 1e-9
    assert math.isnan(pct_change(0, 5))
