# Lab 2 — Verified Data & Calculations (working notes)

> Working notes, not part of the submission. Every number below was read directly from the
> screenshots in `lab_screenshots/` and `lab report 2/`, and every constant was recomputed
> from that data. Delete this folder before submitting if you don't want it in the repo.

---

## 1. Source inventory — what each file actually is

| File | What it really is |
|---|---|
| `Lab 2.pdf` (13 pp) | **The Lab 2 manual** — Festo/Lab-Volt *DC Machines – DC Motors*, theory (Figs 1–12) + the 22-step procedure. Not a sample report. |
| `Lab report template-3.pdf` (1 p) | **The ECU template** — a one-page section list. Written around the Lab 1 transformer example. |
| `IMG-20260926-WA0000…0010.jpg` (11) | Canvas screenshots: assignment header, instructions, and the full marking rubric. |
| `lab_screenshots/` (6 PNG) | Lab-Volt captures 08:58 → 09:31 |
| `lab report 2/` (2 PNG) | Lab-Volt captures 09:48 |
| *(missing)* | A **sample report by another student** was described but is **not in the repo**. |

### Assignment facts (from Canvas screenshots)
- Title: *Assignment 1: Laboratory 2 Report Submission – Lab 2B Group*
- **Due: Sun, 27 Sep 2026, 23:59** · 10 points · worth 10% · submitted **individually**
- No word limit
- Cover page must name all group members who participated
- Turnitin similarity **must not exceed 40%**
- Appendix must contain a lab-computer snapshot **with date and time visible**
- Generative-AI declaration required (tool, version, scope)

### Actual rubric weighting (10 points total)

| Criterion | Max |
|---|---:|
| Report Structure & Presentation | 2.0 |
| Aims | 1.0 |
| **Observation and Analysis** | **5.0** |
| Conclusions | 1.0 |
| References | 1.0 |

**Half the marks sit in Observation and Analysis.** There is no separate "theory" criterion.

---

## 2. What was captured in the lab

| Manual step | Artefact | Screenshot | Status |
|---|---|---|---|
| 7 | Armature-resistance test | `085810.png` | captured |
| 10–11 | **DT211** — speed vs armature voltage | `091123.png` | captured (11 rows) |
| 12 | **G211** — n vs E_A | `091254.png` | captured |
| 14 | E_A at n = 1500 r/min | `092337.png` | captured (255.73 V) |
| 15–16 | **DT212** — torque vs armature current | `093106.png` | captured (**40 rows**) |
| 17 | **G212** — T vs I_A | `093153.png` | captured |
| 20 | **G212-1** — n vs I_A | — | **MISSING** |
| 21 | **G212-2** — n vs T | `094846.png` | captured |

**G212-1 (DC Motor Speed vs Armature Current) was never captured.** Step 20 explicitly
requires it. It has been re-plotted from the DT212 data and is labelled as such in the report.

> ⚠️ **DT212 exists in two versions.** `093106.png` (09:31) holds the complete **40-row**
> record. `094858.png` (09:48) holds only **34 rows** — six were deleted at some point
> between the two captures (I_A = 0.60, 0.65, 0.88, 0.97, 1.02 and 3.05 A). **The 40-row
> version is authoritative** and is what the report and `dt212.csv` use.

---

## 3. Step 7 — Armature resistance

Meter readings from `085810.png`:

| Meter | Reading |
|---|---|
| E arm. (E_A) | 14.44 V |
| I arm. (I_A) | 0.507 A |
| I field (I_F) | 0.001 A (field de-energised, correct) |
| Speed | **−318.8 r/min** |
| Torque | −0.341 N·m |
| Mech Power | 11.38 W |

    R_A = E_A / I_A = 14.44 / 0.507 = 28.48 Ω

⚠️ **The rotor was turning at −318.8 r/min during this measurement.** The manual requires the
motor to be stationary so that E_CEMF = 0. With I_F ≈ 0 the residual flux is tiny, so E_CEMF is
small — but it is not exactly zero, and this is a legitimate error source to discuss.

---

## 4. DT211 — Motor speed vs armature voltage (no load, I_F = 210 mA)

| # | E_A (V) | I_A (A) | I_F (A) | P_IN (W) | T (N·m) | n (r/min) |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0.43 | 0.01 | 0.21 | 0.01 | 0 | 0.08 |
| 1 | 26.03 | 0.18 | 0.20 | 4.64 | 0.21 | 126.00 |
| 2 | 53.17 | 0.20 | 0.20 | 10.58 | 0.23 | 285.97 |
| 3 | 82.58 | 0.22 | 0.20 | 18.55 | 0.25 | 459.05 |
| 4 | 108.93 | 0.24 | 0.20 | 26.46 | 0.26 | 614.33 |
| 5 | 136.59 | 0.26 | 0.20 | 35.54 | 0.28 | 779.98 |
| 6 | 160.82 | 0.27 | 0.20 | 43.20 | 0.29 | 922.85 |
| 7 | 187.72 | 0.27 | 0.20 | 52.12 | 0.30 | 1083.56 |
| 8 | 213.66 | 0.28 | 0.20 | 61.09 | 0.31 | 1240.19 |
| 9 | 239.94 | 0.29 | 0.20 | 70.42 | 0.32 | 1394.89 |
| 10 | 271.14 | 0.29 | 0.20 | 80.62 | 0.33 | 1581.36 |

### K₁ — voltage-to-speed constant

    Two end points (manual step 13):
    K1 = (1581.36 − 0.08) / (271.14 − 0.43) = 5.841 r/min/V

    Least-squares check:
    K1 = 5.893 r/min/V,  intercept −21.8 r/min,  R² = 0.9998

The R² of 0.9998 is the hard evidence for "linear voltage-to-speed converter".
**Use K₁ = 5.841 r/min/V** — the manual asks for the two-end-point method.

---

## 5. DT212 — Torque vs armature current (E_A held at ≈ 255.73 V, n₀ = 1500 r/min)

40 rows, I_A from 0.28 A to 3.95 A. Full table transcribed in `dt212.csv`.

### K₂ — current-to-torque constant

| Fit range | n pts | K₂ (N·m/A) | R² |
|---|---:|---:|---:|
| I_A ≤ 1.0 A | 18 | 1.297 | 0.9979 |
| I_A ≤ 1.5 A | 25 | 1.164 | 0.9943 |
| I_A ≤ 2.0 A | 32 | 1.055 | 0.9893 |
| all 40 rows | 40 | 0.796 | 0.9417 |

    Two end points of the linear portion (0.28 A → 1.50 A), manual step 18:
    K2 = (1.75 − 0.32) / (1.50 − 0.28) = 1.172 N·m/A

⚠️ **Open question:** the cut-off for "the linear portion" depends on the machine's *rated*
armature current, which needs confirming from the module front panel (or the LVSIM tooltip).
The RA test was run at 0.507 A, which suggests rated ≈ 0.5 A; but the torque curve stays
near-linear to ≈ 1.5 A. This choice changes K₂ between 1.17 and 1.30.

### Armature reaction — measured torque shortfall vs the linear extrapolation

| I_A (A) | T measured | T linear | shortfall |
|---:|---:|---:|---:|
| 1.50 | 1.75 | 1.81 | 3.4% |
| 2.07 | 2.14 | 2.47 | 13.4% |
| 2.58 | 2.43 | 3.07 | 20.8% |
| 3.59 | 2.87 | 4.25 | 32.5% |
| 3.95 | 2.96 | 4.66 | **36.5%** |

This is the quantitative proof of armature reaction and it is strong analysis material.

### Speed droop / regulation

| Quantity | Value |
|---|---|
| n at no load (I_A = 0.28 A) | 1501.52 r/min |
| n at I_A = 1.50 A | 1412.45 r/min → **%SR = 6.31 %** |
| n at I_A = 3.95 A | 1079.88 r/min → **%SR = 39.05 %** |
| Peak efficiency P_m/P_in | 78.0 % at I_A = 0.60 A |
| Efficiency at max load | 34.68 % at I_A = 3.95 A |

---

## 6. Table 1 (step 19) — predicted speed droop

Using E_A = 255.73 V (step 14), R_A = 28.48 Ω, K₁ = 5.841 r/min/V:

| I_A (A) | E_RA = I_A·R_A (V) | E_CEMF = E_A − E_RA (V) | n = K₁·E_CEMF (r/min) |
|---:|---:|---:|---:|
| 0.5 | 14.24 | 241.49 | 1410.6 |
| 1.0 | 28.48 | 227.25 | 1327.4 |
| 1.5 | 42.72 | 213.01 | 1244.2 |

Local AC network: 240 V (per the manual's Table 1 header).

---

## 7. ⚠️ The big discrepancy — predicted vs measured droop

| I_A (A) | n predicted (Table 1) | n measured (DT212) | error |
|---:|---:|---:|---:|
| 0.5 | 1410.6 | 1453.1 | −2.9 % |
| 1.0 | 1327.4 | ≈1430 | −7.2 % |
| 1.5 | 1244.2 | 1412.5 | **−11.9 %** |

The model over-predicts the droop badly. The cleanest way to quantify it is to regress the
measured speed against armature current over the linear region, since equation (4) makes that
a straight line of gradient −K₁R_A and intercept K₁E_A:

| Quantity | Value |
|---|---|
| Measured droop gradient (I_A ≤ 1.5 A, 25 pts) | −63.1 r/min/A (R² = 0.81) |
| Predicted gradient, K₁R_A with R_A = 28.48 Ω | −166.4 r/min/A |
| **Over-prediction factor** | **2.64×** |
| **R_A back-fitted = −(dn/dI_A)/K₁** | **10.80 Ω** |
| E_A implied by the intercept | 255.65 V |
| E_A actually measured (step 14) | 255.73 V — agrees to **0.08 V** |

That last line is the important one: the same regression independently recovers the armature
voltage to within 0.08 V, so the 10.80 Ω it returns is trustworthy.

**Most likely cause:** the step-7 test was run at only 0.507 A. The manual warns on page 7
that *"the non-linear characteristic of the motor brushes causes incorrect results when I_A is
too small."* The brush contact drop is roughly a fixed voltage, so at low current it inflates
the apparent E_A/I_A. A secondary contributor is the rotor spinning at −318.8 r/min instead of
being stationary.

**How this was handled in the report:** report R_A = 28.48 Ω as measured, complete Table 1 with
it exactly as the manual instructs, then in Analysis compare the prediction against DT212 and
explain the gap. The ECU template explicitly invites this — *"Even if you find the results are
not satisfactory, try to explain the possible reason"* — and Observation and Analysis is worth
5 of the 10 marks.

---

## 8. Outstanding items

1. ~~G212-1 was never captured~~ — re-plotted from DT212 and labelled as such.
2. **Rated armature current unknown** — needed to justify the K₂ linear-region cut-off. The
   report infers ≈1.5 A from where the torque curve departs from linearity; confirm this from
   the module front panel or the LVSIM tooltip if you can.
3. **Group member names and student IDs** — required on the cover page.
4. **Experiment date** — screenshots say 2 Sep 2026; confirm this is the lab session date.
5. **Sample report by another student** — described but not present in the repo.
6. **AI declaration** — needs the specific tool name, version and scope.
