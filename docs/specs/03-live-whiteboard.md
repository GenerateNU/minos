# Spec 03: live whiteboard

## Board

One board per session. Interviewers open it from the console, the candidate from a link. Both see edits within about a second and both can edit. It autosaves to the session every few seconds and when the part ends. Reconnecting restores the latest board. The debrief opens the saved board read only.

## Candidate link

An unguessable token tied to one session. It gives access to that board and the one line prompt only, never the rubric, scores or notes. It expires when the session ends (plus a short grace period) and a Chief can revoke it. Interviewers join with their signed in account.

## How

The Excalidraw component sends changed elements to the server on change, and merges received elements using Excalidraw's reconcile helper (newer element version wins). FastAPI has a WebSocket endpoint with one in memory room per session. It relays updates and saves the latest scene to Postgres. v1 runs on a single API instance.

## Fallback

The candidate shares their screen. Autosave keeps the last board state.

## Acceptance

- Two browsers see each other's edits live.
- A refresh restores the board.
- The candidate link reads nothing except the board and prompt.
- An expired or revoked token is rejected.
- The saved board opens in the debrief.
