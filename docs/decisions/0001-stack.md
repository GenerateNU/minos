# 0001: Stack

Status: Accepted

## Context

Minos is built and maintained by student leaders who rotate every semester. The stack has to be readable and lean, keep rules in one place, and support a live shared whiteboard during an interview.

## Decision

- `apps/web`: Next.js (React, TypeScript strict, Tailwind, shadcn/ui). Thin client: client components, no server actions, no direct database access.
- `apps/api`: FastAPI, Pydantic v2, SQLAlchemy 2, Alembic, Postgres. Docker Compose runs Postgres for local development and tests. Neon hosts the deployed database.
- Pydantic is the source of truth. FastAPI emits OpenAPI, the TypeScript client is generated from it (openapi-typescript), and CI fails if it is stale. Never hand edit generated code.
- Tooling: uv, ruff, a type checker, pytest. pnpm, eslint, Vitest, Playwright smoke test. GitHub Actions.
- Whiteboard: Excalidraw component (client side only), live shared through a WebSocket relay in FastAPI.
- Postgres over Mongo: relational data, rules enforced by the database, SQL group-bys for stats, JSONB for template snapshots.
- Neon for the deployed database: it scales to zero and does not pause. Local work stays on Docker so it runs offline and never touches shared data. The API reads the database from `DATABASE_URL` in both places.

## Consequences

- Only the API touches the database, so authorization lives in one place.
- API and web types cannot drift without CI failing.
- The whiteboard relay keeps rooms in memory, so v1 runs on a single API instance (see [spec 03](../specs/03-live-whiteboard.md)).

## Open

- Sign in: no outside provider in v1. Accounts come from invite links (see [spec 00](../specs/00-scope.md)).
- API hosting: must support WebSockets and not sleep during an interview.
