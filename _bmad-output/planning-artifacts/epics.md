---
status: final
stepsCompleted: [1, 2, 3, 4]
inputDocuments:
  - _bmad-output/planning-artifacts/prds/prd-hello_ai_project-2026-11-10/prd.md
  - _bmad-output/planning-artifacts/prds/prd-hello_ai_project-2026-11-10/addendum.md
  - _bmad-output/planning-artifacts/architecture/architecture-hello_ai_project-2026-11-11/ARCHITECTURE-SPINE.md
  - _bmad-output/planning-artifacts/ux-designs/ux-hello_ai_project-2026-11-11/DESIGN.md
  - _bmad-output/planning-artifacts/ux-designs/ux-hello_ai_project-2026-11-11/EXPERIENCE.md
---

# hello_ai_project (low-pressure friend invite app) - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for hello_ai_project (low-pressure friend invite app), decomposing the requirements from the PRD, UX Design if it exists, and Architecture requirements into implementable stories.

## Requirements Inventory

### Functional Requirements

FR-1: A person can sign up with only name, email and password, and log in with email and password; a new User can finish sign-up in under 1 minute (home-screen install not counted). There are no guest Answers.
FR-2: A logged-in User can create a Group with a name and automatically becomes its first Member.
FR-3: Any Member can share the Group's Group Link; a person who opens it can sign up (if needed) or log in, join that Group, and then see the Group and its Members.
FR-4: A Member can create an Invitation in one of their Groups with: what (text, required), where (a place, or "open"/Decide later), when (exact time or a time window), a Cost Tag (Free, $, $$, $$$) and a Deadline length chosen from a short fixed list; the Deadline must end before "when" starts, otherwise the Invitation is refused with an error.
FR-5: The Inviter can choose the Guest List from the Group's Members (default: all Members); Members not on the Guest List never see the Invitation or any notification about it.
FR-6: A User can see all Open Invitations where they are an Invitee, across all their Groups, and answer from that list.
FR-7: Only the Inviter can change an Invitation, and only as FR-14 allows; Invitees can only answer; there is no comment or "suggest another plan" field before answering.
FR-8: An Invitee can answer Yes or No with one action, from the notification button (Android/desktop) or from a one-screen Yes/No page (iPhone: tapping the notification opens this page); there is no reason field, and the Answer is final except for the FR-14 reconfirm.
FR-9: Silent No: No Answers and missing Answers are never shown to anyone (including the Inviter); the Inviter sees the Yes List grow before and after the Deadline; an Invitee sees the Yes List before answering but never the full Guest List or who said No.
FR-10: When the Deadline passes, the Invitation Status becomes Closed, missing Answers count as No, and the Inviter gets one result notification; if the Yes List is empty, the Inviter sees "Nobody is free tonight 🌙", never "0 people".
FR-11: The Inviter and the Yes List (from the moment a User joins it) can read and post Notes on an Invitation; a Note is at most 280 characters; Notes show on page open/refresh (polling allowed, not live chat); nobody else can see them.
FR-12: Each Invitee gets exactly one notification per new Invitation (what, where, when, Deadline); the only other notifications are Deadline result, cancelled, and place/time changed; on iPhone notifications work only after Add to Home Screen (sign-up guides this); a User with notifications off sees one dismissible banner when their first Invitation arrives, which never comes back once dismissed.
FR-13: The Inviter can cancel an Open or Closed Invitation; Status becomes Cancelled (not deleted, Notes stay readable); every User on the Yes List gets a notification ("Soroush cancelled: Burger tonight 🍔"); unanswered Invitees stop seeing it with no notification; a reason in Notes is optional.
FR-14: The Inviter can change only "where" and "when", and only before "when" starts; each User on the Yes List (and, while answering is open, each Invitee who has not answered) gets a notification; Yes List Users must reconfirm with **Still in** (UX label for the PRD action "Still OK") or **Not anymore**; Not anymore removes them silently like a No; until they reconfirm they stay on the Yes List marked "not confirmed yet"; any other change needs cancel + new Invitation.
FR-15: The Inviter can save an Invitation as a Draft and publish it later; only the Inviter sees a Draft, nobody is notified until publish, and the Deadline starts counting at publish.
FR-16: A User can see My Plans: Invitations they created or answered Yes to, in any Status (incl. Closed, Cancelled, Draft for own plans); a plan shows an **Updated** mark if place/time changed, it was cancelled, or a new Note was added since the User last opened it; a plan leaves My Plans 24 hours after "when".

### NonFunctional Requirements

NFR-1: Phone first: every screen works at 360px width with no sideways scrolling, in a phone browser and as a home-screen app (PWA).
NFR-2: Tap targets: every button and interactive element is at least 44px tall.
NFR-3: Simple: the main actions (create an Invitation, answer, open My Plans) are reachable in at most 2 taps from the Home screen.
NFR-4: Speed: answering from a notification takes under 5 seconds.
NFR-5: Fast sign-up: a new User can finish sign-up in under 1 minute (not counting home-screen install).
NFR-6: Privacy: a User only sees Groups they belong to, and Invitations they created or are on the Guest List of (never someone else's Draft); hidden Invitations return a normal 404 and never reveal they exist.
NFR-7: Privacy: no screen shows a User's past Answers to other Members (no answer history, no Yes counts, no "last seen").
NFR-8: Silent No privacy: No and missing Answers, and the Guest List, are never exposed by any page, fragment, notification or API, to anyone except where explicitly allowed (Guest List: Inviter only).
NFR-9: Silent No known limit (accepted for v1): the app hides who said No, not how many were asked; in small Guest Lists people may guess. No extra mitigation in v1, but no screen shows counts of who was asked.
NFR-10: No pressure by design: no scores, ratings, streaks, presence points, reminders, or "X is coming" notifications in v1.
NFR-11: Notes are not real-time chat: no WebSockets, no typing indicators, no notification per Note.
NFR-12: Reliability of the Deadline: an Invitation must close and send its result exactly once, even after a server restart (no stored status that can go stale).
NFR-13: Metrics: the app records the data needed for SM-0..SM-C2 from day one, without personal content.

### Additional Requirements

**Starter template: NONE (important for Epic 1, Story 1).**
- There is **no starter template**. This is a greenfield project created from scratch with `uv` (uv 0.13.7, Python 3.14). Epic 1 Story 1 must set up the project by hand: `uv init`, add pinned dependencies, create the source tree (`app/main.py`, `app/config.py`, `app/models/`, `app/services/`, `app/notifications/`, `app/jobs/`, `app/routes/`, `app/templates/` with `fragments/`, `app/static/`, `migrations/`, `tests/`, `fly.toml`), Alembic init with `render_as_batch=True`, pytest setup, and one "hello" page that renders through the base layout.

**Stack (pin exact versions):**
- Python 3.14; uv 0.13.7; FastAPI 0.162.x (pin exact); python-multipart (latest, pinned); SQLModel 0.0.49; Alembic 1.20.1; SQLite (bundled with Python, WAL mode); Jinja2 3.1.6; HTMX 2.0.11 (HTMX 2.x only, served from `static/`); pwdlib[argon2] 0.3.1; itsdangerous (latest, pinned); pydantic-settings (latest, pinned); pywebpush 2.5.0; pytest.
- Hosting: Fly.io, 1 × shared-cpu-1x 512 MB, always on, 1 GB volume.

**Layered monolith rules:**
- One FastAPI process serves HTML (Jinja2 + HTMX), holds all logic, and owns one SQLite database.
- Layers: `routes/` (parse request, get current User, call one service, render template; never query the DB or decide rules) → `services/` (all business rules, visibility, state changes, transactions; never render HTML or read the request) → `models/` (SQLModel tables, enums, shared UTC datetime type; no rules). `notifications/` builds and sends Web Push (asks services who may see what). `jobs/` holds the deadline sweep loop (calls services, no rules).
- Naming: PRD Glossary terms used verbatim in code (`Invitation`, `GuestListEntry`, `Note`, `Group`, `Membership`, `User`, `PushSubscription`, `PlanSeen`, `Event`); `snake_case` files/functions, `PascalCase` classes, `UPPER_CASE` enum values.
- IDs: integer primary keys inside the app; the Group Link uses a separate random token (`secrets.token_urlsafe`), never the database id.
- Errors: services raise `NotFound`, `NotAllowed`, `InvalidState`; one exception handler turns them into 404 / 403 / 409 pages or fragments.
- Config: all secrets and settings from environment variables, read in one `app/config.py` (pydantic-settings); nothing secret in git.
- Logging: Python `logging` to stdout, one line per event; never log passwords, cookies, tokens or push keys.

**Architecture decisions (AD-1..AD-12) as implementation requirements:**
- AD-1 (one direction): dependencies go routes/jobs → services → models/notifications only; only services (and `notifications` for subscriptions) touch the DB session; nothing imports from `routes`.
- AD-2 (one visibility policy): all "who may see what" rules live in `app/services/visibility.py`; every read and write of an Invitation starts with `visibility.get_visible_invitation(user, invitation_id, now)`, which raises `NotFound` (404) when the User may not see it; `NotAllowed` (403) only for Users who can already see it; visible = Inviter, or has a `GuestListEntry` and Status is not Draft; Yes List returns only `YES` and `YES_PENDING` (pending marked "not confirmed yet"); Notes visible to Inviter + `YES`/`YES_PENDING`; Guest List visible to the Inviter only; the public Group Link page shows only the Group name and the sharer's name.
- AD-3 (one owner for Invitation changes): only `app/services/invitations.py` writes `Invitation`, `GuestListEntry`, `Note`, `PlanSeen`; each change is one service function that (1) finds the Invitation via AD-2, (2) checks the action against the Status table (Edit Draft/Publish/Delete Draft: Draft only; Answer: Open only; Edit place/time and Reconfirm: Open or Closed, before `when_start`; Cancel: Open or Closed; Add Note: Open, Closed, Cancelled), (3) writes in one transaction and commits, (4) only then asks `notifications` to send.
- AD-4 (Invitation fields, computed Status): `Invitation` stores `what`, `where` (null = open), `when_start`, `when_end` (null = exact time), `cost_tag`, `deadline_minutes` (from a fixed list in `config`), `published_at`, `deadline_at`, `cancelled_at`, `place_time_changed_at`, `result_notified_at`; only `publish()` sets `published_at` and `deadline_at = published_at + deadline_minutes`; one function checks `deadline_at < when_start` on publish and on every place/time edit; Status is computed by one function `status(invitation, now)` (cancelled_at → Cancelled; published_at null → Draft; now >= deadline_at → Closed; else Open); there is no `status` column.
- AD-5 (Guest List + Answer state machine): one `GuestListEntry` row per invited Member (Inviter has no row) with `answer` and `answered_at`; `publish()` writes the final rows (default all current Members) and they never change after; later joiners do not see it; allowed transitions only NONE→YES, NONE→NO (Open), YES→YES_PENDING (Inviter edits place/time), YES_PENDING→YES (Still in), YES_PENDING→NO (Not anymore); every change is a conditional `UPDATE … WHERE id = ? AND answer = <expected>`, 0 rows → `InvalidState`; reconfirm requests carry the `place_time_changed_at` the User saw and are refused if stale (page reloads); no transitions after `when_start`; NONE after Deadline = No; YES_PENDING stays on the Yes List, keeps Notes access, and receives cancel and edit notifications.
- AD-6 (time): all datetimes stored as UTC through one shared `UTCDateTime` column type in `app/models/`; conversion to/from `Europe/Rome` only in forms and templates (display format `Fri 21 Nov, 20:00`); time-dependent service functions take `now: datetime` as a parameter; only routes and jobs read the clock.
- AD-7 (notifications + deadline sweep): only `app/notifications/` sends Web Push (pywebpush, VAPID keys from env, VAPID `sub` = real `mailto:`); push always after DB commit; a failed push is logged and never undoes the change; subscriptions answering 404/410 are deleted; recipients: New Invitation → every Invitee on the Guest List; Deadline result → Inviter only; Cancelled → `YES` and `YES_PENDING`; Place/time changed → `YES` and `YES_PENDING` (all become `YES_PENDING`) plus, while Open, Invitees with `NONE`; all user-facing notification/result texts in `app/notifications/messages.py`; a loop in `app/jobs/` runs every 60 s and calls `invitations.close_and_notify(now)`, which claims each Invitation with one conditional update on `result_notified_at` (published, not cancelled, deadline passed, not yet notified), commits, then sends; each Invitation is claimed at most once.
- AD-8 (one instance, one SQLite DB): production runs exactly one Fly.io Machine with one Uvicorn worker (`auto_stop_machines = "off"`, `min_machines_running = 1`, scaled to count 1); SQLite on a Fly volume in WAL mode.
- AD-9 (auth, sessions, CSRF): email + password login; passwords hashed with `pwdlib` (Argon2); Starlette signed `SessionMiddleware` cookie holding only the User id, `session_version` and a CSRF token, `HttpOnly`, `SameSite=Lax`, `https_only=True` in production, 90-day lifetime; one `current_user` dependency on every route except sign-up, log-in, static files, Group Link landing, and the push-answer endpoint; every POST carries the CSRF token (hidden `csrf_token` field, or `X-CSRF-Token` header set via `<body hx-headers>`), checked by one dependency; notification buttons post to one endpoint with a signed action token (itsdangerous) in the push payload holding the `GuestListEntry` id + answer, expiring at `deadline_at`, exempt from cookie/CSRF but still going through AD-3 and AD-5; authorization is checked in services, not routes.
- AD-10 (migrations only): tables are created and changed only by Alembic migrations with `render_as_batch=True`; `SQLModel.metadata.create_all` only in tests; enums stored as strings; migrations run on every deploy before the app starts.
- AD-11 (HTMX convention): a route returns the full page on a normal request and only the fragment template (`templates/fragments/…`) when the `HX-Request` header is present; fragments never include `<html>` or the layout; HTMX 2.x only.
- AD-12 (metrics from day one): services append rows to one `Event` table (`user_id`, `type`, `invitation_id`, `group_id`, `at`) for `group_joined`, `invitation_published`, `answered`, `note_added`, `push_enabled`, `push_disabled`; only services write it; no personal content (Note text, places).

**Other architecture conventions:**
- Notifications off = the User has no `PushSubscription`; banner dismissal stored in `User.push_banner_dismissed_at`.
- "Updated" mark = latest of `place_time_changed_at`, `cancelled_at`, newest Note time is after the User's `PlanSeen.seen_at`; My Plans hides a plan 24 h after `when_end` (or `when_start`).
- Onboarding: the Group Link is opened in the browser; the User signs up and joins there, then adds the app to the home screen and logs in once inside it (iPhone keeps separate cookies).
- Password reset: no self-service in v1; Erfan uses an admin command.

**Deployment:**
- Fly.io, one always-on Machine (shared-cpu-1x, 512 MB), `auto_stop_machines = "off"`, `min_machines_running = 1`, count 1, one Uvicorn worker.
- 1 GB Fly volume holding the SQLite file, WAL mode; daily volume snapshots as backup.
- Alembic migrations run on every deploy before the app starts (e.g. release command).
- Secrets (session secret, VAPID keys, VAPID `mailto:`, token signing key) via `fly secrets`, read through `app/config.py`.
- Local: SQLite file in the project, `uv run`; push testing needs HTTPS (e.g. a tunnel) and a real iPhone test before the friend test.
- Monitoring: Fly.io logs only.

**Security:**
- Argon2 password hashing via pwdlib.
- Session cookie: signed, `HttpOnly`, `SameSite=Lax`, `https_only=True` in production, 90 days, holds only User id + `session_version` + CSRF token.
- CSRF token on every POST (form field or HTMX header), checked by one dependency.
- Signed push action tokens (itsdangerous) for notification buttons, expiring at `deadline_at`.
- Group Link token from `secrets.token_urlsafe`, never the DB id.
- Never log passwords, cookies, tokens, or push keys.

**Metrics:**
- `Event` table (AD-12) written only by services, used to compute SM-0..SM-C2 after the 4-week test (`services/metrics.py`).

**Tests:**
- `pytest`; services tested directly with a fixed `now` (no real clock).
- Each AD-2 visibility rule has a test proving a No Answer and a hidden Invitation never appear.
- `SQLModel.metadata.create_all` allowed only in tests.

**Cross-team items (from UX, not yet in PRD/architecture):**
- (a) **New field `Invitation.activity_icon`** (from the UX icon picker): needed by the icon picker, Home cards, plan rows, the Invitation page, and the celebration. Required [ASSUMPTION]; mock list 🍔 🍣 🍕 ☕ 🎬 🍺 (final list open). Must be added through an Alembic migration.
- (b) **New fields `User.avatar` + `User.avatar_color`**: `avatar` = one of 12 emoji faces, `avatar_color` = sun / mint / violet / coral / cream (the shape comes from the color). Chosen once on Pick your avatar right after sign-up; "Skip, surprise me" sets a random face and color; not editable in v1. Must be added through an Alembic migration.
- (c) **Resolved 2026-11-11 (Erfan):** the place/time-changed notification goes to the whole Yes List (`YES` + `YES_PENDING`) and, while Status is Open, to Invitees with `NONE`. Architecture AD-7 table and PRD FR-14 patched.

### UX Design Requirements

**Design tokens and global styles**

UX-DR-1: Color tokens (Notte Pura, dark only, no light mode): implement CSS variables `background #000000`, `surface #141414`, `surface-raised #1F1F1F`, `ink #FFFFFF`, `ink-muted #A3A3A3`, `line #2B2B2B`, `accent #FFB547`, `on-accent #000000`, `inverse #FFFFFF`, `on-inverse #000000`, `error #FF7A6B`; body background is `#000000` on every page.
UX-DR-2: Color usage rules enforced in CSS/templates: amber only for Count me in, Publish, the celebration glow, the "You're in!" bubble, the "just now" Yes List status, and the live dot; every selected state is white (`inverse`), never amber; No is never colored; time left is always white; errors are coral outline + "!" icon + text, never a coral fill.
UX-DR-3: Avatar gradient tokens (135deg, from → to): Sun `#FFD25E→#FF9A1F`, Mint `#4FE3A5→#18B877`, Violet `#7D95FF→#8A5CFF`, Coral `#FF7A6B→#FF4F8B`, Cream `#F7F2E8→#CFC6B4`; used only for avatars, empty-state shapes and confetti, never for UI meaning.
UX-DR-4: Fonts: load Gloock (display serif, weight 400, -0.01em tracking) and Onest (sans) from Google Fonts; Gloock only for big words (screen titles, Invitation title, Home greeting, card titles, "What" input text); Onest for everything else (body, buttons, numbers, labels).
UX-DR-5: Type scale tokens: display-xl 46/1, display-lg 42/1, headline 36/1.05, headline-sm 30/1.1, title 24/1.1 (Gloock); body-lg 16/1.4, body 15/1.45, body-strong 16/600/1.3, meta 14/1.4, caption 13/1.4, label-caps 12/600/0.09em uppercase, button 17/600, button-lg 18/600 (Onest), each used as listed in DESIGN.md Typography.
UX-DR-6: Spacing tokens 4/8/12/16/20/24/32px (`spacing.1`–`spacing.7`), 20px side gutter, `touch-min` 44px; form fields 24px apart, related items 8–12px apart.
UX-DR-7: Radius tokens xs 4px, sm 14px, md 16px, lg 18px, xl 24px, full 9999px, applied as: pills for all buttons/chips/tags/badges/segmented control; xl for cards; lg for big activity tiles and face cells; md for inputs, radio rows, icon cells; sm for small activity tiles; xs only for the Note bubble tail corner.
UX-DR-8: Depth by tone only (#000 → #141414 → #1F1F1F + hairlines); no card shadows; shadows/glows only for the jumping icon, the celebration glow, the "You" ring, and the avatar preview glow.
UX-DR-9: Base layout: single column at 360px, 20px gutter, main action pinned near the bottom of the screen with empty space above; lists use hairline dividers, not boxes; on wider screens the same column is centered with max ~480px and black around it.

**Components (one item each)**

UX-DR-10: Button "Count me in" (`button-yes`): full width, 58px, amber pill, black `button-lg` text; one tap POSTs Yes via HTMX with no confirm dialog; disabled while the request runs (no double send); response swaps in the Yes state and plays the celebration.
UX-DR-11: Button "I'll pass" (`button-no`): exactly the same size and type as Count me in, `surface-raised` pill with white text, directly under it; one tap POSTs No with no confirm and no reason field; response swaps in the Calm No panel; caption "No is always fine. Nobody sees it." under the buttons.
UX-DR-12: Button "Publish" (`button-publish`): amber pill, 58px; server validates the whole form; on error the form returns with the same values and inline errors; on success goes to the Inviter view.
UX-DR-13: Button white (`button-white`, 52px) for Continue and Send, and "+ New plan" (`button-new-plan`, 60px, with "+") which opens New plan.
UX-DR-14: Button ghost (`button-ghost`, transparent with hairline, 52px) for Save as Draft (saves, no notification), Edit place or time (opens edit form), Back to Home.
UX-DR-15: Button text (`button-text`, muted, 44px) for "Cancel plan": shows one simple confirm, then sets Status to Cancelled (FR-13).
UX-DR-16: Back link: "‹ Home" / "‹ My Groups" / "‹ New plan" in `ink-muted`, top left, 44px tall, goes to the parent page; New plan, Create a Group, and Edit place or time use a close "✕" instead.
UX-DR-17: Section label (`label-caps`, muted, uppercase) with an optional count badge (22px white circle, black number) showing how many Invitations wait for an answer; badge hidden at 0.
UX-DR-18: Invitation card (Home): `surface`, 24px radius, 16px padding; activity tile (56px) + `title` serif + meta "Soroush · Fri 21 Nov, 20:00"; after a hairline: avatar stack + "2 going" on the left, Deadline indicator on the right; whole card is one link; sorted by Deadline, soonest first; leaves the section once answered, Deadline passed, or cancelled.
UX-DR-19: Plan row (My Plans): 64px min height, small activity tile (44px), title `body-strong`, meta `caption` ("Sara's plan · Sat 22 Nov, 10:30 · You're in" / "Your plan · only you can see it" for Drafts); right side shows the Updated mark or Draft tag; whole row one link; opening clears Updated; row leaves 24 h after `when_end` (or `when_start`).
UX-DR-20: Updated mark: pill on `surface-raised` with hairline and a white dot, shown when place/time changed, cancelled, or new Note since last open.
UX-DR-21: Draft tag: dashed hairline pill, muted text, shown only to the Inviter.
UX-DR-22: Deadline indicator: white dot + bold time left in plain words ("42 min left", "5 h left"); never changes color; updates on page load (no live countdown).
UX-DR-23: Avatar: emoji face centered on the User's gradient shape (Sun circle, Mint round with sharp bottom-left 10px, Violet round top with 14px bottom, Coral 14px soft square, Cream leaf 50%/10px); sizes 28/40/52/62/132px; small sizes scale corner radii down (10→7px, 14→9px); never initials, photos, or grey icons; labelled with the person's name for screen readers.
UX-DR-24: Avatar stack: 28px avatars overlapping by -8px with 2px `surface` ring; shows the Yes List only (or Members on Group rows), never the Guest List.
UX-DR-25: Activity tile: emoji on `surface-raised`, big 56px (18px radius, 32px emoji) and small 44px (14px radius, 24px emoji); has a text label for screen readers ("Burger").
UX-DR-26: Facts card (Invitation page): `surface` card, 24px radius, rows Where (or "Decide later", address in muted second line) / When (exact or window) / Cost / Answer (Deadline as time left); keys in muted caption, 52px key column; read-only for Invitees.
UX-DR-27: Cost Tag pill: outline pill, bold value Free / $ / $$ / $$$.
UX-DR-28: Going row: "GOING" label + 52px avatars with names under them; shows the current Yes List only; never who was asked, said No, or has not answered; hidden when the Yes List is empty (never "0 going").
UX-DR-29: Celebration stage: 104px round hub (`surface`, hairline) holding the activity emoji (58px); "Reza is in" bubbles (`surface-raised`) around it; "You" last at 62px with amber ring + glow and amber "You're in!" bubble; amber radial glow behind; after the animation it stays as a static header.
UX-DR-30: Yes List (Inviter view): 52px rows with small avatar, name, muted status "is in"; new arrival shows amber "is in · just now" and pops in with a bounce; YES_PENDING rows show the avatar at 50% opacity with a dashed outline and a dashed pill "not confirmed yet" (as text, not style only); shows only YES and YES_PENDING; refreshes by HTMX polling every few seconds while open.
UX-DR-31: Live dot: 7px amber dot + "Updates live" in the Yes List header; pulses softly; no pulse with reduced motion; gone once Closed.
UX-DR-32: Your plan tag: hairline pill top right in the Inviter view.
UX-DR-33: Note bubble: small avatar + name and time in muted caption + `surface` bubble with 4px top-left tail corner and 18px other corners.
UX-DR-34: Note composer: hairline box (20px radius), auto-growing textarea with placeholder "Write a note…", counter "0 / 280" bottom left (counts up, announced to screen readers only near the limit), white Send pill bottom right; Send disabled when empty or over 280; posts via HTMX.
UX-DR-35: Text input: `surface`, 52px, 16px radius, `body-lg`; the "What" input uses the `title` serif; every input has a real label.
UX-DR-36: Icon picker: 6-column grid of emoji cells (`surface`, 16px radius); one choice required; selected = white 2px border on `surface-raised` with `aria-checked`/`aria-pressed`; mock list 🍔 🍣 🍕 ☕ 🎬 🍺.
UX-DR-37: Chip: outline pill, 44px; single choice per group (Cost Tag: Free/$/$$/$$$; Deadline: 10 min/30 min/1 h/3 h); selected = white fill + black text; error = coral 2px outline + coral text (`chip-error`); "Decide later" is a toggle chip that clears and disables the Where input.
UX-DR-38: Segmented control: "Exact time" / "Time window" in a `surface` pill, selected = white; Exact time shows date + time; Time window shows date + start + end.
UX-DR-39: Radio row: `surface`, 56px, 16px radius; selected = white border + white filled dot; "All members" (default, shows avatar stack + count) or "Choose people" (shows "›", opens Choose people).
UX-DR-40: Inline error: coral circled "!" + coral bold line + muted detail line right under the field, with `aria-invalid` and `role="alert"`; message says what is wrong and how to fix (e.g. "The deadline must end before the plan starts." / "3 h ends at 22:18, but the plan starts at 20:00. Try 30 min."); other fields keep their values.
UX-DR-41: Face picker: 4-column grid of 12 emoji faces (`surface`, 18px radius); selected = white 2px border; selection updates the big preview and "Ali is in" chip client-side at once.
UX-DR-42: Color swatch: 52px gradient swatch in its own avatar shape for the 5 colors; selected = black gap + white ring; updates the preview at once.
UX-DR-43: Empty state card: hairline card (24px radius) with three decorative gradient shapes (`aria-hidden`), `headline-sm` serif title, muted line.
UX-DR-44: Calm No panel: small greyed activity tile (grayscale .7, opacity .7) + muted title line, `display-lg` title "Okay. You said no.", muted "Only you can see this.", ghost "Back to Home"; no color, no motion, no list of others.
UX-DR-45: Reconfirm prompt (`reconfirm-card`): `surface` card with white hairline on top of the Invitation page: "Plan changed" label, serif "Still OK?", what changed (old value struck through in muted, new value in white), then **Still in** (`button-white`) and **Not anymore** (`button-no`), same size, stacked, no amber, caption "Not anymore is fine. You just leave the list quietly."; Still in → card disappears, Yes layout stays; Not anymore → removed silently, then Calm No panel; shown only before the plan starts; sends the `place_time_changed_at` the User saw (stale → page reloads).
UX-DR-46: Notification banner: `surface` card at the top of Home, above Waiting for your answer: "🔔 Turn on notifications so you don't miss plans", small white "Turn on" pill (asks browser permission; on iPhone outside the home-screen app opens the Add to Home Screen guide), 44px ✕ dismiss; shown once when notifications are off and the first Invitation arrives; never returns after dismiss.
UX-DR-47: Groups icon button: 44px round hairline button with a two-people line icon, top right of Home above the greeting, screen-reader label "My Groups"; always visible, also on empty Home; opens My Groups.
UX-DR-48: Group picker: `surface` pill "For: Burger Gang 🍔 ▾" at the top of New plan; defaults to the last-used Group (Group of the last published/drafted plan; first time: first Group joined); tap opens a simple list of my Groups; hidden (plain "For: …" line) when the User has only one Group; changing the Group resets Who gets it to All members.
UX-DR-49: Group row (My Groups): 72px min, Group name in `title` serif, meta "7 members" caption, avatar stack, "›"; whole row links to the Group page; sorted by last used.
UX-DR-50: Member row (Group page): 56px, 40px avatar + name in `body-lg`; own row says "you" in muted; read-only; no answer history, "last seen", or Yes counts.
UX-DR-51: Share Group Link button: opens the phone share sheet (Web Share API) with the Group Link; fallback copies the link and shows "Link copied"; caption "Anyone with the link can join this group."; any Member can use it.
UX-DR-52: Check row (Choose people): 56px, avatar + name + 24px rounded (8px) checkbox on the right; tap anywhere toggles; checked = white box with black ✓; starts with nobody checked; "Select all" toggles all; "Done" shows the count, is disabled at 0, and returns to New plan with Who gets it reading "3 people".
UX-DR-53: Status banner: `surface-raised` strip with hairline, `body-strong` white text + emoji on top of the Invitation page ("Soroush cancelled this plan.", "Answers are closed.", "You cancelled this plan."); never colored, no motion.

**State patterns (Invitation page and other surfaces)**

UX-DR-54: Invitation page, Unanswered (Open), Invitee: header "Soroush invites you", activity icon + `display-xl` title, facts card, Going row, Count me in / I'll pass, "No is always fine. Nobody sees it."; Going row hidden when the Yes List is empty.
UX-DR-55: Invitation page, Just said Yes: celebration plays, then title (`headline`) + facts line, Notes, drop-out hint "Can't come anymore? Just say it here."; no "Change answer".
UX-DR-56: Invitation page, Said Yes (later visits): same Yes layout, final frame, no animation.
UX-DR-57: Invitation page, Said No (now or later): Calm No panel only, no animation, no list of others.
UX-DR-58: Invitation page, Not confirmed yet (YES_PENDING): Reconfirm prompt on top, then the Yes layout.
UX-DR-59: Invitation page, Deadline passed with no answer (Invitee): removed from Waiting for your answer; if opened by an old link, status banner "Answers are closed." + "This one's done. No worries." + facts, no buttons, no Going row.
UX-DR-60: Invitation page, Cancelled (Yes List): status banner "Soroush cancelled this plan." + "Notes stay open, if you want to chat."; greyed hub icon; Notes readable and writable; plan row shows Updated; unanswered Invitees no longer see it.
UX-DR-61: Invitation page, Inviter Open: "Your plan" tag, facts line, "Answers close in 36 min", live Yes List, Notes ("Only you and people going"), Edit place or time (hidden once the plan starts), Cancel plan.
UX-DR-62: Invitation page, Inviter Closed with Yes: same as Open but "Answers closed", no countdown, no live dot; Edit place or time until the plan starts; Cancel plan stays.
UX-DR-63: Invitation page, Inviter Closed with empty Yes List: empty-state card "Nobody is free tonight 🌙" + "Your plan is still on. Going solo works too."; never "0 people".
UX-DR-64: Invitation page, Inviter Cancelled: status banner "You cancelled this plan."; final Yes List and Notes (readable and writable); no Edit place or time, no Cancel plan.
UX-DR-65: Draft (Inviter): New plan form prefilled with a Draft tag, "Only you can see this.", actions Publish / Save as Draft / Delete draft.
UX-DR-66: Time window display: "Sat 22 Nov, 19:00–22:00" with "Anytime in this window" under it, everywhere the plan is shown.
UX-DR-67: Hidden / not allowed Invitation: standard 404 page that never reveals the Invitation exists.
UX-DR-68: Home empty: empty-state card "Nothing waiting." / "Start a plan?"; New plan stays one tap away.
UX-DR-69: My Plans empty: "Plans you make or say Yes to will show here."
UX-DR-70: Form error state (New plan, Edit place or time): inline error per broken field, all other values kept.
UX-DR-71: Network/server error on any HTMX action: short coral inline line near the button ("Couldn't send. Try again."), button re-enabled, nothing lost, Answer not saved until success.
UX-DR-72: Conflict (409, e.g. answer already set, stale reconfirm): the page reloads to the true state.
UX-DR-73: Cold load: server-rendered full page, no skeleton loaders; offline = PWA shell only (no offline design in v1).

**Yes celebration interaction**

UX-DR-74: Yes celebration sequence (~3 s, plays once, only on the Count me in response): 0 s icon (130px) jumps up past the top of the screen, rotating a little, then fades (1.5 s, springy) with six confetti bits (avatar gradients + amber); 0 s amber glow fades in (2.6 s) then stays; 0.5 s title and facts line rise in; 0.95 s icon lands in the hub with a bounce (0.7 s); from 1.35 s avatars pop in one by one (0.55 s each, 0.35 s apart) with "X is in"; last, "You" pops in bigger with amber ring, glow and "You're in!"; 2.5 s Notes and drop-out hint rise in. The animation is the same every time (no streaks or counters).
UX-DR-75: Celebration vibration: one short buzz at step 1 on Android only (Vibration API, feature-detected); nothing on iPhone; no vibration with reduced motion.
UX-DR-76: Celebration sound: off by default (no sound in v1 unless a setting is added later).
UX-DR-77: Reduced motion (`prefers-reduced-motion: reduce`): skip jump, confetti, glow growth, pop-ins, rise-ins and the live-dot pulse; show the final state at once; the final state never depends on the animation.
UX-DR-78: Only Yes celebrates: No and every other action have no motion, sound or vibration; a Yes sent from an Android notification button plays no celebration (next open shows the final frame); the only other motion is the new Yes List row bounce and the live-dot pulse; no page transitions or hover effects.

**Voice and microcopy**

UX-DR-79: All user-facing strings must match the EXPERIENCE.md Voice and Tone table exactly (e.g. "Count me in", "I'll pass", "No is always fine. Nobody sees it.", "You're in!", "Okay. You said no. / Only you can see this. / Back to Home", "Hi Ali", "Waiting for your answer", "My Plans", "+ New plan", "Soroush invites you", facts keys "Where · When · Cost · Answer", New plan labels, "Decide later" helper, Deadline helper, "Publish · Save as Draft · Nobody gets a message until you publish.", Notes privacy lines, sign-up/log-in/Group Link/Add to Home Screen/My Groups/Group page/Create a Group/Choose people/Edit place or time/Cancelled/Closed/Draft strings, "Still in" / "Not anymore"); dates always as `Fri 21 Nov, 20:00`.
UX-DR-80: Banned copy and patterns: no "Decline", "Reject", "No thanks 😢", "Are you sure?", "You'll miss out!", "Maybe next time?", "0 people are coming", "Hurry!", "Invalid input", "Error 409"; no "Change answer", confirm dialogs on Yes/No, reason fields, comment/"suggest another plan" fields before answering, counts of who was asked, streaks, scores, red countdowns, guilt copy, pull-to-refresh, infinite scroll.
UX-DR-81: Notification and result texts (new Invitation, Deadline result incl. "Nobody is free tonight 🌙", "Soroush cancelled: Burger tonight 🍔", place/time changed) live only in `app/notifications/messages.py`; Android notification buttons use the same labels "Count me in" / "I'll pass".

**Accessibility floor**

UX-DR-82: Every interactive element is at least 44px tall.
UX-DR-83: Screen reader announcements: an `aria-live="polite"` region announces "You're in! <title>" after Yes and "Okay. You said no." after No; decorative shapes, confetti and the jumping icon are `aria-hidden`.
UX-DR-84: Avatars are labelled with the person's name; activity icons have a text label.
UX-DR-85: Color is never the only signal: errors use coral + "!" + text with `aria-invalid` and `role="alert"`; selected chips/cells use `aria-pressed` or `aria-checked`; "not confirmed yet" is text; the Deadline is text.
UX-DR-86: Visible focus ring (2px white outline) on every interactive element; after an HTMX swap, focus moves to the new state's heading (Yes, No, error).
UX-DR-87: Every form input has a real `<label>`; the 280 counter is announced only near the limit.
UX-DR-88: Layout survives 200% text zoom at 360px with no sideways scroll; all text pairs pass WCAG AA (lowest 7.3:1).

**Responsive and PWA**

UX-DR-89: Web app manifest: name, icons, `display: standalone`, `theme_color` and `background_color` `#000000`, start URL Home; installable from the browser.
UX-DR-90: Service worker: registers on load, receives Web Push, shows notifications with what/where/when/Deadline; on Android/desktop shows "Count me in" / "I'll pass" action buttons that POST the signed token; on tap (or on iPhone) opens the Invitation page directly.
UX-DR-91: Safe-area insets respected (notch, home bar) in standalone mode; theme color meta tag `#000000`.
UX-DR-92: Add to Home Screen guide (iPhone Safari only, after joining via Group Link): "One more thing · Put the app on your home screen, so plans can reach you. · Tap Share ⬆ · Tap "Add to Home Screen" · Open it from your home screen and log in once · Done, it's there · Skip for now"; not shown on Android or inside the installed app.
UX-DR-93: Notification permission flow: after onboarding (and from the banner "Turn on"), ask browser permission, create a `PushSubscription`, record `push_enabled`/`push_disabled` Events.

**Screen surfaces (Information Architecture)**

UX-DR-94: Group Link landing page (public): shows only "Soroush invited you to" + Group name ("Burger Gang 🍔"), "Join the group" and "I already have an account"; nothing else about the Group.
UX-DR-95: Sign up page: "Hey, welcome 👋 · Takes less than a minute.", fields Your name (hint "Friends see this name."), Email, Password, button "Make my account", link "Already have one? Log in"; completes in under 1 minute.
UX-DR-96: Log in page: "Welcome back", Email, Password, "Log in", "New here? Sign up".
UX-DR-97: Pick your avatar page (first time after sign-up only): "Welcome, Ali · Pick your avatar · Friends see it when you say Yes.", 132px preview with its own colored glow, "Ali is in" chip, Face picker (12), Color swatches (5), Continue (saves `User.avatar` + `User.avatar_color` and goes on), "Skip, surprise me" link (random face + color); not editable later in v1.
UX-DR-98: Home page: Groups icon top corner, greeting "Hi <name>" (`display-lg`), optional notification banner, WAITING FOR YOUR ANSWER section (always on top, count badge, Invitation cards, or empty state), MY PLANS section (plan rows or empty line), big "+ New plan" button at the bottom; no tab bar or drawer.
UX-DR-99: My Groups page: "‹ Home", title "My Groups", Group rows, "+ Create a Group" button.
UX-DR-100: Group page: "‹ My Groups", Group name, "7 members", Member rows (own row "you"), Share Group Link button + caption.
UX-DR-101: Create a Group page: close "✕", "New group", Group name field (hint "Like "Burger Gang 🍔". You can share the link next."), "Create group" button; after create → the new Group page.
UX-DR-102: New plan page: close "✕", "New plan" title, Group picker, then Pick an icon → What → Where (+ Decide later) → When (segmented control) → Cost → Deadline (helper "How long friends have to answer.") → Who gets it (radio rows) → Publish + Save as Draft + "Nobody gets a message until you publish."
UX-DR-103: Choose people page: "‹ New plan", "Choose people", "From Burger Gang 🍔", Select all, Check rows, Done with count.
UX-DR-104: Edit place or time page: close "✕", "Edit place or time", "Only place and time can change.", "People who said Yes get a message and need to confirm it still works.", Where and When fields prefilled (same as New plan), inline Deadline error if the Deadline no longer ends before the new start, "Save changes"; only reachable before the plan starts.
UX-DR-105: Invitation page: one URL whose state is chosen by the server (UX-DR-54..UX-DR-67); reached from Invitation cards, plan rows, and notification taps.
UX-DR-106: Navigation rule: answer, create and My Plans each within 2 taps of Home (My Plans is on Home); every inner page has a back link or close; no tab bar, no drawer.

### FR Coverage Map

FR-1: Epic 1 - Sign up and log in (name, email, password; under 1 minute)
FR-2: Epic 1 - Create a Group
FR-3: Epic 1 - Join a Group with a Group Link
FR-4: Epic 2 - Create an Invitation (icon, what, where, when, Cost Tag, Deadline)
FR-5: Epic 2 - Choose the Guest List
FR-6: Epic 2 - See Open Invitations ("Waiting for your answer")
FR-7: Epic 2 - Nobody else can change an Invitation
FR-8: Epic 2 - Answer Count me in / I'll pass (notification buttons in Epic 4)
FR-9: Epic 2 - Silent No
FR-10: Epic 2 - Deadline ends answering (result notification in Epic 4)
FR-11: Epic 3 - Notes for the Inviter and the Yes List
FR-12: Epic 4 - Notifications and the notifications-off banner
FR-13: Epic 3 - Cancel an Invitation (cancel notification in Epic 4)
FR-14: Epic 3 - Edit place or time + reconfirm (change notification in Epic 4)
FR-15: Epic 2 - Save as Draft
FR-16: Epic 2 - My Plans with the Updated mark

## Epic List

### Epic 1: Join the crew
Friends sign up, pick an avatar, create a Group, share the Group Link and join it. The app is live on Fly.io from the start. Starts with creating the project from scratch (no starter template); includes the admin password-reset command.
**FRs covered:** FR-1, FR-2, FR-3

### Epic 2: Make a plan, get real answers
The Inviter creates an Invitation (activity icon, Guest List, Cost Tag, Deadline, or Draft). Invitees see "Waiting for your answer" on Home and answer Count me in (with the celebration) or I'll pass. Silent No, the Deadline, the Yes List and My Plans work end to end inside the app.
**FRs covered:** FR-4, FR-5, FR-6, FR-7, FR-8, FR-9, FR-10, FR-15, FR-16

### Epic 3: Plans can change
The Yes List coordinates with Notes; the Inviter can cancel a plan or edit its place or time, and the Yes List answers Still in / Not anymore.
**FRs covered:** FR-11, FR-13, FR-14

### Epic 4: Plans reach your pocket
The app installs on the phone and sends Web Push notifications (new Invitation, Deadline result, cancelled, place/time changed); Android users answer from the notification; the notifications-off banner; metrics for the 4-week test (SM-0 to SM-4, SM-C1, SM-C2).
**FRs covered:** FR-12 (plus the notification parts of FR-8, FR-10, FR-13, FR-14)

## Epic 1: Join the crew

Friends sign up, pick an avatar, create a Group, share the Group Link and join it. The app is live on Fly.io from the start.

### Story 1.1: The app runs on my laptop

As a developer (Erfan),
I want a new project created from scratch with uv that shows a "hello" page in the Notte Pura style,
So that I have a working base on my laptop where every future story is built and tested.

**Acceptance Criteria:**

**Given** a new folder with no starter template
**When** the project is set up with uv on Python 3.14
**Then** it contains the source tree from the architecture (`app/main.py`, `app/config.py`, `app/models/`, `app/services/`, `app/notifications/`, `app/jobs/`, `app/routes/`, `app/templates/` with `fragments/`, `app/static/`, `migrations/`, `tests/`)
**And** all dependencies are pinned to the architecture's Stack versions (FastAPI 0.162.x, python-multipart, SQLModel 0.0.49, Alembic 1.20.1, Jinja2 3.1.6, pwdlib[argon2] 0.3.1, itsdangerous, pydantic-settings, pywebpush 2.5.0) and HTMX 2.0.11 is served from `app/static/`

**Given** the project is set up
**When** I run the app locally and open `/`
**Then** I see a page rendered from a base layout with the Notte Pura tokens (UX-DR-1, UX-DR-4, UX-DR-5, UX-DR-6, UX-DR-7, UX-DR-8, UX-DR-9): black background, Gloock + Onest fonts, 20px side gutter, no sideways scroll at 360px (NFR-1)
**And** the base styles set the shared rules every later screen uses: amber is used only for the few allowed things and every selected state is white (UX-DR-2); every button and interactive element is at least 44px tall (NFR-2, UX-DR-82); every interactive element has a visible 2px white focus ring (UX-DR-86); the layout survives 200% text zoom at 360px with no sideways scroll, and all text color pairs pass WCAG AA (UX-DR-88)
**And** settings come only from environment variables through `app/config.py` (no secret in git)

**Given** the project is set up
**When** code is added in any later story
**Then** it follows the AD-1 layer rule: imports go only routes/jobs → services → models (and notifications); only services (and `notifications` for subscriptions) touch the database session; nothing imports from `routes`
**And** there is one exception handler that turns the service errors `NotFound`, `NotAllowed` and `InvalidState` into a 404, 403 or 409 page (or a fragment for HTMX requests), with a test for each one
**And** logging uses Python `logging` to stdout, one line per event, and never logs passwords, cookies, tokens or push keys

**Given** the project is set up
**When** I run `pytest`
**Then** at least one test passes that opens `/` and checks the response
**And** Alembic is configured with `render_as_batch=True` and an empty first migration runs on a SQLite file in WAL mode (AD-10, AD-8)
**And** the shared `UTCDateTime` column type exists in `app/models/` (AD-6)
**And** the project is a git repository with a `.gitignore` that excludes the database file and `.env`

### Story 1.2: The app is live on the internet

As Erfan,
I want the hello page running on Fly.io,
So that my friends can reach the app and every later story can go live in minutes (enabler for FR-1..FR-16; NFR-1, NFR-12).

**Acceptance Criteria:**

**Given** the app from Story 1.1
**When** I deploy it to Fly.io
**Then** exactly one Machine runs with one Uvicorn worker, `auto_stop_machines = "off"` and `min_machines_running = 1` (AD-8)
**And** a 1 GB Fly volume is mounted and `DATABASE_URL` points to a SQLite file on it, in WAL mode

**Given** a deploy is started
**When** the new version starts
**Then** Alembic migrations run before the app starts (AD-10)
**And** secrets (session secret, later VAPID keys) are set with `fly secrets`, never in git

**Given** the app is deployed
**When** I open the public HTTPS URL on my phone
**Then** I see the same hello page as on my laptop
**And** after a redeploy, data in the SQLite file is still there (the volume survives)
**And** daily Fly volume snapshots are turned on as the backup

### Story 1.3: Sign up, log in and log out

As a friend (Ali),
I want to create an account with my name, email and password and log in,
So that the app knows who I am and can keep my answers private.

**Acceptance Criteria:**

**Given** I am not logged in
**When** I open the Sign up page (UX-DR-95) and enter my name, email and a password
**Then** a `User` row is created (this story creates the `User` table through a migration) with the password hashed by pwdlib Argon2 (AD-9)
**And** I am logged in, and sign-up takes under 1 minute (FR-1, NFR-5)
**And** every field is a text input in the shared style (`surface`, 52px, 16px radius, `body-lg`) with a real label (UX-DR-35, UX-DR-87)

**Given** I have an account
**When** I log in on the Log in page (UX-DR-96) with the right email and password
**Then** a signed session cookie holding only my User id and a CSRF token is set (Story 1.7 later adds `session_version`): HttpOnly, SameSite=Lax, https_only in production, 90-day lifetime (AD-9)
**And** with a wrong password I see an inline coral error (UX-DR-40) and stay logged out

**Given** I am logged in
**When** I log out
**Then** my session is cleared and pages that need login send me to Log in

**Given** any page except sign-up, log-in, static files and the Group Link landing page
**When** I open it without being logged in
**Then** the `current_user` dependency sends me to Log in (AD-9)
**And** every POST form carries the CSRF token and a POST without a valid token is refused (AD-9)
**And** HTMX requests send the token in the `X-CSRF-Token` header, set once on the page with `<body hx-headers>` in the base layout (AD-9)
**And** passwords, cookies and tokens never appear in logs

### Story 1.4: Pick your avatar

As a new friend (Ali),
I want to pick a face and a color right after sign-up, or let the app surprise me,
So that my friends see me as a fun avatar instead of just a name (FR-1 onboarding; UX handoff fields `avatar`, `avatar_color`).

**Acceptance Criteria:**

**Given** I just signed up
**When** the Pick your avatar page opens (UX-DR-97)
**Then** I see 12 faces (UX-DR-41), 5 color swatches (UX-DR-42, UX-DR-3) and a big live preview (UX-DR-23)
**And** this story adds `avatar` and `avatar_color` to `User` through a migration

**Given** I picked a face and a color
**When** I tap Continue
**Then** my choice is saved and I go to a simple placeholder start page that says "Hi Ali" (Story 1.5 turns this page into Home)

**Given** I don't want to choose
**When** I tap "Skip, surprise me 🎲"
**Then** a random face and color are saved and I go to the same placeholder start page
**And** the page is shown only once; in v1 there is no screen to change the avatar later

**Given** any later screen that shows me
**When** my avatar is drawn
**Then** it is the emoji face on my color's gradient shape, labelled with my name for screen readers (UX-DR-84)

### Story 1.5: Create a Group

As Soroush,
I want to create a Group and see its Members,
So that I have a place to invite my friends.

**Acceptance Criteria:**

**Given** I am logged in
**When** I open Home (this story turns the placeholder start page from Story 1.4 into a simple Home with greeting "Hi Soroush" and the Groups icon top right, UX-DR-47, UX-DR-98)
**Then** one tap on the Groups icon opens My Groups (UX-DR-99), with "+ Create a Group"
**And** every inner page has a back link at the top left ("‹ Home", "‹ My Groups") that goes to the parent page, and Create a Group uses a close "✕" instead (UX-DR-16)

**Given** I am on Create a Group (UX-DR-101)
**When** I enter a name like "Burger Gang 🍔" and save
**Then** a `Group` and my `Membership` are created (this story creates both tables; `Group` already includes a unique random `link_token` column, filled with `secrets.token_urlsafe` on creation, used by Story 1.6) and I am its first Member (FR-2)
**And** I land on the Group page (UX-DR-100) showing the name, "1 member" and my Member row with "you" (UX-DR-50)

**Given** I am in several Groups
**When** I open My Groups
**Then** I see one Group row per Group (UX-DR-49), sorted by last used
**And** I never see Groups I am not a Member of (AD-2, NFR-6)
**And** the Group page and Member rows never show anyone's past Answers: no answer history, no Yes counts, no "last seen" (NFR-7)

### Story 1.6: Join with a Group Link

As Ali,
I want to open the link Soroush shared and join his Group,
So that I can get his plans.

**Acceptance Criteria:**

**Given** I am a Member on a Group page
**When** I tap Share Group Link (UX-DR-51)
**Then** the phone share sheet opens with the Group Link (a random token from `secrets.token_urlsafe`, never the database id)
**And** if sharing is not available, the link is copied and I see "Link copied"

**Given** I am not logged in and I open a Group Link
**When** the landing page loads (UX-DR-94)
**Then** I see only "Soroush invited you to" and the Group name, then sign up (or log in)
**And** after signing up (and picking an avatar) I become a Member and land on the Group page (FR-3)

**Given** I am logged in and I open a Group Link
**When** I tap "Join the group"
**Then** I become a Member and see the Group and its Members
**And** if I am already a Member, I just see the Group page (no duplicate Membership)

**Given** someone joins a Group
**When** the Membership is created
**Then** an `Event` row `group_joined` is recorded (this story creates the `Event` table; AD-12) with no personal content

**Given** an invalid or unknown Group Link
**When** it is opened
**Then** a normal "not found" page is shown

### Story 1.7: Admin: reset a friend's password

As Erfan (the admin),
I want a small command that sets a new password for a friend,
So that a friend who forgot their password can log in again without an email service (FR-1, NFR-6).

**Acceptance Criteria:**

**Given** I can run commands on my laptop or on the Fly.io machine
**When** I run the reset command with a friend's email
**Then** it asks me for a new password (not shown on screen) and saves it hashed with Argon2
**And** the friend's old sessions stop working: this story adds a `session_version` integer to `User` through a migration (default 0); the value is stored in the session cookie at log-in, `current_user` refuses a session whose `session_version` does not match the User's current value (sends to Log in), and the reset command increases `session_version` by 1

**Given** the email does not belong to any User
**When** I run the command
**Then** it says so clearly and changes nothing

**Given** the command runs
**When** it finishes
**Then** the password never appears in logs or in the terminal history

## Epic 2: Make a plan, get real answers

The Inviter creates an Invitation; Invitees find it on Home and answer Count me in or I'll pass. Silent No, the Deadline, the Yes List and My Plans work end to end inside the app.

### Story 2.1: Create and publish a plan

As Soroush,
I want to create a plan with an icon, what, where, when, a Cost Tag and a Deadline, and publish it to my Group,
So that my friends can answer it (FR-4).

**Acceptance Criteria:**

**Given** I am a Member of at least one Group
**When** I tap "+ New plan" on Home (UX-DR-13, UX-DR-98)
**Then** the New plan page opens (UX-DR-102) with the Group picker defaulting to my last-used Group (UX-DR-48; hidden if I am in only one Group), the icon picker (UX-DR-36), What, Where (or "Decide later"), When as an exact time, Cost Tag chips Free/$/$$/$$$ and Deadline chips 10 min / 30 min / 1 h / 3 h (UX-DR-37)
**And** "Who gets it" is "All members" in this story (choosing people comes in Story 2.7)

**Given** I filled the form
**When** I tap Publish (UX-DR-12)
**Then** an `Invitation` is created with `activity_icon`, `what`, `where` (null = open), `when_start`, `cost_tag`, `deadline_minutes`, and `publish()` sets `published_at` and `deadline_at = published_at + deadline_minutes` (AD-4)
**And** this story creates the `Invitation` and `GuestListEntry` tables; the `Invitation` migration creates the full AD-4 column set now: `what`, `where`, `when_start`, `when_end` (nullable), `cost_tag`, `deadline_minutes`, `activity_icon`, `published_at`, `deadline_at`, `cancelled_at`, `place_time_changed_at`, `result_notified_at`; `when_end`, `cancelled_at`, `place_time_changed_at` and `result_notified_at` stay null until the stories that use them (2.8, 3.2, 3.3, 4.5), so `status()` can already read `cancelled_at`
**And** one `GuestListEntry` with answer `NONE` is written for every other current Member; the Inviter has no row (AD-5)
**And** the Guest List is fixed at publish: a Member who joins the Group later never sees this Invitation or any older one (AD-5)
**And** an `Event` `invitation_published` is recorded (AD-12)
**And** after Publish I land on the plan's Invitation page in the Inviter view (UX-DR-12), so I can always reach my new plan before My Plans exists (Story 2.10)

**Given** I enter or see a date and time
**When** the form is read or the plan is shown
**Then** times are typed and shown in `Europe/Rome` time and stored in UTC; the conversion happens only in forms and templates, and every date shows as `Fri 21 Nov, 20:00` (AD-6, UX-DR-79)

**Given** the chosen Deadline would end at or after "when"
**When** I tap Publish
**Then** nothing is saved and an inline coral error says "The deadline must end before the plan starts." with a hint (UX-DR-40, UX-DR-70); my other inputs stay filled
**And** the error is never shown by color only: it has a coral outline, a "!" icon and text, with `aria-invalid` and `role="alert"`, and selected chips and icon cells use `aria-pressed` or `aria-checked` (UX-DR-85)

**Given** an Invitation exists
**When** any code needs its Status
**Then** it uses the single `status(invitation, now)` function (Draft / Open / Closed / Cancelled, no status column) and tests use a fixed `now` (AD-4, AD-6)

### Story 2.2: Waiting for your answer

As Ali,
I want to see new plans for me at the top of Home and open one,
So that I never have to search for a plan I still need to answer.

**Acceptance Criteria:**

**Given** I am an Invitee on an Open Invitation and have not answered
**When** I open Home
**Then** "Waiting for your answer" is the first section (UX-DR-17 with count badge), showing an Invitation card per plan (UX-DR-18) with the activity tile (UX-DR-25), title, Inviter, when, time left (UX-DR-22) and the avatar stack of the Yes List only (UX-DR-24), sorted by Deadline, soonest first (FR-6)
**And** if nothing is waiting, Home shows the empty state card (UX-DR-43) "Nothing waiting." / "Start a plan?" (UX-DR-68)

**Given** I tap an Invitation card
**When** the Invitation page opens (UX-DR-105)
**Then** I see the Unanswered state (UX-DR-54): who invites me, activity tile (UX-DR-25), title, the Facts card (UX-DR-26) with where, when, the Cost Tag pill (UX-DR-27), time left, and the Going row with the current Yes List (UX-DR-28)
**And** I see the Yes List before answering, but never the Guest List or anyone's No (FR-9, NFR-8)
**And** no card or page shows how many people were asked (NFR-9)

**Given** any read of an Invitation
**When** the page or fragment is built
**Then** it goes through `visibility.get_visible_invitation(user, id, now)` in `app/services/visibility.py` (AD-2)
**And** a Member not on the Guest List, or anyone opening a Draft of someone else, gets a normal 404 that never shows the Invitation exists (UX-DR-67, NFR-6)
**And** a test proves a hidden Invitation and a `NO` answer never appear on Home or the Invitation page
**And** the test for "someone else's Draft gives 404" creates the Draft row directly in the test database (the Draft screens come in Story 2.9)

### Story 2.3: Count me in or I'll pass

As Ali,
I want to answer with one tap, without giving a reason,
So that saying no is as easy and safe as saying yes.

**Acceptance Criteria:**

**Given** I am on an Open Invitation I have not answered
**When** I see the two answer buttons
**Then** "Count me in" (amber, UX-DR-10) and "I'll pass" (UX-DR-11) have exactly the same size; there is no reason field (FR-8)

**Given** I tap "Count me in"
**When** the answer is saved
**Then** my `GuestListEntry` changes `NONE → YES` with a conditional update (`WHERE answer = 'NONE'`); 0 rows changed means `InvalidState` and the page reloads to the true state (AD-5, UX-DR-72)
**And** the page shows the Said Yes layout with the Going row including me (UX-DR-56); the celebration comes in Story 2.4, and the Notes area and the drop-out hint are added in Story 3.1

**Given** I tap "I'll pass"
**When** the answer is saved
**Then** `NONE → NO` is saved and I see the Calm No panel "Okay. You said no. Only you can see this." with no animation (UX-DR-44, UX-DR-57)
**And** nobody else ever sees my No: not the Inviter, not other Invitees (FR-9, AD-2)

**Given** I already answered
**When** I come back to the Invitation
**Then** I see my answer's layout; there is no "Change answer" option (FR-8: Answers are final in v1)
**And** every answer records an `Event` `answered` without saying Yes or No to anyone else (AD-12)
**And** all texts match the Voice table (UX-DR-79) and no banned copy is used (UX-DR-80)

**Given** I tap an answer button and the network or server fails
**When** the HTMX request does not succeed
**Then** a short coral line "Couldn't send. Try again." shows near the button, the button works again, nothing is lost, and my Answer is not saved until a request succeeds (UX-DR-71)

**Given** an HTMX answer request succeeds
**When** the new state is swapped in (Yes, No or an error)
**Then** keyboard and screen reader focus moves to the heading of the new content (UX-DR-86)

### Story 2.4: The Yes celebration

As Ali,
I want a little party when I tap "Count me in",
So that saying yes to my friends feels fun.

**Acceptance Criteria:**

**Given** I just tapped "Count me in"
**When** the response arrives
**Then** the celebration plays once (~3 s, UX-DR-74, UX-DR-29): the activity icon jumps out past the top of the screen, then the Yes List avatars pop in one by one ("Reza is in", "Sara is in", "You're in!") with an amber glow, then the page settles in the Said Yes layout (UX-DR-55; the Notes area and the drop-out hint are added in Story 3.1) (FR-8)
**And** an `aria-live="polite"` region announces "You're in! <title>" (UX-DR-83)

**Given** I am on Android with vibration support
**When** the celebration starts
**Then** the phone gives one short buzz (UX-DR-75); on iPhone nothing breaks and there is no buzz
**And** no sound plays (UX-DR-76)

**Given** my device asks for reduced motion
**When** I tap "Count me in"
**Then** the final state shows at once, with no jump, pop-ins, glow growth or vibration (UX-DR-77)

**Given** I visit the Invitation later, or I tapped "I'll pass"
**When** the page loads
**Then** there is no animation, sound or vibration (UX-DR-56, UX-DR-78)

### Story 2.5: Watch the Yes List grow

As Soroush,
I want to see who is coming while friends answer,
So that I know quickly if my plan is happening.

**Acceptance Criteria:**

**Given** I am the Inviter of an Open Invitation
**When** I open it (right after Publish, or by its link)
**Then** I see the Inviter view (UX-DR-61): "Your plan" tag (UX-DR-32), facts line, "Answers close in 36 min", and the Yes List rows (UX-DR-30) with the live dot "Updates live" (UX-DR-31)
**And** I see only the Yes List, never who said No or who has not answered (FR-9, AD-2)
**And** Notes, Edit place or time and Cancel plan are added in Epic 3

**Given** the visibility rules in `app/services/visibility.py`
**When** the tests for this story run (services tested directly with a fixed `now`)
**Then** a test proves the Guest List is returned only to the Inviter, never to an Invitee
**And** a test proves the Yes List returns only `YES` and `YES_PENDING` entries (pending marked "not confirmed yet") and never a `NO` or `NONE` entry (AD-2)

**Given** the Inviter view is open
**When** a friend answers "Count me in"
**Then** the Yes List refreshes by HTMX polling every few seconds and the new person pops in as "just now"; the page returns only a fragment for HTMX requests (AD-11)
**And** with reduced motion the new row appears without animation

### Story 2.6: The Deadline closes the plan

As Soroush and as Ali,
I want answering to stop exactly when the Deadline passes,
So that everyone knows the result and nobody waits forever.

**Acceptance Criteria:**

**Given** an Open Invitation
**When** `now` passes `deadline_at`
**Then** `status()` returns Closed, the answer buttons are gone, and an answer request is refused with `InvalidState` (FR-10, AD-3, AD-4)
**And** a test with a fixed `now` checks the exact second

**Given** I am an Invitee who never answered
**When** the Deadline has passed
**Then** the plan leaves "Waiting for your answer", and if I open it I see "Answers are closed" with no buttons and no Going row (UX-DR-59)
**And** my missing Answer counts as No: I am not on the Yes List and, like a No, it is never shown to anyone (FR-10, AD-5)

**Given** I am the Inviter and the Deadline has passed
**When** I open my plan
**Then** I see "Answers closed" with the final Yes List (UX-DR-62)
**And** if the Yes List is empty I see the empty-state card "Nobody is free tonight 🌙" with "Your plan is still on. Going solo works too." and never "0 people" (UX-DR-63, FR-10)
**And** Notes, Edit place or time and Cancel plan are added in Epic 3

### Story 2.7: Choose people

As Soroush,
I want to send a plan to only some Members of my Group,
So that I can invite just the people I want, even only one.

**Acceptance Criteria:**

**Given** I am on New plan
**When** I choose "Choose people" in "Who gets it" (UX-DR-39)
**Then** the Choose people page opens (UX-DR-103) with a Check row per other Member (UX-DR-52), nobody checked, "Select all", and Done disabled at 0

**Given** I chose some people and publish
**When** the Invitation is created
**Then** `GuestListEntry` rows exist only for the chosen Members (FR-5)
**And** Members not chosen never see the Invitation anywhere: Home, My Plans, links (404) (AD-2)

**Given** I change the Group in the Group picker
**When** I had chosen people before
**Then** "Who gets it" resets to "All members"

### Story 2.8: Plan with a time window

As Soroush,
I want to say "anytime between 19:00 and 22:00" instead of an exact time,
So that friends can join a flexible plan.

**Acceptance Criteria:**

**Given** I am on New plan
**When** I switch the segmented control to "Time window" (UX-DR-38)
**Then** I can enter a date, a start and an end time, and `when_end` is saved (FR-4, AD-4)
**And** the end must be after the start, and the Deadline must end before the start (inline error otherwise, UX-DR-40)

**Given** a plan with a time window
**When** anyone who may see it opens it
**Then** "when" shows as "Sat 22 Nov, 19:00–22:00" with "Anytime in this window" (UX-DR-66), in Europe/Rome time (AD-6)

### Story 2.9: Save as Draft

As Soroush,
I want to save a plan without sending it,
So that I can finish it later.

**Acceptance Criteria:**

**Given** I am on New plan
**When** I tap "Save as Draft" (UX-DR-14)
**Then** the Invitation is saved with `published_at` empty (Status Draft), nobody is notified, and only I can see it (FR-15, AD-2)
**And** I land on my Draft's page, so I can open it again by its link before My Plans exists (Story 2.10)

**Given** I open my Draft
**When** the page shows it
**Then** I see the form prefilled with the Draft tag (UX-DR-21) and "Only you can see this." (UX-DR-65), and I can edit any field, Publish, or Delete draft (AD-3)
**And** the Deadline starts counting only when I publish (`deadline_at` set by `publish()`), and the Guest List is written at publish time from the current Members or my chosen people (AD-5)

**Given** another Member
**When** they try to open my Draft's link
**Then** they get a 404

**Given** someone who is not the Inviter
**When** they try to edit, publish or delete a Draft
**Then** they get a 404, because only the Inviter can see a Draft (FR-7, AD-2)

**Given** an Invitee who can see a published plan (not the Inviter)
**When** they send a request to edit or publish it
**Then** they get a 403 `NotAllowed`; a User who cannot see the plan gets a 404 `NotFound` instead, so the plan's existence is never shown (FR-7, AD-2)

### Story 2.10: My Plans

As Ali,
I want one list of plans I made or said yes to,
So that I can find my evening plans quickly.

**Acceptance Criteria:**

**Given** I created plans or answered "Count me in"
**When** I open Home
**Then** "My Plans" is below "Waiting for your answer", with one Plan row each (UX-DR-19) showing icon, title, when, and a Draft tag on my Drafts (FR-16)
**And** plans I said No to never appear there
**And** Closed and Cancelled plans stay in My Plans (until 24 hours after "when")

**Given** a plan's time has passed
**When** 24 hours have passed after `when_end` (or `when_start`)
**Then** it no longer shows in My Plans

**Given** I have no plans
**When** I look at My Plans
**Then** I see "Plans you make or say Yes to will show here." (UX-DR-69)
**And** creating, answering and opening My Plans are each within 2 taps of Home (NFR-3, UX-DR-106)

## Epic 3: Plans can change

The Yes List coordinates with Notes; the Inviter can cancel a plan or edit its place or time, and the Yes List answers Still in / Not anymore.

### Story 3.1: Notes for the Yes List

As Ali (on the Yes List) and as Soroush (the Inviter),
I want to write short notes on the plan,
So that we can agree on details like "meet at the door at 8" without leaving the app.

**Acceptance Criteria:**

**Given** I am the Inviter or my answer is `YES` or `YES_PENDING`
**When** I open the Invitation page
**Then** I see the Notes (Note bubbles, UX-DR-33) and the Note composer (UX-DR-34) with the hint "Can't come anymore? Just say it here." (FR-11; this story creates the `Note` table)
**And** this story adds the Notes area and the drop-out hint to the Said Yes layout (Stories 2.3, 2.4) and the Inviter view (Stories 2.5, 2.6)
**And** a Note longer than 280 characters is refused with an inline error; the counter is announced only near the limit (UX-DR-87)

**Given** I post a Note
**When** it is saved by `invitations.py` (AD-3)
**Then** it appears for the Inviter and the Yes List; others see the Notes only when the page refreshes (by opening it or by HTMX polling every few seconds, not live chat)
**And** Notes are not live chat: no WebSockets, no typing indicators, and no notification per Note (NFR-11)
**And** an `Event` `note_added` is recorded without the Note text (AD-12)

**Given** I said No, did not answer, or am not on the Guest List
**When** I try to read or post Notes
**Then** I cannot see them and a post is refused (AD-2)

**Given** the Notes rule in `app/services/visibility.py`
**When** the tests for this story run (services tested directly with a fixed `now`)
**Then** tests prove Notes are returned only to the Inviter and to `YES` / `YES_PENDING` Users, never to a User with `NO` or `NONE` or to a Member not on the Guest List, and that a post from such a User is refused (AD-2)

### Story 3.2: Cancel a plan

As Soroush,
I want to cancel my plan,
So that my friends know it is not happening.

**Acceptance Criteria:**

**Given** I am the Inviter and my plan is Open or Closed
**When** I tap "Cancel plan" (UX-DR-15) and confirm once
**Then** `cancelled_at` is set, Status becomes Cancelled, and nothing is deleted (FR-13, AD-3, AD-4)
**And** I see the status banner "You cancelled this plan." (UX-DR-53, UX-DR-64) and can still post an optional reason in Notes

**Given** I am on the Yes List of a cancelled plan
**When** I open it
**Then** I see "Soroush cancelled this plan." and can still read and write Notes (UX-DR-60)

**Given** I am an Invitee who never answered
**When** the plan is cancelled
**Then** it disappears from "Waiting for your answer" without any message

**Given** the plan is a Draft or already Cancelled
**When** someone tries to cancel it
**Then** it is refused (AD-3 Status table)

**Given** an Invitee who can see the plan (not the Inviter)
**When** they send a request to cancel it
**Then** they get a 403 `NotAllowed`; a User who cannot see the plan gets a 404 `NotFound` instead (FR-7, AD-2)

### Story 3.3: Edit place or time

As Soroush,
I want to change where or when my plan happens,
So that I can fix a plan without cancelling it.

**Acceptance Criteria:**

**Given** I am the Inviter, the plan is Open or Closed, and "when" has not started
**When** I open "Edit place or time" (UX-DR-104)
**Then** I can change only "where" and "when"; the page says only place and time can change, and anything else needs a new plan (FR-14, FR-7)

**Given** I save a change
**When** `invitations.py` applies it
**Then** `place_time_changed_at` is set, and every `YES` answer becomes `YES_PENDING` in the same transaction, using a conditional update (`UPDATE … WHERE answer = 'YES'`) like every other Answer change (AD-5)
**And** the Deadline must still end before the new "when" (inline error otherwise)

**Given** the plan is Cancelled, a Draft (use the Draft form instead), or "when" has started
**When** I try to edit place or time
**Then** it is refused (AD-3)

**Given** an Invitee who can see the plan (not the Inviter)
**When** they send a request to edit place or time
**Then** they get a 403 `NotAllowed`; a User who cannot see the plan gets a 404 `NotFound` instead (FR-7, AD-2)

### Story 3.4: Still in or Not anymore

As Ali (who said Count me in),
I want to confirm or drop out after the place or time changed,
So that Soroush knows who is still coming.

**Acceptance Criteria:**

**Given** my answer is `YES_PENDING`
**When** I open the Invitation page
**Then** the Reconfirm prompt (UX-DR-45, UX-DR-58) shows the old value struck through and the new value, with two same-size buttons "Still in" and "Not anymore", and "Not anymore is fine. You just leave the list quietly."
**And** in the meantime I stay on the Yes List marked "not confirmed yet" (FR-14)

**Given** I tap "Still in"
**When** it is saved with a conditional update `YES_PENDING → YES`
**Then** the prompt disappears and the Yes layout stays

**Given** I tap "Not anymore"
**When** it is saved `YES_PENDING → NO`
**Then** I leave the Yes List silently, like a No, and see the Calm No panel; nobody sees that I left (AD-2)

**Given** my page is old (the plan was edited again after I loaded it)
**When** I tap a button
**Then** the request carries the `place_time_changed_at` I saw, is refused, and the page reloads with the latest change (AD-5, UX-DR-72)

**Given** "when" has started
**When** I have not reconfirmed
**Then** no change is possible and I stay "not confirmed yet"

### Story 3.5: The Updated mark

As Ali,
I want to see which of my plans changed since I last looked,
So that I never miss a new time, a cancel or a new Note.

**Acceptance Criteria:**

**Given** a plan in My Plans
**When** its `place_time_changed_at`, `cancelled_at` or newest Note time is later than my last visit to it
**Then** its Plan row shows the Updated mark (UX-DR-20, FR-16)

**Given** I open that plan
**When** the page loads
**Then** `invitations.mark_seen()` records the time in `PlanSeen` (this story creates the table; only `invitations.py` writes it, AD-3)
**And** the Updated mark is gone when I go back to Home

## Epic 4: Plans reach your pocket

The app installs on the phone and sends Web Push notifications; Android users answer from the notification; the notifications-off banner; metrics for the 4-week test.

### Story 4.1: Install the app on my phone

As Ali,
I want to add the app to my home screen,
So that it opens like a real app and can send me notifications.

**Acceptance Criteria:**

**Given** the app is open in a phone browser
**When** the page loads
**Then** a web app manifest is served with name, icons, `display: standalone`, theme and background color `#000000` (UX-DR-89, UX-DR-91), and a service worker registers (UX-DR-90)
**And** in standalone mode the layout respects the notch and home bar (safe-area insets)
**And** a cold load is a full server-rendered page with no skeleton loaders; when offline, only the PWA shell shows (no offline design in v1) (UX-DR-73)

**Given** I am on iPhone
**When** I want notifications
**Then** sign-up guides me to Add to Home Screen first, because on iPhone notifications work only from the home-screen app (FR-12)

**Given** I am on iPhone Safari and I just joined a Group
**When** onboarding finishes
**Then** the Add to Home Screen guide shows ("One more thing", steps with Share and "Add to Home Screen", "Skip for now") (UX-DR-92)
**And** after opening the app from the home screen I log in once (iPhone keeps separate cookies for it)

### Story 4.2: Turn on notifications

As Ali,
I want to allow notifications once,
So that new plans can reach me.

**Acceptance Criteria:**

**Given** I finished onboarding (installed app on iPhone)
**When** the app asks (UX-DR-93) and I allow notifications
**Then** a `PushSubscription` is saved for me (this story creates the table) and an `Event` `push_enabled` is recorded (FR-12)
**And** if I block them, nothing breaks and I can still see and answer plans in the app

**Given** a push is sent to a subscription that answers HTTP 404 or 410
**When** the send fails
**Then** that subscription is deleted and an `Event` `push_disabled` is recorded (AD-7)
**And** "notifications off" means I have no `PushSubscription`

**Given** the app sends any push
**When** pywebpush runs
**Then** it uses VAPID keys from `fly secrets` and a real `mailto:` subject, and push code lives only in `app/notifications/` (AD-7)

### Story 4.3: New plan notification

As Ali,
I want a notification when someone invites me,
So that I can answer from the bus in seconds.

**Acceptance Criteria:**

**Given** Soroush publishes a plan
**When** the database commit succeeds
**Then** every Invitee on the Guest List gets one notification showing what, where, when and the Deadline (FR-12, AD-7), sent only after commit
**And** Members not on the Guest List get nothing; a failed push is logged and never undoes the plan

**Given** I tap the notification
**When** the app opens
**Then** I land directly on the Invitation page and can answer in under 5 seconds from the tap (NFR-4)
**And** all notification texts come from `app/notifications/messages.py` and match the Voice table (UX-DR-81)
**And** before the friend test, this is checked on a real iPhone (home-screen app) and a real Android phone

### Story 4.4: Answer from the notification (Android)

As Ali on Android,
I want "Count me in" and "I'll pass" buttons in the notification,
So that I can answer without opening the app.

**Acceptance Criteria:**

**Given** my device supports notification action buttons
**When** I get a new plan notification
**Then** it shows "Count me in" and "I'll pass" (same labels as the page)

**Given** I tap a button
**When** the service worker posts to the push-answer endpoint
**Then** it sends the signed action token from the push payload (GuestListEntry id + answer, expires at `deadline_at`, itsdangerous); the endpoint needs no cookie or CSRF but still goes through the same service rules and conditional update (AD-9, AD-3, AD-5)
**And** an expired, changed or already-used token is refused safely
**And** no celebration plays for a Yes sent from the notification (UX-DR-78)

**Given** I am on iPhone
**When** I get the notification
**Then** there are no buttons and tapping opens the Invitation page (FR-8)

### Story 4.5: Deadline result notification

As Soroush,
I want a notification when my plan's Deadline passes,
So that I know who is coming without checking.

**Acceptance Criteria:**

**Given** the app is running
**When** the loop in `app/jobs/` runs every 60 seconds
**Then** it calls `invitations.close_and_notify(now)`, which claims each Invitation with one conditional update (`result_notified_at` empty, published, not cancelled, `deadline_at <= now`), commits, then sends (AD-7)
**And** each Invitation is claimed at most once, also after a restart, and cancelled plans and Drafts never get a result (NFR-12)

**Given** my plan closed
**When** the result is sent
**Then** only I (the Inviter) get it, with the Yes List count in friendly words, or "Nobody is free tonight 🌙" if it is empty (FR-10)

### Story 4.6: Cancelled and changed notifications

As Ali,
I want to hear when a plan I care about is cancelled or changed,
So that I don't go to the wrong place or time.

**Acceptance Criteria:**

**Given** Soroush cancels a plan
**When** the commit succeeds
**Then** every User with `YES` or `YES_PENDING` gets a "cancelled" notification; nobody else (FR-13, AD-7)

**Given** Soroush edits place or time
**When** the commit succeeds
**Then** every User with `YES` or `YES_PENDING` gets a "changed" notification that asks them to reconfirm, and while the plan is Open, every Invitee with `NONE` gets a notification with the new details (AD-7, FR-14)
**And** Users who said No get nothing

**Given** any v1 notification
**When** the app decides what to send
**Then** it sends only the four types in the AD-7 table (new Invitation, Deadline result, cancelled, place/time changed): no reminders, no "X is coming" pushes and no other extra pushes (NFR-10)

### Story 4.7: The notifications-off banner

As Ali, who has notifications off,
I want one gentle reminder,
So that I don't miss plans, without being nagged.

**Acceptance Criteria:**

**Given** I have no `PushSubscription` and my first Invitation arrives
**When** I open Home
**Then** the banner "🔔 Turn on notifications so you don't miss plans" shows above "Waiting for your answer" with a "Turn on" button and a dismiss button (UX-DR-46, FR-12)

**Given** I dismiss the banner
**When** I come back later
**Then** it never shows again (`User.push_banner_dismissed_at`, added by this story)

**Given** I tap "Turn on" on iPhone outside the home-screen app
**When** the tap happens
**Then** the Add to Home Screen guide opens instead

### Story 4.8: Test results for the 4 weeks

As Erfan,
I want a simple command that shows my success metrics,
So that I can tell after 4 weeks if v1 worked.

**Acceptance Criteria:**

**Given** the `Event` table has data
**When** I run the metrics command
**Then** it prints SM-0 (joined a Group within 48 h), SM-1 (Invitations published per Group), SM-2 (answered before the Deadline), SM-5 (plans with at least one Note), SM-C1 (Users with notifications off) and SM-C2 (Users who ignored 3 Invitations in a row), with the PRD targets next to each
**And** it shows a warning when SM-C1 > 40% or SM-C2 > 25%
**And** it reminds me that SM-3 and SM-4 come from the weekly check-in with friends
**And** it never prints Note text, places, or who said No (NFR-13, PRD §7)

