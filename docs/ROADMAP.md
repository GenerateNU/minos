# Roadmap

One commit per step. Between steps, stop and wait for "next". Ask questions before any step where a decision is not already in the specs or decisions.

1. `chore: init repo`: README, .gitignore, AGENTS.md (from working rules), CLAUDE.md containing only `@AGENTS.md`.
2. `docs: add specs and stack decision`: turn the planning brief into docs and specs.
3. `chore(skills): add socratic-tutor`: from janestreet/agent_skills into .claude/skills, with its MIT license text.
4. `chore(api): scaffold FastAPI`: uv, ruff, type checker, pytest, a health endpoint with a test.
5. `chore(web): scaffold Next.js`: TypeScript strict, Tailwind, shadcn/ui, eslint, Vitest.
6. `chore(ci): add GitHub Actions` for api and web.
7. `chore(db): Docker Compose Postgres and Alembic baseline`.
8. `test(api): failing tests for template validation` (spec 01). Human reviews before step 9.
9. `feat(api): template models, validator and TL template` (spec 05).
10. `test` then `feat`: scoring and bands (spec 02).
11. `test` then `feat`: score visibility policy module (spec 02).
12. `feat(api)`: sessions (with `recording_url`), scores and events endpoints, with the generated TypeScript client and its CI check.
13. `feat(web)`: design tokens and shell (spec 04), then the interviewer console as pillar and tray. Ask before adding fonts.
14. `feat(web)`: debrief scorecard.
15. `feat`: accounts and invites.
16. `feat`: live whiteboard (spec 03). Proposed: do a throwaway spike of the WebSocket relay right after step 7, to learn if the risky part works before building around it. Keep the spike out of main.
17. `feat`: candidate list, CSV export and score distribution.
18. `skills`: project skills for writing specs and templates.
