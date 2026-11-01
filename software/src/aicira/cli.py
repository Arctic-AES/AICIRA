"""CLI: python -m aicira baseline | cases | check-history FILE."""

import argparse
import csv
import json
from pathlib import Path

from .cases import case_manifest
from .fea import assess_history, read_history
from .physics import analytical_reference


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="aicira")
    sub = parser.add_subparsers(dest="command", required=True)
    base = sub.add_parser("baseline", help="Analytical reference for perfect cylinder")
    base.add_argument("--force", type=float, default=1000.0)
    cases = sub.add_parser("cases", help="Export perfect + twelve dent configurations")
    cases.add_argument("--output", type=Path, default=Path("cases.csv"))
    hist = sub.add_parser("check-history", help="Screen converged ANSYS force history")
    hist.add_argument("file", type=Path)
    hist.add_argument("--target", type=float, default=1.6)
    args = parser.parse_args(argv)
    if args.command == "baseline":
        result = analytical_reference(force_n=args.force)
    elif args.command == "cases":
        result = case_manifest()
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=list(result[0]))
            writer.writeheader()
            writer.writerows(result)
        result = {"created": str(args.output), "count": len(result)}
    else:
        result = assess_history(read_history(args.file), target_mm=args.target)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
