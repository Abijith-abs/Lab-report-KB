# Cross-check of `LAB_REPORT_2 emt.docx` against the laboratory screenshots

Checked on 28 September 2026. Ground truth is the set of Lab-Volt screen captures in
`lab_screenshots/` and `lab report 2/`, transcribed into `analysis/dt211.csv` and
`analysis/dt212.csv` and re-verified cell-by-cell against the images for this check.

---

## Summary

| Area | Result |
|---|---|
| DT211 raw data (Table 3), 11 rows x 6 cols | **66/66 values correct** |
| DT212 raw data (Table 4), 40 rows x 8 cols | **320/320 values correct** |
| Step-7 meter readings (Table 2) | **correct** |
| Derived constants, regressions, efficiencies | **all correct** |
| Table 5 (K2 fit ranges) | **correct** |
| Table 6 (step-19 predictions) | **correct** |
| Table 8 (torque shortfall), all 8 rows | **correct** |
| Table 9 (predicted vs measured) | **correct** |
| Table 10 (summary) | **correct** |
| Document structure: 21 figures, 10 tables, all cross-references resolve | **correct** |

The numbers are in very good shape. The issues below are wording, attribution and
housekeeping, not arithmetic — with one exception (issue 1), which reverses the meaning
of a result.

---

## 1. Section 6.1.4 — the direction of the droop error is reversed  **(must fix)**

Current text:

> "The droop is, however, much less than expected. With an armature current of 1.5 A, the
> model gives 1244.2 r/min while the actual speed is 1412.45 r/min. **In terms of slopes,
> the model under-estimates the actual speed loss by a factor of 2.6.**"

The model predicts **1244.2** r/min and the machine actually ran at **1412.45** r/min. The
model therefore predicts *more* speed loss than occurred, so it **over-estimates** the
droop. As written the sentence contradicts the sentence immediately before it, and it
contradicts Section 7.3, which correctly says the model "greatly overstates its slope",
and the Conclusion.

Suggested replacement:

> In terms of slopes, the model **over-estimates** the actual speed loss by a factor of 2.6.

Supporting numbers: measured gradient 63.1 r/min/A; model gradient K1*RA = 166 r/min/A;
166 / 63.1 = 2.64.

---

## 2. Step 14 armature voltage is attributed to the wrong screenshot  **(should fix)**

Four places state that step 14 gave **255.73 V at 1501.52 r/min**:

- Figure 6 caption
- Figure 17 caption (Appendix A)
- Section 5.3, lead-in to equation (9)
- Section 5.5, "the armature voltage Ea = 255.73 V obtained in step 14"

The step-14 screen capture is `Screenshot 2026-09-02 092337.png`, taken at 09:23, and its
meters read:

| Meter | Reading |
|---|---|
| E arm. (EA) | **254.7 V** |
| Speed | **1501 r/min** |
| I arm. (IA) | 0.279 A |
| I field (IF) | 0.200 A |

The pair 255.73 V / 1501.52 r/min is **row 0 of DT212**, logged at 09:31 — eight minutes
later. So Figure 6's caption describes numbers that are not visible in Figure 6. A marker
comparing the figure with its caption would see the mismatch.

This is worth turning into an observation rather than just correcting, because the 1.0 V
gap (0.4 %) is the same supply drift already discussed in Section 7.6. Suggested handling:

- Equation (9) and the Figure 6 / Figure 17 captions state **254.7 V at 1501 r/min**.
- Add a sentence noting that logging of DT212 began at 09:31 with a first row of 255.73 V
  and 1501.52 r/min, that the two readings describe the same operating point and differ by
  0.4 %, and that the logged 255.73 V is the value carried through the calculations so the
  constants stay consistent with the dataset they came from.
- Section 5.5 then reads "the nominal armature voltage Ea = 255.73 V logged as the first
  row of DT212" instead of "obtained in step 14".

All downstream arithmetic is unaffected — it already uses 255.73 V throughout.

---

## 3. "Nearly three decades of speed" is not right  **(should fix)**

Section 7.1:

> "Given R2 = 0.9998 over a range of nearly three decades of speed..."

DT211 covers 0.08 to 1581.36 r/min. Counting the near-zero point that is 4.3 decades;
ignoring it, the real measured span is 126 to 1581 r/min, which is 1.1 decades. Neither is
"nearly three".

Suggested replacement:

> across a speed range extending from 126 r/min to 1581 r/min, a more than twelvefold
> variation

(I had the same error in the version I generated; it is now fixed there.)

---

## 4. Section 1.0 Aims — malformed relationship  **(should fix)**

> "Verify the no-load voltage and speed relationship **(Ea = Kn1)** of the armature."

`Ea = Kn1` is garbled and disagrees with equation (2) later in the same report, which
correctly gives `n = K1 * Ecemf`. With K1 in r/min/V the voltage is `Ecemf = n / K1`.

Suggested replacement: `(n = K1 * Ecemf)`.

Also in the same list, the first bullet ends with a double full stop (`measurement..`).

---

## 5. Unfilled placeholders in Section 10  **(must fix before submission)**

Still present verbatim:

- `[REVIEW AND EDIT THIS SECTION SO THAT IT ACCURATELY AND COMPLETELY DESCRIBES YOUR OWN USE OF AI TOOLS, THEN DELETE THIS INSTRUCTION.]`
- `I acknowledge the use of [INSERT TOOL NAME AND VERSION NUMBER] ...`

The cover page is complete — all four group members and student IDs are filled in.

---

## 6. Note, not an error: the LVDAM `RA = EA/IA` column is internally inconsistent

Section 7.4 says the values in that column "are just the ratios of the terminal voltage to
the armature current ... between 738 and 61 ohms". The quoted range matches the screen
exactly (max 738.56, min 61.04), so the report is faithful to the instrument.

Worth knowing, though: the column does **not** equal EA/IA computed from the EA and IA
columns beside it.

| Row | EA (V) | IA (A) | EA/IA | Column shows |
|---|---|---|---|---|
| 0 | 255.73 | 0.28 | 913.32 | 738.56 |
| 20 | 250.31 | 1.27 | 197.09 | 193.99 |
| 39 | 243.25 | 3.95 | 61.58 | 61.04 |

The gap is 24 % at the lightest load and under 1 % at the heaviest, consistent with the DAI
computing the ratio from its own internal averaging rather than from the two-decimal values
it displays. This does not weaken the argument in Section 7.4 — it strengthens it, since
the column is unreliable at exactly the low currents where the step-7 test was performed.
If you want to use it, one added sentence would cover it.

---

## Confirmed correct — no action needed

Spot-checked and verified against the screenshots:

- Ra = 14.44 / 0.507 = 28.48 ohm; step-7 meters including the -318.8 r/min and -0.341 N.m
  anomaly, and IF = 0.001 A
- K1 = 5.841 r/min/V two-point; least-squares 5.893; intercept -21.8 r/min = 1.38 % of the
  maximum speed ("less than 1.4 %" is right); R2 = 0.9998
- K2 = 1.172 N.m/A two-point, 1.164 least-squares, R2 = 0.9943 for IA <= 1.5 A
- Table 5 fit ranges: 1.295 / 1.164 / 1.049 / 0.780 and R2 0.9980 / 0.9943 / 0.9881 / 0.9438
- Table 6: ERA 14.24 / 28.48 / 42.72; Ecemf 241.49 / 227.25 / 213.01; n 1410.6 / 1327.4 / 1244.2
- Table 8 shortfalls: 3.4, 5.7, 8.7, 10.4, 13.5, 18.8, 23.4, 32.4 % — all correct to 0.1 %
- Table 9 errors: -2.9, -6.9, -11.9 %
- Droop regression: slope 63.1 r/min/A, R2 = 0.81, intercept 1493.3 r/min -> 255.65 V,
  Ra(eff) = 10.80 ohm = 38 % of 28.48 ohm
- Speed regulation 6.31 % at 1.5 A and 39.05 % at 3.95 A
- Efficiency 70.2 % light load, peak 78.0 % at 0.60 A, 34.7 % at 3.95 A
- Supply drift 255.73 -> 243.25 V = 4.9 %; field current 0.20 -> 0.19 A
- Review question 5 arithmetic: 995 and 875 r/min; 13.7 % regulation for the example machine
- **The 40-row DT212 was used, which is the correct choice.** The 09:48 capture in
  `lab report 2/` holds only 34 rows — six were deleted (IA = 0.60, 0.65, 0.88, 0.97, 1.02
  and 3.05 A). Using it would have moved K2, the efficiency peak and every regression.

Reproduce all of this with:

```
python3 analysis/verify_against_screenshots.py
```
