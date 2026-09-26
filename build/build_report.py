#!/usr/bin/env python3
"""Build the ENS5230.5 Laboratory Report 2 Word document."""
import os, statistics as st
from docx import Document
from docx.shared import Pt, Mm, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

FIG = "build/figs"
LS  = "lab_screenshots"
L2  = "lab report 2"
OUT = "Lab_Report_2_Separately_Excited_DC_Motor.docx"

FONT      = "Arial"
BODY_SIZE = Pt(11)

# ================================================================== data ====
_src = open("build/make_figures.py").read()
ns = {}
exec(_src[_src.index("DT211 = ["):_src.index("EA_R, IA_R")], ns)
DT211, DT212 = ns["DT211"], ns["DT212"]

EA_R, IA_R = 14.44, 0.507
RA   = EA_R / IA_R                 # 28.48 ohm
EA14 = 255.73                      # armature voltage at n = 1500 r/min (step 14)
LIN  = 1.50                        # upper limit of the linear torque region

def linfit(xs, ys):
    mx, my = st.mean(xs), st.mean(ys)
    m = sum((x-mx)*(y-my) for x, y in zip(xs, ys)) / sum((x-mx)**2 for x in xs)
    b = my - m*mx
    sr = sum((y-(m*x+b))**2 for x, y in zip(xs, ys))
    stt = sum((y-my)**2 for y in ys)
    return m, b, 1 - sr/stt

ea211 = [r[0] for r in DT211]; n211 = [r[6] for r in DT211]
K1 = (n211[-1]-n211[0])/(ea211[-1]-ea211[0])          # 5.841 r/min/V
K1_ls, B1, R2_1 = linfit(ea211, n211)

IA  = [r[2] for r in DT212]; T = [r[5] for r in DT212]
N   = [r[6] for r in DT212]; EFF = [r[8] for r in DT212]
xsL = [i for i in IA if i <= LIN]; ysL = [t for i, t in zip(IA, T) if i <= LIN]
K2  = (ysL[-1]-ysL[0])/(xsL[-1]-xsL[0])               # 1.172 N.m/A
K2_ls, B2, R2_2 = linfit(xsL, ysL)

K2_10, _, R2_10 = linfit([i for i in IA if i <= 1.0], [t for i, t in zip(IA, T) if i <= 1.0])
K2_20, _, R2_20 = linfit([i for i in IA if i <= 2.0], [t for i, t in zip(IA, T) if i <= 2.0])
K2_all, _, R2_all = linfit(IA, T)

# effective armature resistance from the gradient of the measured droop
DM, DB, DR2 = linfit(xsL, [n for i, n in zip(IA, N) if i <= LIN])
RA_eff  = -DM / K1          # 10.80 ohm
EA_impl = DB / K1           # 255.65 V  (compare measured 255.73 V)
DROOP_M = -DM               # 63.1 r/min/A measured
DROOP_P = K1 * RA           # 166.4 r/min/A predicted
FACTOR  = DROOP_P / DROOP_M # 2.6

EA_DRIFT = abs(100*(DT212[-1][0]-DT212[0][0])/DT212[0][0])
EFF_MAX  = max(EFF); EFF_MAX_IA = IA[EFF.index(EFF_MAX)]

# ============================================================== registry ====
FIG_ORDER = ['equiv_circuit', 'circuit13', 'ra_meters', 'dt211_shot', 'g211',
             'step14', 'dt212_shot', 'g212', 'g212_2', 'g212_1',
             'armature_reaction', 'droop_model', 'efficiency'] + \
            [f'appA{i}' for i in range(1, 9)]
TAB_ORDER = ['equipment', 'ra_readings', 'dt211', 'dt212', 'k2_fits',
             'table1', 'ar_departure', 'pred_vs_meas', 'summary']
FN = {k: i+1 for i, k in enumerate(FIG_ORDER)}
TN = {k: i+1 for i, k in enumerate(TAB_ORDER)}
def FR(k): return f"Figure {FN[k]}"
def TR(k): return f"Table {TN[k]}"

# =========================================================== doc helpers ====
doc = Document()
_seq = {'Figure': 0, 'Table': 0}

def style(name, size, bold=False, italic=False, before=0, after=6,
          spacing=1.15, align=None, color=(0, 0, 0)):
    s = doc.styles[name]
    s.font.name = FONT; s.font.size = Pt(size)
    s.font.bold = bold; s.font.italic = italic
    s.font.color.rgb = RGBColor(*color)
    rpr = s.element.get_or_add_rPr()
    rf = rpr.find(qn('w:rFonts'))
    if rf is None:
        rf = OxmlElement('w:rFonts'); rpr.append(rf)
    for a in ('w:ascii', 'w:hAnsi', 'w:cs', 'w:eastAsia'):
        rf.set(qn(a), FONT)
    pf = s.paragraph_format
    pf.space_before = Pt(before); pf.space_after = Pt(after)
    pf.line_spacing = spacing
    if align is not None:
        pf.alignment = align
    return s

style('Normal',    11,   after=6,  spacing=1.15, align=WD_ALIGN_PARAGRAPH.JUSTIFY)
style('Heading 1', 15,   bold=True, before=14, after=6,
      align=WD_ALIGN_PARAGRAPH.LEFT, color=(0x1F, 0x3B, 0x63))
style('Heading 2', 12.5, bold=True, before=10, after=4,
      align=WD_ALIGN_PARAGRAPH.LEFT, color=(0x1F, 0x3B, 0x63))
style('Heading 3', 11.5, bold=True, italic=True, before=8, after=3,
      align=WD_ALIGN_PARAGRAPH.LEFT, color=(0x33, 0x33, 0x33))
style('Caption',   9.5,  italic=True, before=3, after=10, spacing=1.0,
      align=WD_ALIGN_PARAGRAPH.CENTER, color=(0x40, 0x40, 0x40))
for h in ('Heading 1', 'Heading 2', 'Heading 3'):
    doc.styles[h].paragraph_format.keep_with_next = True

s0 = doc.sections[0]
s0.top_margin = s0.bottom_margin = Mm(25.4)
s0.left_margin = s0.right_margin = Mm(25.4)

def para(text="", size=None, bold=False, italic=False, align=None,
         after=None, before=None, spacing=None):
    p = doc.add_paragraph()
    if text:
        r = p.add_run(text); r.bold = bold; r.italic = italic; r.font.name = FONT
        if size: r.font.size = Pt(size)
    if align is not None: p.paragraph_format.alignment = align
    if after is not None: p.paragraph_format.space_after = Pt(after)
    if before is not None: p.paragraph_format.space_before = Pt(before)
    if spacing is not None: p.paragraph_format.line_spacing = spacing
    return p

def h1(t): return doc.add_paragraph(t, style='Heading 1')
def h2(t): return doc.add_paragraph(t, style='Heading 2')

def field(paragraph, instr, result="—"):
    r = paragraph.add_run()
    f1 = OxmlElement('w:fldChar'); f1.set(qn('w:fldCharType'), 'begin')
    it = OxmlElement('w:instrText'); it.set(qn('xml:space'), 'preserve'); it.text = instr
    f2 = OxmlElement('w:fldChar'); f2.set(qn('w:fldCharType'), 'separate')
    t  = OxmlElement('w:t'); t.set(qn('xml:space'), 'preserve'); t.text = result
    f3 = OxmlElement('w:fldChar'); f3.set(qn('w:fldCharType'), 'end')
    for e in (f1, it, f2, t, f3): r._r.append(e)
    return r

def caption(kind, text):
    p = doc.add_paragraph(style='Caption')
    p.add_run(f"{kind} ")
    field(p, f' SEQ {kind} \\* ARABIC ', str(_seq[kind] + 1))
    p.add_run(f": {text}")
    _seq[kind] += 1
    return p

def picture(path, width_in, cap, key):
    assert FN[key] == _seq['Figure'] + 1, \
        f"figure order mismatch at {key}: expected {FN[key]}, next is {_seq['Figure']+1}"
    p = doc.add_paragraph()
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(8); p.paragraph_format.space_after = Pt(2)
    p.add_run().add_picture(path, width=Inches(width_in))
    caption('Figure', cap)

def shade(cell, hexcolor):
    tcPr = cell._tc.get_or_add_tcPr()
    sh = OxmlElement('w:shd'); sh.set(qn('w:val'), 'clear')
    sh.set(qn('w:color'), 'auto'); sh.set(qn('w:fill'), hexcolor)
    tcPr.append(sh)

def table(headers, rows, cap, key, size=9.5, widths=None, align_right_from=1):
    assert TN[key] == _seq['Table'] + 1, \
        f"table order mismatch at {key}: expected {TN[key]}, next is {_seq['Table']+1}"
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = 'Table Grid'; t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, htxt in enumerate(headers):
        c = t.rows[0].cells[i]; c.text = ""
        p = c.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(2); p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.line_spacing = 1.0
        r = p.add_run(htxt); r.bold = True; r.font.size = Pt(size); r.font.name = FONT
        shade(c, 'DCE6F1')
    for row in rows:
        cells = t.add_row().cells
        for i, v in enumerate(row):
            cells[i].text = ""
            p = cells[i].paragraphs[0]
            p.alignment = (WD_ALIGN_PARAGRAPH.RIGHT if i >= align_right_from
                           else WD_ALIGN_PARAGRAPH.LEFT)
            p.paragraph_format.space_after = Pt(1); p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.line_spacing = 1.0
            r = p.add_run(str(v)); r.font.size = Pt(size); r.font.name = FONT
    if widths:
        for i, w in enumerate(widths):
            for row in t.rows:
                row.cells[i].width = Inches(w)
    trPr = t.rows[0]._tr.get_or_add_trPr()
    th = OxmlElement('w:tblHeader'); th.set(qn('w:val'), 'true'); trPr.append(th)
    caption('Table', cap)
    doc.add_paragraph().paragraph_format.space_after = Pt(0)
    return t

def equation(text, number=None):
    p = doc.add_paragraph()
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6); p.paragraph_format.space_after = Pt(6)
    r = p.add_run(text); r.font.name = "Cambria Math"; r.font.size = Pt(11.5)
    if number:
        p.paragraph_format.tab_stops.add_tab_stop(Inches(6.25))
        p.add_run("\t")
        rn = p.add_run(f"({number})"); rn.font.name = FONT; rn.font.size = Pt(11)
    return p

def bullets(items):
    for it in items:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r = p.add_run(it); r.font.name = FONT; r.font.size = BODY_SIZE

def page_break():
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

def set_page_numbering(section, fmt, start=None):
    sectPr = section._sectPr
    for el in sectPr.findall(qn('w:pgNumType')):
        sectPr.remove(el)
    pg = OxmlElement('w:pgNumType'); pg.set(qn('w:fmt'), fmt)
    if start is not None: pg.set(qn('w:start'), str(start))
    cols = sectPr.find(qn('w:cols'))
    (cols.addprevious(pg) if cols is not None else sectPr.append(pg))

def footer_pagenum(section, show=True):
    section.footer.is_linked_to_previous = False
    p = section.footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for r in list(p.runs): r._r.getparent().remove(r._r)
    if show:
        field(p, ' PAGE ', "1")
        for r in p.runs:
            r.font.name = FONT; r.font.size = Pt(9.5)

# ================================================================ COVER =====
footer_pagenum(doc.sections[0], show=False)
for _ in range(2): para("", after=0)
para("EDITH COWAN UNIVERSITY", size=13, bold=True,
     align=WD_ALIGN_PARAGRAPH.CENTER, after=2)
para("School of Engineering", size=12, align=WD_ALIGN_PARAGRAPH.CENTER, after=18)
para("ENS5230.5 — Electrical Machines and Power Systems", size=12.5, bold=True,
     align=WD_ALIGN_PARAGRAPH.CENTER, after=30)
para("Laboratory Report 2", size=22, bold=True,
     align=WD_ALIGN_PARAGRAPH.CENTER, after=6)
para("Operating Characteristics of the\nSeparately-Excited DC Motor", size=17, bold=True,
     align=WD_ALIGN_PARAGRAPH.CENTER, after=30, spacing=1.2)
para("Laboratory Group 2B", size=12, italic=True,
     align=WD_ALIGN_PARAGRAPH.CENTER, after=28)

info = doc.add_table(rows=0, cols=2)
info.alignment = WD_TABLE_ALIGNMENT.CENTER
for label, value in [
    ("Author", "[INSERT YOUR FULL NAME]"),
    ("Student number", "[INSERT YOUR STUDENT ID]"),
    ("Laboratory group members", "[INSERT FULL NAME, STUDENT ID]\n"
                                 "[INSERT FULL NAME, STUDENT ID]\n"
                                 "[INSERT FULL NAME, STUDENT ID]"),
    ("Date of experiment", "2 September 2026"),
    ("Date of submission", "27 September 2026"),
    ("Unit coordinator", "[INSERT UNIT COORDINATOR NAME]"),
]:
    cells = info.add_row().cells
    cells[0].width = Inches(2.1); cells[1].width = Inches(3.4)
    p0 = cells[0].paragraphs[0]; p0.paragraph_format.space_after = Pt(4)
    r0 = p0.add_run(label); r0.bold = True; r0.font.size = Pt(11); r0.font.name = FONT
    p1 = cells[1].paragraphs[0]; p1.paragraph_format.space_after = Pt(4)
    r1 = p1.add_run(value); r1.font.size = Pt(11); r1.font.name = FONT

para("", after=24)
para("This report is submitted individually. All laboratory measurements presented were "
     "recorded during the Laboratory 2B session on 2 September 2026.",
     size=9.5, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER)

# ========================================================== FRONT MATTER ====
fm = doc.add_section(WD_SECTION.NEW_PAGE)
fm.top_margin = fm.bottom_margin = Mm(25.4)
fm.left_margin = fm.right_margin = Mm(25.4)
set_page_numbering(fm, 'lowerRoman', start=1)
footer_pagenum(fm, show=True)

HINT = ("[Right-click here and choose \u201cUpdate Field\u201d, or press Ctrl+A then F9, "
        "to generate this list.]")
# not a Heading style, so the contents page does not list itself
para("Table of Contents", size=15, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT,
     before=14, after=6)
p = doc.add_paragraph(); field(p, ' TOC \\o "1-3" \\h \\z \\u ', HINT)
page_break()
h1("List of Figures")
p = doc.add_paragraph(); field(p, ' TOC \\h \\z \\c "Figure" ', HINT)
para("", after=10)
h1("List of Tables")
p = doc.add_paragraph(); field(p, ' TOC \\h \\z \\c "Table" ', HINT)

# ================================================================= BODY =====
bd = doc.add_section(WD_SECTION.NEW_PAGE)
bd.top_margin = bd.bottom_margin = Mm(25.4)
bd.left_margin = bd.right_margin = Mm(25.4)
set_page_numbering(bd, 'decimal', start=1)
footer_pagenum(bd, show=True)

# ------------------------------------------------------------------ 1.0 ----
h1("1.0  Aim of Experiment")
para("The purpose of this laboratory exercise was to establish, by direct measurement, the "
     "steady-state operating characteristics of a separately-excited direct-current motor and "
     "to test how faithfully those characteristics are described by the simplified equivalent "
     "circuit model presented in the unit material.")
para("The specific objectives were:")
bullets([
    "To determine the armature resistance R\u2090 of the Lab-Volt 8211 DC Motor/Generator using "
    "the direct-current volt-ampere method, and to explain why an ordinary ohmmeter cannot be "
    "used for this measurement.",
    "To measure the no-load relationship between armature voltage E\u2090 and rotational speed "
    "n, and to evaluate the voltage-to-speed constant K\u2081 from the resulting characteristic.",
    "To measure the relationship between armature current I\u2090 and developed torque T at a "
    "fixed armature voltage, and to evaluate the current-to-torque constant K\u2082.",
    "To establish the limit of linearity of the current-to-torque characteristic and to "
    "quantify the departure from linearity caused by armature reaction.",
    "To predict the speed droop of the machine under load using the measured R\u2090 and "
    "K\u2081, and to compare that prediction against the measured loaded performance.",
])

# ------------------------------------------------------------------ 2.0 ----
h1("2.0  Theoretical Background")
h2("2.1  Operating principle")
para("A direct-current motor develops continuous rotation from the interaction of two magnetic "
     "fields: a stationary field produced by the stator and a field produced by current in the "
     "rotor (armature) windings. The commutator and brush assembly reverses the direction of "
     "current in each armature coil as the rotor turns, so that the magnetic poles created in "
     "the rotor do not rotate with it but instead oscillate about a fixed position. Because the "
     "rotor poles remain approximately stationary in space, the attractive force between rotor "
     "and stator poles always acts in the same direction and the shaft turns continuously. "
     "Increasing the number of commutator segments reduces the angle through which the rotor "
     "poles swing between successive commutations and therefore smooths the developed "
     "torque [2].")
para("When the stator field winding is supplied from a source that is electrically independent "
     "of the armature supply, the machine is described as separately excited. This arrangement "
     "allows the field flux and the armature voltage to be controlled independently, which is "
     "what makes the machine convenient for studying the voltage-speed and current-torque "
     "relationships in isolation [1].")

h2("2.2  Equivalent circuit and governing relationships")
para(f"The steady-state electrical behaviour of the armature circuit is represented by the "
     f"simplified equivalent circuit of {FR('equiv_circuit')}. The applied armature voltage "
     f"E\u2090 drives a current I\u2090 through the armature resistance R\u2090, producing an "
     f"ohmic drop E\u1d3f\u1d2c, and against the speed-dependent induced voltage "
     f"E\u1d04\u1d07\u1d0d\u1da0.")
picture(f"{FIG}/fig_equiv_circuit.png", 3.9,
        "Simplified equivalent circuit of the armature of a DC motor "
        "(redrawn from the Laboratory 2 manual, Figure 7 [2]).", "equiv_circuit")
para("Applying Kirchhoff's voltage law around the armature loop gives:")
equation("E\u2090 = E\u1d04\u1d07\u1d0d\u1da0 + E\u1d3f\u1d2c "
         "= E\u1d04\u1d07\u1d0d\u1da0 + I\u2090 R\u2090", 1)
para("The induced voltage is proportional to the speed, and the developed torque is "
     "proportional to the armature current, provided the field flux is held constant:")
equation("n = K\u2081 · E\u1d04\u1d07\u1d0d\u1da0", 2)
equation("T = K\u2082 · I\u2090", 3)
para("where K\u2081 is expressed in r/min/V and K\u2082 in N·m/A. Combining equations (1) "
     "and (2) gives the loaded speed of the machine directly in terms of quantities that can be "
     "measured at its terminals:")
equation("n = K\u2081 (E\u2090 − I\u2090 R\u2090)", 4)

h2("2.3  Speed droop under mechanical load")
para("Equation (4) predicts the behaviour of the machine when the armature voltage is held "
     "constant and the mechanical load is increased. A larger load demands a larger torque, and "
     "by equation (3) a larger armature current. The ohmic drop I\u2090R\u2090 therefore rises, "
     "less of the applied voltage remains available as back-EMF, and the speed falls. This "
     "progressive reduction of speed with load is referred to as speed droop, and it is "
     "quantified by the speed regulation:")
equation("%SR = (n_no-load − n_full-load) / n_full-load × 100 %", 5)
para("For an ideal machine with constant R\u2090 the droop is linear in I\u2090, with a "
     "gradient of −K\u2081R\u2090 r/min per ampere.")

h2("2.4  Why the armature resistance cannot be measured with an ohmmeter")
para("The resistance presented by the armature circuit includes the contact resistance of the "
     "carbon brushes, which is strongly non-linear: the voltage dropped across a brush contact "
     "is closer to a fixed value than to a quantity proportional to current. An ohmmeter injects "
     "a very small test current, so the fixed brush drop dominates the measurement and the "
     "resistance is grossly over-read [2]. The accepted alternative is the direct-current "
     "volt-ampere method, in which the field winding is left unexcited so that no flux and "
     "therefore no back-EMF is produced, the rotor is prevented from turning, and the armature "
     "voltage required to circulate the rated armature current is measured. Under those "
     "conditions E\u1d04\u1d07\u1d0d\u1da0 = 0 and equation (1) reduces to:")
equation("R\u2090 = E\u2090 / I\u2090", 6)
para("The validity of this method rests on the test being carried out at, or close to, the "
     "rated armature current. This point is returned to in Section 7.4, because it proved to be "
     "the dominant source of error in the present work.")

# ------------------------------------------------------------------ 3.0 ----
page_break()
h1("3.0  Equipment and Circuit Configuration")
h2("3.1  Equipment")
table(["Model", "Description", "Qty"],
      [["8134", "EMS Workstation", "1"],
       ["8211", "DC Motor / Generator", "1"],
       ["8311", "Resistive Load", "1"],
       ["8942", "Timing Belt", "1"],
       ["8960", "Prime Mover and Dynamometer Module", "1"],
       ["8821", "Power Supply", "1"],
       ["8951", "Connection Leads", "as required"],
       ["9063", "Data Acquisition Interface (DAI)", "1"],
       ["—",    "LVDAM-EMS software (Metering, Data Table and Graph windows)", "1"]],
      "Equipment used in the Laboratory 2 exercise.", "equipment",
      widths=[0.9, 4.2, 1.1], align_right_from=2, size=10)
para("The data acquisition interface was configured with a scale of 800 V / 6 A on a 50 Hz "
     "network, as shown in the status bar of every recorded screen capture in Appendix A.")

h2("3.2  Circuit configuration")
para("The armature of the DC Motor/Generator was supplied from the variable DC output of the "
     "8821 Power Supply through current input I1 of the data acquisition interface, with voltage "
     "input E1 connected across the armature terminals. The shunt field winding was supplied "
     "from the fixed DC output through current input I2, in series with the DC motor rheostat, "
     "so that the field current could be trimmed independently of the armature voltage. The "
     "machine was mechanically coupled to the 8960 dynamometer through a timing belt, with the "
     "dynamometer configured as a brake so that the shaft torque and speed could be measured "
     "directly.")
picture(f"{FIG}/fig_circuit13.png", 4.3,
        "Separately-excited DC motor coupled to a brake (redrawn from the Laboratory 2 manual, "
        "Figure 13 [2]). Points A and B were left open for the armature resistance test and "
        "interconnected for all subsequent measurements.", "circuit13")

# ------------------------------------------------------------------ 4.0 ----
h1("4.0  Method")
para("The procedure of the Laboratory 2 manual was followed. The principal steps are summarised "
     "below; every quantitative result reported in Section 5 is supported by the corresponding "
     "screen capture reproduced in Appendix A.")
bullets([
    "Brush neutral alignment. Before any measurement, an AC source was connected to the armature "
    "and the brush adjustment lever was set so that the voltage induced in the shunt winding, "
    "displayed by meter E1, was a minimum. This places the brushes on the magnetic neutral axis "
    "and minimises sparking and induced circulating currents.",
    "Armature resistance (step 7). With the circuit open at points A and B, so that the field "
    "winding carried no current, the armature voltage was raised until the armature current "
    "reached the test value. The armature voltage and current were then recorded.",
    "Speed versus armature voltage (steps 9–13). Points A and B were interconnected, the brake "
    "torque was set to minimum and the field rheostat was adjusted to give a field current of "
    "210 mA. The armature voltage was then raised in nominal 5 % increments from zero to 100 % "
    "of the supply range, allowing the speed to settle at each step before recording. The data "
    "were stored as data table DT211 and plotted as graph G211.",
    "Torque versus armature current (steps 14–18). The data table was cleared, the field current "
    "was re-checked, and the armature voltage was set to give a no-load speed of 1500 r/min. "
    "That armature voltage was then held constant while the brake torque was increased in "
    "nominal 0.1 N·m increments, the armature voltage being re-trimmed after each increment. "
    "The data were stored as data table DT212 and plotted as graph G212.",
    "Speed droop (steps 19–21). The measured armature resistance and voltage-to-speed constant "
    "were used to predict the speed at three specified armature currents. The recorded DT212 "
    "data were then re-plotted as speed against armature current (G212-1) and speed against "
    "torque (G212-2) for comparison with the prediction.",
])

# ------------------------------------------------------------------ 5.0 ----
page_break()
h1("5.0  Results")
h2("5.1  Armature resistance")
para(f"With the field winding de-energised the meter readings reproduced in "
     f"{FR('ra_meters')} were obtained. The field current of 0.001 A confirms that the stator "
     f"was unexcited.")
picture(f"{FIG}/ra_meters.png", 2.25,
        "Metering window during the armature resistance test (step 7), recorded at 08:58 on "
        "2 September 2026.", "ra_meters")
table(["Quantity", "Meter", "Reading"],
      [["Armature voltage E\u2090", "E arm. (EA)", "14.44 V"],
       ["Armature current I\u2090", "I arm. (IA)", "0.507 A"],
       ["Field current I\uff26",     "I field (IF)", "0.001 A"],
       ["Shaft speed n",             "Speed",        "−318.8 r/min"],
       ["Shaft torque T",            "Torque",       "−0.341 N·m"]],
      "Meter readings recorded during the armature resistance measurement.", "ra_readings",
      widths=[2.3, 1.7, 1.6], align_right_from=2, size=10)
para("Applying equation (6):")
equation(f"R\u2090 = E\u2090 / I\u2090 = 14.44 / 0.507 = {RA:.2f} Ω", 7)
para(f"The armature resistance is therefore reported as {RA:.2f} Ω. Two features of this "
     f"measurement require comment and are examined in Section 7.4: the test current of "
     f"0.507 A, and the fact that the speed meter indicated −318.8 r/min rather than zero.")

h2("5.2  Motor speed versus armature voltage (DT211 and G211)")
para(f"The no-load data recorded in data table DT211 are reproduced in {TR('dt211')}. The field "
     f"current held steady at 0.20–0.21 A throughout, and the armature current remained below "
     f"0.3 A, confirming that the machine was effectively unloaded.")
table(["#", "E\u2090 (V)", "I\u2090 (A)", "I\uff26 (A)", "P_IN (W)", "T (N·m)", "n (r/min)"],
      [[i, f"{r[0]:.2f}", f"{r[2]:.2f}", f"{r[3]:.2f}", f"{r[4]:.2f}",
        f"{r[5]:.2f}", f"{r[6]:.2f}"] for i, r in enumerate(DT211)],
      "Data table DT211 — motor speed as a function of armature voltage at no load "
      "(I\uff26 = 210 mA).", "dt211",
      widths=[0.45, 1.0, 0.95, 0.95, 1.0, 0.95, 1.05], size=9.5)
picture(f"{FIG}/dt211.png", 5.1,
        "Data table DT211 as recorded in LVDAM-EMS at 09:11 on 2 September 2026.", "dt211_shot")
picture(f"{FIG}/g211.png", 4.5,
        "Graph G211 — DC motor speed as a function of armature voltage, plotted in LVDAM-EMS.",
        "g211")
para("The characteristic is a straight line passing close to the origin. Using the two end "
     "points of the data table as directed in step 13:")
equation(f"K\u2081 = Δn / ΔE\u2090 = (1581.36 − 0.08) / (271.14 − 0.43) = {K1:.3f} r/min/V", 8)
para(f"A least-squares regression through all eleven points gives a gradient of {K1_ls:.3f} "
     f"r/min/V with a coefficient of determination of R² = {R2_1:.4f}, confirming that the "
     f"relationship is linear to within the resolution of the instrumentation. The value "
     f"K\u2081 = {K1:.3f} r/min/V obtained by the two-point method is used in all subsequent "
     f"calculations, as required by the laboratory procedure.")

h2("5.3  Motor torque versus armature current (DT212 and G212)")
para("The armature voltage required to produce a no-load speed of 1500 r/min was recorded in "
     "step 14 as:")
equation("E\u2090 = 255.73 V   at   n = 1500 r/min", 9)
picture(f"{FIG}/step14.png", 6.1,
        "Metering and data table windows at step 14, showing the armature voltage of 255.73 V "
        "corresponding to a no-load speed of 1501.52 r/min (09:23 on 2 September 2026).",
        "step14")
para(f"The brake torque was then increased in increments while the armature voltage was held at "
     f"this value. Forty operating points were recorded, reproduced in {TR('dt212')}.")
table(["#", "E\u2090 (V)", "I\u2090 (A)", "I\uff26 (A)", "P_IN (W)", "T (N·m)",
       "n (r/min)", "P\u2098 (W)", "η (%)"],
      [[i, f"{r[0]:.2f}", f"{r[2]:.2f}", f"{r[3]:.2f}", f"{r[4]:.2f}", f"{r[5]:.2f}",
        f"{r[6]:.2f}", f"{r[7]:.2f}", f"{r[8]:.2f}"] for i, r in enumerate(DT212)],
      "Data table DT212 — torque, speed and power as a function of armature current at a "
      "nominally constant armature voltage of 255.73 V.", "dt212",
      widths=[0.4, 0.82, 0.78, 0.72, 0.8, 0.75, 0.85, 0.72, 0.65], size=8.5)
picture(f"{FIG}/dt212.png", 4.75,
        "Data table DT212 as recorded in LVDAM-EMS at 09:31 on 2 September 2026 "
        "(all forty operating points).", "dt212_shot")
picture(f"{FIG}/g212.png", 4.5,
        "Graph G212 — DC motor torque as a function of armature current, plotted in LVDAM-EMS.",
        "g212")
para("The characteristic is linear at low current but bends progressively away from the "
     "straight line as the current rises. Taking the two end points of the linear portion, "
     "which extends to approximately 1.5 A:")
equation(f"K\u2082 = ΔT / ΔI\u2090 = (1.75 − 0.32) / (1.50 − 0.28) = {K2:.3f} N·m/A", 10)
para(f"The sensitivity of this constant to the range chosen for the fit is summarised in "
     f"{TR('k2_fits')}.")
table(["Fit range", "Points", "K\u2082 (N·m/A)", "R²"],
      [["I\u2090 ≤ 1.00 A", "18", f"{K2_10:.3f}", f"{R2_10:.4f}"],
       ["I\u2090 ≤ 1.50 A", "25", f"{K2_ls:.3f}", f"{R2_2:.4f}"],
       ["I\u2090 ≤ 2.00 A", "32", f"{K2_20:.3f}", f"{R2_20:.4f}"],
       ["All 40 points",    "40", f"{K2_all:.3f}", f"{R2_all:.4f}"]],
      "Least-squares current-to-torque constant for different fit ranges, showing the loss of "
      "linearity as the upper limit is extended.", "k2_fits",
      widths=[1.7, 1.0, 1.6, 1.3], size=10)

h2("5.4  Speed as a function of armature current and torque (G212-1 and G212-2)")
para(f"Graph G212-2, speed against torque, was plotted in LVDAM-EMS and is reproduced in "
     f"{FR('g212_2')}. Graph G212-1, speed against armature current, was not captured during "
     f"the laboratory session; it has therefore been re-plotted in {FR('g212_1')} directly from "
     f"the forty recorded points of data table DT212, which are listed in full in "
     f"{TR('dt212')} and evidenced by the screen capture in {FR('dt212_shot')}.")
picture(f"{FIG}/g212_2.png", 4.4,
        "Graph G212-2 — DC motor speed as a function of developed torque, plotted in LVDAM-EMS "
        "at 09:48 on 2 September 2026.", "g212_2")
picture(f"{FIG}/g212_1_replot.png", 5.6,
        "Graph G212-1 — DC motor speed as a function of armature current, re-plotted from the "
        "recorded DT212 data.", "g212_1")
para("Both characteristics fall monotonically: the speed decreases steadily as either the "
     "armature current or the developed torque increases, in the manner anticipated by "
     "equation (4).")

h2("5.5  Predicted speed droop (step 19)")
para(f"Using the measured armature resistance R\u2090 = {RA:.2f} Ω, the voltage-to-speed "
     f"constant K\u2081 = {K1:.3f} r/min/V and the armature voltage E\u2090 = 255.73 V recorded "
     f"in step 14, the speed was predicted at the three specified armature currents from "
     f"E\u1d3f\u1d2c = I\u2090R\u2090, E\u1d04\u1d07\u1d0d\u1da0 = E\u2090 − E\u1d3f\u1d2c and "
     f"n = K\u2081E\u1d04\u1d07\u1d0d\u1da0.")
table(["Local AC network", "240 V\u1d00\u1d04", "240 V\u1d00\u1d04", "240 V\u1d00\u1d04"],
      [["Armature current I\u2090 (A)", "0.5", "1.0", "1.5"],
       ["E\u1d3f\u1d2c (V)", f"{0.5*RA:.2f}", f"{1.0*RA:.2f}", f"{1.5*RA:.2f}"],
       ["E\u1d04\u1d07\u1d0d\u1da0 (V)", f"{EA14-0.5*RA:.2f}", f"{EA14-1.0*RA:.2f}",
        f"{EA14-1.5*RA:.2f}"],
       ["n (r/min)", f"{K1*(EA14-0.5*RA):.1f}", f"{K1*(EA14-1.0*RA):.1f}",
        f"{K1*(EA14-1.5*RA):.1f}"]],
      "Table 1 of the laboratory manual — predicted armature circuit voltages and motor speed "
      "at three armature currents.", "table1",
      widths=[2.2, 1.35, 1.35, 1.35], size=10)

# ------------------------------------------------------------------ 6.0 ----
page_break()
h1("6.0  Answers to Review Questions")
h2("6.1  Step 12 — relationship between armature voltage and speed")
para(f"Graph G211 shows that the motor speed is directly proportional to the armature voltage. "
     f"The characteristic is a straight line through, or very close to, the origin: a "
     f"least-squares fit over the full range from 0.43 V to 271.14 V returns R² = {R2_1:.4f} "
     f"with an intercept of only {B1:.1f} r/min, which is less than 1.4 % of the maximum speed "
     f"recorded.")
para(f"The graph does confirm that, under no-load conditions and with the field current held "
     f"constant, the separately-excited DC motor behaves as a linear voltage-to-speed "
     f"converter: a higher armature voltage produces a proportionally higher speed, with a "
     f"conversion gain of K\u2081 = {K1:.3f} r/min/V. Physically this follows from equations (1) "
     f"and (2): at no load the armature current is small, so the ohmic drop I\u2090R\u2090 is "
     f"negligible, E\u1d04\u1d07\u1d0d\u1da0 is very nearly equal to E\u2090, and the speed is "
     f"therefore proportional to the applied armature voltage.")

h2("6.2  Step 17 — relationship between armature current and torque")
para(f"Provided the armature current does not exceed the nominal value, the developed torque is "
     f"directly proportional to the armature current. Over the range up to 1.5 A a "
     f"least-squares fit returns a gradient of {K2_ls:.3f} N·m/A with R² = {R2_2:.4f}, and the "
     f"two-point calculation required by step 18 gives K\u2082 = {K2:.3f} N·m/A. Within this "
     f"range the machine is therefore confirmed to act as a linear current-to-torque converter, "
     f"with a larger armature current producing a proportionally larger torque.")
para(f"Beyond approximately 1.5 A the measured torque falls increasingly short of the value the "
     f"linear model predicts, as {FR('g212')} and {FR('armature_reaction')} both show. At the "
     f"highest current recorded, 3.95 A, the measured torque of 2.96 N·m is 36 % below the "
     f"linear extrapolation. This departure is the expected consequence of armature reaction, "
     f"which is discussed in Section 7.2.")

h2("6.3  Step 19 — predicted variation of back-EMF and speed with armature current")
para(f"The calculations summarised in {TR('table1')} show that both the back-EMF and the speed "
     f"should fall linearly as the armature current increases. The armature voltage is fixed, so "
     f"every additional ampere of armature current adds I\u2090R\u2090 to the ohmic drop and "
     f"removes the same amount from the back-EMF: with R\u2090 = {RA:.2f} Ω the back-EMF is "
     f"predicted to fall by {RA:.2f} V per ampere. Because the speed is proportional to the "
     f"back-EMF through K\u2081, the predicted speed falls by K\u2081R\u2090 = {DROOP_P:.0f} "
     f"r/min per ampere. Over the range tabulated, the back-EMF is predicted to fall from "
     f"241.49 V to 213.01 V and the speed from 1410.6 r/min to 1244.2 r/min.")

h2("6.4  Step 20 — comparison with measurement and physical explanation")
para(f"Graph G212-1 ({FR('g212_1')}) confirms the direction of the prediction. The measured "
     f"speed decreases monotonically as the armature current increases, from 1501.52 r/min at "
     f"0.28 A to 1079.88 r/min at 3.95 A, so the qualitative prediction made in step 19 is "
     f"supported by the measurements.")
para(f"The magnitude of the droop, however, is considerably smaller than predicted. At an "
     f"armature current of 1.5 A the model predicts 1244.2 r/min whereas 1412.45 r/min was "
     f"measured. Comparing gradients rather than individual points, the model over-predicts the "
     f"rate of speed loss by a factor of {FACTOR:.1f}. This discrepancy is analysed in "
     f"Section 7.3, where it is attributed to the armature resistance measurement rather than "
     f"to any failure of the model itself.")
para("The physical cause of the speed reduction is the ohmic voltage drop across the armature "
     "resistance. When the brake torque is increased the motor must develop more torque, and by "
     "equation (3) it draws a proportionally larger armature current. Since the armature supply "
     "voltage is held constant, the increased drop I\u2090R\u2090 across the armature resistance "
     "leaves a smaller voltage available as back-EMF. The back-EMF is the quantity that sets the "
     "speed, so the machine settles at a lower speed. Equilibrium is reached when the speed has "
     "fallen far enough for the back-EMF to allow exactly the armature current needed to balance "
     "the applied load torque.")

# ------------------------------------------------------------------ 7.0 ----
page_break()
h1("7.0  Analysis and Discussion")
h2("7.1  Validity of the linear voltage-to-speed model")
para(f"The no-load characteristic is the cleanest result obtained in the exercise. With "
     f"R² = {R2_1:.4f} across a range spanning nearly three decades of speed, there is no "
     f"measurable curvature in the data, which supports the assumption that the field flux "
     f"remained constant throughout. That assumption is independently corroborated by the "
     f"recorded field current, which held at 0.20–0.21 A across all eleven points.")
para(f"The small negative intercept of {B1:.1f} r/min returned by the regression is physically "
     f"meaningful rather than an artefact. A real machine must overcome bearing friction, brush "
     f"friction and windage before it will turn at all, so a small armature voltage produces no "
     f"rotation. This is visible in the data: at 0.43 V the recorded speed was 0.08 r/min, "
     f"essentially stationary. The intercept is therefore an estimate of the armature voltage "
     f"consumed by no-load losses, and its presence explains why the two-point value of "
     f"K\u2081 ({K1:.3f} r/min/V) is marginally lower than the regression gradient "
     f"({K1_ls:.3f} r/min/V). The difference of just under 1 % is immaterial to the conclusions "
     f"drawn below.")

h2("7.2  Current-to-torque linearity and the onset of armature reaction")
para(f"The torque characteristic is linear only over the lower part of the range tested. "
     f"{TR('k2_fits')} shows the least-squares gradient falling steadily as the upper limit of "
     f"the fit is extended, from {K2_10:.3f} N·m/A below 1.0 A to {K2_all:.3f} N·m/A over the "
     f"full range, while the coefficient of determination degrades from {R2_10:.3f} to "
     f"{R2_all:.3f}. A gradient that depends on the range over which it is measured is the "
     f"signature of a non-linear characteristic.")
picture(f"{FIG}/armature_reaction.png", 5.7,
        "Measured torque compared with the linear current-to-torque model fitted below 1.5 A. "
        "The measured points fall progressively below the model as the armature current "
        "increases.", "armature_reaction")
para(f"{TR('ar_departure')} quantifies the departure. Up to about 1.5 A the measured torque is "
     f"within 3.5 % of the linear model, which is comparable with the resolution of the torque "
     f"meter. Beyond that the shortfall grows rapidly and reaches 36 % at the highest current "
     f"recorded.")
_lin_rows = [[f"{i:.2f}", f"{t:.2f}", f"{K2_ls*i+B2:.2f}",
              f"{100*((K2_ls*i+B2)-t)/(K2_ls*i+B2):.1f} %"]
             for i, t in zip(IA, T) if i >= 1.5]
table(["I\u2090 (A)", "T measured (N·m)", "T linear model (N·m)", "Shortfall"],
      _lin_rows[::2],
      "Departure of the measured torque from the linear current-to-torque model "
      "(alternate points shown).", "ar_departure",
      widths=[1.2, 1.7, 1.8, 1.2], size=9.5)
para("The accepted explanation is armature reaction [1], [2]. The current flowing in the "
     "armature conductors creates a magneto-motive force of its own, which is oriented across "
     "the main field axis. Vectorially adding this cross-field to the main field distorts the "
     "resultant flux distribution, strengthening the flux at one pole tip and weakening it at "
     "the other. Because the iron near the strengthened tip is already close to magnetic "
     "saturation it cannot accept as much additional flux as is removed from the weakened tip, "
     "so the net flux per pole falls. Since the developed torque is proportional to the product "
     "of flux and armature current, a reduction of flux at high current means that torque no "
     "longer keeps pace with current, exactly as observed. The distortion also shifts the "
     "magnetic neutral axis away from the position to which the brushes were aligned at the "
     "start of the session, which degrades commutation and contributes a further small loss.")
para(f"The practical significance is that the value quoted for K\u2082 is only meaningful if "
     f"the current range over which it was determined is quoted with it. On that basis "
     f"K\u2082 = {K2:.3f} N·m/A is reported for I\u2090 ≤ 1.5 A.")

h2("7.3  Predicted against measured speed droop")
para("The comparison between the step 19 prediction and the corresponding measured points is "
     "the least satisfactory result of the exercise and merits careful examination.")
_cmp = []
for target in (0.5, 1.0, 1.5):
    c = min(DT212, key=lambda r: abs(r[2]-target))
    pred = K1*(EA14 - target*RA)
    _cmp.append([f"{target:.1f}", f"{pred:.1f}", f"{c[6]:.2f}", f"{c[2]:.2f}",
                 f"{100*(pred-c[6])/c[6]:+.1f} %"])
table(["I\u2090 (A)", "n predicted (r/min)", "n measured (r/min)", "at I\u2090 (A)", "Error"],
      _cmp,
      f"Predicted speed from {TR('table1')} compared with the nearest measured operating point "
      f"in data table DT212.", "pred_vs_meas",
      widths=[0.9, 1.6, 1.6, 1.0, 0.9], size=10)
picture(f"{FIG}/droop_model.png", 5.7,
        "Measured speed droop compared with the model of equation (4), evaluated using the "
        "measured armature resistance and using a resistance fitted to the droop.", "droop_model")
para(f"The model reproduces the shape of the characteristic but substantially exaggerates its "
     f"gradient. A least-squares line fitted to the measured speed against armature current "
     f"over the linear region below 1.5 A has a gradient of {DROOP_M:.1f} r/min per ampere, "
     f"whereas equation (4) with R\u2090 = {RA:.2f} Ω predicts K\u2081R\u2090 = {DROOP_P:.0f} "
     f"r/min per ampere. The model is therefore a factor of {FACTOR:.1f} too steep.")
para("Because equation (4) contains only two measured constants, the discrepancy must lie in "
     "one of them. K\u2081 is established to better than 1 % in Section 7.1, so the armature "
     "resistance is the suspect term. Treating equation (4) as a straight line in I\u2090 allows "
     "an effective armature resistance to be recovered from the machine's own loaded behaviour, "
     "since the gradient of that line is −K\u2081R\u2090 and its intercept is K\u2081E\u2090:")
equation("R\u2090(effective) = − (dn / dI\u2090) / K\u2081", 11)
para(f"Applied to the 25 points below 1.5 A this returns R\u2090(effective) = {RA_eff:.2f} Ω, "
     f"roughly {100*RA_eff/RA:.0f} % of the {RA:.2f} Ω obtained in step 7. The same regression "
     f"provides a useful check on its own validity: its intercept of {DB:.1f} r/min corresponds "
     f"to an armature voltage of {EA_impl:.2f} V, which agrees with the {EA14:.2f} V actually "
     f"measured in step 14 to within {abs(EA_impl-EA14):.2f} V. The fit therefore recovers the "
     f"one parameter that is independently known, which gives confidence that the resistance it "
     f"returns is also meaningful. {FR('droop_model')} shows the consequence directly: the "
     f"measured points lie close to the curve computed with the smaller resistance and well "
     f"above the curve computed with the step 7 value.")
para(f"The scatter about this fit (R² = {DR2:.2f}) is considerably larger than for the no-load "
     f"characteristic. That is expected: the speed readings fluctuate by several r/min at fixed "
     f"load, the armature supply voltage drifted during the run, and the field current was not "
     f"perfectly constant. These effects are examined in Section 7.6. None of them is large "
     f"enough to account for a factor of {FACTOR:.1f}.")

h2("7.4  Validity of the armature resistance measurement")
para("Two defects in the step 7 measurement account for the discrepancy identified above.")
para("The first, and by far the more important, is the current at which the test was performed. "
     "The manual is explicit that the volt-ampere method must be carried out at the rated "
     "armature current, precisely because the brush contact drop is not proportional to current. "
     "A carbon brush contact behaves approximately as a fixed voltage drop of the order of one "
     "to two volts per brush rather than as a fixed resistance, so the apparent resistance "
     "E\u2090/I\u2090 is inflated at low current and falls towards the true winding resistance "
     "as the current rises. The test was carried out at 0.507 A, whereas the torque "
     "characteristic of Section 7.2 indicates that the nominal armature current of this machine "
     "is closer to 1.5 A. The measurement was therefore made at roughly one third of the current "
     "at which it should have been made, in exactly the regime the manual warns against, and it "
     "over-reads for exactly the reason the manual gives. This is consistent in both sign and "
     "approximate magnitude with the effective resistance derived in Section 7.3.")
para("The second defect is that the rotor was not stationary. The speed meter indicated "
     "−318.8 r/min and the torque meter −0.341 N·m, corresponding to 11.38 W of mechanical "
     "power, so the shaft was turning slowly in reverse rather than being held locked as the "
     "method requires. With the field current at 0.001 A the flux was residual only, so the "
     "back-EMF generated was small and this is a second-order effect beside the brush drop; "
     "nevertheless it means the condition E\u1d04\u1d07\u1d0d\u1da0 = 0 assumed in equation (6) "
     "was not exactly satisfied.")
para("It should also be noted that the column headed RA = EA/IA in data table DT212 does not "
     "represent the armature resistance. That column simply divides the terminal voltage by the "
     "armature current while the machine is running and generating a back-EMF, which is why it "
     "returns values from 738 Ω down to 61 Ω. It is meaningful only under the locked-rotor, "
     "zero-flux conditions of step 7, and it has not been used anywhere in this report.")
para("Were the exercise to be repeated, the armature resistance test should be performed at the "
     "machine's rated armature current with the rotor positively locked, and ideally repeated at "
     "several currents so that the fixed brush drop could be separated from the true ohmic "
     "resistance by extrapolation.")

h2("7.5  Energy conversion efficiency")
para(f"The data acquisition software computed the ratio of mechanical output power to electrical "
     f"input power for every operating point, plotted in {FR('efficiency')}.")
picture(f"{FIG}/efficiency.png", 5.4,
        "Ratio of mechanical output power to electrical input power as a function of armature "
        "current, computed by LVDAM-EMS from the DT212 data.", "efficiency")
para(f"Efficiency rises steeply from 70.2 % at the lightest load, peaks at {EFF_MAX:.1f} % at an "
     f"armature current of {EFF_MAX_IA:.2f} A, and then declines steadily to {EFF[-1]:.1f} % at "
     f"3.95 A. The shape is characteristic of any electrical machine. At light load the fixed "
     f"losses — friction, windage and the power dissipated in the field winding — represent a "
     f"large fraction of a small input, so efficiency is poor. As load increases these fixed "
     f"losses are spread over a larger output and efficiency improves. Beyond the peak the "
     f"armature copper loss, which rises with the square of the armature current, comes to "
     f"dominate and efficiency falls away. The peak occurs where the current-dependent losses "
     f"have grown to equal the fixed losses, which for this machine is at well under half the "
     f"maximum current tested.")
para("The efficiency peak provides independent support for the conclusion of Section 7.4 that "
     "the machine was operated well beyond its rating at the top of the range. Operating at "
     "3.95 A converted barely a third of the input power into mechanical work, the remainder "
     "being dissipated as heat, which is neither a sustainable nor a representative operating "
     "condition.")

h2("7.6  Sources of error and experimental limitations")
bullets([
    "Armature resistance test current. Discussed in Section 7.4; this is the dominant error and "
    "propagates directly into every prediction made from equation (4).",
    f"Drift of the armature supply voltage. Step 15 requires the armature voltage to be "
    f"re-trimmed to its original value after each torque increment. In practice the recorded "
    f"voltage fell steadily from {DT212[0][0]:.2f} V to {DT212[-1][0]:.2f} V across the run, a "
    f"reduction of {EA_DRIFT:.1f} %. Part of the observed speed reduction is therefore "
    f"attributable to falling supply voltage rather than to load. The regression used in "
    f"Section 7.3 absorbs this into its intercept, which is why the armature voltage it implies "
    f"({EA_impl:.2f} V) sits fractionally below the value set at the start of the run.",
    "Thermal drift. The manual advises completing the torque measurements within five minutes "
    "because the armature current exceeds its rated value. Copper resistivity rises by "
    "approximately 0.4 % per kelvin, so progressive heating of the windings during the run "
    "increases the true armature resistance as the sweep proceeds, meaning the machine did not "
    "have a single fixed R\u2090 throughout.",
    "Field current variation. The recorded field current fell from 0.20 A to 0.19 A at the "
    "highest loads. Since both K\u2081 and K\u2082 depend on flux, this weakens the field "
    "slightly and contributes a small additional speed rise that partially masks the true droop.",
    "Instrument resolution. Armature current and torque were recorded to two decimal places. At "
    "the lowest torque of 0.32 N·m the quantisation alone represents about 3 % of the reading, "
    "which is why the lightest-load points scatter most about the fitted lines.",
    "Brush neutral alignment. The brushes were aligned at the start of the session under "
    "unloaded conditions. Armature reaction shifts the magnetic neutral axis as load increases, "
    "so the alignment is not optimal at high current and commutation degrades.",
    "Single measurement set. Each operating point was recorded once, so random error could not "
    "be estimated statistically. Repeating the sweep two or three times and averaging would "
    "allow uncertainty bounds to be placed on K\u2081 and K\u2082.",
])

# ------------------------------------------------------------------ 8.0 ----
page_break()
h1("8.0  Conclusion")
para(f"The operating characteristics of a separately-excited DC motor were measured and compared "
     f"against the simplified equivalent circuit model. The principal quantitative outcomes are "
     f"summarised in {TR('summary')}.")
table(["Quantity", "Symbol", "Result", "Basis"],
      [["Armature resistance", "R\u2090", f"{RA:.2f} Ω", "Volt-ampere method at 0.507 A"],
       ["Effective armature resistance", "R\u2090(eff)", f"{RA_eff:.2f} Ω",
        "Fitted to the measured speed droop"],
       ["Voltage-to-speed constant", "K\u2081", f"{K1:.3f} r/min/V",
        f"DT211 end points, R² = {R2_1:.4f}"],
       ["Current-to-torque constant", "K\u2082", f"{K2:.3f} N·m/A",
        "DT212 linear portion, I\u2090 ≤ 1.5 A"],
       ["Speed regulation at 1.5 A", "%SR", "6.31 %", "DT212"],
       ["Speed regulation at 3.95 A", "%SR", "39.05 %", "DT212"],
       ["Peak conversion efficiency", "η", f"{EFF_MAX:.1f} %",
        f"at I\u2090 = {EFF_MAX_IA:.2f} A"]],
      "Summary of measured and derived machine parameters.", "summary",
      widths=[2.1, 0.85, 1.25, 2.05], align_right_from=2, size=9.5)
para(f"The experiment confirmed the two linear relationships on which the model rests. Under "
     f"no-load conditions the speed was proportional to the armature voltage with "
     f"R² = {R2_1:.4f}, establishing the machine as a linear voltage-to-speed converter. At "
     f"constant armature voltage the developed torque was proportional to the armature current "
     f"with R² = {R2_2:.4f} for currents up to approximately 1.5 A, establishing it equally as a "
     f"linear current-to-torque converter within that range.")
para("Beyond 1.5 A the torque characteristic departed measurably from linearity, the shortfall "
     "against the linear model growing to 36 % at 3.95 A. This behaviour was identified as "
     "armature reaction, in which the cross-magnetising effect of armature current together with "
     "saturation of the pole tips reduces the net flux per pole. The measurements therefore "
     "define not only the constants of the machine but also the boundary of the range within "
     "which those constants may legitimately be applied.")
para(f"The prediction of speed droop was qualitatively correct but quantitatively poor, "
     f"over-estimating the rate of speed loss by a factor of {FACTOR:.1f}. The cause was traced "
     f"to the armature resistance measurement, which was performed at 0.507 A rather than at the "
     f"rated armature current — a value the torque characteristic suggests lies close to 1.5 A. "
     f"In that low-current regime the non-linear brush contact drop dominates the terminal "
     f"measurement and inflates the apparent resistance, which is the precise effect the "
     f"volt-ampere method is intended to avoid and that the manual warns against. Fitting the "
     f"resistance to the machine's own loaded behaviour instead returned {RA_eff:.2f} Ω, and the "
     f"model reproduces the measured characteristic closely when that value is used. The "
     f"exercise therefore validated the equivalent circuit model itself while demonstrating that "
     f"the model is only as good as the parameter measurements supplied to it.")
para("The most valuable outcome of the laboratory was this last point. A measurement that "
     "appears entirely reasonable in isolation — a single voltage and a single current, "
     "correctly read and correctly divided — can still be substantially wrong if the conditions "
     "under which it is taken violate an assumption of the method. Cross-checking a parameter "
     "against independent data, as was done here, is what exposed the error.")

# ------------------------------------------------------------------ 9.0 ----
h1("9.0  References")
for r in [
    "[1]\tS. J. Chapman, Electric Machinery Fundamentals, 5th ed. New York, NY, USA: "
    "McGraw-Hill, 2012.",
    "[2]\tSchool of Engineering, \u201cLaboratory session: DC machines — DC motors,\u201d "
    "ENS5230 Laboratory 2 manual, Edith Cowan University, Joondalup, WA, Australia, 2026.",
    "[3]\tLab-Volt Ltd., DC Motors and Generators, Electromechanical Training System. "
    "Quebec, Canada: Lab-Volt Ltd.",
    "[4]\tA. E. Fitzgerald, C. Kingsley, and S. D. Umans, Electric Machinery, 6th ed. "
    "New York, NY, USA: McGraw-Hill, 2003.",
    "[5]\tP. C. Sen, Principles of Electric Machines and Power Electronics, 3rd ed. "
    "Hoboken, NJ, USA: Wiley, 2013.",
]:
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.4)
    p.paragraph_format.first_line_indent = Inches(-0.4)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(r); run.font.name = FONT; run.font.size = BODY_SIZE

# ----------------------------------------------------------------- 10.0 ----
h1("10.0  Acknowledgement of Generative Artificial Intelligence")
para("[REVIEW AND EDIT THIS SECTION SO THAT IT ACCURATELY AND COMPLETELY DESCRIBES YOUR OWN USE "
     "OF AI TOOLS, THEN DELETE THIS INSTRUCTION.]", bold=True)
para("I acknowledge the use of [INSERT TOOL NAME AND VERSION NUMBER] in the preparation of this "
     "report. The tool was used for the following purposes:")
bullets([
    "Transcribing the numerical readings from the LVDAM-EMS data table screen captures into a "
    "machine-readable form for calculation.",
    "Performing and checking the arithmetic and least-squares regressions reported in "
    "Sections 5 and 7.",
    f"Producing {FR('g212_1')}, {FR('armature_reaction')}, {FR('droop_model')} and "
    f"{FR('efficiency')} from the transcribed data.",
    "Providing feedback on the structure, clarity and grammar of the written discussion.",
])
para("All laboratory measurements reported are my own, recorded during the Laboratory 2B session "
     "on 2 September 2026. I have verified every figure reproduced in this report against the "
     "original screen captures in Appendix A, and I take full responsibility for the "
     "interpretation, analysis and conclusions presented.")

# -------------------------------------------------------------- APPENDIX ---
page_break()
h1("Appendix A  —  Timestamped Laboratory Recordings")
para("The screen captures reproduced below are unmodified full-screen images taken on the "
     "laboratory computer during the Laboratory 2B session. The Windows taskbar clock and date "
     "are visible in the lower right corner of each image, as required by the assignment "
     "instructions. They are presented in the order in which they were recorded.")

_app = [
    (f"{LS}/Screenshot 2026-09-02 085810.png",
     "08:58 — Metering window during the armature resistance test (step 7). The field current of "
     "0.001 A confirms the stator was unexcited; E arm. 14.44 V and I arm. 0.507 A."),
    (f"{LS}/Screenshot 2026-09-02 091123.png",
     "09:11 — Data table DT211 complete, showing all eleven no-load operating points from "
     "0.43 V to 271.14 V."),
    (f"{LS}/Screenshot 2026-09-02 091254.png",
     "09:12 — Graph G211, motor speed as a function of armature voltage."),
    (f"{LS}/Screenshot 2026-09-02 092337.png",
     "09:23 — Step 14: armature voltage set to give a no-load speed of 1500 r/min. "
     "E arm. 255.73 V, speed 1501.52 r/min, recorded as the first row of DT212."),
    (f"{LS}/Screenshot 2026-09-02 093106.png",
     "09:31 — Data table DT212 complete, showing all forty loaded operating points from 0.28 A "
     "to 3.95 A. This is the dataset used throughout Sections 5 and 7."),
    (f"{LS}/Screenshot 2026-09-02 093153.png",
     "09:31 — Graph G212, motor torque as a function of armature current, showing the departure "
     "from linearity above approximately 1.5 A."),
    (f"{L2}/Screenshot 2026-09-02 094846.png",
     "09:48 — Graph G212-2, motor speed as a function of developed torque."),
    (f"{L2}/Screenshot 2026-09-02 094858.png",
     "09:48 — Data table displayed alongside graph G212-2."),
]
for i, (path, cap) in enumerate(_app):
    picture(path, 4.2 if "094846" in path else 6.2, cap, f"appA{i+1}")
    if i % 2 == 1 and i != len(_app)-1:
        page_break()

# ------------------------------------------------------- update fields -----
uf = OxmlElement('w:updateFields'); uf.set(qn('w:val'), 'true')
doc.settings.element.append(uf)

doc.save(OUT)
print(f"saved {OUT}  ({os.path.getsize(OUT)/1e6:.2f} MB)")
print(f"figures: {_seq['Figure']}/{len(FIG_ORDER)}   tables: {_seq['Table']}/{len(TAB_ORDER)}")
assert _seq['Figure'] == len(FIG_ORDER) and _seq['Table'] == len(TAB_ORDER)
print(f"K1={K1:.3f}  K2={K2:.3f}  RA={RA:.2f}  RA_eff={RA_eff:.2f}  factor={FACTOR:.2f}")
