"""Generate perfect + 12 validated STEP midsurfaces (requires OCP, NumPy, SciPy).

Use: python geometry/generate_all_dents.py (from software/)
STEP output is a surface, NOT a solid; assign 0.4 mm shell section in ANSYS.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "geometry"))

from aicira.cases import default_cases  # noqa: E402
from geometry import generate  # noqa: E402


def main() -> None:
    reports = [generate("perfect_cylinder.step", 0.0, 20.0)]
    for case in default_cases():
        reports.append(generate(f"parameter_variations/{case.case_id}_d{case.depth_mm:g}_w{case.axial_width_mm:g}.step",
                                case.depth_mm, case.axial_width_mm))
    verification = ROOT / "generated" / "verification"
    verification.mkdir(parents=True, exist_ok=True)
    (verification / "geometry.json").write_text(json.dumps(reports, indent=2))
    print(f"Validated and exported {len(reports)} STEP midsurfaces")


if __name__ == "__main__":
    main()
