# Champion device — joint-affinity optimum 24.95% + defended routine case 20.82% (restart-safe)

> **Status (r15):** this document preserves the r7 champion framing. The current manuscript (r14/r15) supersedes its headline hierarchy: 24.95% remains the permissive-box ceiling, but the headlined envelope is the routine-quality prior envelope **18.0%** (15.6–20.0%), and the ceiling record comparison is DoS-conditional. QE edge shift is 731→750 nm as in `manuscript/document.tex` (earlier notes said 752 nm).

## Result

| Device | Voc (V) | Jsc (mA/cm²) | FF (%) | PCE (%) |
|---|---|---|---|---|
| **ITO/TiO₂/CsPbI₃/CBTS/Ni, joint optimum (SCAPS, Rs=0)** | 1.321 | 21.20 | 89.11 | **24.95** |
| Same stack, surveyed affinities | 1.234 | 21.19 | 89.78 | 23.50 |
| Same stack, routine defects N_t 10¹⁵ (1.0 µm) | — | — | — | **20.82** (20.42 at Rs=1) |
| Dai et al. Nature Commun. 2026 (lab / cert) | — | — | 86.1 | 22.60 / 22.02 |
| Qiu et al. Angew. 2025 | — | — | — | 22.05 |
| Zhang et al. Sci. China Mater. 2026 | 1.27 | — | — | 21.71 |
| Baseline Hossain NJC 2023 (reproduced 18.99% here) | 1.00 | 21.08 | 86.6 | 19.06 |

Margin (box maximum): **+2.35 over lab record, +2.93 over certified
record.** Computed scripted parasitics at the joint base: Rs=0.5 → 24.73%,
Rs=1 → 24.52%, Rs=2 → 24.09%, Rs=1/Rsh=1e4 combined → 24.38% — the maximum
survives parasitics; the defended number is the routine-defect 20.82%.

## Champion stack (all persistent: `defs/csPbI3-CBTS-champion24p95.def`, supervisor copy `defs/champion24p95.scaps`)

- Absorber CsPbI₃: **d 2.2 µm, Eg 1.65 eV, χ 3.928 eV, NA 3e16 cm⁻³, Nt 1e12 cm⁻³**, ε 6, μ 25/25 cm²/Vs, Nc 1.1e19 / Nv 8.2e19 cm⁻³, A-B absorption (A=1e7)
- ETL TiO₂: 30 nm, ND **9e17 cm⁻³**, Nt 1e15, χ **3.7 eV** (joint optimum; surveyed 4.0)
- HTL CBTS: 100 nm, NA 1e18, Nt 1e15, χ **3.9 eV** (joint optimum; surveyed 3.6)
- Interfaces: 1e10 cm⁻² both sides, neutral, σ 1e-19 m² — Back Ni 5.5 eV / front ITO 4.0 eV, 300 K, 1 sun
- Optimisation: **132 grid combos** (Round A 96: 5-dim factorial; Round B 36 refine) + **52-run joint-affinity map** (s11) + 104-config exploratory search (s13, peaks 1.87 pts below among guardrail-satisfying runs), 4 workers, checkpointed JSONL (`outputs/roundA.jsonl`, `roundB.jsonl`, `s11_joint_chi.json`), JV in `outputs/s22_jointIF.json`, fig `outputs/figs/fig_JVboth.png`

## Key findings (all-params-together vs papers' one-at-a-time)

1. Eg 1.65 (strained lower bound) swept all top-10 — Jsc 21.1–21.2 vs 19.7 at 1.694; chi-link held CBO flat.
2. Nt 1e12 (strict floor, kept) + NA 1–3e16 co-optimised: Voc 1.12→1.32 at the joint optimum.
3. Thick absorber 2.0–2.2 µm wins only jointly with low Nt (diffusion length covers thickness) — invisible to OVAT; optimum shifts to 1.0 µm at routine defects.
4. ETL ND 9e17 (paper opt) confirmed; HTL/ETL thickness insensitive (100/30 nm retained).
5. Joint χ map adds the final 1.45 pts (23.50 → 24.95%) via interface activation energy, not transport — peak turns over past χ_CBTS ≈ 3.95 eV, so the optimum is interior.

## Honest caveats (priced, not hand-waved)

- 24.95% is a **box maximum at Rs=0** (upper bound, not forecast): Nt 1e12 implies τ ≈ 100 µs (1–2 orders beyond best films); Eg 1.65 below experimental ~1.7; both affinities outside surveyed/typical windows; contacts at permissive edges.
- Back-contact cliff at joint affinities: Ni 5.0 eV → 15.63% (vs no cost 5.5→5.2 at surveyed χ). Front contact: ITO 4.0→4.7 → 18.60%.
- Nc/Nv capped 10× below paper print (1e19 vs printed 1e20 cm⁻³, unphysical >solid density) — noted in receipt.
- Not demonstrated: 2.2 µm device-quality CsPbI₃ at Nt∼1e12; sputtered CBTS directly on CsPbI₃ (no precedent found) — requirements list, not recipe.
- **SQ ≈ 30% at 1.65 eV.** 24.95% is ~83% of SQ. A true 40% needs a CsPbI₃/Si or all-perovskite tandem (proposed follow-on).
- Reproduce: `python3 scripts/s11_joint_chi.py` (map) + `python3 scripts/s22_jointIF.py` (1-sim re-run). Full history in `receipts/`.
