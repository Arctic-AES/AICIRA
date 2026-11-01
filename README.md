# AICIRA

*Adaptive Multi-Fidelity Identification of Critical Localized Imperfections in Axially Compressed Rocket Airframes*

AICIRA investigates how localized geometric imperfections affect the axial buckling of thin-walled rocket airframes. The long-term objective is to identify critical imperfections using fewer expensive nonlinear finite element simulations.

## Architecture

1. **Physics Engine** — Classical shell theory, geometry, analytical validation.
2. **FEA Data Processing** — ANSYS results, critical loads, mesh convergence.
3. **Multi-Fidelity Surrogate** *(planned)* — Model relationships between imperfections and buckling capacity.
4. **Adaptive Experiment Selection** *(planned)* — Identify which imperfection configurations deserve further simulation.
5. **Nemotron Agent + Visualization** *(planned)* — Orchestrate verified tools, communicate uncertainty, and present results.

## Repository

- **[`documentation/`](documentation/)** — Simulation baselines, assessments, and Workbench notes.
- **[`software/`](software/)** — Geometry generation, physics calculations, and FEA data processing; future ML and frontend development.

**Current stage:** Analytical and linear buckling baselines are available. Matched nonlinear buckling loads and adaptive-model performance remain to be established.
