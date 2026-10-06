"""Build record-race-deck.pptx: 20 slides, 16:9, notes, embedded graphs."""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
import pathlib

BASE = pathlib.Path("/home/touhid/Documents/leadpaper/opendesign/mockups/record-race-deck")
FIG = BASE / "pptx_figs"
PAPER, INK = RGBColor(0xFA, 0xF7, 0xF1), RGBColor(0x1C, 0x1A, 0x16)
ACC, ACC2, MUT = RGBColor(0xB3, 0x54, 0x1E), RGBColor(0x2E, 0x6E, 0x5E), RGBColor(0x6F, 0x6A, 0x5E)

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.33), Inches(7.5)
BLANK = prs.slide_layouts[6]


def bg(s):
    s.background.fill.solid()
    s.background.fill.fore_color.rgb = PAPER


def tb(s, x, y, w, h):
    return s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h)).text_frame


def title(s, kicker, head, num):
    t = tb(s, 0.8, 0.4, 11.7, 2.2)
    t.word_wrap = True
    p = t.paragraphs[0]
    p.text = kicker.upper()
    p.font.size, p.font.color.rgb, p.font.name = Pt(14), MUT, "Verdana"
    h = tb(s, 0.8, 0.9, 11.7, 1.6)
    h.word_wrap = True
    p = h.paragraphs[0]
    p.text = head
    p.font.size, p.font.color.rgb, p.font.name = Pt(40), INK, "Georgia"
    f = tb(s, 0.8, 6.9, 11.7, 0.4)
    p = f.paragraphs[0]
    p.text = f"Guardrails for the Record Race    {num} / 20"
    p.font.size, p.font.color.rgb, p.font.name = Pt(12), MUT, "Verdana"


def bullets(s, items, x=0.8, y=2.6, w=11.7, size=24):
    t = tb(s, x, y, w, 4.0)
    t.word_wrap = True
    for i, b in enumerate(items):
        p = t.paragraphs[0] if i == 0 else t.add_paragraph()
        p.text = "▪  " + b
        p.font.size, p.font.name = Pt(size), "Georgia"
        p.space_after = Pt(14)


def table(s, rows, x=0.8, y=2.6, w=11.7, fs=18):
    gt = s.shapes.add_table(len(rows), len(rows[0]), Inches(x), Inches(y),
                            Inches(w), Inches(0.6)).table
    for i, r in enumerate(rows):
        for j, v in enumerate(r):
            c = gt.cell(i, j)
            c.text = v
            for p in c.text_frame.paragraphs:
                p.font.size, p.font.name = Pt(fs + 2 if i == 0 else fs), "Georgia"
            if i == 0:
                c.fill.solid()
                c.fill.fore_color.rgb = INK
                for p in c.text_frame.paragraphs:
                    for r_ in p.runs:
                        r_.font.color.rgb = PAPER
    return gt


def img(s, name, x, y, w, h=None):
    kw = dict(width=Inches(w)) if h is None else dict(width=Inches(w), height=Inches(h))
    s.shapes.add_picture(str(FIG / name) if (FIG / name).exists()
                         else str(BASE / name), Inches(x), Inches(y), **kw)


def note(s, text):
    s.notes_slide.notes_text_frame.text = text


S = []
# 1
s = prs.slides.add_slide(BLANK); bg(s)
title(s, "CsPbI3 perovskites · simulation audit · group seminar",
      "Guardrails for the record race: what a CsPbI3 cell can honestly claim", 1)
t = tb(s, 0.8, 2.9, 11.7, 1.2); t.word_wrap = True
p = t.paragraphs[0]; p.text = "Hussain Touhid Siddiquee & Md. Abdul Malek Fahim · Dept. of EEE, Leading University"
p.font.size, p.font.name = Pt(20), "Georgia"
t = tb(s, 0.8, 4.4, 11.7, 1.4); t.word_wrap = True
p = t.paragraphs[0]; p.text = "24.9% box best  →  20.8% defensible"
p.font.size, p.font.color.rgb, p.font.name = Pt(54), ACC, "Georgia"
note(s, "Open with the punchline: two numbers, not one. 24.9 is the best point inside stated guardrails; 20.8 is the number for an experimentalist. Ask the room which they would publish.")
S.append(s)
# 2
s = prs.slides.add_slide(BLANK); bg(s)
title(s, "The problem", "Simulation records keep climbing past experiment", 2)
bullets(s, ["Certified CsPbI3 record: 22.02% — simulation claims reach 24.2% and beyond",
            "Highest numbers come with interfaces removed or unreachable defect densities",
            "Raw inputs routinely withheld — nobody can re-run anyone else"])
note(s, "The inflation dynamic: 22.02 certified vs 24.17/24.24 simulated. The question is what each number assumes.")
S.append(s)
# 3
s = prs.slides.add_slide(BLANK); bg(s)
title(s, "Where the numbers come from", "Our parameters come from the Hossain programme", 3)
table(s, [["Device", "Voc", "Jsc", "FF"],
          ["Hossain 2022 printed (17.90%)", "0.997 V", "21.07", "85.2%"],
          ["Our baseline (18.99%)", "1.122 V", "19.68", "86.0%"]])
bullets(s, ["2022: 96 transport-layer combos screened, TiO2/CBTS wins",
            "2023: full optimisation, complete table printed — we reproduce, then switch interfaces on"], y=5.2, size=20)
note(s, "Provenance: every def number traces to a printed table. We add only interface blocks and the absorption model, both stated.")
S.append(s)
# 4
s = prs.slides.add_slide(BLANK); bg(s)
title(s, "The device", "The stack, with interfaces switched on", 4)
table(s, [["Layer", "Thickness", "Key setting"],
          ["ITO front contact", "—", "4.0 eV work function"],
          ["TiO2 ETL", "30 nm", "ND 9e17, χ 3.7 eV at optimum"],
          ["CsPbI3 absorber", "2.2 µm", "NA 3e16, Nt 1e12, Eg 1.65 eV"],
          ["CBTS HTL", "100 nm", "NA 1e18, χ 3.9 eV at optimum"],
          ["Ni back contact", "—", "5.5 eV work function"],
          ["Interfaces, both sides", "—", "N = 1e10 cm⁻² (S = 100 cm/s)"]], fs=16)
note(s, "Walk the stack top to bottom. The last row is what matters: deleting it is how inflated numbers are made.")
S.append(s)
# 5
s = prs.slides.add_slide(BLANK); bg(s)
title(s, "Method · SCAPS-1D v3.3.10", "Configured for honest sweeps", 5)
bullets(s, ["AM1.5G, 100 mW/cm², 300 K · Eg-sqrt absorption, gap sweeps move the edge",
            "SRH through stated bulk + interface defects · Krad = 0, Auger off",
            "Flat 10% front reflection, opaque Ni back — conservative except the blue",
            "Resistances scripted (set external.Rs/Rsh), never hand-derated"])
note(s, "Absorption model keeps gap sweeps self-consistent; scripted parasitics block the analytic-derate route.")
S.append(s)
# 6
s = prs.slides.add_slide(BLANK); bg(s)
title(s, "Method · scripting", "Three conventions that keep the numbers honest", 6)
bullets(s, ["Units: def files store SI, script set expects practical units — SI inputs overdose 10⁶×",
            "Cross-sections: the σ set-key restructures the block — definition files only",
            "Uncertainty: 0.017-point IV-step; every difference read against it"])
note(s, "Ghost cells at 27% from a units slip; neutralised interfaces from a set-key slip. Set-then-get verification always.")
S.append(s)
# 7
s = prs.slides.add_slide(BLANK); bg(s)
title(s, "Method · campaign", "One campaign, every run receipted", 7)
table(s, [["Batch", "Runs", "Finding"],
          ["Grid + refinement", "96 + 36", "23.50% surveyed best"],
          ["Joint affinities", "36", "24.95% at (3.9, 3.7)"],
          ["Optimiser (exploratory)", "104", "23.08% guardrailed — brackets nothing"],
          ["Morris + audits + parasitics", "56 + …", "regime flip, Rs/Rsh scripted"]])
note(s, "Grid, then the joint-affinity surprise, then an optimiser whose box excluded χ 3.7 — a limitation, not a trophy.")
S.append(s)
# 8 race chart (native shapes)
s = prs.slides.add_slide(BLANK); bg(s)
title(s, "The record race", "Two races on the same chart", 8)
lx, bx, w, sc = 1.0, 6.3, 11.3, (11.3 / 100)
lo, hi = 10.0, 26.0
def Y(v):
    return 5.3 - (v - lo) / (hi - lo) * 3.4
ax = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(lx), Inches(1.9), Inches(w), Inches(3.4))
ax.fill.background(); ax.line.color.rgb = INK; ax.line.width = Pt(3)
pts = [("10.8\nQD 2016", 10.8, ACC2, 6), ("17.9\nHossain 22", 17.9, ACC2, 26),
       ("19.06\nHossain 23", 19.06, ACC2, 36), ("21.43\ninverted cert.", 21.43, ACC2, 66),
       ("22.02\ncert.", 22.02, ACC2, 82), ("23.10\nZnO/Spiro sim", 23.10, ACC, 44),
       ("24.17\nNazli sim", 24.17, ACC, 58), ("24.24\nOyedele sim", 24.24, ACC, 63),
       ("24.95\nbound (us)", 24.95, INK, 88), ("20.82\ndefensible (us)", 20.82, ACC2, 90)]
import math
KEY = []
for idx, (lab, v, col, x) in enumerate(pts, start=1):
    dw = 0.42 if idx == 10 else 0.28
    d = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(lx + x * sc - dw / 2), Inches(Y(v) - 0.14),
                           Inches(dw), Inches(0.28))
    d.fill.solid(); d.fill.fore_color.rgb = col; d.line.fill.background()
    d.text_frame.word_wrap = False
    q = d.text_frame.paragraphs[0]; q.alignment = PP_ALIGN.CENTER
    q.text = str(idx)
    q.font.size, q.font.name, q.font.color.rgb = (Pt(8) if idx == 10 else Pt(11)), "Verdana", RGBColor(0xFF, 0xFF, 0xFF)
    name = lab.split("\n")[1]
    KEY.append((f"{idx}. {v:g}% {name}", col))
for yv in (12, 16, 20, 24):
    tag = tb(s, lx - 0.75, Y(yv) - 0.18, 0.7, 0.36)
    q = tag.paragraphs[0]; q.alignment = PP_ALIGN.RIGHT
    q.text = f"{yv}%"
    q.font.size, q.font.name = Pt(13), "Verdana"
tag = tb(s, lx, 5.32, 11.3, 0.25)
q = tag.paragraphs[0]; q.alignment = PP_ALIGN.CENTER
q.text = "2016  →  2026 · dot number color = track (green measured, orange simulated, dark this work)"
q.font.size, q.font.name = Pt(12), "Verdana"
left = KEY[:5]; right = KEY[5:]
t1 = tb(s, 0.8, 5.62, 5.6, 1.2); t1.word_wrap = True
t2 = tb(s, 6.9, 5.62, 5.6, 1.2); t2.word_wrap = True
for box, items in ((t1, left), (t2, right)):
    for i, (k, col) in enumerate(items):
        q = box.paragraphs[0] if i == 0 else box.add_paragraph()
        q.space_after = Pt(2)
        r = q.add_run(); r.text = k.split(" ", 1)[0] + " "
        r.font.size, r.font.name, r.font.color.rgb = Pt(14), "Verdana", col
        r = q.add_run(); r.text = k.split(" ", 1)[1]
        r.font.size, r.font.name = Pt(14), "Verdana"
note(s, "Green climbs slowly — fabrication improving. Orange jumps — assumptions loosening. Our two points straddle the certified record; the gap between them is the argument.")
S.append(s)
# 9 champion
s = prs.slides.add_slide(BLANK); bg(s)
title(s, "Result · the upper bound", "The best guardrailed point: 24.95%", 9)
img(s, "fig_JVboth.png", 0.8, 2.6, 7.2)
bullets(s, ["Voc 1.321 V · Jsc 21.20 · FF 89.11%",
            "2.2 µm · Nt 1e12 · NA ceiling · Eg 1.65 · χ (3.9, 3.7)",
            "Corner of the box — a bound, not a forecast"], x=8.4, y=2.6, w=4.1, size=20)
note(s, "Read the JV, then the small print: every coordinate is an edge. Best the box allows — which is why it cannot headline alone.")
S.append(s)
# 10 affinity
s = prs.slides.add_slide(BLANK); bg(s)
title(s, "Result · why affinities move it", "Affinity works through activation energy", 10)
img(s, "affinity_heatmap.png", 0.8, 2.6, 6.0)
img(s, "gap_steps.png", 7.1, 2.6, 5.4)
note(s, "Joint map surprise: both optimum affinities outside surveyed values; efficiency rises through zero hole-side offset. Non-monotonic gap steps map the Ea landscape, not absorption.")
S.append(s)
# 11 dose
s = prs.slides.add_slide(BLANK); bg(s)
title(s, "Result · interfaces", "Interfaces cost four points across the dose", 11)
img(s, "fig_audit.png", 0.8, 2.6, 7.2)
bullets(s, ["25.11% at 1e8 → 23.84% at the 1e10 guardrail → 21.20% at 1e12",
            "Published 24.17 / 24.24 NOT placed here — different stacks, incomplete tables"], x=8.4, y=2.6, w=4.1, size=20)
note(s, "Four points across four decades on our own cell. Placement of others' numbers would be accusation dressed as analysis.")
S.append(s)
# 12 DB
s = prs.slides.add_slide(BLANK); bg(s)
title(s, "Result · the screen", "A radiative ceiling rules out the no-interface band", 12)
bullets(s, ["Detailed-balance Voc from our own absorption: 1.371 V at 1.65 eV",
            "Champion clears it by 0.05 V — every no-interface cell within 0.011 V of it or above",
            "With Krad = 0 nothing pins the splitting: the band has no margin anywhere"])
note(s, "Computed from our absorption, not a textbook number. The old Eg/q rule sat above the limit — retired, stated in the paper.")
S.append(s)
# 13 routine
s = prs.slides.add_slide(BLANK); bg(s)
title(s, "Result · the defensible number", "Routine defects give 20.82%", 13)
img(s, "rs_derate.png", 0.8, 2.6, 5.6)
img(s, "thickness_nt.png", 6.9, 2.6, 5.6)
note(s, "The answer for an experimentalist. Thickness optimum moves with Nt — invisible to single-variable sweeps. Attainable gaps: 24.44/24.73/24.28%.")
S.append(s)
# 14 morris
s = prs.slides.add_slide(BLANK); bg(s)
title(s, "Result · sensitivity", "Interfaces lead at the floor, bulk leads at routine", 14)
img(s, "fig_morris.png", 0.8, 2.6, 6.0)
img(s, "optimizer.png", 7.1, 2.6, 5.4)
note(s, "Paired test: +2.03 [0.70, 3.51], 6 of 8 trajectories. Routine-defect dose goes flat. Both halves are the finding.")
S.append(s)
# 15 loss
s = prs.slides.add_slide(BLANK); bg(s)
title(s, "Result · against experiment", "The excess is fill factor, not voltage", 15)
img(s, "loss_budget.png", 0.8, 2.6, 7.2)
bullets(s, ["Our Voc is ordinary — records reach 1.27–1.29 V",
            "~6-pt FF gap unattributed: no TL recombination, no reflector, numerics"], x=8.4, y=2.6, w=4.1, size=20)
note(s, "Six points of FF excess with three named causes, none isolated. Read left to right with the room.")
S.append(s)
# 16 taus
s = prs.slides.add_slide(BLANK); bg(s)
title(s, "Method · portable metrics", "Report lifetimes and velocities, not just densities", 16)
table(s, [["Density", "τ / S"],
          ["Nt 1e12 (floor)", "τ = 100 µs"],
          ["Nt 1e15 (routine)", "τ = 0.1 µs"],
          ["Nif 1e10 (guardrail)", "S = 100 cm/s"]])
bullets(s, ["N and σ enter only as their product — τ and S are cross-study currency"], y=5.4, size=20)
note(s, "N-sigma degeneracy proved digit-for-digit. The 100 µs floor is 1–2 orders beyond the best films — admitted, not hidden.")
S.append(s)
# 17 traps
s = prs.slides.add_slide(BLANK); bg(s)
title(s, "Honesty · scripting", "Two scripting traps that fabricate cells", 17)
bullets(s, ["Units trap: SI-valued set inputs overdose 10⁶× — ghost cells up to 27%",
            "σ trap: the capture cross-section set-key neutralises interfaces",
            "Rule: definition files for structure, set-then-get verification always"])
note(s, "Mistakes published as findings. Both traps gave plausible efficiencies — that is what makes them dangerous.")
S.append(s)
# 18 checklist
s = prs.slides.add_slide(BLANK); bg(s)
title(s, "Contribution · standard", "A checklist for comparable SCAPS claims", 18)
bullets(s, ["Interface status + Nif + σ (or S) · bulk Nt + σ (or τ)",
            "Unit-system declaration · Rs basis, computed not assumed",
            "Both contact work functions · surveyed vs adopted affinities",
            "Model-derived radiative screen · archived receipts"])
note(s, "Eight disclosure items, each a place where silence moves the headline by points. Propose it as a reviewer checklist.")
S.append(s)
# 19 limits
s = prs.slides.add_slide(BLANK); bg(s)
title(s, "Limits", "What this work cannot say", 19)
bullets(s, ["No optimiser brackets the champion — best-of-evaluated, not proven optimal",
            "No phase stability, ion migration, or damp-heat — SCAPS steady state only",
            "No experimental calibration — the loss budget compares, it does not fit"])
note(s, "A paper that prices others' assumptions prices its own. Questions belong here.")
S.append(s)
# 20 takeaway
s = prs.slides.add_slide(BLANK); bg(s)
title(s, "Takeaway", "Claim 20.8. Cite 24.9 as a bound.", 20)
bullets(s, ["Every number archived · every assumption priced · scripts regenerate every receipt",
            "github.com/touhidsiddiqueeraj-bit/cspbi3-cbts-guardrailed"])
note(s, "One sentence to leave the room with. Then the live demo: open the champion def in SCAPS and read 24.95% off the screen.")
S.append(s)

out = BASE / "record-race-deck.pptx"
prs.save(str(out))
print("slides:", len(prs.slides.__iter__.__self__._sldIdLst), "| saved:", out)
