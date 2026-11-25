"""Tests for template validation, from docs/specs/01-template-schema.md.

Each test starts from one small valid template and breaks one thing.
Rejection tests check that the error names what is wrong, not only that
loading failed.
"""

from typing import Any

import pytest
from pydantic import ValidationError

from app.template import Template


def valid_template() -> dict[str, Any]:
    """Build a small valid template as it would look in a JSON file.

    Three sections (one of each type), one section scoped criterion, one
    overall criterion and one red flag. Minutes add up for both formats:
    75 is 10 + 35 + 30, and 90 is 10 + 40 + 40.

    Returns:
        A fresh template dict that each test can change freely.
    """
    anchors = {"1": "Not yet", "2": "Meets", "3": "Strong"}
    return {
        "id": "test-interview",
        "name": "Test interview",
        "version": 1,
        "formats": {"75": {"total_minutes": 75}, "90": {"total_minutes": 90}},
        "sections": [
            {
                "id": "warmup",
                "title": "Warm up",
                "type": "questions",
                "minutes": {"75": 10, "90": 10},
                "prompt": "Tell us about a project you are proud of.",
                "hints": [],
                "items": ["What would you change?"],
                "criterion_ids": [],
            },
            {
                "id": "sql",
                "title": "SQL",
                "type": "whiteboard",
                "minutes": {"75": 35, "90": 40},
                "prompt": "Find the top customer in each region.",
                "hints": ["Start with a GROUP BY.", "Think about window functions."],
                "items": [],
                "criterion_ids": ["query-design"],
            },
            {
                "id": "review",
                "title": "PR review",
                "type": "checklist",
                "minutes": {"75": 30, "90": 40},
                "prompt": "Review this pull request.",
                "hints": [],
                "items": ["Spots the missing test."],
                "criterion_ids": [],
            },
        ],
        "criteria": [
            {
                "id": "query-design",
                "title": "Query design",
                "anchors": dict(anchors),
                "scope": "sql",
            },
            {
                "id": "communication",
                "title": "Communication",
                "anchors": dict(anchors),
                "scope": "overall",
            },
        ],
        "red_flags": [
            {"id": "no-tests", "text": "Dismisses testing.", "section_id": "review"},
        ],
    }


def section(template: dict[str, Any], section_id: str) -> dict[str, Any]:
    """Find a section in a template dict by id.

    Args:
        template: The template dict.
        section_id: The id of the section to find.

    Returns:
        The section dict, which can be changed in place.
    """
    return next(s for s in template["sections"] if s["id"] == section_id)


def criterion(template: dict[str, Any], criterion_id: str) -> dict[str, Any]:
    """Find a criterion in a template dict by id.

    Args:
        template: The template dict.
        criterion_id: The id of the criterion to find.

    Returns:
        The criterion dict, which can be changed in place.
    """
    return next(c for c in template["criteria"] if c["id"] == criterion_id)


def error_text(error: ValidationError) -> str:
    """Turn a validation error into the text a template editor would read.

    Each problem becomes one line with where it is, what is wrong, and the
    bad value when it is a single value. The whole input is left out on
    purpose, so a test cannot pass just because an id appears in it.

    Args:
        error: The error raised while loading a template.

    Returns:
        One line per problem.
    """
    lines = []
    for problem in error.errors():
        where = ".".join(str(part) for part in problem["loc"])
        line = f"{where}: {problem['msg']}"
        if not isinstance(problem["input"], dict | list):
            line += f" (got {problem['input']!r})"
        lines.append(line)
    return "\n".join(lines)


def assert_rejected(template: dict[str, Any], *expected: str) -> None:
    """Check that a template is rejected with an error that names the problem.

    Args:
        template: The template dict to load.
        *expected: Pieces of text that must all appear in the error.
    """
    with pytest.raises(ValidationError) as caught:
        Template.model_validate(template)
    text = error_text(caught.value)
    for piece in expected:
        assert piece in text, f"expected {piece!r} in the error:\n{text}"


# A good template loads


def test_a_correct_template_loads() -> None:
    template = Template.model_validate(valid_template())

    assert [s.id for s in template.sections] == ["warmup", "sql", "review"]
    assert [c.id for c in template.criteria] == ["query-design", "communication"]


def test_a_template_with_no_scale_gets_the_default_scale() -> None:
    template = Template.model_validate(valid_template())

    assert [(level.value, level.label) for level in template.scale] == [
        (1, "Not yet"),
        (2, "Meets"),
        (3, "Strong"),
    ]


def test_a_template_with_every_kind_of_material_and_audience_loads() -> None:
    data = valid_template()
    section(data, "sql")["materials"] = [
        {
            "kind": "code",
            "label": "Starter query",
            "content": "SELECT * FROM orders;",
            "audience": "candidate",
        },
        {
            "kind": "image",
            "label": "Schema diagram",
            "url": "https://example.com/schema.png",
            "audience": "both",
        },
    ]
    section(data, "review")["materials"] = [
        {
            "kind": "link",
            "label": "PR to review",
            "url": "https://example.com/pr/1",
            "audience": "candidate",
        },
        {
            "kind": "file",
            "label": "Issue map",
            "url": "https://example.com/issues.pdf",
            "audience": "interviewer",
        },
    ]

    template = Template.model_validate(data)

    kinds = [m.kind for s in template.sections for m in s.materials]
    assert sorted(kinds) == ["code", "file", "image", "link"]


def test_a_template_where_both_formats_add_up_loads() -> None:
    template = Template.model_validate(valid_template())

    assert set(template.formats) == {"75", "90"}


def test_a_section_and_a_criterion_with_the_same_id_load() -> None:
    data = valid_template()
    criterion(data, "query-design")["id"] = "sql"
    section(data, "sql")["criterion_ids"] = ["sql"]

    template = Template.model_validate(data)

    assert "sql" in [c.id for c in template.criteria]


def test_a_red_flag_with_no_section_loads() -> None:
    data = valid_template()
    data["red_flags"].append({"id": "rude", "text": "Is rude to the interviewer."})

    template = Template.model_validate(data)

    assert [f.id for f in template.red_flags] == ["no-tests", "rude"]


# No two things of the same kind share an id


def test_two_sections_with_the_same_id_are_rejected() -> None:
    data = valid_template()
    section(data, "review")["id"] = "warmup"

    assert_rejected(data, "duplicate", "section", "warmup")


def test_two_criteria_with_the_same_id_are_rejected() -> None:
    data = valid_template()
    criterion(data, "communication")["id"] = "query-design"

    assert_rejected(data, "duplicate", "criterion", "query-design")


def test_two_red_flags_with_the_same_id_are_rejected() -> None:
    data = valid_template()
    data["red_flags"].append({"id": "no-tests", "text": "Skips edge cases."})

    assert_rejected(data, "duplicate", "red flag", "no-tests")


# The scale


def test_a_scale_with_a_gap_is_rejected() -> None:
    data = valid_template()
    data["scale"] = [
        {"value": 1, "label": "Not yet"},
        {"value": 2, "label": "Meets"},
        {"value": 4, "label": "Strong"},
    ]

    assert_rejected(data, "scale", "1, 2, 4")


def test_a_scale_out_of_order_is_rejected() -> None:
    data = valid_template()
    data["scale"] = [
        {"value": 3, "label": "Strong"},
        {"value": 1, "label": "Not yet"},
        {"value": 2, "label": "Meets"},
    ]

    assert_rejected(data, "scale", "3, 1, 2")


def test_a_scale_that_repeats_a_level_is_rejected() -> None:
    data = valid_template()
    data["scale"] = [
        {"value": 1, "label": "Not yet"},
        {"value": 2, "label": "Meets"},
        {"value": 2, "label": "Also meets"},
        {"value": 3, "label": "Strong"},
    ]

    assert_rejected(data, "scale", "1, 2, 2, 3")


def test_a_scale_with_only_one_level_is_rejected() -> None:
    data = valid_template()
    data["scale"] = [{"value": 1, "label": "Pass"}]

    assert_rejected(data, "scale", "at least 2")


# Every scale level has an anchor


def test_a_criterion_missing_an_anchor_for_a_level_is_rejected() -> None:
    data = valid_template()
    del criterion(data, "query-design")["anchors"]["3"]

    assert_rejected(data, "query-design", "level 3")


def test_a_criterion_with_an_anchor_for_a_level_not_on_the_scale_is_rejected() -> None:
    data = valid_template()
    criterion(data, "query-design")["anchors"]["4"] = "Exceptional"

    assert_rejected(data, "query-design", "level 4")


# Everything connects


def test_a_section_listing_a_criterion_that_does_not_exist_is_rejected() -> None:
    data = valid_template()
    section(data, "review")["criterion_ids"] = ["debugging"]

    assert_rejected(data, "review", "debugging", "does not exist")


def test_a_criterion_its_own_section_does_not_list_is_rejected() -> None:
    data = valid_template()
    section(data, "sql")["criterion_ids"] = []

    assert_rejected(data, "query-design", "sql", "not listed")


def test_a_criterion_listed_in_a_section_it_does_not_belong_to_is_rejected() -> None:
    data = valid_template()
    section(data, "review")["criterion_ids"] = ["query-design"]

    assert_rejected(data, "review", "query-design", "belongs to sql")


def test_an_overall_criterion_listed_in_a_section_is_rejected() -> None:
    data = valid_template()
    section(data, "warmup")["criterion_ids"] = ["communication"]

    assert_rejected(data, "warmup", "communication", "overall")


def test_a_criterion_scoped_to_a_section_that_does_not_exist_is_rejected() -> None:
    data = valid_template()
    criterion(data, "query-design")["scope"] = "stats"

    assert_rejected(data, "query-design", "stats", "does not exist")


def test_a_red_flag_pointing_to_a_section_that_does_not_exist_is_rejected() -> None:
    data = valid_template()
    data["red_flags"][0]["section_id"] = "stats"

    assert_rejected(data, "no-tests", "stats", "does not exist")


# Materials have what they need


def test_a_code_material_with_no_content_is_rejected() -> None:
    data = valid_template()
    section(data, "sql")["materials"] = [
        {"kind": "code", "label": "Starter query", "audience": "candidate"},
    ]

    assert_rejected(data, "Starter query", "content")


@pytest.mark.parametrize("kind", ["link", "image", "file"])
def test_a_link_image_or_file_material_with_no_url_is_rejected(kind: str) -> None:
    data = valid_template()
    section(data, "review")["materials"] = [
        {"kind": kind, "label": "PR to review", "audience": "candidate"},
    ]

    assert_rejected(data, "PR to review", "url")


# The times add up


def test_a_format_whose_section_minutes_do_not_add_up_is_rejected() -> None:
    data = valid_template()
    section(data, "review")["minutes"]["75"] = 25

    assert_rejected(data, "75", "70", "minutes")


def test_a_section_missing_minutes_for_a_format_is_rejected() -> None:
    data = valid_template()
    del section(data, "review")["minutes"]["90"]

    assert_rejected(data, "review", "90")


def test_a_section_with_minutes_for_a_format_that_does_not_exist_is_rejected() -> None:
    data = valid_template()
    section(data, "review")["minutes"]["60"] = 20

    assert_rejected(data, "review", "60")


# The template is not empty


def test_a_template_with_no_sections_is_rejected() -> None:
    data = valid_template()
    data["sections"] = []
    data["red_flags"] = []
    data["criteria"] = [criterion(data, "communication")]

    assert_rejected(data, "sections", "at least 1")


def test_a_template_with_no_criteria_is_rejected() -> None:
    data = valid_template()
    data["criteria"] = []
    section(data, "sql")["criterion_ids"] = []

    assert_rejected(data, "criteria", "at least 1")


# Unknown fields and values are rejected, not ignored


def test_a_typo_in_a_field_name_is_rejected() -> None:
    data = valid_template()
    review = section(data, "review")
    review["minuts"] = review.pop("minutes")

    assert_rejected(data, "minuts")


def test_an_unknown_section_type_is_rejected() -> None:
    data = valid_template()
    section(data, "warmup")["type"] = "essay"

    assert_rejected(data, "type", "essay")


def test_an_unknown_material_audience_is_rejected() -> None:
    data = valid_template()
    section(data, "sql")["materials"] = [
        {
            "kind": "code",
            "label": "Starter query",
            "content": "SELECT 1;",
            "audience": "everyone",
        },
    ]

    assert_rejected(data, "audience", "everyone")


def test_an_unknown_material_kind_is_rejected() -> None:
    data = valid_template()
    section(data, "sql")["materials"] = [
        {
            "kind": "video",
            "label": "Walkthrough",
            "url": "https://example.com/walkthrough.mp4",
            "audience": "candidate",
        },
    ]

    assert_rejected(data, "kind", "video")


# Errors list every problem


def test_a_template_with_several_problems_lists_all_of_them() -> None:
    data = valid_template()
    section(data, "review")["criterion_ids"] = ["debugging"]
    data["red_flags"][0]["section_id"] = "stats"
    section(data, "review")["minutes"]["75"] = 25

    assert_rejected(data, "debugging", "stats", "70")


def test_a_template_with_several_typos_lists_all_of_them() -> None:
    data = valid_template()
    data["nmae"] = data.pop("name")
    warmup = section(data, "warmup")
    warmup["promt"] = warmup.pop("prompt")

    assert_rejected(data, "nmae", "promt")


# JSON Schema


def test_json_schema_can_be_exported_from_the_template_model() -> None:
    schema = Template.model_json_schema()

    assert {"sections", "criteria", "red_flags", "scale"} <= set(schema["properties"])
