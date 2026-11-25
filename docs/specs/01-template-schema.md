# Spec 01: template schema

Pydantic models are the source of truth. JSON Schema is exported from them.

## Models

- **Template**: id, name, version, scale (ordered levels with value and label, default 1 Not yet, 2 Meets, 3 Strong), formats (for example "75" and "90", each with total_minutes), sections, criteria, red_flags.
- **Section**: id, title, type (`questions`, `whiteboard` or `checklist`), minutes (map from format to minutes), prompt, hints (ordered), items (checklist items or follow ups), criterion_ids, materials (optional list).
- **Material**: kind (`code`, `link`, `image` or `file`), label, content or url (`code` needs content; `link`, `image` and `file` need url), audience (`candidate`, `interviewer` or `both`). Stimulus for a part, for example a code snippet to read or a PR link plus an interviewer only issue map. Items with audience `interviewer` are never returned by the candidate endpoint, and there is a test for that.
- **Criterion**: id, title, anchors (one description per scale level, all required), scope (a section id or `overall`).
- **Red flag**: id, text, optional section_id. If set, section_id must name a real section.

## Shape

How the template looks in its JSON file:

- `scale` is a list of levels, each with `value` and `label`. Leave it out to get the default.
- `formats` maps a format name to its `total_minutes`.
- A section's `minutes` maps each format name to that section's minutes.
- A criterion's `anchors` maps each scale value to its description. JSON keys are strings, so level 1 is `"1"`.
- `hints`, `items`, `criterion_ids`, `materials` and `red_flags` can be left out and default to empty lists.

A small example with one section:

```json
{
  "id": "example",
  "name": "Example interview",
  "version": 1,
  "scale": [
    {"value": 1, "label": "Not yet"},
    {"value": 2, "label": "Meets"},
    {"value": 3, "label": "Strong"}
  ],
  "formats": {
    "75": {"total_minutes": 75},
    "90": {"total_minutes": 90}
  },
  "sections": [
    {
      "id": "sql",
      "title": "SQL",
      "type": "whiteboard",
      "minutes": {"75": 75, "90": 90},
      "prompt": "Find the top customer in each region.",
      "hints": ["Start with a GROUP BY."],
      "criterion_ids": ["query-design"],
      "materials": [
        {
          "kind": "code",
          "label": "Starter query",
          "content": "SELECT * FROM orders;",
          "audience": "candidate"
        }
      ]
    }
  ],
  "criteria": [
    {
      "id": "query-design",
      "title": "Query design",
      "anchors": {
        "1": "Can't get a working query",
        "2": "Correct query with a GROUP BY",
        "3": "Correct, explains the tradeoffs and edge cases"
      },
      "scope": "sql"
    }
  ],
  "red_flags": [
    {"id": "guesses", "text": "Guesses instead of saying not sure", "section_id": "sql"}
  ]
}
```

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
