"""Inspect displacement-controlled ANSYS reaction histories without inventing peaks.

This module never solves FEA. It validates exported *converged* substep data.
Required CSV columns: shortening_mm, top_compression_N; optional time.
"""

import csv
import math
from pathlib import Path


def read_history(path: str | Path) -> list[dict]:
    with open(path, newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        required = {"shortening_mm", "top_compression_N"}
        if not reader.fieldnames or not required.issubset(set(reader.fieldnames)):
            raise ValueError(f"History must contain columns: {', '.join(sorted(required))}")
        rows = []
        for n, raw in enumerate(reader, start=2):
            try:
                item = {key: float(raw[key]) for key in required}
                if raw.get("time") not in (None, ""):
                    item["time"] = float(raw["time"])
            except (TypeError, ValueError, KeyError) as exc:
                raise ValueError(f"Non-numeric or missing history values at row {n}") from exc
            if not all(math.isfinite(x) for x in item.values()):
                raise ValueError(f"Non-finite value at row {n}")
            rows.append(item)
    return rows


def assess_history(rows: list[dict], target_mm: float = 1.6,
                   tolerance_mm: float = 1e-3) -> dict:
    if not rows:
        raise ValueError("No converged history rows")
    if target_mm <= 0 or tolerance_mm < 0:
        raise ValueError("Target must be positive and tolerance nonnegative")
    offsets = [r["shortening_mm"] for r in rows]
    forces = [r["top_compression_N"] for r in rows]
    if any(x < -tolerance_mm for x in offsets) or any(
            offsets[i] + tolerance_mm < offsets[i-1] for i in range(1, len(rows))):
        raise ValueError("Shortening history must be nonnegative and nondecreasing")
    if any(not math.isfinite(f) for f in forces):
        raise ValueError("Non-finite force")
    end = offsets[-1]
    completed = abs(end - target_mm) <= tolerance_mm
    idx = max(range(len(forces)), key=forces.__getitem__)
    # A recorded interior maximum is not enough unless later converged samples
    # confirm at least 1% load drop. Full target completion is tracked separately.
    postpeak = idx < len(forces) - 1 and min(forces[idx+1:]) <= 0.99 * forces[idx]
    validated_peak = bool(completed and postpeak)
    return {
        "n_converged_rows": len(rows),
        "last_shortening_mm": end,
        "target_shortening_mm": target_mm,
        "reached_target": completed,
        "observed_max_force_n": forces[idx],
        "observed_max_shortening_mm": offsets[idx],
        "observed_postpeak_drop_at_least_1pct": postpeak,
        "peak_eligible_for_comparison": validated_peak,
        "accepted_peak_force_n": forces[idx] if validated_peak else None,
        "note": ("History-based screening passed; mesh, stabilization and solver verification remain required."
                 if validated_peak else "Incomplete or no resolved postpeak; do not call observed force a collapse load."),
    }
