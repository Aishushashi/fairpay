"""FairPay page design (HTML/CSS). Self-contained: no external fonts or scripts."""
PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>FairPay - Private AI auditor for gig workers</title>
<style>
:root{--ink:#14213d;--muted:#5b6478;--bg:#f4f6fb;--card:#ffffff;--brand:#4f46e5;--warn:#d97706;--bad:#dc2626;--line:#e5e9f2}
*{box-sizing:border-box}
body{margin:0;font-family:system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;background:var(--bg);color:var(--ink);line-height:1.5}
.hero{background:linear-gradient(135deg,#1e1b4b 0%,#4f46e5 55%,#06b6d4 100%);color:#fff;padding:44px 20px 70px}
.wrap{max-width:1000px;margin:0 auto;padding:0 16px}
.badge{display:inline-block;background:rgba(255,255,255,.16);border:1px solid rgba(255,255,255,.3);padding:4px 12px;border-radius:999px;font-size:12px;letter-spacing:.04em;margin:0 6px 6px 0}
.hero h1{font-size:40px;margin:14px 0 6px;letter-spacing:-.02em}
.hero p{font-size:17px;max-width:640px;margin:0;opacity:.92}
main{margin-top:-44px}
.card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:20px 22px;margin:16px 0;box-shadow:0 6px 24px rgba(20,33,61,.07)}
.card h2,.card h3{margin:0 0 10px}
.muted{color:var(--muted);font-size:14px}
.row{display:flex;gap:12px;flex-wrap:wrap;align-items:center}
button{border:0;border-radius:10px;padding:11px 18px;font-size:15px;font-weight:600;cursor:pointer;background:var(--brand);color:#fff;transition:transform .12s,box-shadow .12s}
button:hover{transform:translateY(-1px);box-shadow:0 6px 16px rgba(79,70,229,.35)}
button.alt{background:#fff;color:var(--brand);border:1.5px solid var(--brand)}
input[type=file]{padding:9px;border:1.5px dashed #b6bdd3;border-radius:10px;background:#fafbff;max-width:100%}
.err{background:#fef2f2;border:1px solid #fecaca;color:#991b1b;padding:12px 16px;border-radius:12px;margin:16px 0}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px}
.stat{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 16px;box-shadow:0 4px 14px rgba(20,33,61,.05)}
.stat .k{font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:.05em}
.stat .v{font-size:24px;font-weight:700;margin-top:2px}
.flag{border-left:6px solid var(--warn);background:#fffaf0}
.flag.high{border-left-color:var(--bad);background:#fff5f5}
.flag .top{display:flex;justify-content:space-between;gap:8px;flex-wrap:wrap;align-items:center}
.pill{padding:3px 10px;border-radius:999px;font-size:12px;font-weight:700;color:#fff;background:var(--warn)}
.pill.high{background:var(--bad)}
.chg{font-size:22px;font-weight:800;color:var(--bad)}
.tag{background:#eef2ff;color:#3730a3;padding:2px 9px;border-radius:8px;font-size:12px;font-weight:600;margin-right:6px}
.steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px}
.step{background:#f8faff;border:1px solid var(--line);border-radius:12px;padding:14px}
.step b{display:block;margin-bottom:4px}
.step .n{display:inline-block;width:26px;height:26px;border-radius:50%;background:var(--brand);color:#fff;text-align:center;line-height:26px;font-size:13px;margin-bottom:6px}
img{max-width:100%;border-radius:10px}
footer{margin:26px 0 40px}
.lock{border:1px solid #bbf7d0;background:#f0fdf4}
.spin{opacity:.7;pointer-events:none}
@media(max-width:600px){.hero h1{font-size:30px}}
</style></head><body>
<div class="hero"><div class="wrap">
<span class="badge">AI FOR GOOD</span><span class="badge">IBM LinuxONE</span><span class="badge">PRIVATE BY DESIGN</span>
<h1>FairPay</h1>
<p>A private AI auditor that helps gig workers spot unusual drops in pay, rising deductions and disappearing incentives, and explains them in plain language.</p>
</div></div>
<main class="wrap">
{% if error %}<div class="err"><b>Please check your file.</b> {{ error }}</div>{% endif %}
<div class="card">
<h2>Check a payout history</h2>
<p class="muted">Upload a CSV, or try the built-in demo. No names, phone numbers or bank details are needed.</p>
<div class="row">
<form id="f1" method="post" action="/analyze" enctype="multipart/form-data" class="row">
<input type="file" name="file" accept=".csv"><button type="submit">Analyze my file</button></form>
<form id="f2" method="post" action="/analyze"><input type="hidden" name="source" value="demo">
<button class="alt" type="submit">Try synthetic demo data</button></form>
</div>
<p class="muted" style="margin-top:12px">Columns: worker_id, platform, date, city, time_slot, trips_completed, distance_km, active_hours, base_pay, incentive, deductions, total_payout</p>
</div>
{% if not result %}
<div class="card"><h3>How it works</h3><div class="steps">
<div class="step"><span class="n">1</span><b>Upload</b><span class="muted">Your payout records in one simple format.</span></div>
<div class="step"><span class="n">2</span><b>Analyze</b><span class="muted">Transparent calculations compare earlier and recent weeks.</span></div>
<div class="step"><span class="n">3</span><b>Compare privately</b><span class="muted">Only group totals of similar workers, hidden if the group is small.</span></div>
<div class="step"><span class="n">4</span><b>Understand</b><span class="muted">Plain-language explanation of each change.</span></div>
</div></div>
{% endif %}
{% if result %}
{% set names = {'pay_rate_drop':'Pay per km dropped','deduction_increase':'Deductions increased','incentive_drop':'Incentives dropped'} %}
<div class="card"><div class="row">
<span class="tag">{{ result.label }}</span>
<span class="muted">{{ result.rows }} records | {{ result.workers }} workers | {{ result.n_flags }} flagged changes</span></div></div>
<div class="stats">
<div class="stat"><div class="k">Total earnings</div><div class="v">Rs {{ "%.0f"|format(result.s.total_earnings) }}</div></div>
<div class="stat"><div class="k">Per trip</div><div class="v">Rs {{ "%.2f"|format(result.s.earnings_per_trip) }}</div></div>
<div class="stat"><div class="k">Per km</div><div class="v">Rs {{ "%.2f"|format(result.s.earnings_per_km) }}</div></div>
<div class="stat"><div class="k">Per hour</div><div class="v">Rs {{ "%.2f"|format(result.s.earnings_per_hour) }}</div></div>
<div class="stat"><div class="k">Deduction share</div><div class="v">{{ "%.1f"|format(result.s.deduction_share * 100) }}%</div></div>
</div>
{% if result.chart %}<div class="card"><h3>Most serious change: weekly pay per km</h3><img alt="Weekly base pay per km" src="data:image/png;base64,{{ result.chart }}"></div>{% endif %}
<h3 style="margin:24px 0 4px">Detected changes</h3>
<p class="muted">Showing up to {{ result.shown }}, most serious first.</p>
{% if result.flag_items %}
{% for i in result.flag_items %}
<div class="card flag {{ i.severity }}">
<div class="top"><div><b>{{ names.get(i.kind, i.kind) }}</b> <span class="tag">Worker {{ i.worker }}</span><span class="tag">{{ i.slot }}</span></div>
<div><span class="chg">{{ "%.1f"|format(i.change) }}%</span> <span class="pill {{ i.severity }}">{{ i.severity }}</span></div></div>
<p style="margin:10px 0 0">{{ i.text }}</p></div>
{% endfor %}
{% else %}<div class="card"><b>No unusual changes found.</b></div>{% endif %}
<p class="muted">{{ result.template_label }}</p>
{% endif %}
<footer><div class="card lock"><b>Privacy and limits.</b>
<p class="muted" style="margin:6px 0 0">Everything runs on IBM LinuxONE and uploaded files are not stored. Peer comparisons show only group totals and are hidden when fewer than 20 other workers are in the group. This is aggregation, not differential privacy. A flag shows an unusual change in records and does not prove intentional underpayment. Results on the demo data come from simulated records with planted changes.</p></div></footer>
</main>
<script>
document.querySelectorAll("form").forEach(function(f){f.addEventListener("submit",function(){
var b=f.querySelector("button");if(b){b.textContent="Analyzing...";}document.body.classList.add("spin");});});
</script>
</body></html>"""
