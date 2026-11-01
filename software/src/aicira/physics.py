"""Thin-cylinder analytical reference, not a nonlinear buckling solver.

Units throughout: millimetres, newtons, megapascals (N/mm^2), kilograms.
The classical long-cylinder buckling relation describes an ideal shell; it is
not a prediction of a finite-cylinder nonlinear collapse load.
"""

from dataclasses import asdict, dataclass
from math import pi, sqrt


@dataclass(frozen=True)
class Cylinder:
    radius_mm: float = 75.0
    length_mm: float = 450.0
    thickness_mm: float = 0.4
    youngs_modulus_mpa: float = 69_000.0
    poisson_ratio: float = 0.33
    density_kg_m3: float = 2700.0

    def __post_init__(self) -> None:
        if min(self.radius_mm, self.length_mm, self.thickness_mm,
               self.youngs_modulus_mpa, self.density_kg_m3) <= 0:
            raise ValueError("Geometry, modulus and density must be positive")
        if self.thickness_mm >= self.radius_mm:
            raise ValueError("Thin-shell model requires thickness < radius")
        if not -1.0 < self.poisson_ratio < 0.5:
            raise ValueError("Poisson ratio must lie between -1 and 0.5")


def analytical_reference(cylinder: Cylinder = Cylinder(), force_n: float = 1000.0) -> dict:
    """Return pre-buckling checks and classical ideal-shell buckling reference."""
    if force_n <= 0:
        raise ValueError("Compressive reference force must be positive")
    c = cylinder
    area = 2 * pi * c.radius_mm * c.thickness_mm
    stiffness = c.youngs_modulus_mpa * area / c.length_mm
    stress = force_n / area
    shortening = force_n / stiffness
    sigma_cr = (c.youngs_modulus_mpa / sqrt(3 * (1 - c.poisson_ratio ** 2))
                * c.thickness_mm / c.radius_mm)
    critical_load = area * sigma_cr
    volume_mm3 = area * c.length_mm
    mass_kg = volume_mm3 * 1e-9 * c.density_kg_m3
    return {
        "model": "ideal_thin_cylindrical_shell",
        "cylinder": asdict(c),
        "reference_force_n": force_n,
        "membrane_area_mm2": area,
        "axial_stiffness_n_per_mm": stiffness,
        "nominal_axial_stress_mpa": stress,
        "elastic_shortening_mm": shortening,
        "ideal_buckling_stress_mpa": sigma_cr,
        "ideal_buckling_load_n": critical_load,
        "ideal_mass_kg": mass_kg,
        "warning": "Analytical values are reference checks, not validated FEA collapse loads.",
    }
