"""FairPay dashboard (Flask). Runs on the server; view it through an SSH tunnel."""
import base64
import io
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from flask import Flask, request, render_template_string
from src.metrics import validate, summarize
from src.detect import detect_all
from src.peers import peer_benchmark
from src.explain import explain_flag, LABEL
from src.page import PAGE

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024   # 5 MB upload limit
DEMO_PATH = "data/payouts_synthetic.csv"
MAX_FLAGS_SHOWN = 40


def weekly_chart(df, worker_id):
    w = df[df["worker_id"] == worker_id].copy()
    w["week"] = pd.to_datetime(w["date"]).dt.to_period("W").dt.start_time
    g = w.groupby(["week", "time_slot"]).agg(
        base=("base_pay", "sum"), km=("distance_km", "sum")).reset_index()
    g["rate"] = g["base"] / g["km"].where(g["km"] > 0)
    fig, ax = plt.subplots(figsize=(7, 3.2))
    for slot, part in g.groupby("time_slot"):
        ax.plot(part["week"], part["rate"], marker="o", label=slot)
    ax.set_title("Worker %s: weekly base pay per km (Rs)" % worker_id)
    ax.set_ylabel("Rs per km")
    ax.legend(fontsize=8)
    fig.autofmt_xdate()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=110)
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode()


OLD_PAGE = """<!doctype html><html><head><meta charset="utf-8"><title>FairPay</title>
<style>
body{font-family:sans-serif;max-width:900px;margin:24px auto;padding:0 12px;color:#222}
.card{background:#f5f7fa;border-radius:8px;padding:12px 16px;margin:10px 0}
.cards{display:flex;gap:10px;flex-wrap:wrap}.cards .card{flex:1;min-width:140px}
table{border-collapse:collapse;width:100%}
td,th{border-bottom:1px solid #ddd;padding:6px;text-align:left;font-size:14px}
.high{color:#b00020;font-weight:bold}.err{background:#fde8e8;padding:10px;border-radius:6px}
.note{font-size:13px;color:#555}img{max-width:100%}
</style></head><body>
<h1>FairPay</h1>
<p>A private auditor for gig-worker payouts, running on IBM LinuxONE.</p>
{% if error %}<div class="err">{{ error }}</div>{% endif %}
<div class="card"><b>Upload a payout CSV</b>
<form method="post" action="/analyze" enctype="multipart/form-data">
<input type="file" name="file" accept=".csv"> <button type="submit">Analyze</button></form>
<form method="post" action="/analyze" style="margin-top:8px">
<input type="hidden" name="source" value="demo">
<button type="submit">Use synthetic demo data</button></form>
<p class="note">Columns: worker_id, platform, date, city, time_slot, trips_completed,
distance_km, active_hours, base_pay, incentive, deductions, total_payout.
No names, phone numbers or bank details.</p></div>
{% if result %}
<div class="card"><b>Data source:</b> {{ result.label }}<br>
Rows: {{ result.rows }} | Workers: {{ result.workers }} | Flags: {{ result.n_flags }}</div>
<div class="cards">
<div class="card">Total earnings<br><b>Rs {{ "%.0f"|format(result.s.total_earnings) }}</b></div>
<div class="card">Per trip<br><b>Rs {{ "%.2f"|format(result.s.earnings_per_trip) }}</b></div>
<div class="card">Per km<br><b>Rs {{ "%.2f"|format(result.s.earnings_per_km) }}</b></div>
<div class="card">Per hour<br><b>Rs {{ "%.2f"|format(result.s.earnings_per_hour) }}</b></div>
<div class="card">Deduction share<br><b>{{ "%.1f"|format(result.s.deduction_share * 100) }}%</b></div>
</div>
{% if result.chart %}<div class="card"><img src="data:image/png;base64,{{ result.chart }}"></div>{% endif %}
<h3>Detected changes (showing up to {{ result.shown }})</h3>
{% if result.flag_items %}<table><tr><th>Worker</th><th>Change</th><th>Slot</th><th>Change %</th><th>Severity</th></tr>
{% for i in result.flag_items %}<tr><td>{{ i.worker }}</td><td>{{ i.kind }}</td><td>{{ i.slot }}</td>
<td>{{ "%.1f"|format(i.change) }}%</td><td class="{{ i.severity }}">{{ i.severity }}</td></tr>
<tr><td colspan="5" class="note">{{ i.text }}</td></tr>{% endfor %}</table>
{% else %}<p>No unusual changes found.</p>{% endif %}
<p class="note">{{ result.template_label }}</p>
{% endif %}
<div class="card note"><b>Privacy and limits.</b> Peer comparisons show only group totals and are
hidden when fewer than 20 other workers are in the group. This is aggregation, not differential
privacy. Flags show unusual changes in records. They do not prove intentional underpayment.
Results on the demo data come from simulated records with planted changes.</div>
</body></html>"""


@app.route("/")
def home():
    return render_template_string(PAGE, result=None, error=None)


@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        if request.form.get("source") == "demo":
            df = pd.read_csv(DEMO_PATH)
            label = "SYNTHETIC demonstration data"
        else:
            f = request.files.get("file")
            if f is None or f.filename == "":
                return render_template_string(PAGE, result=None, error="Please choose a CSV file.")
            df = pd.read_csv(f)
            label = "USER-PROVIDED data (not stored by this app)"
    except Exception:
        return render_template_string(PAGE, result=None, error="Could not read that file as a CSV.")
    problems = validate(df)
    if problems:
        return render_template_string(PAGE, result=None, error=" ".join(problems))
    flags = detect_all(df)
    items, chart = [], None
    if len(flags):
        flags["_s"] = (flags["severity"] == "high").astype(int)
        flags["_a"] = flags["pct_change"].abs()
        flags = flags.sort_values(["_s", "_a"], ascending=False)
        shown = flags.head(MAX_FLAGS_SHOWN)
        for _, row in shown.iterrows():
            peer = None
            if row["flag_type"] == "pay_rate_drop":
                peer = peer_benchmark(df, row["worker_id"], row["slot"])
            items.append({"worker": row["worker_id"], "kind": row["flag_type"],
                          "slot": row["slot"], "change": row["pct_change"],
                          "severity": row["severity"], "text": explain_flag(row, peer)})
        chart = weekly_chart(df, shown.iloc[0]["worker_id"])
    result = {"label": label, "rows": len(df), "workers": int(df["worker_id"].nunique()),
              "n_flags": len(flags), "s": summarize(df), "flag_items": items, "chart": chart,
              "shown": MAX_FLAGS_SHOWN, "template_label": LABEL}
    return render_template_string(PAGE, result=result, error=None)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
