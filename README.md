# Guardrailed CsPbI3 constrained maximum (SCAPS-1D)

Best point in a stated box for an ITO/TiO₂/CsPbI₃/CBTS/Ni cell (23.49%),
with every load-bearing assumption priced: interface dose–response,
scripted Rs/Rsh, contact work functions, Nt×σ, Morris sensitivity,
and a realistic-settings result (20.68%).

Manuscript: `manuscript/document.tex` → `drafts/draft-jbss-r5.pdf`
(compile: `pdflatex` + `bibtex` + `pdflatex` ×2 in `manuscript/`).

## Layout

| Path | Contents |
|---|---|
| `manuscript/` | paper source (`document.tex`, `references.bib`) |
| `drafts/` | submission snapshots r0–r5 (r5 current) |
| `defs/` | device definitions: `csPbI3-CBTS-r7.def` (guardrailed), `noIF`, WF/σ variants + builders |
| `outputs/` | all sweep data: `roundA/B.jsonl` (grid), `char.jsonl` (IV/T/audit/CV/QE/EB), `s0/s1/s4/s6` dose+parasitics, `s5_morris.jsonl`, `figs/` |
| `receipts/` | champion + baseline receipts |
| `scripts/` | runners (`roundA/B`, `champion`, `characterize*`, `s0/s1/s4/s5/s6`, `fig_rev1`, `fig_timeline_v4`); `archive/` holds superseded one-offs |
| `review/` | JBSS format excerpts + r0 screenshots |
| `sources/` | reference PDFs (not tracked: copyrighted — see REFERENCES.md) |

## Reproduce

Requires SCAPS-1D 3.3.10 under WINE + [`scaps-runner`](https://github.com/)
(`~/scaps-runner`, 4 workers). Sync defs, then e.g.:

```bash
python3 scripts/champion.py     # 23.49% fine-step champion
python3 scripts/s1_dose.py      # interface dose + Rs/Rsh + WF grids
python3 scripts/s5_morris.py   # Morris screen (r=8, p=4, seed 7)
python3 scripts/fig_rev1.py     # alignment / audit / Morris figures
```

## Headline numbers (all in `outputs/`)

- Box best: 23.49% (2.2 µm, Nt 1e12, Rs=0, N_if 1e10) — corner of box, stated as such
- Realistic: 20.68% (ITO 4.4 eV, Nt 1e15, N_if 1e10); routine-defect peak 20.82% @1.0 µm
- Interfaces: 25.04 (1e8) → 20.64 (1e12); σ×10 reproduces N×10 (22.21%)
- Parasitics (scripted): Rs=1 → 23.07, Rsh=1e4 → 23.38
- Morris μ* (pts/decade): N_if 1.02 > N_t 0.68 > E_g 17.5/eV
