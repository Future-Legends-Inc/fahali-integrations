"""
Fahali quickstart — runs with NO API KEY.

Two public endpoints prove the thing that matters before you sign up for anything:
Fahali scores its own calls against what the market actually did, and keeps the
misses in the same record.

    python no_key_demo.py
"""
import json
import urllib.request

BASE = "https://app.fahaliai.com"


def get(path: str):
    with urllib.request.urlopen(BASE + path, timeout=20) as r:
        return json.loads(r.read().decode("utf-8"))


# 1. Is the platform live, and what is it covering right now?
stats = get("/api/public/stats")
print(f"Instruments monitored : {stats.get('instrumentsMonitored')}")
print(f"Detections (24h)      : {stats.get('detections24h')}")

# 2. The verified lead-time record — how early it warned, judged against outcomes.
#    Engines without enough resolved history are absent rather than guessed.
rec = get("/api/track-record/lead-time")
rows = rec.get("trackRecord") or []
print(f"\nVerified lead-time record ({rec.get('claimTier')}, {len(rows)} engines):")
for r in sorted(rows, key=lambda x: -(x.get("lead_median_hours") or 0))[:5]:
    lead = r.get("lead_median_hours")
    if lead is None:
        continue
    print(
        f"  {r['engine']:<26} warns ~{lead:>5.1f}h ahead"
        f" | precision {r.get('precision_pct'):.0f}% vs base {r.get('base_rate_pct'):.0f}%"
        f" (n={r.get('effective_sample')})"
    )

print("\nRead the precision against the BASE RATE, not on its own:")
print("beating a 60% base rate with 63% is noise; beating 33% with 72% is signal.")
print("\nFree key for the full tool surface: https://app.fahaliai.com/developer")
