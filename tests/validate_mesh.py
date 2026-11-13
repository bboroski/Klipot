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




def _rgb(hex_color: str, label: str) -> tuple[float, float, float]:
    assert isinstance(hex_color, str) and re.fullmatch(r"#[0-9A-Fa-f]{6}", hex_color), (
        f"{label}: expected #RRGGBB, got {hex_color!r}"
    )
    return tuple(int(hex_color[index:index + 2], 16) / 255 for index in (1, 3, 5))


def _luminance(hex_color: str, label: str) -> float:
    channels = _rgb(hex_color, label)
    linear = tuple(
        channel / 12.92 if channel <= 0.04045 else ((channel + 0.055) / 1.055) ** 2.4
        for channel in channels
    )
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def _contrast_ratio(foreground: str, background: str, label: str) -> float:
    values = sorted(
        (_luminance(foreground, f"{label} foreground"),
         _luminance(background, f"{label} background")),
        reverse=True,
    )
    return (values[0] + 0.05) / (values[1] + 0.05)


def validate_accessibility_contract(repo: str, tokens: dict, css: str) -> None:
    """Check measurable accessibility, responsive and source-of-truth invariants."""
    colors = tokens.get("color", {})
    accessibility = tokens.get("accessibility", {})
    components = tokens.get("components", {})
    layout = tokens.get("layout", {})
    targets = tokens.get("targets", {})
    motion = tokens.get("motion_ms", {})
    behavior = tokens.get("behavior", {})

    text_threshold = float(accessibility.get("minimum_text_contrast_ratio", 4.5))
    assert text_threshold >= 4.5, (repo, "text contrast threshold must be at least WCAG AA 4.5:1")

    contrast_pairs = (
        ("primary text / canvas", colors["text"], colors["canvas"]),
        ("primary text / surface", colors["text"], colors["surface"]),
        ("secondary text / canvas", colors["text_secondary"], colors["canvas"]),
        ("secondary text / surface", colors["text_secondary"], colors["surface"]),
        ("muted text / canvas", colors["text_muted"], colors["canvas"]),
        ("muted text / surface", colors["text_muted"], colors["surface"]),
        ("primary action label", components["primary_button"]["foreground"],
         components["primary_button"]["background"]),
        ("secondary action label", components["secondary_button"]["foreground"],
         components["secondary_button"]["background"]),
        ("success status", colors["success"], colors["success_surface"]),
        ("warning status", colors["warning"], colors["warning_surface"]),
        ("danger status", colors["danger"], colors["danger_surface"]),
        ("information status", colors["info"], colors["info_surface"]),
    )
    for label, foreground, background in contrast_pairs:
        ratio = _contrast_ratio(foreground, background, f"{repo}: {label}")
        assert ratio >= text_threshold, (
            f"{repo}: {label} contrast {ratio:.2f}:1 is below {text_threshold:.1f}:1"
        )

    focus_threshold = float(accessibility.get("large_text_contrast_ratio", 3))
    for background_name in ("canvas", "surface"):
        ratio = _contrast_ratio(
            colors["focus"], colors[background_name], f"{repo}: focus / {background_name}"
        )
        assert ratio >= focus_threshold, (
            f"{repo}: focus indicator contrast {ratio:.2f}:1 is below {focus_threshold:.1f}:1"
        )

    required_flags = (
        "focus_visible_required",
        "keyboard_navigation_required",
        "status_requires_text_and_icon",
        "color_independent_state_cues",
        "high_contrast_mode_respected",
        "browser_zoom_supported",
    )
    for flag in required_flags:
        assert accessibility.get(flag) is True, (repo, f"accessibility.{flag} must be true")

    minimum_target = int(accessibility.get("minimum_touch_target_px", 44))
    assert minimum_target >= 44, (repo, "minimum touch target must be at least 44 px")
    assert int(targets.get("touch_hit_area_px", 0)) >= minimum_target, (
        repo, "touch hit area is below the declared minimum"
    )
    assert int(targets.get("recommended_hit_area_px", 0)) >= minimum_target, (
        repo, "recommended hit area is below the declared minimum"
    )
    assert int(components["primary_button"]["minimum_height_px"]) >= 40, (
        repo, "primary button must be at least 40 px high"
    )
    assert int(components["secondary_button"]["minimum_height_px"]) >= 40, (
        repo, "secondary button must be at least 40 px high"
    )

    mobile = int(layout["mobile_navigation_below_px"])
    secondary = int(layout["collapse_secondary_panels_below_px"])
    compact = int(layout["compact_navigation_below_px"])
    assert mobile < secondary < compact, (
        repo, "responsive breakpoints must progress from mobile to secondary collapse to compact navigation"
    )
    assert float(layout["ui_scale_min"]) <= float(layout["ui_scale_default"]) <= float(layout["ui_scale_max"]), (
        repo, "default UI scale must remain inside the supported range"
    )

    assert int(motion.get("reduced_motion", -1)) == 0, (
        repo, "reduced-motion duration must be zero"
    )
    assert behavior.get("animations_must_respect_reduced_motion") is True, (
        repo, "animations must respect reduced-motion preferences"
    )
    assert ":focus-visible" in css, (repo, "stylesheet must expose a visible keyboard focus style")
    assert "prefers-reduced-motion" in css, (repo, "stylesheet must implement reduced-motion behavior")

    # The JSON design tokens are authoritative; prevent CSS drift in the core palette.
    css_variables = {
        "--duck-canvas": "canvas",
        "--duck-surface": "surface",
        "--duck-yellow": "accent",
        "--duck-text": "text",
        "--duck-focus": "focus",
    }
    for variable, token_name in css_variables.items():
        match = re.search(
            rf"(?m)^\\s*{re.escape(variable)}\\s*:\\s*(#[0-9A-Fa-f]{{6}})\\s*;",
            css,
        )
        assert match, (repo, f"stylesheet is missing {variable}")
        assert match.group(1).upper() == colors[token_name].upper(), (
            repo, f"{variable} does not match design token color.{token_name}"
        )


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
        supported_token_versions = {"2.1.0", "3.0.0"}
        assert tokens.get("schema_version") in supported_token_versions, (
            repo, tokens.get("schema_version")
        )
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
        validate_accessibility_contract(repo, tokens, css)

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
