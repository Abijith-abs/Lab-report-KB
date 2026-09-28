#!/usr/bin/env python3
"""
Cross-check every headline number used in the Lab 2 report against the data
transcribed from the Lab-Volt screenshots.

Ground truth = analysis/dt211.csv and analysis/dt212.csv, both of which were
verified cell-by-cell against:
    lab_screenshots/Screenshot 2026-09-02 091123.png   (DT211, 11 rows)
    lab_screenshots/Screenshot 2026-09-02 093106.png   (DT212, 40 rows)

Run from the repository root:   python3 analysis/verify_against_screenshots.py
Exits non-zero if any claim fails.
"""
import csv
import statistics as st
import sys

# ---------------------------------------------------------------- ground truth
DT211 = list(csv.DictReader(open("analysis/dt211.csv")))
DT212 = list(csv.DictReader(open("analysis/dt212.csv")))

EA_R, IA_R = 14.44, 0.507      # step-7 meters, Screenshot 09:58:10 -> 085810.png
EA_STEP14 = 254.7              # step-14 live meter, Screenshot 092337.png
N_STEP14 = 1501                # step-14 live meter speed
LIN = 1.50                     # upper limit of the linear torque region


def linfit(xs, ys):
    mx, my = st.mean(xs), st.mean(ys)
    m = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    b = my - m * mx
    sr = sum((y - (m * x + b)) ** 2 for x, y in zip(xs, ys))
    stt = sum((y - my) ** 2 for y in ys)
    return m, b, 1 - sr / stt


ea211 = [float(r["E arm EA (V)"]) for r in DT211]
n211 = [float(r["Speed (r/min)"]) for r in DT211]
ea212 = [float(r["E arm EA (V)"]) for r in DT212]
ia = [float(r["I arm IA (A)"]) for r in DT212]
tq = [float(r["Torque (N.m)"]) for r in DT212]
sp = [float(r["Speed (r/min)"]) for r in DT212]
eff = [float(r["Pm/Pin (%)"]) for r in DT212]

RA = EA_R / IA_R
EA14 = ea212[0]                                  # nominal armature voltage, DT212 row 0
K1 = (n211[-1] - n211[0]) / (ea211[-1] - ea211[0])
K1_ls, B1, R2_1 = linfit(ea211, n211)

lin = [(i, t, s) for i, t, s in zip(ia, tq, sp) if i <= LIN]
K2 = ([t for i, t, _ in lin if i == LIN][0] - tq[0]) / (LIN - ia[0])
K2_ls, B2, R2_2 = linfit([x[0] for x in lin], [x[1] for x in lin])
DM, DB, R2_D = linfit([x[0] for x in lin], [x[2] for x in lin])
RA_eff = -DM / K1

# ---------------------------------------------------------------- the checks
FAILS = []


def chk(label, claimed, actual, tol=0.006):
    ok = abs(claimed - actual) <= tol * max(1.0, abs(actual))
    if not ok:
        FAILS.append(label)
    print(f"  {'ok ' if ok else 'FAIL'}  {label:<44}{claimed:>11}{actual:>15.4f}")


print(f"\n{'':6}{'CLAIM':<44}{'REPORT':>11}{'SCREENSHOT':>15}")
print("  " + "-" * 74)
chk("step-7 E_A (V)", 14.44, EA_R)
chk("step-7 I_A (A)", 0.507, IA_R)
chk("R_A = E_A / I_A (ohm)", 28.48, RA)
chk("step-14 meter E_A (V)", 254.7, EA_STEP14)
chk("DT212 row-0 E_A (V)", 255.73, EA14)
chk("K1 two-point (r/min/V)", 5.841, K1)
chk("K1 least-squares", 5.893, K1_ls)
chk("K1 intercept (r/min)", -21.8, B1, 0.02)
chk("K1 intercept as % of max speed", 1.38, 100 * abs(B1) / max(n211), 0.02)
chk("K1 R-squared", 0.99979, R2_1)
chk("K2 two-point (N.m/A)", 1.172, K2)
chk("K2 least-squares", 1.164, K2_ls)
chk("K2 R-squared", 0.99429, R2_2)
chk("droop slope (r/min/A)", -63.07, DM, 0.01)
chk("droop R-squared", 0.8098, R2_D, 0.01)
chk("droop intercept -> E_A (V)", 255.65, DB / K1, 0.01)
chk("R_A effective (ohm)", 10.80, RA_eff)
chk("model droop K1*R_A (r/min/A)", 166.4, K1 * RA, 0.01)
chk("over-prediction factor", 2.64, (K1 * RA) / abs(DM), 0.01)
chk("no-load speed (r/min)", 1501.52, sp[0])
chk("speed at 1.5 A (r/min)", 1412.45, [s for i, _, s in lin if i == LIN][0])
chk("speed at 3.95 A (r/min)", 1079.88, sp[-1])
chk("speed regulation to 1.5 A (%)", 6.31, 100 * (sp[0] - 1412.45) / 1412.45)
chk("speed regulation to 3.95 A (%)", 39.05, 100 * (sp[0] - sp[-1]) / sp[-1])
chk("peak efficiency (%)", 78.00, max(eff))
chk("peak efficiency at I_A (A)", 0.60, ia[eff.index(max(eff))])
chk("efficiency at 3.95 A (%)", 34.68, eff[-1])
chk("E_A drift start (V)", 255.73, ea212[0])
chk("E_A drift end (V)", 243.25, ea212[-1])
chk("E_A drift (%)", 4.88, 100 * (ea212[0] - ea212[-1]) / ea212[0])
chk("torque shortfall at 1.50 A (%)", 3.4, 100 * ((K2_ls * 1.5 + B2) - 1.75) / (K2_ls * 1.5 + B2), 0.05)
chk("torque shortfall at 3.95 A (%)", 36.5, 100 * ((K2_ls * 3.95 + B2) - tq[-1]) / (K2_ls * 3.95 + B2), 0.02)

print("\n  Step-19 Table 1 predictions (E_A = 255.73 V, R_A = 28.48 ohm, K1 = 5.8412):")
for i, exp in [(0.5, 1410.6), (1.0, 1327.4), (1.5, 1244.2)]:
    chk(f"  n at I_A = {i} A (r/min)", exp, K1 * (EA14 - i * RA), 0.001)

print("\n  Dataset integrity:")
print(f"       DT211 rows: {len(DT211)}   DT212 rows: {len(DT212)}")
missing = sorted(set([0.6, 0.65, 0.88, 0.97, 1.02, 3.05]))
print(f"       rows deleted in the 09:48 DT212 capture: {missing}")

if FAILS:
    print(f"\n  {len(FAILS)} CHECK(S) FAILED: {FAILS}\n")
    sys.exit(1)
print("\n  All checks passed.\n")
