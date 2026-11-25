# Spec 00: v1 scope

## What it is

Minos is an interview scoring platform for the Data branch at Generate Northeastern. One interviewer runs each interview live from a template (timed parts, hints, rubric), scores the candidate, and the result goes to a scorecard that Chiefs compare across candidates. Interviews are recorded outside Minos and the session stores the recording link.

First use is TL interviews this spring (75 min, up to 90). Templates are generic so other interview types can be added later by adding a template, not by changing code.

Leaders rotate every semester, so optimize for readable, lean, easily maintained code.

## In

- Load and validate templates.
- Interviewer console: part timer for 75 or 90 min, hint cards revealed in order, notes, 1 to 3 score per criterion with a required one line evidence field, red flag toggles, recording link.
- One interviewer per session.
- Debrief scorecard per candidate: levels with evidence, total, red flags, what they did well, recording link, Chief decision.
- Candidate list per cycle with comparison across candidates and CSV export.
- Live shared whiteboard.
- Accounts created from invite links. Candidates use a link with no account.
- Raw event recording.
- Score distribution page per criterion (Chiefs only).

## Out

- Notion integration
- Written application scoring
- Other interview types in the UI
- AI summaries
- Automatic ranking
- Demographics or protected attributes
- Whiteboard cursors
- History and end to end encryption

## Users

- **Admins** (Chiefs): templates, candidates, cycles, all scores, calibration.
- **Leads** (TLs and PLs): run interviews.

Admins invite people with an expiring, single-use link, and the person creates their account from it. Leads run interviews, see only their own sessions, and create an expiring link for each candidate. There is no outside sign-in in v1.

## Success

One full 75 minute TL interview runs end to end with one interviewer and one live shared whiteboard, and results export cleanly.
