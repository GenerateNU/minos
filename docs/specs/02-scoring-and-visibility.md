# Spec 02: scoring and visibility

## Scoring

- One interviewer per session. There is no averaging and no per criterion agreement check.
- The interviewer scores each criterion. A non empty evidence line is required.
- Total is the sum of the levels. Band is the band with the highest `min_total` that is less than or equal to the total.

## Red flags and decision

- The interviewer can toggle a red flag with a note. A session with any red flag shows "Needs discussion" instead of a band.
- The final decision (Strong, Maybe, Not yet) is entered by a Chief with a short rationale, separate from the computed band.

## Visibility

- An interviewer sees only sessions they ran. Chiefs see every session.
- Submitting locks the scores. A Chief can unlock, and the unlock is recorded.
- Enforced server side in the policy module with tests. The UI hides data too.

## What they do well

The interviewer writes one line for "what this candidate does well" before submitting. The scorecard shows it.

Status: Proposed, from the principles in the [UI spec](04-ui-and-style.md). Confirm before building.

## Recording

The session has an optional `recording_url`, set by the interviewer. Minos stores the link only, with no upload or playback. It appears in the console and scorecard and is included in exports.

## Fairness across interviewers

Chiefs only: average total and level distribution per interviewer, so a lenient or harsh scorer is visible. Re-scoring a sample from recordings to calibrate is a later idea, not v1.

## Events

Recorded with timestamp, session and interviewer:

- `part_started`
- `part_ended`
- `hint_revealed`
- `score_submitted`
- `score_unlocked`
- `red_flag_toggled`

## Retention

Candidate data is deleted after a configurable period (default: end of the cycle). Aggregate counts can remain.
