"""Build record-race-deck.pptx: 20 slides, plain language, 16:9, notes, embedded graphs."""
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


# 1
s = prs.slides.add_slide(BLANK); bg(s)
title(s, "Solar cells · computer models · group seminar",
      "Guardrails for the record race: what a CsPbI3 cell can honestly claim", 1)
t = tb(s, 0.8, 2.9, 11.7, 1.2); t.word_wrap = True
p = t.paragraphs[0]; p.text = "Hussain Touhid Siddiquee & Md. Abdul Malek Fahim · Dept. of EEE, Leading University"
p.font.size, p.font.name = Pt(20), "Georgia"
t = tb(s, 0.8, 4.2, 11.7, 2.0); t.word_wrap = True
p = t.paragraphs[0]; p.text = "We checked how much of a record solar-cell number is real, and how much comes from optimistic settings."
p.font.size, p.font.name = Pt(30), "Georgia"
t = tb(s, 0.8, 5.6, 11.7, 1.0); t.word_wrap = True
p = t.paragraphs[0]; p.text = "24.9% best case  →  20.8% honest case"
p.font.size, p.font.color.rgb, p.font.name = Pt(44), ACC, "Georgia"
note(s, "Open with the punchline in plain words: two numbers, not one. 24.9 is the best our simulation could build inside fixed rules; 20.8 is the number for real-world dirt. Ask the room which one they would publish.")
# 2
s = prs.slides.add_slide(BLANK); bg(s)
title(s, "The problem", "Computer models now beat the best real solar cells — on paper", 2)
bullets(s, ["The best certified cesium-lead-iodide cell turns 22.02 percent of sunlight into electricity.",
            "Computer simulations of similar cells claim over 24 percent.",
            "The gap is not fraud. It is hidden assumptions: missing dirt, perfect contacts, ideal materials."])
note(s, "Set up the puzzle simply: the computer beats the lab, but only because the computer is allowed to assume a perfect world.")
# 3
s = prs.slides.add_slide(BLANK); bg(s)
title(s, "Where our settings come from", "Every setting we used comes from a published table", 3)
table(s, [["Cell", "Voltage", "Current", "Fill factor"],
          ["Hossain 2022, printed (17.90%)", "0.997 V", "21.07", "85.2%"],
          ["Our rebuild (18.99%)", "1.122 V", "19.68", "86.0%"]])
bullets(s, ["In 2022, the Hossain team tested 96 layer combinations and picked the winning stack.",
            "In 2023 they tuned it fully and printed every setting, so anyone can rebuild it.",
            "We rebuilt their cell in software and landed nearby — then added the dirt layers they left out."], y=5.2, size=20)
note(s, "Provenance in one sentence: nothing in our files is invented; everything traces to a printed table, and our additions are stated.")
# 4
s = prs.slides.add_slide(BLANK); bg(s)
title(s, "The device", "The cell has five layers, and we model the dirt between them", 4)
table(s, [["Layer", "Thickness", "Setting"],
          ["Transparent front contact (ITO)", "—", "energy level 4.0 eV"],
          ["Electron-carrying layer (titanium dioxide)", "30 nm", "doping 9e17, energy 3.7 eV at best"],
          ["Light absorber (cesium lead iodide)", "2.2 µm", "doping 3e16, defects 1e12, gap 1.65 eV"],
          ["Hole-carrying layer (CBTS)", "100 nm", "doping 1e18, energy 3.9 eV at best"],
          ["Nickel back contact", "—", "energy level 5.5 eV"],
          ["Dirt traps at both joints", "—", "a fixed, stated amount at each boundary"]], fs=16)
t = tb(s, 0.8, 6.0, 11.7, 0.75); t.word_wrap = True
p = t.paragraphs[0]
p.text = ("Names in brackets are the materials: ITO = transparent conductor, CBTS = copper barium tin sulfide. "
          "nm = billionth of a meter, µm = thousandth of a millimeter, eV = energy unit. "
          "Doping and defect numbers are atoms per cubic centimeter, written as powers of ten (9e17 means 9 followed by 17 zeros).")
p.font.size, p.font.name = Pt(15), "Georgia"
note(s, "Where two layers meet, electrons get trapped and lost — that is what an interface block models. Deleting this row is how inflated numbers are made.")
# 5
s = prs.slides.add_slide(BLANK); bg(s)
title(s, "Method · the simulator", "We set up the simulator so it cannot flatter us", 5)
bullets(s, ["We simulate standard sunlight at room temperature.",
            "When we change the light-absorbing gap, the absorption edge moves with it, as in real physics.",
            "Electrical resistance is simulated inside the software, never subtracted by hand afterwards.",
            "Anything that absorbs light in the contact layers is left out in the open, not hidden."])
note(s, "Each choice closes one cheating route: self-consistent gaps, scripted resistance, visible optics.")
# 6
s = prs.slides.add_slide(BLANK); bg(s)
title(s, "Method · careful computing", "Tiny input mistakes can invent fake record cells", 6)
bullets(s, ["The files store metric units but the command line expects practical units. Mixing them overdoses the cell a million-fold and invents ghost cells near 27 percent.",
            "One command for trap sizes silently switches the traps off instead of resizing them.",
            "We rerun key cells at finer resolution. Differences below 0.017 points do not count."])
note(s, "We publish our mistakes as findings. Both traps gave plausible-looking efficiencies, which is what makes them dangerous.")
# 7
s = prs.slides.add_slide(BLANK); bg(s)
title(s, "Method · the campaign", "We ran hundreds of simulations and saved every one", 7)
table(s, [["Stage", "Runs", "What it found"],
          ["Broad grid + refinement", "96 + 36", "23.50% best with standard settings"],
          ["Energy-lineup map", "36", "24.95% at the best lineup"],
          ["Automatic search (limited box)", "104", "nothing fair beats the grid best"],
          ["Sensitivity + checks + resistance", "56 + …", "what matters flips with dirt level"]])
note(s, "Layers of searching: broad grid, then the energy lineup surprise, then a search that could not reach the winner because its box excluded it — stated as a limitation.")
# 8 race chart (native shapes)
s = prs.slides.add_slide(BLANK); bg(s)
title(s, "The record race", "Real cells improve slowly, simulations jump fast", 8)
lx, w, sc = 1.0, 11.3, (11.3 / 100)
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
note(s, "Green climbs slowly because fabrication gets better. Orange jumps because assumptions get looser. Our two ringed points sit on opposite sides of the certified record.")
# 9 champion
s = prs.slides.add_slide(BLANK); bg(s)
title(s, "Result · the upper bound", "Our best fair cell reaches 24.95 percent", 9)
img(s, "fig_JVboth.png", 0.8, 2.6, 7.2)
bullets(s, ["It produces 1.321 volts at 21.20 milliamps per square centimeter.",
            "Thick absorber, cleanest allowed dirt, lowest gap, tuned energy lineup.",
            "Every setting sits at the extreme edge — a ceiling, not a promise."], x=8.4, y=2.6, w=4.1, size=20)
note(s, "Read the curve, then the small print. Best the box allows is exactly why it cannot headline alone.")
# 10 affinity
s = prs.slides.add_slide(BLANK); bg(s)
title(s, "Result · why the lineup matters", "Tiny energy shifts decide the efficiency", 10)
img(s, "affinity_heatmap.png", 0.8, 2.6, 6.0)
img(s, "gap_steps.png", 7.1, 2.6, 5.4)
note(s, "The surprise of the campaign: moving layer energy levels changes how hard trapped charges must work to escape, and efficiency climbs even past textbook rules. The winning values are aggressive — stated, not hidden.")
# 11 dose
s = prs.slides.add_slide(BLANK); bg(s)
title(s, "Result · dirty joints", "Dirty joints cost four percentage points", 11)
img(s, "fig_audit.png", 0.8, 2.6, 7.2)
bullets(s, ["From almost-clean to very dirty joints, our own cell falls from 25.11 to 21.20 percent.",
            "We do not place other teams' numbers on our curve: their cells differ and their tables are incomplete."], x=8.4, y=2.6, w=4.1, size=20)
note(s, "Four points across four decades of dirt. Placing others here would be an accusation dressed as analysis, so we refuse.")
# 12 DB
s = prs.slides.add_slide(BLANK); bg(s)
title(s, "Result · the speed limit", "Physics sets a voltage ceiling, and our cell obeys it", 12)
bullets(s, ["From our own light-absorption model, no cell of this gap can exceed 1.371 volts.",
            "Our champion stops at 1.321 volts. Cells with deleted joints crowd right up against the ceiling.",
            "A band with no margin anywhere is not evidence of a working cell."])
note(s, "Computed from our absorption, not a textbook. The old rulebook ceiling sat above the physical limit, so we retired it and said so.")
# 13 routine
s = prs.slides.add_slide(BLANK); bg(s)
title(s, "Result · the honest number", "A realistically dirty cell gives 20.82 percent", 13)
img(s, "rs_derate.png", 0.8, 2.6, 5.6)
img(s, "thickness_nt.png", 6.9, 2.6, 5.6)
note(s, "The answer for an experimentalist. The best thickness moves with dirt level — invisible to one-variable-at-a-time testing. With realistic resistance: 20.42.")
# 14 morris
s = prs.slides.add_slide(BLANK); bg(s)
title(s, "Result · what matters most", "It depends on how dirty the cell is", 14)
img(s, "fig_morris.png", 0.8, 2.6, 6.0)
img(s, "optimizer.png", 7.1, 2.6, 5.4)
note(s, "In ultra-clean cells joints win by 2 points; in everyday cells bulk dirt wins and joints go flat. There is no single most-important factor.")
# 15 loss
s = prs.slides.add_slide(BLANK); bg(s)
title(s, "Result · against the real world", "Our extra points come from fill factor, not voltage", 15)
img(s, "loss_budget.png", 0.8, 2.6, 7.2)
bullets(s, ["Our voltage is ordinary — real records already reach 1.27 to 1.29 volts.",
            "The six-point fill-factor gap has three possible causes, and we do not pretend to know which dominates."], x=8.4, y=2.6, w=4.1, size=20)
note(s, "Read left to right with the room: voltage ordinary, current ordinary, squareness of the curve is where simulation exceeds experiment.")
# 16 taus
s = prs.slides.add_slide(BLANK); bg(s)
title(s, "Method · fair comparison", "Compare lifetimes, not just dirt counts", 16)
table(s, [["Dirt level", "Lifetime / surface speed"],
          ["Cleanest allowed", "charges live 100 microseconds"],
          ["Everyday dirt", "charges live 0.1 microseconds"],
          ["Joint floor", "surface speed 100 cm/s"]])
bullets(s, ["Dirt count times trap size is what physics actually sees.",
            "Lifetimes and surface speeds let studies compare fairly — and our 100-microsecond floor is far cleaner than the best real films."], y=5.4, size=20)
note(s, "Counts alone cannot be compared across studies; we proved the equivalence digit-for-digit. The floor's cleanliness is admitted, not hidden.")
# 17 traps
s = prs.slides.add_slide(BLANK); bg(s)
title(s, "Honesty · software traps", "Two software traps that invent fake cells", 17)
bullets(s, ["Mixing metric and practical units overdoses the cell a million-fold and invents ghost cells near 27 percent.",
            "One trap-size command silently switches the traps off instead of resizing them.",
            "Rule: build structure in files, and always read every scripted value back before believing a run."])
note(s, "Plausible-looking efficiencies from pure input errors — that is what makes them dangerous. One-line rule to defeat both.")
# 18 checklist
s = prs.slides.add_slide(BLANK); bg(s)
title(s, "Contribution · a standard", "A checklist so future studies can be compared", 18)
bullets(s, ["State joint dirt plus trap size — or the lifetime and surface speed.",
            "State which unit system every number uses, and the resistance basis.",
            "State both contact energy levels, and which affinities were surveyed versus adopted.",
            "State the radiative ceiling used, and archive every input file."])
note(s, "Eight disclosure items, each a place where silence moves the headline by points. Propose it as a reviewer checklist.")
# 19 limits
s = prs.slides.add_slide(BLANK); bg(s)
title(s, "Limits", "What this work cannot tell you", 19)
bullets(s, ["No search method proves our best cell is the global best — it is the best we evaluated.",
            "We model steady electricity only: no aging, no moisture damage, no crystal decay.",
            "We never fitted the model to a real measured cell, so the comparison table compares rather than calibrates."])
note(s, "A paper that prices others' assumptions prices its own. Questions belong here.")
# 20 takeaway
s = prs.slides.add_slide(BLANK); bg(s)
title(s, "Takeaway", "Claim 20.8. Cite 24.9 as a limit.", 20)
bullets(s, ["Every number archived, every assumption priced, every receipt regenerable from scripts.",
            "github.com/touhidsiddiqueeraj-bit/cspbi3-cbts-guardrailed"])
note(s, "One sentence to leave the room with. Then the live demo: open the champion file in SCAPS and read the number off the screen.")

out = BASE / "record-race-deck.pptx"
prs.save(str(out))
print("slides:", len(prs.slides.__iter__.__self__._sldIdLst), "| saved:", out)
