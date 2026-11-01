# AICIRA simulation baseline

| Quantity | Value |
|---|---:|
| Cylinder midsurface radius | 75 mm |
| Length | 450 mm |
| Shell thickness | 0.40 mm |
| Young's modulus | 69 GPa |
| Poisson ratio | 0.33 |
| Gaussian dent | 0.040 mm deep; 20 mm axial/arc widths |
| Linear static / eigenvalue reference load | 1,000 N |
| Nonlinear displacement target | −1.6 mm |

**Analytical reference:** 0.034599 mm shortening at 1,000 N; classical ideal-cylinder buckling load approximately 42.425 kN.

**Completed ANSYS results:** Linear static for both cylinders; first eigenvalue buckling estimates of 43.336 kN (perfect) and 43.264 kN (dented). These are *not* measured nonlinear collapse loads.

**Unfinished:** Matched nonlinear simulations stopped near 1.34 mm before the −1.6 mm target, with element distortion. Mesh/stabilization sensitivity, dent parameter sweep, and adaptive model validation remain outstanding. Do not infer nonlinear strength knockdown from these incomplete curves.
