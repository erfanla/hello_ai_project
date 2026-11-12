# Rubric Review — Architecture Spine, Low-pressure friend invite app v1

- **Spine:** `ARCHITECTURE-SPINE.md` (status: draft, 2026-11-11)
- **Context read:** `.memlog.md`, PRD `prd.md` (+ `addendum.md` §stack)
- **Reviewed:** 2026-11-11
- **Level used for judging:** a beginner's first project, about 12 users, 4-week test. Findings are only raised when two separately built stories could really build things differently, or when the chosen setup would really fail at this size.

## Verdict

A good spine for this size: the main divergence points (layers, one visibility module, one Invitation writer, computed Status, Answer state machine, time handling, single sweep) are fixed with clear rules. But the chosen operational setup has a real failure: the 60-second sweep keeps Neon Free awake and will use up its monthly compute in about two weeks, and the "single instance / always on" rule does not match Fly.io defaults. A few data-shape and cross-story seams (the "when" field, SQLite vs PostgreSQL datetimes, the notification-answer endpoint, metrics data) are still open. Fix the critical and high items before writing epics.

**Counts:** critical 1 · high 3 · medium 7 · low 6

---

## Findings

### C-1 (critical) — The deadline sweep keeps Neon Free awake; free compute runs out mid-test

- **Where:** AD-7 (sweep every 60 s queries `deadline_at <= now`), Stack (`PostgreSQL | Neon Free`), Deferred "Backups and monitoring".
- **Problem:** Neon Free scales compute to zero only after 5 minutes with no queries, and gives 100 CU-hours per project per month (official Neon FAQ, updated 2026-10-01; scale-to-zero cannot be turned off on Free). A query every 60 s means the compute never sleeps: 0.25 CU × 24 h ≈ 6 CU-hours/day, so the 100 CU-hours are gone after about 16 days. The 4-week test (PRD §7) needs about 28 days. When the quota is used, the database stops, and the whole app stops. The memlog price check (2026-11-11) records "suspends compute after 5 min idle" but did not connect it to the sweep.
- **Fix (pick one, write it in the spine):**
  1. **SQLite in production on a Fly volume** (simplest at this size, and AD-8 already forces one instance). This also removes the SQLite/PostgreSQL split in AD-10 and H-2. The addendum only ruled out SQLite because free hosts delete files; a paid Fly machine with a volume does not. Add a backup rule (e.g. Litestream or a daily copy).
  2. Keep Neon, but make the sweep not hit the database every minute: e.g. keep the next `deadline_at` in memory (reloaded on start and after each publish), query only when it is due.
  3. Pay for Neon Launch, or use Fly-managed Postgres — but check the < 5 EUR/month budget.

### H-1 (high) — AD-8 "exactly one process, always on" is not enforceable against Fly.io defaults

- **Where:** AD-8, Stack (`Fly.io, 1 × shared-cpu-1x 512 MB, always on`), Structural Seed "Production" row.
- **Problem:** On the first `fly launch` / `fly deploy`, Fly creates **two** Machines for an app with an HTTP service, and the generated `fly.toml` has `auto_stop_machines = "stop"`, `min_machines_running = 0`. So by default you get two sweeps (double result notifications — the exact thing AD-8 is meant to prevent), and machines that stop when idle (no sweep at all, no Deadline results). The rule says what to want, but not how to hold it.
- **Fix:** Make the rule concrete: `fly.toml` sets `auto_stop_machines = "off"` and `min_machines_running = 1`; after the first deploy run `fly scale count 1`; uvicorn runs with one worker. Optional extra safety: the sweep claims each Invitation with a conditional `UPDATE … SET result_notified_at = now WHERE id = ? AND result_notified_at IS NULL` and only sends if one row changed — then even two processes cannot double-send.

### H-2 (high) — Timezone-aware datetimes behave differently on SQLite and PostgreSQL

- **Where:** AD-6 ("stored as UTC, timezone-aware"), AD-10 ("must run on both SQLite and PostgreSQL"), Conventions "Tests" (services tested on SQLite).
- **Problem:** SQLite has no timezone type. With SQLAlchemy `DateTime(timezone=True)`, SQLite gives back **naive** datetimes, PostgreSQL gives back **aware** ones. Comparing `now` (aware) with a naive value raises `TypeError`. One story will add `.replace(tzinfo=UTC)` in its code, another will not; tests pass on SQLite and production breaks (or the reverse). The same split hits enums (native `ENUM` type on PostgreSQL, `VARCHAR` on SQLite, and Alembic autogenerate does not handle enum changes) and `ALTER TABLE` (SQLite needs Alembic batch mode).
- **Fix:** Add to AD-6/AD-10: one `UTCDateTime` type in `app/models/` that every datetime column uses (always returns aware UTC); enums stored as strings (`native_enum=False`); Alembic `render_as_batch=True`. And add one CI/check step that runs migrations + tests against PostgreSQL — or take C-1 option 1 and use SQLite everywhere.

### H-3 (high) — The shape of "when" (and the Draft's Deadline length) is not fixed, but four rules depend on it

- **Where:** AD-4 (stores `published_at`, `deadline_at`, `cancelled_at` only), AD-5 ("until 'when' starts"), Structural Seed ER diagram (no fields), PRD FR-4 ("exact time or a time window"; "where or when is open"), FR-4 "Deadline must be before when starts", FR-14 "only before when starts", FR-15 "Deadline starts counting when the Draft is published", FR-16 "leaves My Plans 24 hours after when".
- **Problem:** Four stories (create, edit, reconfirm, My Plans) all need "when starts" as a value, but the spine does not say how "when" is stored: one `when_start` + nullable `when_end`? Can "when" be fully open (no time)? If it is open, what does "before when starts" mean? Also, a Draft has no `deadline_at` yet (FR-15), so the chosen Deadline length must be stored somewhere — no column is named, and PRD Open Question 1 (which Deadline choices) is not carried over.
- **Fix:** Add a short rule: `when_start` (required, UTC), `when_end` (nullable, for a window); "where" nullable means open. "when starts" = `when_start`. A Draft stores `deadline_minutes` from one fixed list (one enum/constant in `models/`); `publish` sets `deadline_at = published_at + deadline_minutes` and checks `deadline_at < when_start`. Either decide whether "when" can be fully open, or list it as an Open Question.

### M-1 (medium) — Answering from a notification: the endpoint, CSRF, and auth are not decided

- **Where:** Conventions "Forms & CSRF" (every change is a POST form with a CSRF token), AD-9, Capability map FR-8 (only `services/invitations.py`), FR-12 row (`static/service-worker.js`).
- **Problem:** FR-8 wants Yes/No straight from the notification on Android. A notification action runs in the service worker, which has no form and no CSRF token. One story will skip CSRF for this route, another will try to put a token in the push payload. iPhone opens a one-screen Yes/No page instead — its URL is not fixed either, and the push payload (which URL to open, which fields) is shared between `notifications/` and `service-worker.js`.
- **Fix:** Name the push payload shape once (e.g. `{type, invitation_id, title, body, url}`), the Yes/No page URL (e.g. `/invitations/{id}/answer`), and the rule for the action endpoint (e.g. the service worker opens/focuses the Yes/No page with the choice pre-selected, so every answer still goes through a normal CSRF form; or a documented CSRF exception that relies on `SameSite=Lax` + a same-origin check).

### M-2 (medium) — "Send notifications in one transaction" is unclear about push vs commit

- **Where:** AD-3 ("checks permission, applies the change, and asks `notifications` to send, in one transaction"), AD-7 ("Push failures … never undo the business change"; sweep "sends the result, then sets `result_notified_at`").
- **Problem:** Web Push is an HTTP call; it cannot be part of a database transaction. If one story sends before commit and the commit fails, people get a notification for a change that did not happen; if another sends after commit, the rules differ. Also, AD-3 says only `invitations.py` writes `Invitation` rows, but AD-7 has the sweep writing `result_notified_at` — it is not said that the sweep must call `invitations.py` for this.
- **Fix:** Rule: services commit first, then call `notifications.send_…` after commit (push errors are logged only). The sweep calls a function in `services/invitations.py` (e.g. `mark_result_notified`) — no direct write from `jobs/` or `notifications/`.

### M-3 (medium) — Who gets each notification is not bound to the visibility policy

- **Where:** AD-2 (covers "reads … for a User"), AD-7 (lists the four notification types), Notifications row in the layer table ("asks services").
- **Problem:** Notification recipients are a privacy rule too (FR-5: non-Guest-List Members get no notification; FR-13: only the Yes List — does that include `YES_PENDING`?; FR-14: second edit — are `YES_PENDING` people notified again?). AD-5's diagram has no `YES_PENDING → YES_PENDING` arrow for a second edit. Different stories could pick different recipient sets.
- **Fix:** Add one line to AD-2/AD-7: recipient lists come only from `visibility.py` functions (e.g. `invitees_to_notify`, `yes_list_to_notify`), where "Yes List" = `YES` + `YES_PENDING` everywhere. Add the `YES_PENDING → YES_PENDING` (edit again) arrow, and say what Cancel does to `YES_PENDING` and reconfirming after Cancel.

### M-4 (medium) — Success-metric data is not captured, and it cannot be recovered later

- **Where:** Capability map (no row for PRD §7), AD-7 binds SM-C1 but stores nothing for it.
- **Problem:** PRD says SM-0, SM-1, SM-2, SM-C1, SM-C2 "come from app data". SM-0 needs when a person got/opened the Group Link and when they joined; SM-C1 needs when someone turned notifications off (a deleted subscription in AD-7 leaves no trace); SM-C2 needs to know who ignored Invitations (`NONE` after Deadline is kept — good). If these timestamps are not recorded from day one, the 4-week test cannot be measured. Different stories will not add them on their own.
- **Fix:** Add a small rule: `Membership.joined_at`, `GroupLink` opens logged (or a simple `events` table: `type, user_id, group_id, at`), subscription removals recorded (soft delete or event), not hard delete only. Add a "PRD §7 metrics" row to the capability map.

### M-5 (medium) — Group Link flow across sign-up is a seam between the accounts and groups stories

- **Where:** AD-9 (Group Link landing page is public), Conventions "IDs" (token), Capability map FR-1 vs FR-2/FR-3 (different modules).
- **Problem:** UJ-3: open link → sign up → land in the Group. How the token survives sign-up/log-in is not fixed (query `?next=`, a hidden form field, or the session cookie). The accounts story and the groups story will each guess. A free `next` URL is also an open-redirect risk.
- **Fix:** One rule: the landing page stores the pending Group token in the session (or a hidden field); after sign-up/log-in, `accounts` calls `groups.join_by_token`; redirects only to internal paths.

### M-6 (medium) — Sync vs async is not decided

- **Where:** Paradigm (FastAPI), AD-7 ("background loop"), Stack (SQLModel, pywebpush).
- **Problem:** SQLModel sessions and pywebpush are both blocking. If some routes are `async def` and others `def`, or the sweep runs as an `asyncio` task that calls blocking code, the single process (AD-8) freezes while it waits on the database or a push service. With one process this hurts even at 12 users. Stories will differ by default.
- **Fix:** Rule: routes and services are plain `def` (FastAPI runs them in a thread pool); the sweep runs in its own thread (or calls services via `run_in_threadpool`), and must catch and log every exception so the loop never dies silently.

### M-7 (medium) — Stack versions are not verified, and two are not versions

- **Where:** Stack table; memlog "(version) … Versions from search snippets; confirm with uv add".
- **Problem:** The checklist asks for verified-current tech. The memlog says the versions came from search snippets and were not confirmed. `SQLModel 0.0.4x` and `pwdlib latest, pinned` are not versions, so two stories created at different times can get different packages until a lock file exists. Python 3.14 is a fine choice (3.15 just came out; 3.14 is safer).
- **Fix:** Run `uv init` + `uv add …` once, copy the exact versions from `uv.lock` into the Stack table, and add the rule "`uv.lock` is committed; only `uv add` changes versions". Name the CSRF and session libraries too (see L-2).

### L-1 (low) — AD-1 has no automatic check

- **Where:** AD-1.
- **Problem:** "No DB session in routes" is easy to break by accident; an AI coding agent will sometimes do it.
- **Fix:** Optional: `import-linter` contract (layers: routes → services → models) in the test run, or a simple test that greps `app/routes/` for `Session`/`select(`.

### L-2 (low) — Session and CSRF mechanism not named

- **Where:** AD-9, Conventions "Forms & CSRF".
- **Problem:** FastAPI has no built-in CSRF. "One middleware" and "signed cookie" are clear in intent, but HTMX requests need the token in a header (`hx-headers` on `<body>`), which the template stories must all do the same way.
- **Fix:** Name it: Starlette `SessionMiddleware` (secret from `config.py`) for the cookie; one CSRF approach (library or a 20-line middleware) that accepts the token from a form field or `X-CSRF-Token` header; the base layout sets `hx-headers`.

### L-3 (low) — HTMX + expired login and errors

- **Where:** AD-11, Conventions "Errors".
- **Problem:** When `current_user` fails on an HTMX request, a normal redirect puts the login page inside a fragment — the thing AD-11 wants to prevent.
- **Fix:** One line: for `HX-Request`, auth failures return `HX-Redirect: /login`; error fragments are small `templates/fragments/error.html`.

### L-4 (low) — Owner of `PLAN_SEEN`, the "Updated" mark data, and the banner flag

- **Where:** Structural Seed (`PLAN_SEEN`), AD-3 (owner list), FR-12 banner.
- **Problem:** Opening an Invitation writes `PLAN_SEEN` from a read page; AD-3 does not list an owner. "Updated" needs a `changed_at`-like field on Invitation (place/time change, cancel, new Note) — not named. Banner "dismissed forever" could be server-side or `localStorage`.
- **Fix:** Say: `visibility.py` (or `plans.py`) owns `PLAN_SEEN` writes; Invitation has `last_change_at` set by `invitations.py`; `User.push_banner_dismissed_at` server-side.

### L-5 (low) — Operations: sweep health, backups, region, admin command

- **Where:** Deferred "Backups and monitoring", AD-8, Deferred "password reset" (admin command).
- **Problem:** At this size it is fine to defer most operations, but: (a) if the sweep thread dies, nobody notices — Fly health checks only see HTTP; (b) Neon Free restore history is short, and if you move to SQLite (C-1) you need your own backup; (c) the Fly region and database region are not named (pick the same, e.g. Europe, near Italy); (d) the admin reset command should call `services/accounts.py`, not write the table directly.
- **Fix:** A `/healthz` that also reports "last sweep ran at"; one line on backups for the chosen database; name the region; one line that admin commands go through services. Also say how deploys happen (manual `fly deploy` from the laptop is fine; migrations via `release_command`).

### L-6 (low) — Privacy for Groups/Members is outside AD-2

- **Where:** AD-2 (lists Invitations, Yes Lists, Notes, My Plans), NFR Privacy ("only sees Groups they belong to").
- **Problem:** Group pages and Member lists (FR-3) are not under the visibility module; `groups.py` could check membership its own way.
- **Fix:** Extend AD-2 to Groups and Members (non-member → "not found").

---

## Checklist summary

| Check | Result |
| --- | --- |
| Fixes the real divergence points, misses none | Mostly. Missing: "when"/Deadline-length shape (H-3), datetime/enum DB types (H-2), notification payload + answer endpoint (M-1), recipients (M-3), Group Link token (M-5), sync/async (M-6). |
| Every AD Rule enforceable and prevents its divergence | Mostly. AD-8 not enforceable as written on Fly (H-1); AD-3 "one transaction" unclear (M-2); AD-1 has no check (L-1). |
| Nothing under Deferred lets units diverge | OK. "Backups and monitoring" deferral is fine at this size, but see C-1 / L-5. |
| Named tech is verified-current | Not yet: versions from snippets, two non-versions (M-7). |
| Covers the PRD's capabilities | FR-1..FR-16 covered; PRD §7 metrics data not covered (M-4). |
| Operational envelope (deploy, environments, infra, operations) | Decided, but the Neon + sweep combination fails in practice (C-1) and Fly defaults break AD-8 (H-1). |

## Sources checked

- Neon Free plan limits (official FAQ, updated 2026-10-01): 100 CU-hours/project/month, scale to zero after 5 min, cannot be disabled on Free — https://neon.com/faqs/free-plan-limits-and-quotas
- Fly.io autostop defaults (`auto_stop_machines = "stop"`, `min_machines_running = 0`) and two Machines on first deploy — https://fly.io/docs/launch/autostop-autostart/ , https://fly.io/docs/blueprints/resilient-apps-multiple-machines/
