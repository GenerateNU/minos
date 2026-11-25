# Roadmap

Already done: repo setup, specs, the Socratic tutor skill, the API and web app skeletons, and CI.

## Now

- Local Postgres (Docker) and database migrations, with Neon for the deployed database

## Next

- Template validation, tests first, then the TL template
- Scoring and bands, tests first
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

## Open questions

- Where to host the API. It must support WebSockets and not sleep during an interview.
- The "what this candidate does well" line: proposed, confirm before building.
- TL template placeholders: the PR review checklist items and the Part 2 feature.
