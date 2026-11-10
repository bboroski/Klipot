from __future__ import annotations

import json
import re
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(".")
REPOS = ("Klipot", "Kloz", "CO", "SaintSI", "ReaperCripple", "SAMBU", "ToolNG", "NUN", "NUNLauncher")
SPECIFICATION_ONLY = {"NUN", "NUNLauncher"}
EXPECTED = {
    "Klipot": "klipot",
    "Kloz": "kloz",
    "CO": "co",
    "SaintSI": "saintsi",
    "ReaperCripple": "reapercripple",
    "SAMBU": "sambu",
    "ToolNG": "toolng",
    "NUN": "nun",
    "NUNLauncher": "nunlauncher",
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

        module = json.loads((base / "sambu.module.json").read_text(encoding="utf-8"))
        policy = json.loads((base / "ecosystem" / "update-policy.json").read_text(encoding="utf-8"))
        assert module["repository"] == f"bboroski/{repo}"
        assert module["schema_version"] == 1 and module["ecosystem"] == "SAMBU"
        assert module["module_id"] == policy["module_id"]
        assert policy["repository"] == f"bboroski/{repo}"
        assert policy["updates"]["delivery"] == "pull-request-only"
        assert policy["updates"]["automatic_merge"] is False
        assert policy["updates"]["automatic_installation"] is False
        assert policy["updates"]["require_ci"] is True

        for readme_name in readme_paths(repo):
            readme_path = base / readme_name
            body = readme_path.read_text(encoding="utf-8")
            if repo in SPECIFICATION_ONLY:
                assert "Багатошарова автономність" in body, f"{repo}/{readme_name}: missing layered integration section"
                assert "Оновлення та відновлення" in body, f"{repo}/{readme_name}: missing update and recovery section"
                assert "специфікац" in body.lower(), f"{repo}/{readme_name}: implementation maturity must be explicit"
                continue
            assert "NUN Mesh" in body, f"{repo}/{readme_name}: missing mesh section"
            refs = re.findall(r'<img[^>]+src="([^"]+nun-mesh[^"]*\.svg)"', body)
            assert refs, f"{repo}/{readme_name}: missing local mesh diagram"
            for ref in refs:
                assert (base / ref).is_file(), f"{repo}/{readme_name}: missing {ref}"

        if repo not in SPECIFICATION_ONLY:
            diagrams = list((base / "assets").glob("*nun-mesh*.svg"))
            assert diagrams, f"{repo}: no mesh SVG"
            for diagram in diagrams:
                ET.parse(diagram)

    registry = json.loads((ROOT / "Klipot" / "registry" / "ecosystem.json").read_text(encoding="utf-8"))
    registry_ids = {item["id"] for item in registry["projects"]}
    assert registry_ids == set(EXPECTED.values()), registry_ids

    canonical = json.loads((ROOT / "SAMBU" / "ecosystem" / "registry.json").read_text(encoding="utf-8"))
    canonical_ids = {item["id"] for item in canonical["modules"]}
    policy_ids = {
        json.loads((ROOT / repo / "ecosystem" / "update-policy.json").read_text(encoding="utf-8"))["module_id"]
        for repo in REPOS
    }
    assert canonical_ids == policy_ids, (canonical_ids, policy_ids)
    assert canonical["governance"]["updates"]["automatic_merge"] is False
    assert canonical["governance"]["updates"]["automatic_installation"] is False

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
    script_match = re.search(r"<script>(.*?)</script>", portal, re.DOTALL)
    assert script_match, "portal has no application script"
    with tempfile.NamedTemporaryFile(mode="w", suffix=".js", encoding="utf-8") as handle:
        handle.write(script_match.group(1))
        handle.flush()
        subprocess.run(["node", "--check", handle.name], check=True)
    for marker in ("project-grid", "arena-alloc", "co-start", "health-heartbeat", "gate-validate"):
        assert marker in portal, f"portal missing functional control: {marker}"
    print("NUN Mesh registry, nine module manifests, update policies, contracts and portal controls are valid.")


if __name__ == "__main__":
    main()
