from __future__ import annotations

import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(".")
REPOS = ("Klipot", "Kloz", "CO", "SaintSI", "ReaperCripple", "SAMBU", "ToolNG")
EXPECTED = {
    "Klipot": "klipot",
    "Kloz": "kloz",
    "CO": "co",
    "SaintSI": "saintsi",
    "ReaperCripple": "reapercripple",
    "SAMBU": "sambu",
    "ToolNG": "toolng",
}


def readme_paths(repo: str) -> tuple[str, ...]:
    if repo in ("SAMBU", "ToolNG"):
        return ("README.md", "README.en.md", "README.ru.md")
    return ("README.md",)


def main() -> None:
    for repo in REPOS:
        base = ROOT / repo
        manifest_path = base / "ecosystem" / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        assert manifest["project_id"] == EXPECTED[repo], (repo, manifest.get("project_id"))

        for readme_name in readme_paths(repo):
            readme_path = base / readme_name
            body = readme_path.read_text(encoding="utf-8")
            assert "NUN Mesh" in body, f"{repo}/{readme_name}: missing mesh section"
            refs = re.findall(r'<img[^>]+src="([^"]+nun-mesh[^"]*\.svg)"', body)
            assert refs, f"{repo}/{readme_name}: missing local mesh diagram"
            for ref in refs:
                assert (base / ref).is_file(), f"{repo}/{readme_name}: missing {ref}"

        diagrams = list((base / "assets").glob("*nun-mesh*.svg"))
        assert diagrams, f"{repo}: no mesh SVG"
        for diagram in diagrams:
            ET.parse(diagram)

    registry = json.loads((ROOT / "Klipot" / "registry" / "ecosystem.json").read_text(encoding="utf-8"))
    registry_ids = {item["id"] for item in registry["projects"]}
    assert registry_ids == set(EXPECTED.values()), registry_ids

    portal = (ROOT / "Klipot" / "index.html").read_text(encoding="utf-8")
    for marker in ("project-grid", "arena-alloc", "co-start", "health-heartbeat", "gate-validate"):
        assert marker in portal, f"portal missing functional control: {marker}"
    print("NUN Mesh registry, manifests, localized README diagrams and portal controls are valid.")


if __name__ == "__main__":
    main()
