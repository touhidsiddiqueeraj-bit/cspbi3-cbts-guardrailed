# CsPbI3 / Pb-perovskite reference list — frozen before optimisation
Survey date: 2026-10-04. Stored persistently (no /tmp). `E` = experimental, `T` = SCAPS-1D simulation.

## E — Experimental CsPbI3 records (target to match/beat)

| # | Ref | Stack | PCE | Voc / Jsc / FF | Note |
|---|-----|-------|-----|----------------|------|
| E1 | Dai et al., Nature Commun. Mar 2026 (PTES moisture strategy) | FTO/TiO2/CsPbI3/PTABr/Spiro-OMeTAD/Au | **22.60% lab / 22.02% cert**, 21.00% @55%RH | FF 86.1% | Current ceiling. Target ≥22.1% |
| E2 | Qiu et al., Angew. Chem. 2025 (fluorinated dipole DFAz) | CsPbI3 + Az/DFAz interface | **22.05%** | — | Interface passivation route |
| E3 | Zhang et al., Sci. China Mater. 2026 ((ETP)2SbCl5) | TiO2/CsPbI3 dual-interface+bulk | **21.71%** | Voc 1.27V | Bulk stress relief |
| E4 | Joule 2026 (HPDA grain-boundary stitching, inverted) | p-i-n CsPbI3 | **21.43% cert** | — | Inverted record |
| E5 | Nature Commun. May 2026 (oriented DMAPbI3 → C-electrode) | FTO/TiO2/CsPbI3/Carbon HTL-free | 20.72% (20.35% cert) | Voc 1.202V, Jsc 20.72, FF 83.2% | HTL-free carbon |
| E6 | 6-IQL dual-site anchoring, J. Rare Earths / SciDirect Jun 2026 | CsPbI3 + 6-IQL surface | 19.66% | Voc 1.164V | Surface reconstruction |
| E7 | Wang et al., Angew. 2019 (choline iodide) | FTO/TiO2/CsPbI3/Spiro/Ag | 18.40% | — | Cited in baseline paper as prior exp. best |
| E8 | NREL Best Research-Cell Chart Aug 2026 + PIP Tables v66 | perovskite/Si tandem 33–34%; SJ perovskite ~26–27% | — | — | Proves 40% SJ 1-sun impossible; SQ(CsPbI3, Eg~1.7) ≈ 30% |

## T — SCAPS theory / baseline papers in folder

| # | Ref | Stack | PCE | Params to reuse |
|---|-----|-------|-----|-----------------|
| T0a | **Hossain et al., New J. Chem. 2023, DOI 10.1039/d2nj06206b — BASELINE (in folder as `4 d2nj06206b (1).pdf`)** | ITO/TiO2/CsPbI3/CBTS/Ni(Au) | 17.90% initial → **19.06% opt** (Voc~1.02V, Jsc~21.57, FF~86.5%) | Table 1: ITO 500nm/3.5/4.0/9; TiO2 30nm/3.2/4.0/9/ND9e16→9e17/Nt1e15; CsPbI3 800→1500nm/1.694/3.95/6/NA1e15→1e16/Nt1e15→1e12; CBTS 100nm/1.9/3.6/5.4/NA1e18/Nt1e15; IF both 1e10cm⁻²; Ni 5.5eV; AM1.5G 300K |
| T0b | Mushtaq et al., Solar Energy 249 (2023) 401–413 — lead-free ref (in folder) | FTO/SnO2/MASnBr3/NiO/Au | **34.52% claimed** (Voc1.12, Jsc34.86, FF88.3) | Flagged >SQ(1.3eV≈29.4%) → idealised Rs=0/Rsh=∞ artefact; reuse only HTL/ETL doping method, not numbers |
| T1 | Hossain et al., ACS Omega 2022 (96-stack screen, precursor to T0a) | ITO/TiO2/CsPbI3/CBTS/Au best of 96 | 17.90% (Voc0.997, Jsc21.075, FF85.21) | ETL/HTL band-alignment screen method |
| T2 | Jayan & Sebastian, Solar Energy 221 (2021) | FTO/ZnO/CsPbI3/CuSbS2/Se | 15.60% | Lower-bound theory |
| T3 | Boussaada et al. 2025 | FTO/SnCoOx/CsPbI3/Cu2O/Au, abs 900nm, NA1.5e15, Nt1e12 | **21.34%** (Voc1.277, Jsc20.32, FF82.4) | SnCoOx ETL + Cu2O HTL alternative if CBTS caps |
| T4 | Ristiansyah et al., Greensusmater 2026 | FTO/ZnO/CsPbI3/Spiro, 0.5→1.6µm, NA1e15→1e18, ND_ETL1e17→1e19 | 16.3%→**23.1%** (Voc1.39, Jsc20.5, FF87.4) | Upper-bound; NA1e18 flagged experimentally hard → treat as optimistic cap |
| T5 | Nazli et al. 2025 | ITO/TiO2/CsPbI3/CBTS/Ni | **24.17%** (+26.5%) | Same stack as T0a pushed further |
| T6 | Chalil et al., MDPI Energies 2022 (inverted) | ITO/CuI/CsPbI3/ZnO/Ag, 750nm, Nt1e12 | 18.9%→**26.5%** | Shows Nt1e12 inflation; keep ≥1e12 floor per strict-realism rule |
| T7 | DEMOTED (unverifiable manuscript, removed from evidentiary chain) | -- | -- | χ-optimised (MAPbI3 χ3.75, Rs=1Ω) | Pb-fallback params (MAPbI3 Eg1.5/χ3.9; FAPbI3 Eg1.48) |
| T8 | Mohamad 2025, STO/FAPbI3/CuScN + BSF | **31.49%** (Voc1.45) | STO μe5300, Nt1e12, BSF photon recycling | Only sub-40% path is BSF/buffer; single-junction still <SQ |
| T12 | Oyedele et al. 2023, FTO/ZnO/CsPbI3/PTAA | **24.24%** (Voc1.45, FF81.57) | No interface layers (stated) | Sits in no-IF band; audit target |
| T13 | Alshaikh 2026, Crystals 16:310, FTO/WS2/CsSnI3/CuSCN/Au + GP-BO, DOI 10.3390/cryst16050310 | 27.83% | 12k sims, SHAP Nt-dominance | ML precedent on CsSnI3 |
| T14 | Rahman & Alam 2026, J Mater Sci: Mater Eng, FTO/WS2/MASnI3/V2O5/Pt + RF | **40.17%** idealized | Admits >SQ artefact | Cautionary tale for guardrails |
| T9 | Son et al., Appl. Sci. 2024 | ITO/TiO2/MAPbI3/Cu2O/Au, PAL1300nm, Nt1e14, IF1e13 | **19.30%** | MAPbI3 fallback recipe |
| T10 | Ritu et al., AIP Conf. Proc. 2024 | FTO/TiO2/FAPbI3/Spiro/Ag, gradient doping G=1000 | **20.34%** | FAPbI3 fallback recipe |
| T11 | Zenodo 2025, 7182 SCAPS runs + CatBoost/SHAP | CsPbI3/MAPbI3/FAPbI3 mixed, 200–800nm | — | Validates simultaneous-sweep ranges; thickness/SHAP priors |

## Physics cap (agreed with user: Cs first, then Pb)

- SQ limit Eg≈1.694–1.73eV → Jsc≈23–24, Voc≈1.4–1.5, FF≈84–85, **η≈29–30%**. Any claim >30% SJ 1-sun is unphysical; 40% needs tandem/concentrator/BSF stack (separate plan).
- Agreed stop rule: **match/beat E1 (≥22.1% SCAPS + strict checklist: Nt≥1e12/cm³, Voc deficit 0.35–0.45V, Rs≥1Ω·cm² checked, T=300K, A–B absorption, CBO 0–+0.3 / VBO −0.3–−0.1)**; fallback MAPbI3/FAPbI3 if CsPbI3 plateaus <21.5%.
