# Build Tasks: Version 1

**The app's promise:** Post a plan. Friends just say yes or no. Your plan stays your plan.

**The design rule:** Nobody gets hurt, and nobody loses face. When you are not sure how a feature should work, choose the way that protects people's feelings. Examples: a "no" is never shown, and people who are not invited never see the invite.

**What is in version 1 (the MUST list):**
- Create a group, and join a group with an invite link
- Post an invite: what, where, exact time or time window, cost tag (Free / $ / $$ / $$$)
- Private guest list: the inviter picks which members are invited; people not invited never see it
- Yes / No answer
- Deadline: after the deadline, no answer = no
- Silent no: the inviter sees only who said yes
- Notifications

**Stack:** installable PWA web app, Python + FastAPI, Jinja2 HTML templates + HTMX, SQLModel with SQLite on your computer, SQLite also in production on a Fly.io volume, hosting on one always-on Fly.io machine. *(Updated 2026-11-11 by the architecture; the spine wins if anything here disagrees.)*

**How to use this list:**
- Do the milestones in order. Each one ends with something you can run and see.
- Make a git commit after every small task that works. Push to GitHub at the end of every milestone.
- Write a few tests with pytest in every milestone, not only at the end.
- Tasks marked **✍️ Try yourself** are for you to write alone first. Then ask Claude to review your code.

---

## Milestone 0: Setup and tools

**Goal:** Your computer is ready, and the project lives on GitHub.

- [ ] Install Python 3.12+ and check it with `python --version`
- [ ] Create the project folder and a virtual environment (`python -m venv .venv`), then activate it
- [ ] Install the first packages: `fastapi`, `uvicorn[standard]`, `jinja2`, `sqlmodel`, `pytest`, `httpx`
- [ ] Save them in `requirements.txt` (`pip freeze > requirements.txt`)
- [ ] `git init`, add a `.gitignore` (ignore `.venv/`, `__pycache__/`, `*.db`, `.env`)
- [ ] Create a GitHub repository and push the first commit
- [ ] ✍️ Try yourself: write a short `README.md` that explains the app's promise in 3-4 sentences, in your own words

**What you will learn:**
- Why a virtual environment keeps each project's packages separate
- The basic git flow: `add`, `commit`, `push`

**Done when:** you can see your project with the README on github.com.

---

## Milestone 1: Hello FastAPI

**Goal:** A tiny web server that shows an HTML page in your browser.

- [ ] Create `app/main.py` with a FastAPI app and a `/health` route that returns `{"status": "ok"}`
- [ ] Run it with `uvicorn app.main:app --reload` and open `http://127.0.0.1:8000/health`
- [ ] Open `http://127.0.0.1:8000/docs` and look at the automatic API page
- [ ] Add a `templates/` folder with `base.html` (shared layout) and `home.html`
- [ ] Add a `/` route that renders `home.html` with Jinja2
- [ ] Write your first test in `tests/test_main.py` using FastAPI's `TestClient`, and run `pytest`
- [ ] ✍️ Try yourself: write a test that checks the home page returns status 200 and contains the app name

**What you will learn:**
- How a web request goes from browser → route function → response
- How Jinja2 templates fill HTML with Python data (`{{ name }}`)
- How to test a web app without opening a browser

**Done when:** the browser shows your home page, and `pytest` shows all tests green.

---

## Milestone 2: Data models

**Goal:** The app has a database with all the tables version 1 needs.

- [ ] Create `app/db.py`: a SQLModel engine for `sqlite:///app.db` and a `get_session` function
- [ ] Read the database URL from an environment variable (`DATABASE_URL`), with SQLite as the default. This makes a switch to PostgreSQL possible later.
- [ ] Create `app/models.py` with these tables:
  - `User` (id, name, email, password_hash)
  - `Group` (id, name, invite_code, created_by)
  - `Membership` (user_id, group_id) — who is in which group
  - `Invite` (id, group_id, inviter_id, what, where, start_time, end_time (optional, for a time window), cost_tag, deadline, created_at)
  - `InviteGuest` (invite_id, user_id) — the private guest list
  - `Answer` (invite_id, user_id, answer yes/no, answered_at)
  - `PushSubscription` (user_id, endpoint, keys) — for Milestone 10
- [ ] Use a Python `Enum` for the cost tag: Free, $, $$, $$$
- [ ] Create the tables when the app starts
- [ ] Write tests that use a separate test database (SQLite in memory) so tests never touch your real data
- [ ] ✍️ Try yourself: write the `Invite` model yourself, then compare it with the list above

**What you will learn:**
- How tables connect to each other (one-to-many, many-to-many through a "link" table like `Membership`)
- What an ORM does: you write Python classes, it writes SQL for you

**Done when:** you can open `app.db` with a SQLite viewer (for example "DB Browser for SQLite") and see all the tables, and the model tests pass.

---

## Milestone 3: Users and login

**Goal:** People can sign up, log in and log out.

**Our choice (can change later):** email + password, with the password stored as a hash, and a signed session cookie to remember who is logged in. This is the simplest way for a beginner because it needs no outside service. Later you can switch to "Login with Google" or Supabase Auth.

- [ ] Install `pwdlib[argon2]` (or `passlib[bcrypt]`) for password hashing and `itsdangerous` for the session cookie
- [ ] Add Starlette's `SessionMiddleware` with a secret key from an environment variable (`.env` file, never committed)
- [ ] Build the sign-up page: form → check email is not used → hash password → save user
- [ ] Build the login page and a logout link
- [ ] Write a `get_current_user` dependency; pages that need login send people to the login page
- [ ] Tests: sign up works; same email twice fails; wrong password fails; a protected page without login redirects
- [ ] ✍️ Try yourself: write the `get_current_user` function

**What you will learn:**
- Why we never save the real password (hashing)
- What a cookie and a session are
- FastAPI "dependencies" (`Depends`) — a clean way to share code between routes

**Done when:** you can sign up, log out, log in again, and see "Hello, <your name>" on the home page.

---

## Milestone 4: Groups and invite link

**Goal:** A user can create a group and share a link; friends join by opening the link.

- [ ] "Create group" page: enter a name → save the group → make the creator a member
- [ ] Make a random, hard-to-guess `invite_code` with `secrets.token_urlsafe()`
- [ ] Group page shows the group name, the members, and the join link (with a "Copy link" button)
- [ ] `/join/{invite_code}` route: if not logged in → log in or sign up first, then come back and join
- [ ] Joining twice does nothing bad (no duplicate member)
- [ ] "My groups" list on the home page
- [ ] Only members can open a group page; others get "not found"
- [ ] Tests: create group, join with link, join twice, non-member cannot see the group
- [ ] ✍️ Try yourself: write the test "a non-member gets 404 on the group page"

**What you will learn:**
- How to make safe random codes for links
- Access control: checking "is this user allowed to see this?" on every page

**Done when:** in two browsers (one normal, one private window) with two users, user B joins user A's group with the link, and both see each other in the member list.

---

## Milestone 5: Create an invite

**Goal:** A member can post an invite in a group.

- [ ] "New invite" form: what, where, exact time **or** time window (start + end), cost tag (Free / $ / $$ / $$$), deadline
- [ ] Check the form: deadline must be in the future and before the start time; end time after start time
- [ ] Save the invite; show it on an invite detail page
- [ ] The plan is locked: after posting, others cannot edit or comment on it (the plan stays your plan)
- [ ] Store all times in UTC in the database; show them in local time on the page
- [ ] Tests: valid invite is saved; bad times are refused
- [ ] ✍️ Try yourself: write the function that checks the times (deadline, start, end) and returns a list of error messages

**What you will learn:**
- HTML forms and form validation on the server
- Working with dates and time zones in Python (`datetime`, UTC)

**Done when:** you post "Burger at Joe's, 7-9 pm, $, answer in 1 hour" and see it on its page.

---

## Milestone 6: Private guest list

**Goal:** The inviter picks who is invited, and people who are not invited never see the invite.

- [ ] Add checkboxes with the group members to the "New invite" form (with a "Select all" option)
- [ ] Save one `InviteGuest` row for each chosen person
- [ ] Group page shows only the invites where you are the inviter or a guest
- [ ] Invite detail page returns "not found" (404, not "forbidden") for people not invited, so they cannot even tell it exists
- [ ] Tests: guest sees the invite; non-guest member does not see it in the list; non-guest gets 404 on the direct link
- [ ] ✍️ Try yourself: write the database query "invites in this group that this user is allowed to see"

**What you will learn:**
- Filtering data with SQLModel queries (`select`, `where`, joins)
- Privacy by design: hiding is safer than showing "you are not allowed"

**Done when:** with three users, A invites only B; B sees the invite, C sees nothing at all.

---

## Milestone 7: Yes / No and silent no

**Goal:** Guests answer Yes or No; the inviter sees only the yes list.

- [ ] Add big "Yes" and "No" buttons on the invite page (only for guests, not the inviter)
- [ ] Save the answer in the `Answer` table (one answer per guest per invite)
- [ ] The guest sees their own answer ("You said yes")
- [ ] The inviter's view shows **only** the people who said yes. No count of "no", no list of who did not answer.
- [ ] Make sure "no" answers never appear anywhere in the HTML (not even hidden)
- [ ] Tests: answer is saved; answering twice keeps one answer; inviter page contains yes names and does not contain no names
- [ ] ✍️ Try yourself: write the test "the inviter's page never shows a person who said no"

**What you will learn:**
- POST requests and changing data safely
- Unique rules in the database (one answer per person)
- Turning a human rule ("silent no") into code and a test

**Done when:** B says yes and C says no; A sees only "B is coming", and nothing about C.

---

## Milestone 8: Deadline

**Goal:** After the deadline, answers are closed and no answer counts as no.

- [ ] Write a helper `is_open(invite)` that checks `now < deadline`
- [ ] After the deadline: hide the Yes/No buttons, show "Answers are closed", and refuse late answers on the server too
- [ ] No background job is needed: "no answer = no" just means people without a yes are not on the list
- [ ] Show the time left on the invite page ("answer in 45 min")
- [ ] Tests: answer before the deadline works; answer after the deadline is refused (tip: create an invite with a deadline in the past)
- [ ] ✍️ Try yourself: write the function that turns the time left into friendly text ("2 h 10 min", "5 min", "closed")

**What you will learn:**
- Never trust only the page: rules must be checked on the server
- How to test code that depends on the current time

**Done when:** an invite with a past deadline shows "Answers are closed", and a late answer is refused.

---

## Milestone 9: HTMX polish and mobile-friendly UI

**Goal:** The app feels fast and simple on a phone.

- [ ] Add HTMX (one `<script>` tag)
- [ ] Yes/No buttons use `hx-post` and update only the answer area, without reloading the whole page
- [ ] The inviter's yes list refreshes by itself every 30 seconds (`hx-trigger="every 30s"`)
- [ ] Add a small CSS framework (for example Pico.css) for a clean look with little work
- [ ] Mobile first: big buttons, one column, readable text; test with the phone view in browser dev tools
- [ ] Keep it very simple: from the home page, every action should be at most 2 taps away
- [ ] Tests: the HTMX routes return only the small HTML piece (a "partial"), not the whole page
- [ ] ✍️ Try yourself: turn the "New invite" form into an HTMX form that shows errors without a page reload

**What you will learn:**
- How HTMX swaps parts of the page with HTML from the server (no big JavaScript needed)
- Basic responsive design for phones

**Done when:** on your phone (same Wi-Fi, run with `--host 0.0.0.0`) you can post an invite and answer one easily.

---

## Milestone 10: PWA and push notifications

**Goal:** The app can be installed on the phone home screen and sends notifications.

- [ ] Add `manifest.json` (name, icons, colors) and link it in `base.html`
- [ ] Add a service worker (`sw.js`) and register it
- [ ] Make VAPID keys (one time) and keep them in `.env`
- [ ] "Turn on notifications" button: ask permission, subscribe, send the subscription to the server, save it in `PushSubscription`
- [ ] Use the `pywebpush` library to send a push to every guest when a new invite is posted
- [ ] In the service worker, show the notification with "Yes" and "No" action buttons; a tap on an action sends the answer to the server
- [ ] **iPhone note:** action buttons in notifications do not work on iPhone. iPhone users tap the notification and land on a page with big Yes/No buttons. Also, on iPhone, push works only after the user adds the app to the Home Screen — show a short help text for this.
- [ ] Tell the inviter when someone says yes (never when someone says no)
- [ ] Delete subscriptions that the push service says are expired
- [ ] Tests: when an invite is created, the send function is called once for each guest (replace the real send with a fake one using `monkeypatch`)
- [ ] ✍️ Try yourself: write the service worker `notificationclick` handler that opens the invite page

**What you will learn:**
- What a PWA and a service worker are
- How Web Push works (browser subscription → your server → push service → phone)
- Mocking: testing code that talks to outside services

**Done when:** on an Android phone (or Chrome on desktop), you get a notification for a new invite and can answer Yes from the notification; on iPhone, the tap opens the Yes/No page.

Note: push needs HTTPS. On your computer `localhost` is OK; for a phone, it is easiest to test after Milestone 11 (deploy).

---

## Milestone 11: Deploy to Fly.io

**Goal:** The app is live on the internet, always on, with its SQLite database on a Fly.io volume.

*Updated 2026-11-11: the architecture chose SQLite everywhere (no PostgreSQL in v1). See the architecture spine, AD-8 and AD-10.*

- [ ] Create a Fly.io app and a 1 GB volume; mount it and point `DATABASE_URL` to a SQLite file on the volume
- [ ] In `fly.toml`: `auto_stop_machines = "off"`, `min_machines_running = 1`; then scale to exactly 1 Machine
- [ ] Turn on SQLite WAL mode
- [ ] Make sure Alembic migrations run on every deploy, before the app starts
- [ ] Set the secrets with `fly secrets` (session secret, VAPID keys), never in git
- [ ] Set the start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT` (one worker only)
- [ ] Add GitHub Actions to run `pytest` on every push
- [ ] ✍️ Try yourself: write the GitHub Actions file (`.github/workflows/tests.yml`) that installs packages and runs pytest

**What you will learn:**
- Environment variables and secrets in production
- Why a SQLite file needs a volume (a disk that survives redeploys), and why only one server may use it
- Continuous integration (CI): tests run by themselves

**Done when:** you open your app's public URL on your phone, install it to the home screen, and get a push notification from a real invite.

---

## Milestone 12: Test with real friends

**Goal:** Real people use it, and you learn what to fix.

- [ ] Invite 3-6 friends into one group
- [ ] Each person posts at least one real invite during one week
- [ ] Watch for: Is it easy? Did notifications arrive (Android and iPhone)? Did anyone feel awkward?
- [ ] Ask each friend 3 short questions: What was easy? What was confusing? Did you ever feel pressure or shame?
- [ ] Write down bugs as GitHub Issues; fix the top 3
- [ ] ✍️ Try yourself: write a short "what I learned" note in the README — it is great for job interviews

**What you will learn:**
- Real users find problems that tests do not
- How to choose what to fix first

**Done when:** at least one real outing happened because of your app.

---

## Later (not v1)

**Should (next version):**
- Change your answer later in the app
- Last-chance reminder 10 minutes before the deadline
- Several options (burger or sushi) + time picks, with auto-pick of the best one
- Answer visibility control: you choose who can see your answer
- Soft result screen: "Nobody is free tonight" + one tap to repost for another day

**Could (later):**
- Shared photo album for each outing
- Mood status ("in the mood today", "short on money this week") + follow a friend's status
- Anonymous gift: "your share is covered 🎁", never showing who paid
- "Pay me back later" tracker
- AI suggestions: private activity ideas and best-time tips, based on what the group says yes to
- Mutual secret crush: revealed only if both people mark each other

**Won't (for now):** presence score, native mobile app, in-app chat.
