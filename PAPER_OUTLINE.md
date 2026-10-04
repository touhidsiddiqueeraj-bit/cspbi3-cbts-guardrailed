# Manuscript blueprint — guardrailed CsPbI3 record + reproducibility audit

## Working titles (pick one)
1. "A strictly-realistic 23.5%-efficient CsPbI3 solar cell by simultaneous multi-parameter SCAPS-1D optimisation: record, guardrails, and a reproducibility audit"
2. "How realistic are 24%+ SCAPS claims for CsPbI3? Interfaces, units, and a 23.49% guardrailed optimum"
3. "Beyond one-at-a-time: factorial co-optimisation of thickness, doping, defects and band alignment in CsPbI3/CBTS cells"

## Angle (decided)
Guardrailed record + audit (main), scripting unit-trap (methods box), factorial interactions + cheap ML/SHAP-style importances (supporting). ML test R² 0.9971 (80/20 split, n=126): logNt 0.479 > Eg 0.345 > logNA 0.105 > logND 0.057 > thickness 0.014 — matches PerovskiteOpt-AI's Nt-dominance on a different (CsSnI3) stack; first such quantification for CsPbI3-CBTS.

## Core numbers (all in receipts/, reproducible)
- Baseline repro: 18.99% (paper 17.9–19.06%) — validates def.
- Champion ITO/TiO2/CsPbI3/CBTS/Ni: **23.49%** (Voc 1.234, Jsc 21.19, FF 89.78; 2.2µm, NA 3e16, Nt 1e12, ND_ETL 9e17, Eg 1.65/χ 3.928, IF 1e10cm⁻² both sides, Ni 5.5eV, 300K 1-sun). Deterministic dup exact.
- Audit (same cells ± interfaces): 23.40→24.87 / 23.47→24.73 / 23.50→25.16 (**+1.3–1.7 abs inflation**, Voc +0.13V without IF). Literature 24.17/24.24% sit in the no-IF band.
- Unit-trap demos: NA set 1e21/1e22 (cm⁻³, i.e. 1e6× overdose from /m³ confusion) → 25.93%/27.02% with Voc 1.47–1.53 / FF 91+ — guardrail flags (Voc>Eg/q−0.1, FF>90.5).
- T-sweep: 24.44% (275K) → 16.70% (475K); Jsc flat ~21.19; FF 90.75→82.50 (275K FF marginally above ideal-diode 90.2% — disclose as scan artefact).
- Rs: not scriptable in SCAPS 3.3.10 (verified vs scriptdescription3310.txt) → analytic derate ×0.965 ≈ 22.68%, still beats 22.02% cert.

## Figure/table map (figs/ done)
| Paper element | File | Status |
|---|---|---|
| JV champion (+baseline) | figs/champion_JV.png | done |
| QE 300–850nm, edge 731→752nm | figs/fig_QE.png | done |
| C-V + Mott-Schottky 1MHz | figs/fig_CV_MS.png | done |
| Band diagram @0V | figs/fig_EB.png | done |
| G/R profiles @0V | figs/fig_GR.png | done |
| T-dependence | figs/fig_T.png | done |
| Audit bars IF on/off | figs/fig_audit.png | done |
| thickness×Nt contour | figs/fig_contour.png | done |
| Comparison table vs E1–E8/T0–T11 | REFERENCES.md → paper Table 1 | to write |
| Guardrail box (floors, flags, derate) | receipts/ + UNITS.md | to write |

## Sections
1. Intro (CsPbI3 record race 22.02% cert; SCAPS inflation problem; OVAT vs factorial; paper contributions ×3)
2. Simulation framework (def Table 1 Hossain-mapped; A-B absorption; IF blocks; unit map; guardrail definitions; factorial design 96+36; ML surrogate)
3. Results: baseline validation → factorial optimum (champion) → interactions (contour, Eg-χ, thickness×Nt) → characterization (QE/CV/EB/GR/T) → ML importances
4. Audit: noIF re-runs + unit-trap demos + literature re-placement (table: claims drop under guardrails)
5. Discussion: fab plausibility (NA 3e16 OK; Nt 1e12 = single-crystal-grade upper bound; Eg 1.65 strained bound); 40% impossible SJ (SQ~30%); tandem outlook
6. Methods appendix: unit-trap details, receipt/reproducibility (open defs+JSONL+scripts)
7. Data availability: everything in leadpaper/{defs,outputs,receipts,logs} (no /tmp, restart-safe)

## Journal (decide after draft)
1st: Solar Energy (baseline venue, full-char fit) or Surfaces & Interfaces (ML-angle precedent 28.38% paper). Fallback: MDPI Micromachines/Energies. Decision rule: if audit margin narrative + full figs → Q1; if reviewers demand experiment → MDPI + frame as simulation-guided design.

## Left to write (no more sims needed except optional)
- Prose per sections above; Rs analytic-derate one-paragraph calc; refs.bib from REFERENCES.md (18 entries mapped).
- Optional (only if targeting Solar Energy): ETL/HTL thickness micro-sweep (paper says insensitive — 8 sims, skip unless reviewer asks).
