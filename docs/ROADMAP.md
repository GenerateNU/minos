# Roadmap

Already done: repo setup, specs, the Socratic tutor skill, and the API skeleton.

## Now

- Web app skeleton (Next.js, Tailwind, shadcn/ui, Vitest)
- CI for the API and the web app
  - Pin Node 24 LTS in the repo (`.nvmrc` plus an `engines` field) and use the same version in CI.

## Next

- Local Postgres and database migrations
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
- Neon for Postgres: leaning yes, confirm before setting it up.
- The "what this candidate does well" line: proposed, confirm before building.
- TL template placeholders: the PR review checklist items and the Part 2 feature.
