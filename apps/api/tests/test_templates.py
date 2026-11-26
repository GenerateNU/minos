"""Tests that the real template files in templates/ load and match their specs.

CI runs these, so a broken template file blocks the pull request.
"""

from pathlib import Path

import pytest

from app.template import Template

TEMPLATES_DIR = Path(__file__).resolve().parents[3] / "templates"
TEMPLATE_FILES = sorted(TEMPLATES_DIR.glob("*.json"))


def test_the_templates_folder_has_at_least_one_template() -> None:
    assert TEMPLATE_FILES, f"no template files found in {TEMPLATES_DIR}"


@pytest.mark.parametrize("path", TEMPLATE_FILES, ids=lambda path: path.name)
def test_every_template_file_loads(path: Path) -> None:
    Template.model_validate_json(path.read_text())


def test_the_tl_template_matches_its_spec() -> None:
    template = Template.model_validate_json(
        (TEMPLATES_DIR / "tl-interview.json").read_text()
    )

    assert {c.id for c in template.criteria} == {
        "code_review",
        "scoping",
        "architecture",
        "walkthrough_depth",
        "member_ownership",
        "pressure_communication",
        "coachability",
    }
    assert [c.id for c in template.criteria if c.scope == "overall"] == ["coachability"]
    assert {name: f.total_minutes for name, f in template.formats.items()} == {
        "75": 75,
        "90": 90,
    }
