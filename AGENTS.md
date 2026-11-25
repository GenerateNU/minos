# AGENTS.md

Minos is an interview scoring platform for the Data branch at Generate Northeastern. Interviewers run a live interview from a template, score candidates blind, and compare in a debrief. Leaders rotate every semester, so keep the code readable, lean, and easy to maintain.

## Repo layout

- `apps/web`: Next.js thin client. No server actions, no direct database access.
- `apps/api`: FastAPI, the only thing that touches the database.
- `docs/specs`: behavior specs. The source of truth for what the app does.
- `docs/decisions`: decision records, such as the stack choice.
- `docs/design`: link to the wireframes.
- `docs/ROADMAP.md`: what's now, next and later.
- `templates`: interview templates (JSON).

Some of these folders do not exist yet.

## Commands

Database, run from the repo root: `docker compose up -d` starts local Postgres on port 5433.

API, run from `apps/api`:

- Install: `uv sync`
- Local config: `cp .env.example .env`
- Migrate: `uv run --env-file .env alembic upgrade head`
- New migration: `uv run --env-file .env alembic revision --autogenerate -m "short description"`
- Run: `uv run uvicorn app.main:app --reload`
- Test: `uv run pytest`
- Lint and format: `uv run ruff check .` and `uv run ruff format .`
- Type check: `uv run mypy app tests`

Web, run from `apps/web` (pnpm comes from Corepack):

- Install: `pnpm install`
- Run: `pnpm dev`
- Test: `pnpm test`
- Lint: `pnpm lint`
- Type check: `pnpm typecheck`
- Build: `pnpm build`

This Next.js version may differ from what you know. Read the guides in `apps/web/node_modules/next/dist/docs/` before writing web code.

## Working rules

1. Spec first. Behavior lives in docs/specs. If it is not in a spec, ask or write the spec before coding.
2. Tests first for domain logic (scoring, bands, template validation, authorization, session state). The human reviews tests before implementation.
3. Small slices, reviewable in 10 minutes. One commit per step.
4. Lean: no new dependency without asking, no abstraction until two real uses, delete dead code.
5. Authorization lives in one policy module in the API, with tests. Only the API touches the database.
6. Never swallow errors. No secrets in the repo.
7. Plain language in comments and docs. No em dashes.
8. No Co-Authored-By trailer on commits.
9. Always hand review: authorization and score visibility, migrations, anything touching scores or candidate data.
10. The person who accepts a change owns it.
11. Deviating from these rules is allowed, but record why in docs/decisions.
12. Get a rough version working first, then improve it. Spike risky parts early and throw the spike away.
13. Ask before guessing. Be specific in specs, comments and commit messages.

## Git

- Never force push, rewrite history or push to main without asking first.
- PR descriptions use the template in .github and never include a 'Generated with' line or any AI attribution. Commits have no Co-Authored-By trailer.

## Testing

- Before writing tests, show the human a plain-English list of cases and wait for approval.
- During a feat step, never edit tests. If a test looks wrong, stop and ask.
- After implementing, flip one condition and confirm a test fails, then revert.

## Definition of done

Spec updated, tests pass, types check, lint clean, generated client current.
