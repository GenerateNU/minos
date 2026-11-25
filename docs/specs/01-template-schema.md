# Spec 01: template schema

Pydantic models are the source of truth. JSON Schema is exported from them.

## Models

- **Template**: id, name, version, scale (ordered levels with value and label, default 1 Not yet, 2 Meets, 3 Strong), formats (for example "75" and "90", each with total_minutes), sections, criteria, red_flags.
- **Section**: id, title, type (`questions`, `whiteboard` or `checklist`), minutes (map from format to minutes), prompt, hints (ordered), items (checklist items or follow ups), criterion_ids, materials (optional list).
- **Material**: kind (`code`, `link`, `image` or `file`), label, content or url (`code` needs content; `link`, `image` and `file` need url), audience (`candidate`, `interviewer` or `both`). Stimulus for a part, for example a code snippet to read or a PR link plus an interviewer only issue map. Items with audience `interviewer` are never returned by the candidate endpoint, and there is a test for that.
- **Criterion**: id, title, anchors (one description per scale level, all required), scope (a section id or `overall`).
- **Red flag**: id, text, optional section_id. If set, section_id must name a real section.

## Validation

Validation fails at load and in CI.

1. Ids are unique within each kind. Two sections cannot share an id, but a section and a criterion can.
2. The scale has at least two levels, and its values count up by one with no gaps or repeats (1, 2, 3 is fine; 1, 2, 4 and 3, 1, 2 are not).
3. Every criterion has an anchor for every scale level, and none for a level that is not on the scale.
4. Every `criterion_ids` entry exists. A section scoped criterion appears in that section's `criterion_ids` and nowhere else. `overall` criteria appear in no section and are scored once after the interview.
5. A criterion's scope and a red flag's section_id, when set, name a real section.
6. For each format, section minutes sum to `total_minutes`, every section has minutes for every format, and no section has minutes for a format the template does not define.
7. A `code` material has content. A `link`, `image` or `file` material has a url.
8. A template has at least one section and at least one criterion.
9. Unknown fields (for example a typo like `minuts`) and unknown values (for example section type `essay`, audience `everyone` or material kind `video`) are rejected, not ignored.

When a template has several problems, the error lists all of them. Each message names the section, criterion, red flag or field it is about.

## Snapshots

A session stores a snapshot of its template, so editing a template never changes past sessions.

## Part types

Only three part types in v1. Add one only when an interview truly cannot be expressed with these.
