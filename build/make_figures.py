#!/usr/bin/env python3
"""Crop Lab-Volt screenshots into report figures and generate the analysis charts."""
import os, subprocess, statistics as st
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

FIG = "build/figs"
LS  = "lab_screenshots"
L2  = "lab report 2"
os.makedirs(FIG, exist_ok=True)

def crop(src, geom, out, scale=None):
    cmd = ["convert", src, "-crop", geom, "+repage"]
    if scale:
        cmd += ["-filter", "Lanczos", "-resize", scale]
    cmd.append(out)
    subprocess.run(cmd, check=True)
    print("  ", out, subprocess.run(["identify","-format","%wx%h",out],
          capture_output=True, text=True).stdout)

# --- line art extracted from the Laboratory 2 manual -----------------------
print("Extracting circuit diagrams from Lab 2.pdf ...")
from pypdf import PdfReader
_r = PdfReader("Lab 2.pdf")
for _page, _idx, _out in [(4, 0, f"{FIG}/pdf_p5_0.jpg"),    # Figure 7  equivalent circuit
                          (8, 0, f"{FIG}/pdf_p9_0.jpg")]:   # Figure 13 motor + brake
    open(_out, "wb").write(_r.pages[_page].images[_idx].data)
    print("  ", _out)

print("Cropping screenshots ...")
crop(f"{LS}/Screenshot 2026-09-02 085810.png", "300x560+0+50",  f"{FIG}/ra_meters.png",  "200%")
crop(f"{LS}/Screenshot 2026-09-02 091123.png", "660x470+640+295", f"{FIG}/dt211.png",    "180%")
crop(f"{LS}/Screenshot 2026-09-02 091254.png", "650x500+300+110", f"{FIG}/g211.png",     "180%")
crop(f"{LS}/Screenshot 2026-09-02 092337.png", "1610x540+0+68",   f"{FIG}/step14.png",   "120%")
crop(f"{LS}/Screenshot 2026-09-02 093106.png", "800x852+0+60",    f"{FIG}/dt212.png",    "190%")
crop(f"{LS}/Screenshot 2026-09-02 093153.png", "640x500+80+30",   f"{FIG}/g212.png",     "180%")
crop(f"{L2}/Screenshot 2026-09-02 094846.png", "634x478+0+0",     f"{FIG}/g212_2.png",   "180%")

# manual line-art, upscaled for print
for src, out in [("build/figs/pdf_p5_0.jpg", f"{FIG}/fig_equiv_circuit.png"),
                 ("build/figs/pdf_p9_0.jpg", f"{FIG}/fig_circuit13.png")]:
    subprocess.run(["convert", src, "-filter", "Lanczos", "-resize", "300%",
                    "-unsharp", "0x1+0.6+0.02", "-bordercolor", "white",
                    "-border", "10x10", out], check=True)
    print("  ", out)

# ----------------------------------------------------------------------------
# DT211 - speed vs armature voltage (no load, IF = 210 mA)
# ----------------------------------------------------------------------------
DT211 = [
    (0.43,0.02,0.01,0.21,0.01,0.00,0.08),   (26.03,0.04,0.18,0.20,4.64,0.21,126.00),
    (53.17,0.03,0.20,0.20,10.58,0.23,285.97),(82.58,0.03,0.22,0.20,18.55,0.25,459.05),
    (108.93,0.03,0.24,0.20,26.46,0.26,614.33),(136.59,0.04,0.26,0.20,35.54,0.28,779.98),
    (160.82,0.03,0.27,0.20,43.20,0.29,922.85),(187.72,0.03,0.27,0.20,52.12,0.30,1083.56),
    (213.66,0.03,0.28,0.20,61.09,0.31,1240.19),(239.94,0.03,0.29,0.20,70.42,0.32,1394.89),
    (271.14,0.02,0.29,0.20,80.62,0.33,1581.36),
]
# ----------------------------------------------------------------------------
# DT212 - torque vs armature current, EA held ~ 255.7 V, n0 = 1500 r/min
# 40 rows, read from Screenshot 2026-09-02 093106.png (the complete record)
# ----------------------------------------------------------------------------
DT212 = [
    (255.73,0.04,0.28,0.20,72.07,0.32,1501.52,50.63,70.24,738.56),
    (252.74,0.03,0.28,0.20,72.46,0.35,1499.06,54.47,75.18,727.83),
    (252.88,0.03,0.32,0.20,82.10,0.40,1492.44,62.75,76.43,668.29),
    (252.91,0.04,0.36,0.20,92.74,0.46,1477.29,70.70,76.24,610.95),
    (252.82,0.04,0.40,0.20,103.38,0.52,1462.26,78.88,76.30,559.64),
    (252.64,0.03,0.43,0.20,110.49,0.56,1462.12,84.98,76.91,528.92),
    (252.50,0.03,0.47,0.20,119.75,0.61,1461.53,92.62,77.35,493.67),
    (252.44,0.04,0.50,0.20,128.67,0.66,1453.14,100.11,77.80,462.92),
    (252.28,0.03,0.56,0.20,142.74,0.73,1443.73,109.92,77.01,421.97),
    (252.37,0.02,0.60,0.20,152.52,0.78,1453.51,118.97,78.00,397.74),
    (251.95,0.03,0.65,0.20,164.77,0.84,1438.24,127.22,77.21,369.36),
    (251.71,0.05,0.69,0.20,174.33,0.89,1441.41,134.81,77.33,350.02),
    (251.65,0.04,0.73,0.20,185.93,0.95,1439.30,142.64,76.72,329.21),
    (251.17,0.04,0.77,0.20,195.62,0.99,1432.59,149.13,76.23,312.60),
    (251.27,0.03,0.84,0.20,211.36,1.07,1427.05,160.62,75.99,290.88),
    (251.19,0.05,0.88,0.20,223.62,1.14,1433.82,170.65,76.31,275.47),
    (250.96,0.03,0.93,0.20,234.92,1.19,1422.61,176.57,75.16,262.34),
    (250.80,0.04,0.97,0.20,244.95,1.23,1425.06,183.92,75.08,251.71),
    (250.97,0.04,1.02,0.20,256.36,1.28,1425.09,191.56,74.72,241.11),
    (250.70,0.04,1.16,0.20,293.23,1.44,1417.57,214.18,73.04,211.20),
    (250.31,0.05,1.27,0.20,319.21,1.54,1418.89,228.91,71.71,193.99),
    (250.32,0.02,1.33,0.20,335.22,1.60,1415.50,237.08,70.72,184.88),
    (250.11,0.01,1.38,0.20,346.00,1.64,1419.54,243.54,70.39,179.05),
    (249.97,0.04,1.46,0.20,365.99,1.71,1409.04,251.80,68.80,169.31),
    (249.83,0.04,1.50,0.20,376.53,1.75,1412.45,258.13,68.56,164.40),
    (249.51,0.03,1.59,0.20,399.02,1.81,1405.96,266.49,66.79,154.91),
    (249.35,0.03,1.63,0.20,409.19,1.85,1411.35,273.04,66.73,150.91),
    (249.11,0.05,1.68,0.20,419.81,1.88,1410.48,278.37,66.31,146.87),
    (248.88,0.05,1.76,0.20,438.85,1.93,1393.70,281.89,64.23,140.31),
    (248.85,0.05,1.82,0.20,454.61,1.98,1409.10,292.67,64.38,135.48),
    (248.41,0.03,1.90,0.20,474.41,2.04,1399.07,298.61,62.94,129.47),
    (248.35,0.04,1.98,0.20,493.69,2.08,1396.34,303.93,61.56,124.33),
    (248.15,0.04,2.07,0.20,516.25,2.14,1396.23,313.18,60.66,118.79),
    (247.78,0.02,2.26,0.19,561.79,2.24,1358.41,318.99,56.78,108.88),
    (247.34,0.04,2.42,0.20,600.14,2.34,1347.34,330.37,55.05,101.62),
    (246.97,0.04,2.58,0.19,638.68,2.43,1317.12,334.89,52.43,95.23),
    (246.54,0.04,2.77,0.19,684.38,2.52,1284.36,338.83,49.51,88.59),
    (245.75,0.05,3.05,0.19,752.96,2.57,1133.84,305.09,40.52,80.08),
    (244.39,0.03,3.59,0.19,880.53,2.87,1147.08,344.38,39.11,67.63),
    (243.25,0.04,3.95,0.19,965.66,2.96,1079.88,334.94,34.68,61.04),
]

EA_R, IA_R = 14.44, 0.507
RA = EA_R / IA_R
EA14 = 255.73

def linfit(xs, ys):
    mx, my = st.mean(xs), st.mean(ys)
    m = sum((x-mx)*(y-my) for x, y in zip(xs, ys)) / sum((x-mx)**2 for x in xs)
    b = my - m*mx
    sr = sum((y-(m*x+b))**2 for x, y in zip(xs, ys))
    stt = sum((y-my)**2 for y in ys)
    return m, b, 1 - sr/stt

ea211 = [r[0] for r in DT211]; n211 = [r[6] for r in DT211]
K1_end = (n211[-1]-n211[0])/(ea211[-1]-ea211[0])
K1_ls, b1, r2_1 = linfit(ea211, n211)

IA = [r[2] for r in DT212]; T = [r[5] for r in DT212]
N  = [r[6] for r in DT212]; EFF = [r[8] for r in DT212]

LIN = 1.50                                   # linear portion cut-off
xs = [i for i in IA if i <= LIN]
ys = [t for i, t in zip(IA, T) if i <= LIN]
K2_end = (ys[-1]-ys[0])/(xs[-1]-xs[0])
K2_ls, b2, r2_2 = linfit(xs, ys)

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 10,
    "axes.grid": True, "grid.alpha": 0.3, "grid.linestyle": "--",
    "figure.dpi": 200, "savefig.bbox": "tight", "axes.axisbelow": True,
})

# --- G212-1 : speed vs armature current (step 20, never captured in the lab) ---
fig, ax = plt.subplots(figsize=(6.0, 3.6))
ax.plot(IA, N, "o-", color="#1f4e79", ms=3.4, lw=1.3)
ax.set_xlabel("Armature Current $I_A$ (A)")
ax.set_ylabel("DC Motor Speed $n$ (r/min)")
ax.set_title("G212-1  —  DC Motor Speed vs Armature Current", fontsize=10.5)
ax.set_xlim(0, 4.2); ax.set_ylim(1000, 1550)
fig.savefig(f"{FIG}/g212_1_replot.png"); plt.close(fig)

# --- armature reaction: measured torque vs linear extrapolation ---
fig, ax = plt.subplots(figsize=(6.0, 3.6))
ax.plot(IA, T, "o", color="#1f4e79", ms=4, label="Measured torque")
xe = [0, 4.1]
ax.plot(xe, [K2_ls*x + b2 for x in xe], "--", color="#c00000", lw=1.4,
        label=f"Linear fit over $I_A \\leq$ {LIN} A  ($K_2$ = {K2_ls:.3f} N·m/A)")
ax.axvline(LIN, color="grey", lw=1, ls=":")
ax.annotate("onset of armature reaction", xy=(LIN, 0.45), xytext=(1.75, 0.35),
            fontsize=8.5, color="grey")
ax.set_xlabel("Armature Current $I_A$ (A)")
ax.set_ylabel("DC Motor Torque $T$ (N·m)")
ax.set_title("Measured torque vs linear current-to-torque model", fontsize=10.5)
ax.set_xlim(0, 4.2); ax.set_ylim(0, 5.0); ax.legend(fontsize=8.5, loc="upper left")
fig.savefig(f"{FIG}/armature_reaction.png"); plt.close(fig)

# --- predicted vs measured speed droop ---
fig, ax = plt.subplots(figsize=(6.0, 3.6))
ax.plot(IA, N, "o", color="#1f4e79", ms=4, label="Measured (DT212)")
xm = [0.2 + 0.05*k for k in range(80)]
ax.plot(xm, [K1_end*(EA14 - x*RA) for x in xm], "--", color="#c00000", lw=1.4,
        label=f"Model with measured $R_A$ = {RA:.2f} Ω")
# effective resistance from the gradient of the measured droop over the linear region
_m, _b, _r2 = linfit([i for i in IA if i <= LIN],
                     [n for i, n in zip(IA, N) if i <= LIN])
RA_fit = -_m / K1_end
ax.plot(xm, [K1_end*(EA14 - x*RA_fit) for x in xm], "-.", color="#2e7d32", lw=1.4,
        label=f"Model with fitted $R_A$ = {RA_fit:.2f} Ω")
ax.set_xlabel("Armature Current $I_A$ (A)")
ax.set_ylabel("DC Motor Speed $n$ (r/min)")
ax.set_title("Speed droop: measured vs predicted by $n = K_1(E_A - I_A R_A)$", fontsize=10.5)
ax.set_xlim(0, 4.2); ax.set_ylim(600, 1600); ax.legend(fontsize=8.5, loc="lower left")
fig.savefig(f"{FIG}/droop_model.png"); plt.close(fig)

# --- efficiency ---
fig, ax = plt.subplots(figsize=(6.0, 3.4))
ax.plot(IA, EFF, "o-", color="#6a1b9a", ms=3.4, lw=1.3)
ax.set_xlabel("Armature Current $I_A$ (A)")
ax.set_ylabel("$P_m / P_{in}$  (%)")
ax.set_title("Conversion efficiency vs armature current", fontsize=10.5)
ax.set_xlim(0, 4.2); ax.set_ylim(30, 85)
fig.savefig(f"{FIG}/efficiency.png"); plt.close(fig)

print("\nConstants (40-row DT212):")
print(f"  RA      = {RA:.2f} ohm")
print(f"  K1(end) = {K1_end:.4f} r/min/V   K1(ls) = {K1_ls:.4f}, R2 = {r2_1:.5f}")
print(f"  K2(end) = {K2_end:.4f} N.m/A     K2(ls) = {K2_ls:.4f}, R2 = {r2_2:.5f}  (IA<={LIN})")
print(f"  RA fitted from droop gradient = {RA_fit:.2f} ohm (implied EA = {_b/K1_end:.2f} V, R2 = {_r2:.4f})")
for ia in (0.5, 1.0, 1.5):
    era = ia*RA; ec = EA14-era
    print(f"  Table1  IA={ia}: ERA={era:.2f} V, ECEMF={ec:.2f} V, n={ec*K1_end:.1f} r/min")
print(f"  n no-load {N[0]:.2f}, n@1.5A {N[24]:.2f} -> SR {100*(N[0]-N[24])/N[24]:.2f} %")
print(f"  n@3.95A {N[-1]:.2f} -> SR {100*(N[0]-N[-1])/N[-1]:.2f} %")
print(f"  peak eff {max(EFF):.2f} % at IA={IA[EFF.index(max(EFF))]} A")
