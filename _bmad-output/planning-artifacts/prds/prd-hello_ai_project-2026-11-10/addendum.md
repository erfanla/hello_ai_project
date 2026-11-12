# Addendum: PRD for the low-pressure friend invite app

Supporting details that do not belong in the PRD itself.

## A. Comparable products (web research, 2026-11-10)

Many sources are vendor or SEO pages, so read them with care.

| Product | What it does | Difference from our idea |
|---|---|---|
| Partiful | Party pages, quick RSVP, guest chat | Built for parties; chat lets the plan drift; the host seems to see declines |
| Howbout | Shared calendar for friend groups ($8M raised in 2024) | About who is free, not yes/no on one plan; users disliked the paywall |
| Apple Invites | Accept / decline / maybe, approve guests; needs iCloud+ to create | Declines are visible |
| WhatsApp group events | Going / not going inside the group chat | Opposite of our idea: rejection is public, chat takes over |
| Google "Who's Down" (2015) | "I'm free" switch; you only see friends who are down | Closest to a Silent No |
| down? / Walking Up | Text link, friends tap "in" / "can't"; post a ping with activity, time, place | They show "can't" or the full RSVP list |
| Timeleft | Dinners for 6 strangers, with a sign-up deadline | Strangers, not friends |

**Gap:** none of the products we found clearly hides declines from the host. A Silent No plus a Deadline looks like a real gap.

**Failures:** IRL shut down in 2023 (95% fake users, fraud). Down To Lunch reached #2 in the US App Store in 2016, then a fake rumor hurt it.

**Takeaways:**
1. Friends can answer from a link with no install or account (down?, Apple Invites, Partiful).
2. The Silent No plus a Deadline is the core difference. Leave out chat.
3. Many apps go viral and then die. Measure whether people keep using the app week after week.

**What we decided against these takeaways:** we chose required sign-up (against takeaway 1), because Silent No and notifications need known Users. SM-0 tracks this risk. We added simple Notes for the Yes List (takeaway 2 says no chat), because Notes are not live and only the Inviter and the Yes List see them, so they cannot take over the plan.

Sources: producthunt.com/products/partiful/alternatives, party.pro/Partiful, cbinsights.com/compare/howbout-vs-partiful, marlvel.ai/apps/howbout-shared-calendar, axios.com/2025/02/05/apple-invites-app-iphone-invitations, androidauthority.com/whatsapp-new-features-group-events-more-3428668, engadget.com/2015/10/30/google-whos-down-friend-finding-app, mwm.ai/apps/down-group-hangout-planner/6789345455, apps.apple.com/us/app/walking-up/id6751792898, connexionfrance.com (Timeleft), fortune.com (IRL), businessinsider.in (Down To Lunch).

## B. Technical choices (from the brainstorm, for the architect)

- Web app that installs on the phone home screen (PWA), with Web Push notifications.
- Notification Yes/No buttons work on Android and desktop, not on iPhone. iPhone users tap and get a one-screen Yes/No page.
- Backend: Python + FastAPI.
- Frontend: server-rendered HTML (Jinja2) + HTMX.
- Database: SQLModel with SQLite everywhere: on the laptop and in production on a Fly.io volume (a disk that survives redeploys). *Updated 2026-11-11 by the architecture:* PostgreSQL on Neon was dropped because the Neon Free compute quota would run out mid-test. PostgreSQL comes later.
- Hosting: Fly.io, one always-on machine (about $3.69/month). *Updated 2026-11-11.*
- The binding technical decisions are in `_bmad-output/planning-artifacts/architecture/architecture-hello_ai_project-2026-11-11/ARCHITECTURE-SPINE.md`. If this list and the spine disagree, the spine wins.
- Notes (FR-11) are not live. They are shown when the page is opened or refreshed (HTMX polling, an automatic refresh every few seconds, is an option and still counts as "not live" for FR-11). Live chat would need WebSockets, so it is deferred.
- Later: photos go to object storage (Supabase Storage, Cloudflare R2, S3), with only the file path in the database.
