# Epic 1 Context: Join the crew

<!-- Compiled from planning artifacts. Edit freely. Regenerate with compile-epic-context if planning docs change. -->

## Goal

Build the base of the app and the first real flow for friends: a new project made from scratch (no starter template), live on Fly.io from day one, where friends sign up, pick an avatar, create a Group, share its Group Link and join it. Every later epic (plans, answers, notifications) builds on the project layout, auth, Group membership and design tokens set up here. It also gives the admin a command to reset a friend's password, because there is no email service.

## Stories

- Story 1.1: The app runs on my laptop
- Story 1.2: The app is live on the internet
- Story 1.3: Sign up, log in and log out
- Story 1.4: Pick your avatar
- Story 1.5: Create a Group
- Story 1.6: Join with a Group Link
- Story 1.7: Admin: reset a friend's password

## Requirements & Constraints

- Sign-up asks only for name, email and password; log-in uses email + password; a new User finishes sign-up in under 1 minute. No guest access.
- A logged-in User can create a named Group and becomes its first Member automatically.
- Any Member can share the Group Link; a person who opens it signs up or logs in, joins, then sees the Group and its Members. Joining twice must not create a second Membership. An unknown link shows a normal "not found" page.
- Privacy: a User sees only Groups they belong to. No screen shows anyone's past answers, Yes counts or "last seen".
- No self-service password reset in v1; the admin command resets the password and ends the friend's old sessions.
- Phone first: works at 360px with no sideways scroll, also at 200% text zoom; every interactive element at least 44px tall; all text passes WCAG AA.
- Metrics from day one: record a `group_joined` event, with no personal content.

## Technical Decisions

- **Stack (pin exact versions):** Python 3.14, uv 0.13.7, FastAPI 0.162.x, python-multipart, SQLModel 0.0.49, Alembic 1.20.1, SQLite (WAL), Jinja2 3.1.6, HTMX 2.0.11 served from `app/static/`, pwdlib[argon2] 0.3.1, itsdangerous, pydantic-settings, pywebpush 2.5.0, pytest.
- **Source tree:** `app/main.py`, `app/config.py`, `app/models/`, `app/services/`, `app/notifications/`, `app/jobs/`, `app/routes/`, `app/templates/` (with `fragments/`), `app/static/`, `migrations/`, `tests/`, `fly.toml`.
- **Layers (one direction):** routes/jobs → services → models (and notifications). Routes parse the request, get the current User, call one service, render a template; they never query the DB or decide rules. Only services touch the DB session and hold business rules. Nothing imports from `routes`.
- **Errors:** services raise `NotFound`, `NotAllowed`, `InvalidState`; one exception handler maps them to 404 / 403 / 409 pages (or fragments for HTMX). Hidden things return 404, never revealing they exist.
- **Visibility:** all "who may see what" rules live in `app/services/visibility.py`. The public Group Link page shows only the Group name and the sharer's name.
- **Naming:** use glossary terms verbatim (`User`, `Group`, `Membership`, `Event`); `snake_case` files/functions, `PascalCase` classes, `UPPER_CASE` enum values (stored as strings).
- **IDs:** integer primary keys; the Group Link uses a separate `Group.link_token` from `secrets.token_urlsafe`, never the DB id.
- **Time:** all datetimes stored as UTC via one shared `UTCDateTime` column type in `app/models/`; convert to `Europe/Rome` only in forms/templates. Time-dependent services take `now` as a parameter.
- **Migrations only:** tables are created and changed only by Alembic (`render_as_batch=True`); `SQLModel.metadata.create_all` only in tests. Each story adds its own tables/columns: `User` (1.3), `avatar` + `avatar_color` (1.4), `Group` + `Membership` (1.5), `Event` (1.6), `session_version` (1.7).
- **Auth:** pwdlib Argon2 hashes. Starlette signed `SessionMiddleware` cookie holding only User id, CSRF token and (from 1.7) `session_version`; HttpOnly, SameSite=Lax, `https_only` in production, 90 days. One `current_user` dependency on every route except sign-up, log-in, static files and Group Link landing; it redirects to Log in and refuses a stale `session_version`. Every POST carries a CSRF token (hidden `csrf_token` field, or `X-CSRF-Token` header set via `<body hx-headers>`), checked by one dependency. Authorization is checked in services.
- **HTMX:** a route returns the full page normally and only the fragment template when the `HX-Request` header is present; fragments never include the layout.
- **Events:** only services write the `Event` table (`user_id`, `type`, `invitation_id`, `group_id`, `at`).
- **Config & logging:** all settings and secrets from env vars via `app/config.py` (pydantic-settings); nothing secret in git (`.gitignore` excludes the DB file and `.env`). Python `logging` to stdout, one line per event; never log passwords, cookies, tokens or push keys.
- **Deploy:** Fly.io, exactly one always-on Machine (shared-cpu-1x 512 MB, `auto_stop_machines = "off"`, `min_machines_running = 1`), one Uvicorn worker, 1 GB volume with the SQLite file, daily volume snapshots, migrations run before app start on every deploy, secrets via `fly secrets`.
- **Tests:** pytest; services tested directly with a fixed `now`.

## UX & Interaction Patterns

- **Notte Pura, dark only:** CSS variables `background #000`, `surface #141414`, `surface-raised #1F1F1F`, `ink #FFF`, `ink-muted #A3A3A3`, `line #2B2B2B`, `accent #FFB547`, `error #FF7A6B`. Amber only for a few named things (Count me in, Publish, celebration); every selected state is white. Errors: coral outline + "!" + text, never a coral fill.
- **Fonts:** Gloock (serif) only for big words (titles, Home greeting, Group names); Onest for everything else. Use the type scale tokens (e.g. `display-lg` for greeting, `title` for Group rows, `body-lg` for inputs).
- **Layout:** single column, 20px gutter, centered max ~480px on wide screens; main action pinned near the bottom; lists use hairline dividers, no boxes; depth by tone, no card shadows. Buttons are pills; inputs are `surface`, 52px tall, 16px radius, with a real `<label>`. 2px white focus ring on everything.
- **Inline error:** coral "!" + bold line + muted detail under the field, `aria-invalid` and `role="alert"`; other fields keep their values.
- **Navigation:** inner pages have a muted back link top left ("‹ Home", "‹ My Groups"); Create a Group uses a close "✕". Home shows the Groups icon (44px round, label "My Groups") top right and "Hi <name>".
- **Screens:** Sign up ("Hey, welcome 👋", Your name / Email / Password, "Make my account"); Log in ("Welcome back"); Pick your avatar (once only, after sign-up: 12 faces in a 4-column grid, 5 gradient swatches Sun/Mint/Violet/Coral/Cream, 132px live preview, Continue, "Skip, surprise me 🎲" for random); My Groups (rows sorted by last used, "+ Create a Group"); Create a Group ("New group", "Create group" → new Group page); Group page (name, "N members", Member rows with "you" on own row, Share Group Link + caption "Anyone with the link can join this group."); Group Link landing (only "<Sharer> invited you to" + Group name, "Join the group", "I already have an account").
- **Avatar:** emoji face on the User's gradient shape (each color has its own shape), never initials or photos, labelled with the person's name for screen readers.
- **Share:** use the Web Share API; fallback copies the link and shows "Link copied".
- **Onboarding:** the Group Link is opened in the browser; the friend signs up and joins there, picks an avatar, then lands on the Group page.

## Cross-Story Dependencies

- 1.1 is the base for all; 1.2 deploys it, and every later story should go live the same way.
- 1.3 creates `User` and auth; 1.4 adds avatar fields and a placeholder start page that 1.5 turns into Home.
- 1.5 creates `Group` (already with `link_token`) and `Membership`; 1.6 uses the token and creates `Event`.
- 1.6 joins after sign-up + avatar, so it depends on 1.3 and 1.4 flows keeping the Group Link target.
- 1.7 adds `session_version` to the cookie set up in 1.3 and to the `current_user` check.
- Epic 2 Home sections (Waiting for your answer, My Plans, "+ New plan") extend the Home built in 1.5; Invitations depend on Groups and Memberships from this epic.
