# ANSYS Workbench baseline

**Geometry:** Midsurface radius 75 mm, length 450 mm, SHELL181 thickness 0.40 mm. Linear isotropic aluminum: E = 69,000 MPa, ν = 0.33, density = 2700 kg/m³. Baseline dent: 0.040 mm depth, 20 mm axial/arc widths, centered at Z = 225 mm.

**Linear static:** Bottom rim fixed; 1,000 N compressive top reference load. Compare axial shortening with the analytical 0.034599 mm.

**Eigenvalue buckling:** Link the matching 1,000 N static solution to eigenvalue buckling; extract six modes. These are linearized estimates, not nonlinear collapse loads.

**Nonlinear static (both cylinders):** Bottom rim fixed; top rim UX = UY = 0, top UZ ramps from 0 to −1.6 mm, top rotations free. Large Deflection ON; use identical end conditions and comparable meshes. Extract converged reaction-force histories.

**Current blocker:** Both newer nonlinear runs stopped near 1.34 mm with excessive element distortion. Use a *copy* of the baseline for solver diagnostics, starting with `software/ansys/diagnostic_controls.mac`. Check that iteration and stepping controls actually appear in Solver Output. If failure persists, locate the distorted elements and examine the equilibrium path. Numerical controls are diagnostic, not guaranteed fixes.

**Data:** Keep the native Workbench files outside Git. Export `shortening_mm,top_compression_N` (optional `time`) for Python screening; an incomplete history is not a verified peak load.
