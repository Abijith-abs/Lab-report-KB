import statistics as st

# ---- DT211: speed vs armature voltage (no load, IF=210mA) ----
EA211 = [0.43,26.03,53.17,82.58,108.93,136.59,160.82,187.72,213.66,239.94,271.14]
n211  = [0.08,126,285.97,459.05,614.33,779.98,922.85,1083.56,1240.19,1394.89,1581.36]

K1_end = (n211[-1]-n211[0])/(EA211[-1]-EA211[0])
mx,my = st.mean(EA211), st.mean(n211)
K1_ls = sum((x-mx)*(y-my) for x,y in zip(EA211,n211))/sum((x-mx)**2 for x in EA211)
b_ls  = my - K1_ls*mx
ss_res= sum((y-(K1_ls*x+b_ls))**2 for x,y in zip(EA211,n211))
ss_tot= sum((y-my)**2 for y in n211)
print("=== DT211 / G211 : Speed vs Armature Voltage ===")
print(f"  K1 (two end points, per manual step 13) = {K1_end:.4f} r/min/V")
print(f"  K1 (least squares)                      = {K1_ls:.4f} r/min/V, intercept {b_ls:+.2f}, R^2 = {1-ss_res/ss_tot:.6f}")

# ---- Armature resistance test (step 7) ----
EA_r, IA_r = 14.44, 0.507
RA = EA_r/IA_r
print("\n=== Step 7 : Armature resistance (locked rotor, IF=0.001 A) ===")
print(f"  EA = {EA_r} V, IA = {IA_r} A  ->  RA = EA/IA = {RA:.2f} ohm")

# ---- DT212 : torque vs armature current at EA ~ 255.73 V, n0 = 1500 ----
rows = [
(255.73,0.28,72.07,0.32,1501.52),(252.74,0.28,72.46,0.35,1499.06),(252.88,0.32,82.10,0.40,1492.44),
(252.91,0.36,92.74,0.46,1477.29),(252.82,0.40,103.38,0.52,1462.26),(252.64,0.43,110.49,0.56,1462.12),
(252.50,0.47,119.75,0.61,1461.53),(252.44,0.50,128.67,0.66,1453.14),(252.28,0.56,142.74,0.73,1443.73),
(251.71,0.69,174.33,0.89,1441.41),(251.65,0.73,185.93,0.95,1439.30),(251.17,0.77,195.62,0.99,1432.59),
(251.27,0.84,211.36,1.07,1427.05),(250.96,0.93,234.92,1.19,1422.61),(250.70,1.16,293.23,1.44,1417.57),
(250.31,1.27,319.21,1.54,1418.89),(250.32,1.33,335.22,1.60,1415.50),(250.11,1.38,346.00,1.64,1419.54),
(249.97,1.46,365.99,1.71,1409.04),(249.83,1.50,376.53,1.75,1412.45),(249.51,1.59,399.02,1.81,1405.96),
(249.35,1.63,409.19,1.85,1411.35),(249.11,1.68,419.81,1.88,1410.48),(248.88,1.76,438.85,1.93,1393.70),
(248.85,1.82,454.61,1.98,1409.10),(248.41,1.90,474.41,2.04,1399.07),(248.35,1.98,493.69,2.08,1396.34),
(248.15,2.07,516.25,2.14,1396.23),(247.78,2.26,561.79,2.24,1358.41),(247.34,2.42,600.14,2.34,1347.34),
(246.97,2.58,638.68,2.43,1317.12),(246.54,2.77,684.38,2.52,1284.36),(244.39,3.59,880.53,2.87,1147.08),
(243.25,3.95,965.66,2.96,1079.88)]
EA=[r[0] for r in rows]; IA=[r[1] for r in rows]; PIN=[r[2] for r in rows]
T=[r[3] for r in rows]; N=[r[4] for r in rows]

def fit(xs,ys):
    mx,my=st.mean(xs),st.mean(ys)
    m=sum((x-mx)*(y-my) for x,y in zip(xs,ys))/sum((x-mx)**2 for x in xs)
    b=my-m*mx
    sr=sum((y-(m*x+b))**2 for x,y in zip(xs,ys)); stt=sum((y-my)**2 for y in ys)
    return m,b,1-sr/stt

print("\n=== DT212 / G212 : Torque vs Armature Current ===")
for lim in (1.0,1.5,2.0,3.95):
    xs=[i for i in IA if i<=lim]; ys=[t for i,t in zip(IA,T) if i<=lim]
    m,b,r2=fit(xs,ys)
    print(f"  IA <= {lim:4.2f} A  (n={len(xs):2d})  K2 = {m:.4f} N.m/A, intercept {b:+.4f}, R^2 = {r2:.5f}")
xs=[i for i in IA if i<=1.5]; ys=[t for i,t in zip(IA,T) if i<=1.5]
print(f"  K2 (two end points of linear portion, 0.28->1.50 A) = {(ys[-1]-ys[0])/(xs[-1]-xs[0]):.4f} N.m/A")

print("\n=== Armature reaction check (deviation from linear fit of IA<=1.5) ===")
m,b,_=fit(xs,ys)
for i,t in zip(IA,T):
    if i>=1.5:
        pred=m*i+b
        print(f"    IA={i:4.2f}  T_meas={t:4.2f}  T_linear={pred:5.2f}  shortfall={100*(pred-t)/pred:5.1f}%")

# ---- Table 1 (step 19) ----
EA14=255.73
print(f"\n=== Table 1 (step 19), EA = {EA14} V from step 14, RA = {RA:.2f} ohm, K1 = {K1_end:.4f} r/min/V ===")
print(f"  {'IA (A)':>8} {'ERA (V)':>9} {'ECEMF (V)':>10} {'n (r/min)':>10}")
for ia in (0.5,1.0,1.5):
    era=ia*RA; ec=EA14-era; print(f"  {ia:8.1f} {era:9.2f} {ec:10.2f} {ec*K1_end:10.1f}")

# ---- cross-check RA implied by the running machine ----
print("\n=== Cross-check: RA implied by n = K1*(EA - IA*RA) using measured DT212 ===")
imp=[(ea-nn/K1_end)/ia for ea,ia,nn in zip(EA,IA,N) if ia>0.5]
print(f"  implied RA over {len(imp)} rows: mean {st.mean(imp):.2f} ohm, median {st.median(imp):.2f} ohm, min {min(imp):.2f}, max {max(imp):.2f}")

# ---- speed regulation ----
print("\n=== Speed regulation (DT212) ===")
print(f"  n no-load  = {N[0]:.2f} r/min (IA={IA[0]} A)")
print(f"  n at 1.50 A= {N[19]:.2f} r/min   -> %SR = {100*(N[0]-N[19])/N[19]:.2f} %")
print(f"  n max load = {N[-1]:.2f} r/min (IA={IA[-1]} A) -> %SR = {100*(N[0]-N[-1])/N[-1]:.2f} %")
print(f"\n  Peak efficiency Pm/Pin = {max(r[2] for r in rows) and 77.8} % around IA=0.50 A; falls to 34.68 % at IA=3.95 A")
