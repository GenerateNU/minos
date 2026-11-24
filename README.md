# minos

Interview scoring platform for the Data branch at Generate Northeastern.

Interviewers run a live interview from a template (timed parts, hints, rubric), score each candidate independently and blind, then compare scores in a debrief. Templates are data, so a new interview type is a new template, not new code.

## Layout

- `apps/web`: Next.js client
- `apps/api`: FastAPI service and Postgres
- `docs/specs`: what the app does
- `docs/decisions`: why it is built this way
- `templates`: interview templates

The apps and docs are added step by step. Setup instructions arrive with each scaffold.

## Contributing

Read [AGENTS.md](AGENTS.md) first. It has the working rules for people and coding agents.
