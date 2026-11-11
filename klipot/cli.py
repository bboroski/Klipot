"""Command-line interface for Klipot's manifest and review planner."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

from . import __version__
from .consensus import ConsensusError, evaluate_consensus
from .planner import ManifestError, build_plan, validate_manifest


def _load(path: str):
    try:
        with Path(path).open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except OSError as exc:
        raise ManifestError(f"cannot read '{path}': {exc}") from exc
    except json.JSONDecodeError as exc:
        raise ManifestError(
            f"invalid JSON in '{path}' at line {exc.lineno}, "
            f"column {exc.colno}: {exc.msg}"
        ) from exc


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="klipot",
        description="Validate, plan, and assess evidence-linked ecosystem changes",
    )
    parser.add_argument(
        "--version", action="version", version=f"klipot {__version__}"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    validate_parser = subparsers.add_parser(
        "validate", help="validate a manifest and its capability graph"
    )
    validate_parser.add_argument("manifest")
    plan_parser = subparsers.add_parser(
        "plan", help="print a deterministic dependency-first plan"
    )
    plan_parser.add_argument("manifest")
    plan_parser.add_argument(
        "--json", action="store_true", help="emit machine-readable JSON"
    )
    consensus_parser = subparsers.add_parser(
        "consensus", help="evaluate a review record without merging or deploying"
    )
    consensus_parser.add_argument("review")
    consensus_parser.add_argument("--quorum-percent", type=int, default=60)
    consensus_parser.add_argument("--minimum-votes", type=int, default=1)
    args = parser.parse_args(argv)

    try:
        document = _load(args.review if args.command == "consensus" else args.manifest)
        if args.command == "validate":
            index = validate_manifest(document)
            print(
                f"valid: {len(index)} components; "
                "dependency and capability contracts resolved"
            )
            return 0
        if args.command == "consensus":
            result = evaluate_consensus(
                document.get("proposal_id") if isinstance(document, dict) else None,
                document.get("eligible_reviewers") if isinstance(document, dict) else None,
                document.get("votes") if isinstance(document, dict) else None,
                quorum_percent=args.quorum_percent,
                minimum_votes=args.minimum_votes,
            )
            print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
            return 0
        plan = build_plan(document)
        if args.json:
            print(json.dumps(plan, ensure_ascii=False, indent=2, sort_keys=True))
        else:
            print(f"Integration plan: {plan['system']}")
            for number, step in enumerate(plan["steps"], start=1):
                dependencies = ", ".join(step["depends_on"]) or "none"
                print(
                    f"{number:02d}. {step['id']} — {step['role']} "
                    f"(depends on: {dependencies})"
                )
        return 0
    except (ManifestError, ConsensusError) as exc:
        print(f"klipot: error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
