"""Deterministic Gaussian dent definitions for the 12-case baseline study."""

from dataclasses import asdict, dataclass
from math import atan2, cos, exp, pi, sin

from .physics import Cylinder

DEPTHS_MM = (0.02, 0.04, 0.08, 0.12)
WIDTHS_MM = (10.0, 20.0, 40.0)


@dataclass(frozen=True)
class Dent:
    case_id: str
    depth_mm: float
    axial_width_mm: float
    circumferential_width_mm: float
    center_z_mm: float = 225.0
    center_theta_rad: float = 0.0

    def __post_init__(self) -> None:
        if self.depth_mm < 0 or min(self.axial_width_mm, self.circumferential_width_mm) <= 0:
            raise ValueError("Dent depth cannot be negative; widths must be positive")

    def radius_at(self, theta_rad: float, z_mm: float, radius_mm: float = 75.0) -> float:
        """Periodic inward dent radial coordinate, measured on shell midsurface."""
        delta_theta = atan2(sin(theta_rad - self.center_theta_rad),
                            cos(theta_rad - self.center_theta_rad))
        arc_mm = radius_mm * delta_theta
        exponent = -0.5 * ((z_mm - self.center_z_mm) / self.axial_width_mm) ** 2
        exponent -= 0.5 * (arc_mm / self.circumferential_width_mm) ** 2
        return radius_mm - self.depth_mm * exp(exponent)


def default_cases() -> list[Dent]:
    return [Dent(f"I{i:02d}", depth, width, width)
            for i, (depth, width) in enumerate(
                ((d, w) for d in DEPTHS_MM for w in WIDTHS_MM), start=1)]


def case_manifest(cylinder: Cylinder = Cylinder()) -> list[dict]:
    rows = [{"case_id": "P00", "kind": "perfect", "depth_mm": 0.0,
             "axial_width_mm": None, "circumferential_width_mm": None,
             "center_z_mm": None, "center_theta_rad": None,
             "thickness_mm": cylinder.thickness_mm, "status": "not_run"}]
    for c in default_cases():
        rows.append({**asdict(c), "kind": "gaussian_dent",
                     "thickness_mm": cylinder.thickness_mm, "status": "not_run"})
    return rows
