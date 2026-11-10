#!/usr/bin/env python3
"""One-knob control plane for the eleven-repository SAMBU Mesh workspace."""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import webbrowser
from pathlib import Path

from klipot.uncertainty import build_resolution_plan, build_workspace_plan

ROOT = Path(__file__).resolve().parent
REPOSITORIES = (
    "SAMBU", "ToolNG", "ReaperCripple", "Kloz", "CO", "SaintSI",
    "NUN", "NUNLauncher", "Fragile-Baby", "Luci",
)
ASSETS = ("assets/nun-mesh-overview.svg", "assets/portal-ui-preview.svg")


def run(label: str, command: list[str], cwd: Path) -> None:
    print(f"\n==> {label}", flush=True)
    subprocess.run(command, cwd=cwd, check=True)


def local_check() -> None:
    for relative in (
        "sambu.module.json",
        "ecosystem/manifest.json",
        "registry/ecosystem.json",
        "registry/uncertainties.json",
        "ecosystem/uncertainty.json",
    ):
        path = ROOT / relative
        json.loads(path.read_text(encoding="utf-8"))
        print(f"valid JSON: {relative}")

    registry = json.loads(
        (ROOT / "registry" / "uncertainties.json").read_text(encoding="utf-8")
    )
    plan = build_resolution_plan(registry)
    local_registry = json.loads(
        (ROOT / "ecosystem" / "uncertainty.json").read_text(encoding="utf-8")
    )
    local_plan = build_resolution_plan(local_registry)
    print(
        "central uncertainty registry: "
        f"{plan['total']} items "
        f"({plan['counts']['open']} open, "
        f"{plan['counts']['resolved']} resolved, "
        f"{plan['counts']['blocked']} blocked)"
    )
    print(f"Klipot local uncertainty items: {local_plan['total']}")

    for relative in ASSETS:
        if not (ROOT / relative).is_file():
            raise RuntimeError(f"Required portal asset is missing: {relative}")
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    for marker in (
        "project-grid", "arena-alloc", "co-start",
        "health-heartbeat", "gate-validate",
    ):
        if marker not in html:
            raise RuntimeError(f"Portal control marker is missing: {marker}")
    scripts = re.findall(r"<script[^>]*>(.*?)</script>", html, flags=re.DOTALL)
    if not scripts:
        raise RuntimeError("The portal has no inline application script.")
    node = shutil.which("node")
    if node:
        import tempfile
        with tempfile.TemporaryDirectory(prefix="klipot-one-") as directory:
            for index, source in enumerate(scripts):
                path = Path(directory) / f"portal-{index}.js"
                path.write_text(source, encoding="utf-8")
                run(
                    f"Validate portal JavaScript {index + 1}",
                    [node, "--check", str(path)],
                    ROOT,
                )
    run(
        "Run Klipot unit tests",
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
        ROOT,
    )
    print("Klipot portal assets, contracts, uncertainty registry and tests are valid.")


def workspace_check() -> None:
    workspace = ROOT.parent
    repositories = (ROOT.name, *REPOSITORIES)
    missing = [name for name in repositories if not (workspace / name).is_dir()]
    if missing:
        print(
            "Cross-repository run skipped; missing sibling checkouts: "
            + ", ".join(missing)
        )
        print("Local Klipot validation is complete.")
        return

    registry_documents = []
    for name in repositories:
        repository_root = ROOT if name == ROOT.name else workspace / name
        registry_path = repository_root / "ecosystem" / "uncertainty.json"
        if not registry_path.is_file():
            raise RuntimeError(f"{name} has no ecosystem/uncertainty.json registry.")
        registry_documents.append(
            json.loads(registry_path.read_text(encoding="utf-8"))
        )

    workspace_plan = build_workspace_plan(registry_documents)
    print(
        "\nWorkspace uncertainty plan: "
        f"{workspace_plan['repository_count']} repositories, "
        f"{workspace_plan['total']} items; "
        f"{workspace_plan['counts']['open']} open, "
        f"{workspace_plan['counts']['resolved']} resolved, "
        f"{workspace_plan['counts']['blocked']} blocked."
    )
    print(
        "Implementation states: "
        f"{workspace_plan['implementation_counts']['planned']} planned, "
        f"{workspace_plan['implementation_counts']['implemented']} implemented, "
        f"{workspace_plan['implementation_counts']['verified']} verified."
    )

    for name in REPOSITORIES:
        entry = workspace / name / "one.py"
        if not entry.is_file():
            raise RuntimeError(f"{name} is missing its one-knob entrypoint.")
        run(
            f"Verify repository {name}",
            [sys.executable, str(entry), "check"],
            workspace / name,
        )

    validator = ROOT / "tests" / "validate_mesh.py"
    if validator.is_file():
        run(
            "Validate manifests, cross-repository diagrams and shared contracts",
            [sys.executable, str(validator)],
            workspace,
        )
    print("\nAll eleven repository checks completed.")


def check() -> None:
    local_check()
    workspace_check()


def main() -> int:
    parser = argparse.ArgumentParser(description="Klipot one-knob mesh launcher.")
    parser.add_argument("command", nargs="?", choices=("check", "run"), default="run")
    args = parser.parse_args()
    try:
        check()
        if args.command == "run":
            target = (ROOT / "index.html").resolve().as_uri()
            opened = webbrowser.open(target)
            print(f"\nPortal: {target}")
            if not opened:
                print("Open the portal URL above in a browser.")
    except (OSError, ValueError, subprocess.CalledProcessError, RuntimeError) as exc:
        print(f"Klipot one-knob failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
