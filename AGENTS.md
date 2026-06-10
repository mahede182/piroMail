# piroMail — Agent Context

---

## Product Goal

A locally hosted, AI-powered email assistant that reads a mock inbox, classifies emails using Google Gemini, and displays important notifications on a real-time dashboard..

## Stack

| Layer | Tech |
|-------|------|
| Backend Framework | Django 4.2+ (Python 3.11) |
| Database | SQLite (default Django) |
| AI Classification | Google Gemini (`google-generativeai`) |
| API | `JsonResponse` (or DRF if needed) |
| Frontend | Vite + React (`App.jsx`) |
| DevOps | Docker + Docker Compose |
| Package Manager | `uv` (Python), `npm` (Node) |

---

## Rules (Non-Negotiable)

1. **KISS.** Do not over-engineer. Every module should be as simple as possible while meeting requirements.
2. **Duplicate prevention is mandatory.** The `email_id` field is `unique`. Always check existence before processing.
3. **Gemini must return strict JSON.** The system prompt must enforce a raw JSON response with exactly these keys: `important` (bool), `priority` (string), `category` (string), `reason` (string). No markdown fences.
4. **The API only exposes important emails.** `GET /api/notifications/` returns `is_important=True` records, ordered newest first. Keep the view minimal.
5. **Frontend polls, never pushes.** The React dashboard uses `setInterval` in `useEffect` to re-fetch every 10 seconds. No WebSockets.
6. **Environment secrets stay out of code.** `GEMINI_API_KEY` is read from environment variables or `.env`, never hardcoded.

---

## Coding Conventions

- **Engineering Principles**: Follow KISS, SOLID, and DRY strictly.
- **Django Models**: Use `TextChoices` for enums. Always set `db_index` on frequently queried fields. Define `Meta.ordering`.
- **Django Views**: Use `JsonResponse` for simplicity. Wrap DB writes in `transaction.atomic()`.
- **Management Commands**: Inherit `BaseCommand`. Use `self.stdout.write` / `self.stderr.write` for logging. Handle all exceptions gracefully.
- **Gemini Prompting**: Always sanitize response (strip markdown fences). Always `json.loads()` inside try/except.
- **React**: Extract constants (`API_URL`, `POLL_INTERVAL_MS`). Clean up intervals in `useEffect` return. Handle loading and error states.
- **Docker**: Use `python:3.11-slim` for backend. Multi-stage build for frontend (Node build → Nginx serve). Keep `docker-compose.yml` minimal.

---

## Container Configuration

| Service | Dockerfile | Port | Notes |
|---------|-----------|------|-------|
| Backend (Django) | `Dockerfile.backend` — `python:3.11-slim` | `8000` | Runs migrations on startup |
| Frontend (React) | `frontend/Dockerfile` — Node build + Nginx | `3000 → 80` | Multi-stage build |

Launch: `docker compose up --build`