"""Creates a SYNTHETIC (fake) gig-worker payout dataset for FairPay testing."""
import numpy as np
import pandas as pd

rng = np.random.default_rng(2026)      # fixed seed: same data every run

N_WORKERS = 300
START = pd.Timestamp("2026-08-31")     # a Monday
DAYS = 56                              # 8 weeks of records
CHANGE_DAY = 28                        # planted problems begin in week 5

PLATFORMS = ["PlatformA", "PlatformB"]
CITIES = ["Bengaluru", "Chennai", "Mumbai"]
SLOTS = ["morning", "afternoon", "evening", "night"]
WORK_PROB = {"morning": 0.35, "afternoon": 0.40, "evening": 0.60, "night": 0.25}
TRIP_LAMBDA = {"morning": 5, "afternoon": 5, "evening": 7, "night": 4}

# Randomly choose which workers get which planted problem
order = rng.permutation(np.arange(1, N_WORKERS + 1))
n_even, n_ded, n_inc = int(0.12 * N_WORKERS), int(0.08 * N_WORKERS), int(0.08 * N_WORKERS)
evening_cut = set(order[:n_even])
deduction_spike = set(order[n_even:n_even + n_ded])
incentive_drop = set(order[n_even + n_ded:n_even + n_ded + n_inc])

rows = []
for w in range(1, N_WORKERS + 1):
    platform = PLATFORMS[int(rng.integers(0, len(PLATFORMS)))]
    city = CITIES[int(rng.integers(0, len(CITIES)))]
    rate_per_km = rng.normal(9, 1)          # each worker's normal pay per km
    for d in range(DAYS):
        date = START + pd.Timedelta(days=d)
        after_change = d >= CHANGE_DAY
        for slot in SLOTS:
            if rng.random() > WORK_PROB[slot]:
                continue
            trips = max(1, int(rng.poisson(TRIP_LAMBDA[slot])))
            distance = round(float(trips * np.clip(rng.normal(3.5, 0.5), 1.5, 6)), 2)
            hours = round(float(trips * np.clip(rng.normal(0.35, 0.05), 0.15, 0.7)), 2)
            base = distance * rate_per_km + trips * 12
            incentive = base * rng.uniform(0.05, 0.15) if trips >= 5 else 0.0
            ded_rate = float(np.clip(rng.normal(0.03, 0.005), 0.0, 0.08))
            # ---- planted problems (only after CHANGE_DAY) ----
            if after_change and w in evening_cut and slot == "evening":
                base *= 0.82
            if after_change and w in incentive_drop:
                incentive *= 0.30
            if after_change and w in deduction_spike:
                ded_rate = 0.12
            deductions = (base + incentive) * ded_rate
            total = base + incentive - deductions
            rows.append((w, platform, date.date().isoformat(), city, slot, trips,
                         distance, hours, round(base, 2), round(incentive, 2),
                         round(deductions, 2), round(total, 2)))

cols = ["worker_id", "platform", "date", "city", "time_slot", "trips_completed",
        "distance_km", "active_hours", "base_pay", "incentive", "deductions",
        "total_payout"]
df = pd.DataFrame(rows, columns=cols)
df.to_csv("data/payouts_synthetic.csv", index=False)

# Answer key, kept separate on purpose (used only to test our detector)
truth = []
for w in range(1, N_WORKERS + 1):
    kind = ("evening_cut" if w in evening_cut else
            "deduction_spike" if w in deduction_spike else
            "incentive_drop" if w in incentive_drop else "normal")
    truth.append((w, kind))
pd.DataFrame(truth, columns=["worker_id", "planted_problem"]).to_csv(
    "data/ground_truth.csv", index=False)

print("SYNTHETIC data written.")
print("Rows:", len(df), "| Workers:", df.worker_id.nunique())
print("Dates:", df.date.min(), "to", df.date.max())
print(pd.DataFrame(truth, columns=["w", "kind"]).kind.value_counts().to_string())
