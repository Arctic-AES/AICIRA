# AICIRA

**Adaptive Multi-Fidelity Identification of Critical Localized Imperfections in Axially Compressed Rocket Airframes**

AICIRA studies how localized dents affect cylindrical-shell buckling and, eventually, how to identify critical imperfections with fewer nonlinear simulations.

- **[`documentation/`](documentation/)** — Current simulation baseline, assessments, and Workbench notes.
- **[`software/`](software/)** — Geometry generation, physics calculations, FEA-data screening, and tests. Machine learning and frontend code will be added here when implemented.

## Run the baseline

```bash
cd software
python -m pip install -e .
python -m aicira baseline
python -m aicira cases --output generated/cases.csv
python -m unittest discover -s tests -v
```

Generate the perfect and 12 dented STEP midsurfaces (requires OCP, NumPy, SciPy):

```bash
python geometry/generate_all_dents.py
```

**Current limitation:** Linear static and eigenvalue analyses exist; matched nonlinear collapse loads are not yet established. See [`documentation/BASELINE.md`](documentation/BASELINE.md).
