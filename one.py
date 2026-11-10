#!/usr/bin/env python3
"""One-knob control plane for the seven-repository SAMBU Mesh workspace."""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPOSITORIES = ("Kloz", "CO", "SaintSI", "ReaperCripple", "SAMBU", "ToolNG")
ASSETS = ("assets/nun-mesh-overview.svg", "assets/portal-ui-preview.svg")


def run(label: str, command: list[str], cwd: Path) -> None:
    print(f"\n==> {label}", flush=True)
    subprocess.run(command, cwd=cwd, check=True)


def local_check() -> None:
    for relative in ("sambu.module.json", "ecosystem/manifest.json", "registry/ecosystem.json", "registry/reaper-domain.json"):
        path = ROOT / relative
        json.loads(path.read_text(encoding="utf-8"))
        print(f"valid JSON: {relative}")
    for relative in ASSETS:
        if not (ROOT / relative).is_file():
            raise RuntimeError(f"Required portal asset is missing: {relative}")
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    for marker in ("project-grid", "arena-alloc", "co-start", "health-heartbeat", "gate-validate"):
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
                run(f"Validate portal JavaScript {index + 1}", [node, "--check", str(path)], ROOT)
    print("Klipot portal assets and control surface are valid.")


def workspace_check() -> None:
    workspace = ROOT.parent
    required = (ROOT.name, *REPOSITORIES)
    missing = [name for name in required if not (workspace / name).is_dir()]
    if missing:
        print("Cross-repository run skipped; missing sibling checkouts: " + ", ".join(missing))
        print("Local Klipot validation is complete. Place all seven repositories side by side to enable mesh mode.")
        return
    for name in REPOSITORIES:
        entry = workspace / name / "one.py"
        if not entry.is_file():
            raise RuntimeError(f"{name} is missing its one-knob entrypoint.")
        run(f"Verify repository {name}", [sys.executable, str(entry), "check"], workspace / name)
    validator = ROOT / "tests" / "validate_mesh.py"
    if validator.is_file():
        run("Validate manifests, cross-repository diagrams and shared contracts", [sys.executable, str(validator)], workspace)
    print("\nAll seven repository checks completed.")


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
