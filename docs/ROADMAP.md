# Roadmap

Already done: repo setup, specs, the Socratic tutor skill, the API and web app skeletons, CI, local Postgres (Docker) and migrations with Neon for the deployed database, and template validation.

## Milestone: MVP for Chief testing

In:

- Template validation and the TL template
- Scoring
- Sessions API
- Interviewer console
- Debrief scorecard
- Live shared whiteboard, with candidate session links
- Invite links, with everyone as admin for now
- Deploy

Deferred until after testing:

- Lead role and visibility rules
- Candidate list
- CSV export and score distribution

Order: finish template validation, then a throwaway spike of the whiteboard relay (kept off main, with a short report on what we learned), then continue with the rest.

## Now

- The TL template, with a test that every template file loads

## Next

- Scoring (adding up levels), tests first
- Score visibility rules, tests first
- Sessions, scores and events in the API, with the generated TypeScript client
- A throwaway spike of the live whiteboard relay, kept out of main

## Later

- Interviewer console
  - Switch fonts to Newsreader, Public Sans and IBM Plex Mono per the UI spec, and remove Geist.
- Debrief scorecard
- Accounts and invites
- Live shared whiteboard
- Candidate list, CSV export and score distribution
- Project skills for writing specs and templates
- Bands (labels for score totals), once we have real totals from interviews

## Open questions

- Where to host the API. It must support WebSockets and not sleep during an interview.
- The "what this candidate does well" line: proposed, confirm before building.
- TL template placeholders: the PR review checklist items and the Part 2 feature.
