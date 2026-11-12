# Review: Technology Currency — Architecture Spine v1

- **Lens:** tech currency (are the named versions and technologies current, real, and a good fit?)
- **Reviewed:** `ARCHITECTURE-SPINE.md` and `.memlog.md` (same folder)
- **Date:** 2026-11-11
- **Method:** PyPI JSON API and npm registry queried live; official docs fetched (FastAPI release notes, Starlette middleware, SQLModel releases, Neon FAQ, Fly.io pricing); web search where no official page was found.

## Verdict

**PASS WITH FIXES.** Most named technologies exist, are maintained, and fit. The memlog's one `version` entry says its versions came "from search snippets; confirm with uv add". Live checks confirm most of them. Two are wrong in ways that matter:

- The FastAPI pin is 21 minor versions old, and the versions since then contain form-handling breaking changes.
- The 60-second sweep keeps Neon awake all the time, which uses more compute than the Neon Free plan allows.

Several other decisions (the CSRF library, the Postgres driver, and Apple push details) are only asserted and were never checked.

## Findings

| # | Severity | Finding | Evidence |
| --- | --- | --- | --- |
| F1 | **High** | **The Neon Free compute budget runs out about 20 days into each month.** AD-7's sweep queries the database every 60 s. Neon suspends compute only after 5 min idle, so the database never sleeps. Free gives 100 CU-hours per project per month, which is about 400 h at 0.25 CU. A month has about 730 h. When the budget runs out, "compute is suspended until the next billing period": connections drop and the app goes down mid-test. The memlog checked "suspends after 5 min idle" but not how it interacts with the sweep. **Fix options:** (a) the sweep reads the next deadline once and sleeps until then, touching the DB only when a deadline is due or after a write; (b) use Neon Launch (paid) or Fly Managed Postgres; (c) use SQLite on a Fly volume in production too (a single instance is already required by AD-8). Record the choice as an AD or a constraint. | https://neon.com/faqs/free-plan-limits-and-quotas |
| F2 | **High** | **FastAPI 0.141.x is out of date.** The latest is **0.162.4** (2026-11-10), and 0.141.0 is from 2026-07-29. Versions 0.147, 0.148, 0.149, 0.150, 0.160 and 0.162 contain breaking changes to **Form** parsing (omitted bool and checkbox fields, empty values, unvalidated defaults, `extra="forbid"` on form models). This app is built on POST forms, so tutorials and AI agents that target current FastAPI will not match 0.141. **Fix:** pin `0.162.x`, or say on purpose why 0.141 was chosen. Use `fastapi[standard]` or add `python-multipart` (needed for `Form`). | https://pypi.org/project/fastapi/ ; https://fastapi.tiangolo.com/release-notes/ |
| F3 | Medium | **No CSRF library or pattern is named, and Starlette has no built-in CSRF protection.** The Conventions row says "one middleware" but does not name it. The options found have problems: `starlette-csrf` 3.0.0 (last release 2023-06) checks only the `x-csrftoken` **header**, so plain HTML form POSTs fail without JS; `asgi-csrf` 0.11 (2024-11) uses a double-submit cookie and supports form fields; `fastapi-csrf-protect` 1.0.7 (2025-09) is per-route, not middleware. **Fix:** pick one, or decide on a small hand-written middleware (a session-bound token in a hidden field plus `hx-headers` on `<body>` for HTMX), and record it. Also check that SameSite=Lax plus POST-only changes is an accepted extra defence. | https://starlette.dev/middleware/ ; https://pypi.org/project/starlette-csrf/ ; https://pypi.org/project/asgi-csrf/ ; https://pypi.org/project/fastapi-csrf-protect/ |
| F4 | Medium | **The SQLModel `0.0.4x` range hides a behavior change.** In **0.0.45**, `datetime` fields became UTC-normalized by default, and naive datetimes now raise errors. This matches AD-6, but code or tutorials written for an earlier version will break. Latest is **0.0.49** (released today), which adds SQLAlchemy 2.1 support. **Fix:** pin `0.0.49` (at least 0.0.45) and say that AD-6 relies on this behavior. Also say SQLite has no real timezone storage, so rely on SQLModel's UTC type, not on the database. | https://github.com/fastapi/sqlmodel/releases ; https://pypi.org/project/sqlmodel/ |
| F5 | Medium | **pywebpush with iOS is not fully checked.** pywebpush 2.5.0 (2026-08-30) is confirmed latest. The memlog records iOS 16.4+ and home-screen-only. Not recorded: Apple returns `403 BadJwtToken` when the VAPID `sub` is malformed or uses a reserved domain (`.local`, `example.com`), and pywebpush expects a specific key format. **Fix:** add to AD-7: `VAPID_SUB=mailto:<real address>`, keys made in pywebpush's expected format, and a manual test on a real iPhone with the installed PWA as an early story. | https://pypi.org/project/pywebpush/ ; https://github.com/web-push-libs/pywebpush/issues/175 ; https://developer.apple.com/forums/thread/725473 |
| F6 | Low | **Required dependencies are not named.** The spine does not name (a) the PostgreSQL driver (`psycopg` 3.3.8 or `psycopg2-binary` 2.9.13; this affects the Neon `DATABASE_URL` scheme `postgresql+psycopg://` and `sslmode=require`), (b) `itsdangerous` (2.2.0), which Starlette `SessionMiddleware` needs, or (c) `python-multipart`. Add them to the Stack table. | https://pypi.org/project/psycopg/ ; https://starlette.dev/middleware/ |
| F7 | Low | **Starlette session cookie defaults need explicit settings.** `SessionMiddleware` is confirmed in Starlette **1.10.0**. HttpOnly is always on and SameSite defaults to `lax`, but `https_only` (the Secure flag) **defaults to False** and `max_age` defaults to 2 weeks. AD-9 says "Secure", so the config must set `https_only=True` in production. Also note that the session is signed, not encrypted: the User id is readable by the client, which AD-9 accepts. | https://starlette.dev/middleware/ |
| F8 | Info | **Python 3.14 is fine but was not checked against 3.15.** 3.15 came out on 2026-10-09 (3.15.2 is out now). 3.14 (3.14.10) is supported until 2027-10 for bug fixes. All core packages list 3.14. Keeping 3.14 is reasonable. The memlog's reason ("some packages may lag") is plausible; note that SQLModel already supports 3.15. | https://endoflife.date/python |

## Confirmed (checked live today)

| Item | Spine says | Live status (2026-11-11) | OK? |
| --- | --- | --- | --- |
| Python | 3.14 | 3.14.10 current; 3.15.2 newest | Yes |
| uv | 0.13.x | 0.13.7 (2026-11-03) | Yes |
| FastAPI | 0.141.x | **0.162.4** | **No (F2)** |
| SQLModel | 0.0.4x | 0.0.49 (2026-11-11) | Pin needed (F4) |
| Alembic | 1.20.x | 1.20.1 (2026-10-22), Stable | Yes |
| Jinja2 | 3.1.6 | 3.1.6 (still latest) | Yes |
| HTMX | 2.x not 4 | npm `latest` = 2.0.11 (2026-09-22); `next` = 4.0.1 (4.0.0 out 2026-08-28) | Yes, 2.x is still the default npm tag |
| pwdlib[argon2] | latest, pinned | 0.3.1 (2026-08-12), Beta, Python 3.14 classifier | Yes; pin `0.3.1` |
| pywebpush | 2.5.0 | 2.5.0 (2026-08-30) | Yes (see F5) |
| pydantic-settings | (no version) | 2.16.2 (2026-10-28) | Yes; add to Stack table |
| Starlette signed session cookie | AD-9 | `SessionMiddleware` present in Starlette 1.10.0 | Yes (see F7) |
| Fly.io shared-cpu-1x 512 MB | ~$3.69/mo always-on | $3.69/mo confirmed on official docs; no free tier; bills under $5 waived for personal orgs | Yes |
| Neon Free | 0.5 GB, scale to zero | Now **1 GB** storage, 100 CU-h/project/month, scale to zero after 5 min, cannot be turned off | Storage OK; compute fails (F1) |
| SQLModel + Alembic on SQLite and Postgres | AD-10 | SQLModel 0.0.47 added CI-tested Postgres support; Alembic 1.20 is stable. SQLite `ALTER` limits mean Alembic needs `render_as_batch=True` in `env.py` (not stated) | Yes, add the batch-mode note |
| fastapi-users avoided | memlog | No reason to change | Yes |
| APScheduler avoided | memlog | Spine uses a plain asyncio loop instead, which fits | Yes |

## Suggested spine edits (for the architect; not applied)

1. Stack: FastAPI → `0.162.x` (or a written reason for 0.141), SQLModel → `0.0.49`, pwdlib → `0.3.1`, add `pydantic-settings 2.16.x`, `psycopg[binary] 3.3.x`, `itsdangerous 2.2.x`, `python-multipart`.
2. AD-7 / Hosting: fix the Neon compute budget problem (F1). This is the only finding that can take the app down during the 4-week test.
3. Conventions → Forms & CSRF: name the library or the hand-written pattern (F3).
4. AD-7: VAPID `sub` format and a real-iPhone test (F5).
5. AD-9: `https_only=True` in production (F7). AD-10: Alembic `render_as_batch=True` for SQLite.
