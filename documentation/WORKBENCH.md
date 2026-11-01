# ANSYS Workbench baseline

**Geometry:** Midsurface radius 75 mm, length 450 mm, SHELL181 thickness 0.40 mm. Linear isotropic aluminum: E = 69,000 MPa, ν = 0.33, density = 2700 kg/m³. Baseline dent: 0.040 mm depth, 20 mm axial/arc widths, centered at Z = 225 mm.

**Linear static:** Bottom rim fixed; 1,000 N compressive top reference load. Compare axial shortening with the analytical 0.034599 mm.

**Eigenvalue buckling:** Link the matching 1,000 N static solution to eigenvalue buckling; extract six modes. These are linearized estimates, not nonlinear collapse loads.

**Nonlinear static (both cylinders):** Bottom rim fixed; top rim UX = UY = 0, top UZ ramps from 0 to −1.6 mm, top rotations free. Large Deflection ON; use identical end conditions and comparable meshes. Extract converged reaction-force histories.

## Solver diagnostics

The newer nonlinear runs stopped near 1.34 mm with excessive element distortion. Work with **copies** of the baseline analyses, leaving the geometry, material, loads, and boundary conditions unchanged.

Start with automatic time stepping (initial 200, minimum 200, maximum 20,000 substeps), full Newton–Raphson, up to 50 equilibrium iterations, predictor OFF, and stabilization OFF. These controls are diagnostic, not guaranteed fixes.

If needed, enter the following in an ANSYS Mechanical Commands object attached to the **nonlinear analysis**. Keep the Analysis Settings and Commands object consistent; do not specify conflicting time-step controls in both places.

```apdl
/SOLU
NLGEOM,ON
AUTOTS,ON
NSUBST,200,20000,200
NROPT,FULL
NEQIT,50
PRED,OFF
LNSRCH,AUTO
STABILIZE,OFF
EQSLV,SPARSE
OUTRES,ALL,ALL
```

Confirm that the intended iteration limit, step limits, and predictor setting are reflected in Solver Output. If the analysis still fails, locate the distorted elements and inspect the last converged deformation rather than changing physical parameters merely to force convergence.

**Data:** Keep native Workbench files outside Git. Export `shortening_mm,top_compression_N` (optional `time`) for Python screening. An incomplete history is not a verified peak load.
