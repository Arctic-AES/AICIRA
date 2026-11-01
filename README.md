# AICIRA

*Adaptive Multi-Fidelity Identification of Critical Localized Imperfections in Axially Compressed Rocket Airframes*

A small dent can change how a thin rocket airframe buckles. AICIRA studies that effect through shell mechanics and ANSYS simulations, with the goal of finding the most critical imperfections without having to simulate every possible dent.

## Architecture

1. **Physics Engine** — Classical shell theory, geometry, analytical validation.
2. **FEA Data Processing** — ANSYS results, critical loads, mesh convergence.
3. **Multi-Fidelity Surrogate** *(planned)* — Model relationships between imperfections and buckling capacity.
4. **Adaptive Experiment Selection** *(planned)* — Identify which imperfection configurations deserve further simulation.
5. **Nemotron Agent + Visualization** *(planned)* — Orchestrate verified tools, communicate uncertainty, and present results.

## Repository

- **[`documentation/`](documentation/)** — Simulation baselines, assessments, and Workbench notes.
- **[`software/`](software/)** — Geometry generation, physics calculations, and FEA data processing; future ML and frontend development.

