# Spec 04: UI and style

Wireframes are in the Minos Wireframes canvas (link in [docs/design/README.md](../design/README.md)). They are sketches. Follow the structure, not the pixels.

## Principles

- **Calm to run live.** No clutter, no surprises and no wasted clicks mid interview.
- **Kind to candidates.** Interviewers are often students scoring other students. The candidate view stays kind and clear.
- **The scorecard notes strengths.** It records what a candidate does well, not only what went wrong.
- Small touches of delight are fine when they don't cost clarity.

## Direction

Greek editorial. Warm paper background, serif headings, mono labels, thin rules instead of heavy cards, square corners except arch shaped score tiles. One decorative motif: a Greek key rule, used sparingly.

## Palette A

Tokens live in one place, as CSS variables.

| Token | Hex | Use |
|---|---|---|
| paper | #F3EEE4 | background |
| ink | #1F1B16 | text |
| clay | #B5502F | primary action, red flag |
| olive | #6B7048 | Strong |
| rule | #D8CFBF | rules and dividers |

Do not rely on red and green. Distinguish states with weight, outline and numerals.

## Type

- Newsreader: headings and prompts
- Public Sans: body
- IBM Plex Mono: labels and numbers

Confirm before adding fonts.

## Scores

Scores are shown as Roman numerals I, II, III with the label (Not yet, Meets, Strong). The anchor text for the selected level is always visible beside the score.

## Interviewer console: pillar and tray

- A vertical pillar on the left lists sections as Roman numeral chapters with planned versus actual minutes.
- The main column shows the current part.
- A tray pinned to the bottom holds the score tiles for the current criterion, the red flags and submit. Overall criteria are scored last in the tray.

The console must be calm to run live: no modals mid interview, no layout shift when a hint is revealed, targets at least 44px, usable on a laptop in a video call.

## Debrief scorecard

Reads like one printed page: criteria down the page with level, evidence and anchor, then totals, red flags, what they did well, recording link and the Chief decision.

## Candidate view

Same palette, but shows no scores, rubric, hints or timer targets. Prompt, candidate materials and the whiteboard only.

## Templates drive everything

The shell never contains TL specific text. The same console renders the member interview template with no code change, and the web app has a test that renders both.
