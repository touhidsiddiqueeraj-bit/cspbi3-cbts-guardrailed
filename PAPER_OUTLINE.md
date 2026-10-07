# Manuscript blueprint — guardrailed CsPbI3 record + reproducibility audit

## Working titles (pick one)
1. "Guardrails for the Record Race: What a CsPbI3 Cell Can Honestly Claim (24.9% → 20.8%)" (current manuscript title)
2. "How realistic are 24%+ SCAPS claims for CsPbI3? Interfaces, units, and a 24.95% guardrailed optimum"
3. "Beyond one-at-a-time: factorial co-optimisation of thickness, doping, defects and band alignment in CsPbI3/CBTS cells"

## Angle (decided)
Guardrailed record + audit (main), scripting unit-trap (methods box), factorial interactions + cheap ML/SHAP-style importances (supporting). ML test R² 0.9971 (80/20 split, n=126): logNt 0.479 > Eg 0.345 > logNA 0.105 > logND 0.057 > thickness 0.014 — matches PerovskiteOpt-AI's Nt-dominance on a different (CsSnI3) stack; first such quantification for CsPbI3-CBTS.

## Core numbers (all in outputs/, reproducible; manuscript r7 hierarchy)
- Baseline repro: 18.99% (paper 17.9–19.06%) — validates def.
- Joint-affinity optimum ITO/TiO2/CsPbI3/CBTS/Ni: **24.95%** (Voc 1.321, Jsc 21.20, FF 89.11; 2.2µm, NA 3e16, Nt 1e12, ND_ETL 9e17, Eg 1.65/χ 3.928, χ_CBTS 3.9/χ_TiO2 3.7, IF 1e10cm⁻² both sides, Ni 5.5eV, 300K 1-sun). s22 receipt 24.9464%; def-file load 24.9441% (0.002-pt path gap, inside 0.017-pt IV-step threshold).
- Surveyed-affinity best: 23.50% (Round B; Round A best 23.47%). Exploratory 104-config search peaks 1.87 pts below among guardrail-satisfying runs — does not bracket the champion by construction.
- Defended routine-defect case: **20.82%** (1.0µm, N_t=10¹⁵, surveyed χ) → **20.42%** at scripted R_s=1; 20.68% with ITO 4.4eV on the 0.8µm base (18.11% when that ITO meets the adopted χ).
- Audit (same cells ± interfaces): 23.40→24.87 / 23.47→24.73 / 23.50→25.16 (**+1.3–1.7 abs inflation**, Voc +0.13V without IF). No-interface V_oc (1.363–1.382V) hugs the model-derived detailed-balance limit (1.371V at 1.65eV) — no margin, none trusted; literature 24.17/24.24% NOT placed on our curve (differing stacks, incomplete parameter tables).
- Unit-trap demos: NA set 1e21/1e22 (cm⁻³, i.e. 1e6× overdose from /m³ confusion) → 25.93%/27.02% with Voc 1.47–1.53 / FF 91+ — guardrail flags (Voc above model-derived DB limit, FF above Green's ideal at computed Voc).
- T-sweep (joint base): 25.88% (275K) → 18.13% (475K); Jsc pinned ~21.20; FF 89.96→82.43; −0.16%/K over 300–475K (475K end is a solver stress test, ignores E_g(T) and phase stability).
- Rs/Rsh: scriptable in SCAPS 3.3.10 (`set external.Rs/Rsh`) — scripted sweeps throughout (joint: 24.73/24.52/24.09 at Rs 0.5/1/2; 24.38 combined with Rsh 1e4). No analytic derate used.

## Figure/table map (all in outputs/figs/, done; manuscript uses portable manuscript/figs/ copies)
| Paper element | File | Status |
|---|---|---|
| JV champion (+baseline) | figs/fig_JVboth.png | done |
| QE 300–850nm, edge 731→752nm | figs/fig_QE.png | done |
| C-V + Mott-Schottky 1MHz | figs/fig_CV_MS.png | done |
| Band diagram @0V | figs/fig_EB.png | done |
| G/R profiles @0V | figs/fig_GR.png | done |
| T-dependence | figs/fig_T.png | done |
| Audit dose–response | figs/fig_audit.png | done |
| thickness×Nt contour | figs/fig_contour.png | done |
| Joint-optimum band alignment | figs/fig_align.png | done |
| Morris μ*/σ | figs/fig_morris.png | done |
| Record-race timeline | figs/fig_timeline.png | done |
| Comparison table vs E1–E8/T0–T11 | manuscript Table tab:lit | done |
| Guardrail box + reporting checklist | manuscript Tables tab:guard, tab:checklist | done |

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
- DONE in manuscript r7: prose per sections above; scripted Rs/Rsh sweeps (no analytic derate); refs.bib enriched (Dai2026 + Qiu2025 vol/pages/doi verified).
- Optional (only if targeting Solar Energy): ETL/HTL thickness micro-sweep (paper says insensitive — 8 sims, skip unless reviewer asks).
