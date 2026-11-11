from __future__ import annotations

import json
import re
import subprocess
import tempfile
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
            try:
                ET.parse(diagram)
            except ET.ParseError as error:
                raise AssertionError(f"{repo}/{diagram}: invalid SVG XML: {error}") from error

    for repo in REPOS:
        token_path = ROOT / repo / "design" / "duck-ui.tokens.json"
        tokens = json.loads(token_path.read_text(encoding="utf-8"))
        assert tokens["schema_version"] == "2.1.0", (repo, tokens.get("schema_version"))
        experience = tokens.get("workspace_experience", {})
        assert experience.get("status") == "design_contract", repo
        for capability in ("material_surfaces", "adaptive_typography", "chromatic_context",
                           "adaptive_density", "timeline_and_undo", "privacy_and_sandbox"):
            assert capability in experience, (repo, capability)

        stylesheet = ROOT / repo / "assets" / "duck-ui" / "duck-ui.css"
        assert stylesheet.is_file(), f"{repo}: missing shared adaptive stylesheet"
        css = stylesheet.read_text(encoding="utf-8")
        for marker in (".duck-glass", ".duck-metal", ".duck-paper",
                       "prefers-reduced-motion", "duck-density-calm"):
            assert marker in css, (repo, marker)

        integration_doc = ROOT / repo / "docs" / "ADAPTIVE_WORKSPACE_INTEGRATION.md"
        assert integration_doc.is_file(), f"{repo}: missing adaptive workspace contract"

    registry = json.loads((ROOT / "Klipot" / "registry" / "ecosystem.json").read_text(encoding="utf-8"))
    registry_ids = {item["id"] for item in registry["projects"]}
    assert set(EXPECTED.values()).issubset(registry_ids), registry_ids
    assert len(registry_ids) == len(registry["projects"]), "registry contains duplicate project ids"
    extended_catalog = {"nun", "nunlauncher", "fragile-baby", "luci"}
    assert extended_catalog.issubset(registry_ids), registry_ids

    signal_schema_path = ROOT / "SAMBU" / "schemas" / "text-signal-envelope.schema.json"
    signal_fixture_path = ROOT / "SAMBU" / "examples" / "multilingual_signal_envelope.sample.json"
    signal_spec_path = ROOT / "SAMBU" / "docs" / "MULTILINGUAL_SIGNAL_PIPELINE.md"
    signal_schema = json.loads(signal_schema_path.read_text(encoding="utf-8"))
    signal_fixture = json.loads(signal_fixture_path.read_text(encoding="utf-8"))
    assert signal_schema["properties"]["schema_version"]["const"] == 1
    assert signal_schema["properties"]["raw_text_stored"]["const"] is False
    assert signal_fixture["schema_version"] == 1 and signal_fixture["raw_text_stored"] is False
    supported_scripts = set(signal_schema["$defs"]["representation"]["properties"]["script_profile"]["items"]["enum"])
    for representation in signal_fixture["representations"]:
        assert set(representation["script_profile"]).issubset(supported_scripts)
    signal_contract = registry["shared_contracts"]["multilingual_text_signal_v1"]
    assert signal_contract["version"] == 1 and signal_contract["metadata_only"] is True
    assert signal_contract["raw_text_embedded"] is False
    assert signal_spec_path.is_file()

    integration_docs = {
        "Kloz": "docs/UNICODE_BUFFER_BOUNDARY.md",
        "CO": "docs/SIGNAL_PIPELINE_LIFECYCLE.md",
        "SaintSI": "docs/SIGNAL_PIPELINE_ASSURANCE.md",
        "ReaperCripple": "docs/SEMANTIC_TELEMETRY_BOUNDARY.md",
        "ToolNG": "docs/LOCALIZED_SIGNAL_REPORTS.md",
        "Klipot": "docs/MULTILINGUAL_SIGNAL_CONTRACT.md",
    }
    for repo, relative_path in integration_docs.items():
        assert (ROOT / repo / relative_path).is_file(), f"{repo}: missing {relative_path}"

    portal = (ROOT / "Klipot" / "index.html").read_text(encoding="utf-8")
    assert 'src="assets/nun-mesh-overview.svg"' in portal
    portal_project_ids = set(re.findall(r'\{id:"([^"]+)",name:"', portal))
    expected_catalog = set(EXPECTED.values()) | {"nun", "nunlauncher", "fragile-baby", "luci"}
    assert portal_project_ids == expected_catalog, portal_project_ids
    assert 'id="workspace-density"' in portal and 'id="workspace-cycle"' in portal
    assert 'id="workspace-material"' in portal
    script_match = re.search(r"<script>(.*?)</script>", portal, re.DOTALL)
    assert script_match, "portal has no application script"
    with tempfile.NamedTemporaryFile(mode="w", suffix=".js", encoding="utf-8") as handle:
        handle.write(script_match.group(1))
        handle.flush()
        subprocess.run(["node", "--check", handle.name], check=True)
    for marker in ("project-grid", "arena-alloc", "co-start", "health-heartbeat", "gate-validate"):
        assert marker in portal, f"portal missing functional control: {marker}"
    print("NUN Mesh registry, manifests, localized README diagrams and portal controls are valid.")


if __name__ == "__main__":
    main()
