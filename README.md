# AICIRA

**Adaptive Multi-Fidelity Identification of Critical Localized Imperfections in Axially Compressed Rocket Airframes**

AICIRA studies how localized dents affect the axial buckling response of thin-walled cylindrical rocket airframes, and ultimately whether adaptive sampling can locate critical imperfections with fewer nonlinear FEA runs.

## Status

The Python baseline analytical solver, geometry case definitions, STEP generator, and FEA-history screening utility are available. These do **not** replace ANSYS. Matched nonlinear buckling peaks, mesh independence, and adaptive multi-fidelity performance are **not yet established**.

## Quick start

Python 3.10+; no runtime dependencies for the analytical baseline or CSV utilities.

```bash
python -m pip install -e .
python -m aicira baseline
python -m aicira cases --output datasets/cases.csv
python -m unittest discover -s tests -v
```

To generate actual CAD STEP midsurfaces, install NumPy, SciPy and a compatible `cadquery-ocp`/`OCP` build, then:

```bash
python scripts/generate_all_dents.py
```

CAD outputs are intentionally ignored by Git; generated meshes and Workbench projects are not source code. For ANSYS setup, constraints, iteration controls, and data export, see **[docs/WORKBENCH.md](docs/WORKBENCH.md)**.

To screen an exported *converged* reaction-force history:

```bash
python -m aicira check-history path/to/history.csv --target 1.6
```

Required headers: `shortening_mm,top_compression_N`, optional `time`. Missing or incomplete postpeak data are **never** converted to accepted buckling peaks.

## Research workflow

1. Establish analytical checks and matching linear static / eigenvalue simulations.
2. Complete matching nonlinear compression for perfect and dented cylinders.
3. Verify mesh and stabilization sensitivity.
4. Generate and solve additional dent configurations; export clean, traceable results.
5. Train and independently evaluate low-/high-fidelity surrogates and adaptive selection.
6. Build interactive analysis software on top of validated data.

## Model baseline

| Quantity | Value |
|---|---:|
| Midsurface radius | 75 mm |
| Cylinder length | 450 mm |
| Shell thickness | 0.40 mm |
| Young's modulus | 69 GPa |
| Poisson ratio | 0.33 |
| Density | 2700 kg/m³ |
| Baseline dent depth | 0.040 mm |
| Dent axial/arc Gaussian widths | 20 mm / 20 mm |
| Linear prestress reference | 1000 N |
| Nonlinear imposed shortening | 0 → -1.6 mm |

All results must distinguish analytical reference values, linearized eigenvalue buckling predictions, and verified nonlinear buckling loads.
