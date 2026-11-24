# Spec 01: template schema

Pydantic models are the source of truth. JSON Schema is exported from them.

## Models

- **Template**: id, name, version, scale (ordered levels with value and label, default 1 Not yet, 2 Meets, 3 Strong), formats (for example "75" and "90", each with total_minutes), sections, criteria, red_flags, bands.
- **Section**: id, title, type (`questions`, `whiteboard` or `checklist`), minutes (map from format to minutes), prompt, hints (ordered), items (checklist items or follow ups), criterion_ids, materials (optional list).
- **Material**: kind (`code`, `link`, `image` or `file`), label, content or url, audience (`candidate`, `interviewer` or `both`). Stimulus for a part, for example a code snippet to read or a PR link plus an interviewer only issue map. Items with audience `interviewer` are never returned by the candidate endpoint, and there is a test for that.
- **Criterion**: id, title, anchors (one description per scale level, all required), scope (a section id or `overall`).
- **Red flag**: id, text, optional section_id.
- **Band**: label, min_total.

## Validation

Validation fails at load and in CI.

1. All ids unique.
2. Every criterion has an anchor for every scale level.
3. Every `criterion_ids` entry exists. A section scoped criterion appears in that section's `criterion_ids` and nowhere else. `overall` criteria appear in no section and are scored once after the interview.
4. For each format, section minutes sum to `total_minutes`, and every section has minutes for every format.
5. Bands have no gaps and cover the possible total range.

## Snapshots

A session stores a snapshot of its template, so editing a template never changes past sessions.

## Part types

Only three part types in v1. Add one only when an interview truly cannot be expressed with these.
