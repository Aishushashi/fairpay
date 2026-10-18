"""Original vector illustrations for FairPay (inline SVG, no external files)."""

HERO_SVG = '''<svg viewBox="0 0 400 260" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Delivery rider on a scooter">
<circle cx="330" cy="58" r="34" fill="#fde68a" opacity=".9"/>
<g fill="#ffffff" opacity=".18"><rect x="14" y="120" width="40" height="110"/><rect x="60" y="88" width="46" height="142"/><rect x="112" y="130" width="36" height="100"/><rect x="250" y="108" width="44" height="122"/><rect x="300" y="140" width="40" height="90"/></g>
<rect x="0" y="228" width="400" height="32" fill="#1e1b4b" opacity=".55"/>
<line x1="0" y1="244" x2="400" y2="244" stroke="#ffffff" stroke-width="3" stroke-dasharray="18 14" opacity=".6"/>
<circle cx="140" cy="214" r="22" fill="#111827"/><circle cx="140" cy="214" r="9" fill="#9ca3af"/>
<circle cx="268" cy="214" r="22" fill="#111827"/><circle cx="268" cy="214" r="9" fill="#9ca3af"/>
<path d="M140 214 L170 172 L250 172 L268 214" fill="none" stroke="#f97316" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M250 172 L258 130 L282 126" fill="none" stroke="#e5e7eb" stroke-width="7" stroke-linecap="round"/>
<rect x="160" y="160" width="86" height="16" rx="8" fill="#f97316"/>
<rect x="98" y="112" width="62" height="58" rx="8" fill="#ef4444"/>
<rect x="98" y="112" width="62" height="14" rx="6" fill="#b91c1c"/>
<rect x="116" y="138" width="26" height="6" rx="3" fill="#fecaca"/>
<circle cx="212" cy="102" r="15" fill="#fcd9b6"/>
<path d="M196 100 Q212 76 228 98 L228 103 L196 103 Z" fill="#4f46e5"/>
<rect x="198" y="117" width="30" height="46" rx="12" fill="#06b6d4"/>
<path d="M220 134 L252 128" stroke="#06b6d4" stroke-width="10" stroke-linecap="round"/>
<path d="M208 160 L228 184 L220 204" fill="none" stroke="#1e293b" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>
</svg>'''


_RIDER = '''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg"><circle cx="32" cy="32" r="30" fill="#eef2ff"/><circle cx="32" cy="22" r="8" fill="#fcd9b6"/><path d="M22 19 Q32 6 42 19Z" fill="#4f46e5"/><rect x="22" y="31" width="20" height="18" rx="6" fill="#06b6d4"/><rect x="34" y="38" width="16" height="14" rx="3" fill="#ef4444"/></svg>'''
_DRIVER = '''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg"><circle cx="32" cy="32" r="30" fill="#eef2ff"/><path d="M12 40 L18 29 H46 L52 40 V47 H12Z" fill="#4f46e5"/><rect x="20" y="31" width="24" height="8" rx="2" fill="#bae6fd"/><circle cx="21" cy="47" r="5" fill="#111827"/><circle cx="43" cy="47" r="5" fill="#111827"/></svg>'''
_COURIER = '''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg"><circle cx="32" cy="32" r="30" fill="#eef2ff"/><rect x="16" y="20" width="32" height="26" rx="3" fill="#f59e0b"/><rect x="29" y="20" width="6" height="26" fill="#b45309"/><rect x="16" y="29" width="32" height="5" fill="#d97706"/></svg>'''

PERSONAS_HTML = (
    '<div class="card"><h3>Built for the people who keep our cities moving</h3><div class="who">'
    '<div class="p">' + _RIDER + '<br><b>Delivery riders</b><div class="muted">Food and grocery delivery</div></div>'
    '<div class="p">' + _DRIVER + '<br><b>Cab and auto drivers</b><div class="muted">Ride-hailing earnings</div></div>'
    '<div class="p">' + _COURIER + '<br><b>Parcel couriers</b><div class="muted">Per-delivery payouts</div></div>'
    '</div></div>'
)
