# AGENTS.md

Minos is an interview scoring platform for the Data branch at Generate Northeastern. Interviewers run a live interview from a template, score candidates blind, and compare in a debrief. Leaders rotate every semester, so keep the code readable, lean, and easy to maintain.

## Repo layout

- `apps/web`: Next.js thin client. No server actions, no direct database access.
- `apps/api`: FastAPI, the only thing that touches the database.
- `docs/specs`: behavior specs. The source of truth for what the app does.
- `docs/decisions`: decision records, such as the stack choice.
- `templates`: interview templates (JSON).

Some of these folders do not exist yet. They are added by the roadmap steps.

## Working rules

1. Spec first. Behavior lives in docs/specs. If it is not in a spec, ask or write the spec before coding.
2. Tests first for domain logic (scoring, bands, template validation, authorization, session state). The human reviews tests before implementation.
3. Small slices, reviewable in 10 minutes. One commit per roadmap step.
4. Lean: no new dependency without asking, no abstraction until two real uses, delete dead code.
5. Authorization lives in one policy module in the API, with tests. Only the API touches the database.
6. Never swallow errors. No secrets in the repo.
7. Plain language in comments and docs. No em dashes.
8. No Co-Authored-By trailer on commits.
9. Always hand review: authorization and score visibility, migrations, anything touching scores or candidate data.
10. Own the output. The person who accepts a change owns it. Never say "the AI wrote it".
11. Deviating from these rules is allowed, but record why in docs/decisions.
12. Prefer a rough working version first, then improve it. Spike risky parts early and throw the spike away.
13. Ask before guessing. Be specific in specs, comments and commit messages.

## Definition of done

Spec updated, tests pass, types check, lint clean, generated client current.
