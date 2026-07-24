"""
Pre-trade risk gate — the pattern most agents are missing.

Your agent decides it wants a position. Before it acts, ask Fahali what the
structure under the price says, and let a transparent rule decide whether to
proceed, size down, or wait. Fahali informs the decision; your agent owns it.

    pip install fahali
    FAHALI_API_KEY=sk_live_... python gate.py BTCUSDT
"""
import os
import sys

from fahali import FahaliClient

client = FahaliClient(api_key=os.environ.get("FAHALI_API_KEY"))
symbol = (sys.argv[1] if len(sys.argv) > 1 else "BTCUSDT").upper()

verdicts = client.verdict([symbol])
v = (verdicts if isinstance(verdicts, list) else verdicts.get("verdicts", []))
read = v[0] if v else {}

state = str(read.get("state") or read.get("verdict") or "UNKNOWN").upper()
conf = read.get("confidence")
missing = read.get("missingSignals") or []

# A transparent gate — you own this policy, not Fahali.
reasons = []
posture = "PROCEED"
if state in ("DEFEND", "ELEVATED", "CRITICAL"):
    posture, _ = "HOLD", reasons.append(f"state is {state}")
if isinstance(conf, (int, float)) and conf < 0.5:
    posture = "HOLD" if posture == "HOLD" else "CAUTION"
    reasons.append(f"low conviction ({conf})")
if missing:
    posture = "CAUTION" if posture == "PROCEED" else posture
    reasons.append("missing inputs: " + ", ".join(map(str, missing[:3])))

print(f"{symbol}: {state}" + (f" (confidence {conf})" if conf is not None else ""))
print(f"POSTURE: {posture}")
print("  " + ("; ".join(reasons) if reasons else "no blocking conditions"))
if read.get("receipt"):
    print(f"  receipt: {read['receipt']}   # attach to your trade log")
