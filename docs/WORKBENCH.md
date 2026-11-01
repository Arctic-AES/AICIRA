# ANSYS Workbench baseline: what's done and what's next

The Python modules in this repository are **not ANSYS** and cannot compute an FEA buckling load. Use ANSYS Mechanical 2025 R1 (or verify behavior on a different version) for structural solves.

## Baseline geometry and material

- Cylindrical **midsurface**: radius 75 mm; axial length 450 mm.
- Assign shell thickness **0.40 mm** inside Mechanical, not as a second solid wall.
- Aluminum linear elastic: E = 69,000 MPa, ν = 0.33, density 2700 kg/m³.
- Gaussian inward dent: depth 0.040 mm, center Z = 225 mm, axial/arc widths 20 mm.
- SHELL181; start with 5 mm global shell element size, then do mesh sensitivity.

## Systems and loads

| System | Perfect | Dented | Purpose |
|---|---|---|---|
| Linear Static | 1000 N axial compression | 1000 N | Verify small-strain axial stiffness |
| Eigenvalue Buckling | Prestressed from matching linear static | Likewise | First six linearized buckling modes |
| Nonlinear Static | Ramp top UZ 0 → -1.6 mm | Same | Seek matched peak reaction and postbuckling |

The 1000 N force is **a reference load for linear static and eigenvalue buckling**, not the nonlinear load. The nonlinear systems impose **displacement**, and the reaction force is an output.

**Matching nonlinear boundary conditions:** bottom shell rim fixed; top rim UX=0, UY=0, UZ ramps to -1.6 mm; top rotations free; cylindrical wall free. Apply the same to both geometries. These are the original guided/clamped end constraints; if a more realistic physical fixture requires changes, modify and rerun **both** models, including reference buckling analyses.

## Reproducible nonlinear diagnostic

1. Duplicate each baseline nonlinear system; preserve the current native Workbench project and solver files.
2. Confirm surface bodies and shell thickness, edge scoping, material, top/bottom supports, and large deflection ON.
3. In Mechanical Analysis Settings, set automatic stepping ON, initial 200, minimum 200, maximum 20000, solver sparse-direct. Change maximum equilibrium iterations to 50 if exposed.
4. Where a Mechanical Commands object is needed, see `ansys/diagnostic_controls.mac`. Avoid duplicated conflicting controls: use the Mechanical settings OR the commands for time stepping, not both.
5. Confirm in **Solver Output** that `NEQIT=50`, the actual minimum step, and predictor OFF were applied. Earlier runs requested changes that did not appear in the solver log.
6. Record all converged substeps and export at least `time,shortening_mm,top_compression_N` with **positive compression**. Record full solver log, error file, stabilization energy if used, and mesh/node counts.
7. If excessive element distortion recurs, locate failed element IDs and the final converged deformation. Do not relabel the last converged force as the collapse load. Do not change geometry or load target to conceal failure.
8. Only after obtaining a resolved peak and checking mesh/stabilization sensitivity, run additional dent configurations.

These controls are diagnostic, **not guaranteed to converge**. For physical instability, different equilibrium-path techniques may be required. Avoid claiming nonlinear buckling capacity from incomplete curves.

## STEP generation and import

`python scripts/generate_all_dents.py` creates one perfect shell midsurface and **twelve Gaussian-dented STEP midsurfaces** under `geometry/`. Inspect one imported STEP and verify geometry validity, top and bottom edge scoping, and shell-normal orientation before repeating in Workbench.

Existing Workbench journals from the October 2026 experiments are not reproduced here as a verified universal one-click workflow. Workbench API object selection and license availability are installation-specific. The native `.wbpj`, `*_files`, and result `.rst` files remain outside Git because of size and environment specificity.

## Acceptance for a nonlinear comparison

- Same geometry dimensions, material, BCs, solver parameters, comparable meshes.
- Actual peak reaction occurs **before** the last converged point, with a sampled postpeak decrease.
- Solver log documents convergence status for each reported point.
- Report mesh sensitivity and stabilization dependence; high artificial stabilization invalidates unqualified capacity claims.
- `python -m aicira check-history FILE.csv` is an **initial data screening**, not a substitute for physical validation.
