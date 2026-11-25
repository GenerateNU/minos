"""Interview template models and validation, from docs/specs/01-template-schema.md.

The Pydantic models are the source of truth for the template format. Field
level problems (missing fields, typos, unknown values) are caught by Pydantic.
Problems that need the whole template (ids, references, minutes, anchors) are
collected by Template.check_whole_template and reported together.
"""

from collections import Counter
from typing import Literal, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class StrictModel(BaseModel):
    """Base for every template model. Unknown fields are rejected, not ignored."""

    model_config = ConfigDict(extra="forbid")


class Level(StrictModel):
    """One level of the scoring scale, for example 2 Meets."""

    value: int
    label: str


def default_scale() -> list[Level]:
    """Build the default scale used when a template does not set one.

    Returns:
        The levels 1 Not yet, 2 Meets and 3 Strong.
    """
    return [
        Level(value=1, label="Not yet"),
        Level(value=2, label="Meets"),
        Level(value=3, label="Strong"),
    ]


class Format(StrictModel):
    """An interview length, for example the 75 minute version."""

    total_minutes: int


class Material(StrictModel):
    """Stimulus for a section, such as a code snippet or a PR link."""

    kind: Literal["code", "link", "image", "file"]
    label: str
    content: str | None = None
    url: str | None = None
    audience: Literal["candidate", "interviewer", "both"]

    @model_validator(mode="after")
    def check_content_or_url(self) -> Self:
        """Check that a material has what its kind needs.

        Returns:
            The material, unchanged.

        Raises:
            ValueError: If a code material has no content, or any other
                material has no url.
        """
        if self.kind == "code" and not self.content:
            raise ValueError(f"code material {self.label!r} needs content")
        if self.kind != "code" and not self.url:
            raise ValueError(f"{self.kind} material {self.label!r} needs a url")
        return self


class Section(StrictModel):
    """One part of the interview."""

    id: str
    title: str
    type: Literal["questions", "whiteboard", "checklist"]
    minutes: dict[str, int]
    prompt: str
    hints: list[str] = Field(default_factory=list)
    items: list[str] = Field(default_factory=list)
    criterion_ids: list[str] = Field(default_factory=list)
    materials: list[Material] = Field(default_factory=list)


class Criterion(StrictModel):
    """Something the interviewer scores, with a description for each level."""

    id: str
    title: str
    anchors: dict[int, str]
    scope: str


class RedFlag(StrictModel):
    """A warning sign the interviewer can toggle, optionally tied to a section."""

    id: str
    text: str
    section_id: str | None = None


class Template(StrictModel):
    """A whole interview template, as loaded from a JSON file."""

    id: str
    name: str
    version: int
    scale: list[Level] = Field(default_factory=default_scale, min_length=2)
    formats: dict[str, Format]
    sections: list[Section] = Field(min_length=1)
    criteria: list[Criterion] = Field(min_length=1)
    red_flags: list[RedFlag] = Field(default_factory=list)

    @model_validator(mode="after")
    def check_whole_template(self) -> Self:
        """Run every check that needs the whole template, and report them all.

        Returns:
            The template, unchanged.

        Raises:
            ValueError: If any check fails. The message has one line per
                problem.
        """
        problems = [
            *duplicate_ids(self),
            *scale_problems(self),
            *anchor_problems(self),
            *reference_problems(self),
            *minutes_problems(self),
        ]
        if problems:
            raise ValueError("\n".join(problems))
        return self


def duplicate_ids(template: Template) -> list[str]:
    """Find ids used twice within one kind.

    Args:
        template: The template to check.

    Returns:
        One message per duplicated id.
    """
    kinds = {
        "section": [s.id for s in template.sections],
        "criterion": [c.id for c in template.criteria],
        "red flag": [f.id for f in template.red_flags],
    }
    return [
        f"duplicate {kind} id {id_}"
        for kind, ids in kinds.items()
        for id_, count in Counter(ids).items()
        if count > 1
    ]


def scale_problems(template: Template) -> list[str]:
    """Check that scale values count up by one with no gaps or repeats.

    Args:
        template: The template to check.

    Returns:
        A message if the scale is wrong, otherwise nothing.
    """
    values = [level.value for level in template.scale]
    expected = list(range(values[0], values[0] + len(values)))
    if values == expected:
        return []
    shown = ", ".join(str(v) for v in values)
    return [f"scale levels must count up by one with no gaps or repeats, got {shown}"]


def anchor_problems(template: Template) -> list[str]:
    """Check that every criterion has an anchor for exactly the scale levels.

    Args:
        template: The template to check.

    Returns:
        One message per missing or extra anchor.
    """
    levels = {level.value for level in template.scale}
    problems = []
    for c in template.criteria:
        for value in sorted(levels - c.anchors.keys()):
            problems.append(f"criterion {c.id} has no anchor for level {value}")
        for value in sorted(c.anchors.keys() - levels):
            problems.append(
                f"criterion {c.id} has an anchor for level {value}, "
                "which is not on the scale"
            )
    return problems


def reference_problems(template: Template) -> list[str]:
    """Check that sections, criteria and red flags point at things that exist.

    Args:
        template: The template to check.

    Returns:
        One message per broken or misplaced reference.
    """
    sections = {s.id: s for s in template.sections}
    criteria = {c.id: c for c in template.criteria}
    problems = []

    for s in template.sections:
        for criterion_id in s.criterion_ids:
            c = criteria.get(criterion_id)
            if c is None:
                problems.append(
                    f"section {s.id} lists criterion {criterion_id}, "
                    "which does not exist"
                )
            elif c.scope == "overall":
                problems.append(
                    f"section {s.id} lists criterion {c.id}, which is scored "
                    "overall and belongs in no section"
                )
            elif c.scope != s.id:
                problems.append(
                    f"section {s.id} lists criterion {c.id}, which belongs to {c.scope}"
                )

    for c in template.criteria:
        if c.scope == "overall":
            continue
        home = sections.get(c.scope)
        if home is None:
            problems.append(
                f"criterion {c.id} is scoped to section {c.scope}, which does not exist"
            )
        elif c.id not in home.criterion_ids:
            problems.append(
                f"criterion {c.id} belongs to section {c.scope} "
                "but is not listed in its criterion_ids"
            )

    for f in template.red_flags:
        if f.section_id is not None and f.section_id not in sections:
            problems.append(
                f"red flag {f.id} points to section {f.section_id}, "
                "which does not exist"
            )

    return problems


def minutes_problems(template: Template) -> list[str]:
    """Check section minutes against the template's formats.

    Args:
        template: The template to check.

    Returns:
        One message per missing or unknown format, and per format whose
        section minutes do not add up to its total.
    """
    formats = template.formats.keys()
    problems = []
    for s in template.sections:
        for name in sorted(formats - s.minutes.keys()):
            problems.append(f"section {s.id} has no minutes for format {name}")
        for name in sorted(s.minutes.keys() - formats):
            problems.append(
                f"section {s.id} has minutes for format {name}, "
                "which the template does not define"
            )
    for name, fmt in template.formats.items():
        total = sum(s.minutes.get(name, 0) for s in template.sections)
        if total != fmt.total_minutes:
            problems.append(
                f"format {name}: sections add up to {total} minutes, "
                f"expected {fmt.total_minutes}"
            )
    return problems
