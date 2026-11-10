#!/usr/bin/env python3
"""Print the deterministic uncertainty-to-feature plan for this ecosystem."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from klipot.uncertainty import UncertaintyError, build_resolution_plan  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = parser.parse_args()
    try:
        registry = json.loads(
            (ROOT / "registry" / "uncertainties.json").read_text(encoding="utf-8")
        )
        plan = build_resolution_plan(registry)
    except (OSError, json.JSONDecodeError, UncertaintyError) as exc:
        print(f"uncertainty report failed: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(plan, indent=2, ensure_ascii=False))
    else:
        print(f"{plan['repository']}: {plan['total']} uncertainty items")
        for item in plan["actions"]:
            print(
                f"- [{item['status']}] {item['id']}: "
                f"{item['feature']} -> {item['next_step']}"
            )
        print("Unknown facts remain unknown until evidence is supplied.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
