---
name: Low-pressure friend invite app
status: final
created: 2026-11-11
updated: 2026-11-11
sources:
  - _bmad-output/planning-artifacts/prds/prd-hello_ai_project-2026-11-10/prd.md
  - _bmad-output/planning-artifacts/architecture/architecture-hello_ai_project-2026-11-11/ARCHITECTURE-SPINE.md
---

# Low-pressure friend invite app — Experience Spine

## Foundation

- **Form factor:** phone-first web app, installed as a PWA (home-screen app). Designed at 360px. No native app in v1.
- **UI system:** none. Server-rendered pages (Jinja2) with HTMX 2 for partial updates, per the architecture spine (AD-11: full page on normal requests, fragment on `HX-Request`). Small custom CSS from `DESIGN.md` tokens; a little JavaScript only for the Yes celebration (vibration, motion trigger) and the service worker.
- **Visual identity:** `DESIGN.md` (Notte Pura, dark only). This file owns behavior.
- **Words:** PRD Glossary terms are used as written: Invitation, Inviter, Invitee, Yes List, Notes, My Plans, Deadline, Cost Tag, Group, Group Link, Draft, Guest List, Answer, Silent No. User-facing labels may be friendlier ("plan", "Going") but code and specs use the Glossary.
- **Core rules that shape every screen** (from the PRD, §1):
  - **Nobody gets hurt.** Nobody is shown who said No, and nobody is asked "why?". No and missing Answers never appear (Silent No, FR-9). Saying No is calm and kind, never sad.
  - **Your plan stays your plan.** Only the Inviter changes an Invitation, and only its place and time (FR-7, FR-14). Invitees can only answer. There is no place to comment or suggest another plan before answering.
  - **Simple first.** Every screen is easy on a phone. Create, answer, and My Plans are at most 2 taps from Home. Answering from a notification takes under 5 seconds (PRD NFR).
- **Why it matters** (PRD Jobs To Be Done): going out should be easy even on a bad day. A friend who feels down can be with friends without having to talk about why. Every screen should feel safe for shy or introverted people.
- **Answers are final in v1** (FR-8). There is no "Change answer" option anywhere. To drop out after Yes, a User writes in Notes.
- **Mocks:** every screen in one page: **[mockups/all-screens.html](mockups/all-screens.html)** (built from the single `mockups/key-*.html` files linked below). They show layout and component decisions. **The spines (`DESIGN.md` + this file) win on any conflict.**

## Information Architecture

| Surface | Reached from | Purpose |
|---|---|---|
| Group Link landing | Group Link (e.g. from WhatsApp) | Shows only the Group name and who shared the link (AD-2). Sign up or log in, then join. → [mockups/key-grouplink.html](mockups/key-grouplink.html) |
| Sign up / Log in | Group Link landing, or app open when logged out | Name + email + password (FR-1, AD-9). Sign-up in under 1 minute. → [mockups/key-signup.html](mockups/key-signup.html) |
| Pick your avatar | Right after sign-up (first time only) | Choose a face + a color. → [mockups/key-avatar.html](mockups/key-avatar.html) |
| Add to Home Screen guide | After joining via Group Link, on iPhone Safari only | Short step-by-step guide, then log in once inside the home-screen app (UJ-3). → [mockups/key-grouplink.html](mockups/key-grouplink.html) |
| Home | App open (logged in) | **Groups icon** (top corner) · **Waiting for your answer** (always on top; the User's Open Invitations, FR-6) · **My Plans** · big **New plan** button. → [mockups/key-home.html](mockups/key-home.html), banner state [mockups/key-banner.html](mockups/key-banner.html) |
| My Groups | Groups icon on Home | List of my Groups + **Create a Group**. → [mockups/key-groups.html](mockups/key-groups.html) |
| Invitation page | Invitation card or plan row on Home; tapping a notification | One page, many states (see State Patterns). → [mockups/key-invitation.html](mockups/key-invitation.html) |
| New plan (create) | New plan button on Home | One scrolling form: **For: <Group> ▾** (Group picker, defaults to the last-used Group) → icon → what / where / when → Cost Tag → Deadline → who gets it → Publish or Save as Draft. → [mockups/key-create.html](mockups/key-create.html) |
| Choose people | "Choose people" row in New plan | Pick the Guest List from the chosen Group's Members. Full-screen checklist. → [mockups/key-choose-people.html](mockups/key-choose-people.html) |
| Edit place or time | Inviter view of the Invitation page, only before the plan starts | Change only where / when (FR-14). Same fields as New plan, prefilled. The Deadline rule still applies: the Deadline must end before the new start (AD-4). → [mockups/key-edit.html](mockups/key-edit.html) |
| Group page | A row in My Groups | Group Members (avatars + names) + **Share Group Link**. → [mockups/key-groups.html](mockups/key-groups.html) |
| Create a Group | **Create a Group** button in My Groups | Group name (FR-2). After create → the new Group page, ready to share. → [mockups/key-groups.html](mockups/key-groups.html) |

Navigation rules:

- **Max 2 taps from Home** (PRD NFR Simple). Answer: tap the Invitation card → tap Count me in. Create: tap New plan → tap Publish. My Plans: already on Home (0 taps). Groups are also 2 taps: Groups icon (opens My Groups) → a Group row.
- Pending Invitations are always the first thing on Home, so Ali finds them after reopening the app without searching.
- No tab bar, no drawer. The only extra entry on Home is the small **Groups icon** in the top corner. Every inner page has a "‹ Home" back link (top left); a Group page has "‹ My Groups". New plan, Create a Group, and Edit place or time have a close "✕" instead; Choose people has "‹ New plan".
- Hidden Invitations (not on the Guest List, or someone else's Draft) return the normal 404 page; the app never shows that they exist (AD-2).

## Voice and Tone

Copy sounds like friends in a daily chat: casual, young US English, friendly slang, sometimes a bit unexpected for an "official" app. Brand posture lives in `DESIGN.md.Brand & Style`.

**Guardrail:** playful never pressures, never guilt-trips, never jokes about saying No. No is always fine, and the copy says so.

Chosen strings:

| Where | String |
|---|---|
| Yes button | **Count me in** |
| No button | **I'll pass** |
| Under the answer buttons | No is always fine. Nobody sees it. |
| Celebration, you | You're in! |
| Celebration, friends | Reza is in · Sara is in |
| After No (title / line / button) | Okay. You said no. · Only you can see this. · Back to Home |
| Home greeting | Hi Ali |
| Home sections | Waiting for your answer · My Plans |
| Invitation card | Soroush · Fri 21 Nov, 20:00 · 2 going · 42 min left |
| Plan row meta | Sara's plan · Sat 22 Nov, 10:30 · You're in |
| Draft row meta | Your plan · only you can see it |
| Home empty | Nothing waiting. · Start a plan? |
| My Plans empty | Plans you make or say Yes to will show here. |
| Main button on Home | + New plan |
| Invitation header | Soroush invites you |
| Facts card keys | Where · When · Cost · Answer |
| Pre-answer Yes List label | Going |
| New plan labels | Pick an icon · What · Where · When · Cost · Deadline · Who gets it |
| Where helper | Decide later — "Decide later" means you agree on the place in Notes. |
| When options | Exact time · Time window |
| Deadline helper | How long friends have to answer. |
| Guest List options | All members · Choose people |
| Create actions | Publish · Save as Draft · Nobody gets a message until you publish. |
| Deadline error | The deadline must end before the plan starts. *(detail)* 3 h ends at 22:18, but the plan starts at 20:00. Try 30 min. |
| Notes label + privacy | Notes · Only people going see these (Invitee) · Only you and people going (Inviter) |
| Note composer | Write a note… · 0 / 280 · Send |
| Drop-out hint (after Yes) | Can't come anymore? Just say it here. |
| Inviter view | Your plan · Answers close in 36 min · Yes List · Updates live · is in · is in · just now · not confirmed yet |
| Inviter actions | Edit place or time · Cancel plan |
| Avatar picker | Welcome, Ali · Pick your avatar · Friends see it when you say Yes. · Face · Color · Continue |
| Empty Yes List after Deadline (PRD) | Nobody is free tonight 🌙 |
| Notifications-off banner (PRD) | 🔔 Turn on notifications so you don't miss plans |
| Cancel notification (PRD) | Soroush cancelled: Burger tonight 🍔 |
| Reconfirm after edit (PRD actions Still OK / Not anymore) | Plan changed · Still OK? · Still in · Not anymore · Not anymore is fine. You just leave the list quietly. (label "Still in" confirmed by Erfan; it performs the PRD action Still OK) |
| Sign up | Hey, welcome 👋 · Takes less than a minute. · Your name · Friends see this name. · Email · Password · Make my account · Already have one? Log in |
| Log in | Welcome back · Email · Password · Log in · New here? Sign up |
| Group Link landing | Soroush invited you to · Burger Gang 🍔 · Join the group · I already have an account |
| Add to Home Screen (iPhone) | One more thing · Put the app on your home screen, so plans can reach you. · Tap Share ⬆ · Tap "Add to Home Screen" · Open it from your home screen and log in once · Done, it's there · Skip for now |
| Groups icon (screen-reader label) | My Groups |
| My Groups | My Groups · 7 members · + Create a Group |
| Group page | 7 members · you · Share Group Link · Anyone with the link can join this group. |
| Create a Group | New group · Group name · Like "Burger Gang 🍔". You can share the link next. · Create group |
| Group picker | For: Burger Gang 🍔 ▾ |
| Choose people | Choose people · From Burger Gang 🍔 · Select all · Done · 3 people |
| Edit place or time | Edit place or time · Only place and time can change. · People who said Yes get a message and need to confirm it still works. · Save changes |
| Cancelled (Yes List) | Soroush cancelled this plan. · Notes stay open, if you want to chat. |
| Closed (Invitee) | Answers are closed. · This one's done. No worries. |
| Closed (Inviter) | Answers closed · Your plan is still on. Going solo works too. *(with empty Yes List)* |
| Draft | Draft · Only you can see this. · Delete draft |
| Time window | Sat 22 Nov, 19:00–22:00 · Anytime in this window |

Do / Don't:

| Do | Don't |
|---|---|
| "I'll pass" | "Decline", "Reject", "No thanks 😢" |
| "Okay. You said no." | "Are you sure?", "You'll miss out!", "Maybe next time?" |
| "Nobody is free tonight 🌙" | "0 people are coming" |
| "42 min left" | "Hurry! Only 42 min!" |
| "The deadline must end before the plan starts." + how to fix | "Invalid input", "Error 409" |
| Short, casual lines, like a text from a friend | Formal app language, exclamation spam |

All notification and result texts live in one module (`app/notifications/messages.py`, AD-7).

## Component Patterns

Behavioral. Visual specs live in `DESIGN.md.Components`; names match.

| Component | Use | Behavioral rules |
|---|---|---|
| Button: Count me in | Invitation page, unanswered | **Same size as I'll pass** (same height, same width); only the amber fill marks Yes, so size never pushes an answer. One tap answers Yes (POST via HTMX). No confirm dialog. Disabled while the request runs, so a double tap can't send twice (the server also refuses a second change, AD-5). Response swaps in the Yes state and plays the celebration. |
| Button: I'll pass | Invitation page, unanswered | One tap answers No. No confirm, no reason field. Response swaps in the Calm No panel. |
| Button: Publish | New plan | Validates the whole form on the server. On error, the form comes back with the same values and an inline error. On success, goes to the Inviter view of the new Invitation. |
| Button: white / New plan | Home, Pick your avatar, Note composer | New plan opens New plan. Continue saves the avatar and goes to Home. Send posts a Note. |
| Button: ghost | New plan, Inviter view, Calm No panel | Save as Draft saves without notifying anyone. Edit place or time opens the edit form. Back to Home returns Home. |
| Button: text (Cancel plan) | Inviter view | [ASSUMPTION: asks one simple confirm, because cancelling notifies the Yes List and cannot be undone.] Status becomes Cancelled (FR-13). |
| Back link | Every inner page | Goes to the parent page: Home, or My Groups from a Group page, or New plan from Choose people. |
| Section label + count badge | Home | Count shows how many Invitations wait for an answer. Hidden when 0. |
| Invitation card | Home, Waiting for your answer | Whole card is one link to the Invitation page. Sorted by Deadline, soonest first [ASSUMPTION]. Leaves the section once answered, or when the Deadline passes, or when cancelled. |
| Plan row | Home, My Plans | Whole row is one link. Shows the Updated mark when the place or time changed, the plan was cancelled, or a new Note came since the User last opened it (FR-16). Opening it clears the mark. Drafts show the Draft tag and are seen only by the Inviter. A row leaves 24 hours after "when" ends (`when_end`, or `when_start` for an exact time; architecture "Updated" convention). |
| Deadline indicator | Invitation card, facts card | Shows time left in plain words ("42 min left", "5 h left"). Updates on page load [ASSUMPTION: no live countdown]. |
| Avatar / Avatar stack | Everywhere a person appears | Always face + color + shape from the User's choice. Stacks show the Yes List only, never the Guest List. |
| Facts card | Invitation page | Where (or "Decide later"), When (exact time or window), Cost Tag, and the Deadline as time left (row label "Answer"). Read-only for Invitees (FR-7). |
| Going row | Invitation page, unanswered | Shows the current Yes List so Ali knows who is coming before he answers (FR-9). Never shows who was asked, who said No, or who has not answered. No comment or "suggest another plan" field here (FR-7). |
| Celebration stage | Invitation page, right after Yes | Plays once, on the Yes response only (see Interaction Primitives). Then stays as a static header: hub icon + Yes List avatars. |
| Yes List | Inviter view | Shows `YES` and `YES_PENDING` people only. New arrivals pop in with "is in · just now". Refreshes by HTMX polling [ASSUMPTION: every few seconds while the page is open]. |
| Live dot | Yes List header | Shows that the list refreshes by itself. Stops pulsing with reduced motion. |
| Note bubble / Note composer | Invitation page (Yes state and Inviter view) | Only the Inviter and the Yes List see and write Notes. Max 280 characters; counter counts up; Send is disabled when empty or over the limit. New Notes show on open/refresh (HTMX polling allowed, not live chat). |
| Icon picker | New plan | Pick one activity icon. Required [ASSUMPTION]. Mock shows 6 icons: 🍔 🍣 🍕 ☕ 🎬 🍺 [OPEN: final list]. |
| Text input | New plan | "What" is required. "Where" can be left open with **Decide later**. |
| Chip | New plan | Single choice per group (Cost Tag: Free / $ / $$ / $$$; Deadline: 10 min / 30 min / 1 h / 3 h [ASSUMPTION: list from the mock; PRD Q1 still open]). Decide later is a toggle chip that clears and disables the Where input. |
| Segmented control | New plan, When | Exact time shows date + time; Time window shows date + start + end [ASSUMPTION: no mock]. |
| Radio row | New plan, Who gets it | All members (default, shows stack + count) or Choose people (opens Choose people). |
| Inline error | New plan, Edit place or time | Shown under the broken field after submit; field marked invalid; message says what is wrong and how to fix it. Everything else keeps its typed value. |
| Face picker / Color swatch | Pick your avatar | Tap to select; the big preview and the "Ali is in" chip update at once (client-side). 12 faces, 5 colors. |
| Empty state | Home | Shows when nothing waits. Decorative shapes; New plan stays one tap away. |
| Calm No panel | Invitation page, after No | Static. Back to Home only. |
| Reconfirm prompt | Invitation page, `YES_PENDING` | Shows what changed (old value struck through, new value) and two same-size buttons: **Still in** (button-white, PRD Still OK) / **Not anymore** (button-no) (FR-14). No amber. Still in → card disappears, Yes layout stays. Not anymore → removed silently, then Calm No panel. Shown only before the plan starts; after that no change is possible and the User stays "not confirmed yet" (AD-5). → [mockups/key-edit.html](mockups/key-edit.html) |
| Notification banner | Home | Shown once when notifications are off and the first Invitation arrives; top of Home, above Waiting for your answer; dismissible with ✕; never returns (FR-12). [ASSUMPTION: a small **Turn on** pill asks the browser for permission; on iPhone outside the home-screen app it opens the Add to Home Screen guide.] → [mockups/key-banner.html](mockups/key-banner.html) |
| Groups icon button | Home, top corner | Opens My Groups. Always visible, also on empty Home. |
| Group picker | New plan, first field | Shows "For: <Group> ▾". Defaults to the **last-used Group** (the Group of the User's last published or drafted plan; first time: the first Group joined). Tap → a simple list of my Groups. Hidden when the User is in only one Group [ASSUMPTION]; then a plain "For: Burger Gang 🍔" line shows. Changing the Group resets Who gets it to All members of that Group [ASSUMPTION]. |
| Group row | My Groups | Whole row is one link to the Group page. Sorted by last used [ASSUMPTION]. Avatar stack shows a few Members (Group Members are not private inside the Group). |
| Member row | Group page | Read-only list of Members with avatar + name. No answer history, no "last seen", no counts of Yes (privacy NFR). |
| Share Group Link | Group page | Opens the phone's share sheet (Web Share API) with the Group Link; fallback: copies the link and shows "Link copied" [ASSUMPTION]. Any Member can share (FR-3). |
| Create a Group | My Groups | One field (Group name, required). Create → the new Group page with Share Group Link ready (FR-2). |
| Check row | Choose people | Tap anywhere on the row toggles the person. Starts with nobody checked [ASSUMPTION]; "Select all" toggles all. Done shows the count and returns to New plan with the Who gets it row reading "3 people". Done is disabled at 0. |
| Status banner | Invitation page, Cancelled or Closed | Plain line on top ("Soroush cancelled this plan.", "Answers are closed."). No color, no motion. |

## State Patterns

**Invitation page** (one page; the server picks the state):

| State | Who | Treatment |
|---|---|---|
| Unanswered (Open) | Invitee | Header "Soroush invites you", activity icon + title, facts card, Going row, Count me in / I'll pass, "No is always fine. Nobody sees it." |
| Unanswered, empty Yes List | Invitee | Going row hidden [ASSUMPTION]. Never "0 going". |
| Just said Yes | Invitee | Celebration, then title + facts line, Notes, drop-out hint. No "Change answer". |
| Said Yes (later visits) | Invitee | Same layout, final frame, no animation [ASSUMPTION]. |
| Just said No / said No (later) | Invitee | Calm No panel. No animation, no list of others. |
| Not confirmed yet (`YES_PENDING`) | Invitee | Reconfirm prompt on top, then the Yes layout. Not anymore → removed silently, then Calm No panel. |
| Deadline passed, no answer | Invitee | Leaves Waiting for your answer. If opened (old link) [ASSUMPTION]: status banner "Answers are closed." + facts, no buttons, no Going row. → [mockups/key-states.html](mockups/key-states.html) |
| Cancelled | Yes List | Plan row shows Updated. Page shows the status banner "Soroush cancelled this plan." on top; greyed hub icon; Notes stay readable and writable (FR-13, AD-3 allows Notes when Cancelled). Unanswered Invitees stop seeing it. → [mockups/key-states.html](mockups/key-states.html) |
| Inviter, Open | Inviter | "Your plan" tag, facts line, "Answers close in 36 min", Yes List (live), Notes, Edit place or time (hidden once the plan starts), Cancel plan. |
| Inviter, Closed with Yes | Inviter | Same, without the close countdown [ASSUMPTION: "Answers closed"]; the live dot is gone. Edit place or time stays until the plan starts; Cancel plan stays while the plan is Open or Closed (AD-3, FR-13). → [mockups/key-states.html](mockups/key-states.html) |
| Inviter, Closed, empty Yes List | Inviter | Soft message "Nobody is free tonight 🌙" in an empty-state card. Never "0 people". → [mockups/key-states.html](mockups/key-states.html) |
| Inviter, Cancelled | Inviter | Status banner on top [ASSUMPTION: "You cancelled this plan."]; final Yes List and Notes; Notes stay readable and writable (AD-3). No Edit place or time, no Cancel plan. |
| Draft | Inviter | New plan form prefilled with a Draft tag; Publish / Save as Draft / Delete draft (AD-3). → [mockups/key-states.html](mockups/key-states.html) |
| Time window | Anyone who sees the plan | When shows "Sat 22 Nov, 19:00–22:00" with "Anytime in this window" under it. → [mockups/key-states.html](mockups/key-states.html) |
| Hidden / not allowed | Anyone else | Standard 404 page. |

**Other surfaces:**

| State | Surface | Treatment |
|---|---|---|
| Nothing waiting | Home | Empty state "Nothing waiting." / "Start a plan?" |
| No plans | Home, My Plans | "Plans you make or say Yes to will show here." |
| Updated | Home, plan row | Updated mark until opened. |
| Notifications off | Home | Banner once (FR-12). → [mockups/key-banner.html](mockups/key-banner.html) |
| Form error | New plan, Edit place or time | Inline error per field; form keeps values. |
| Server error / network fail on an action | Any HTMX action | [ASSUMPTION: short coral inline line near the button ("Couldn't send. Try again."), button re-enabled; nothing is lost.] |
| Conflict (409, e.g. answer already set, stale reconfirm) | Invitation page | Page reloads to the true state (AD-5). |
| Offline | Any | [OPEN: no offline design decided; PWA shell only.] |
| Cold load | Any | Server-rendered full page; no skeletons. |
| Focus | Forms, buttons | Visible focus ring on every interactive element [ASSUMPTION: 2px white outline]. |
| First time after sign-up | Pick your avatar | Shown once. A small "Skip" link gives a random avatar and color; in v1 the avatar cannot be changed later (decided by Erfan). |

## Interaction Primitives

- **Tap to act.** One tap answers. No swipes, no long-press, no drag.
- **HTMX swaps** for answer, Notes, Yes List refresh, and form errors. Full page loads for navigation.
- **No confirm dialogs on answers.** Yes and No are one tap each.

### The Yes celebration (signature moment)

Runs once, right after Count me in succeeds. Total about 3 seconds. Timings lifted from [mockups/key-invitation.html](mockups/key-invitation.html) (state b):

1. **0 s — Icon pops out.** The activity icon (e.g. 🍔, 130px) jumps up from the middle and flies **past the top of the phone screen**, rotating a little, then fades out (1.5 s, springy ease). Six small confetti bits (avatar gradients + amber) fly up and fall.
2. **0 s — Amber glow** fades in behind the stage (2.6 s), then stays softly.
3. **0.5 s** — Title and facts line rise in.
4. **0.95 s — Icon lands** in the hub with a small bounce (0.7 s).
5. **1.35 s, 1.7 s … — Avatars pop in one by one** around the hub with a bounce (0.55 s each, 0.35 s apart): "Reza is in", "Sara is in".
6. **Last — You.** Your avatar pops in bigger, with the amber ring and glow and the amber "You're in!" bubble.
7. **2.5 s** — Notes and the drop-out hint rise in.

Rules:

- **Vibration:** one short buzz at step 1, **Android only** (Vibration API). iPhone has no vibration in the browser/PWA; nothing replaces it. [OPEN: exact pattern]
- **Sound:** off by default. [OPEN: where a User turns it on.]
- **Reduced motion** (`prefers-reduced-motion: reduce`): skip all motion (jump, confetti, glow growth, pop-ins, rise, live-dot pulse). Show the final state at once. No vibration [ASSUMPTION].
- **Only Yes celebrates.** No has no motion, no sound, no vibration.
- **Not addictive.** The celebration is the same every time. No streaks, no counters, no "you said Yes 5 times!".
- Motion comes from the **Tavolo direction's burger pop** only, not its table look.
- [OPEN: how many avatars fit around the hub when the Yes List is large.]
- [ASSUMPTION: a Yes sent from an Android notification button plays no celebration; the next page open shows the final frame.]

### Other motion

- New Yes List row (Inviter view) pops in with the same bounce.
- Live dot pulses softly.
- Nothing else animates. No page transitions, no hover effects.

**Banned:** "Change answer", confirm dialogs on Yes/No, reason fields, comment or "suggest another plan" fields before answering (FR-7), showing No or missing Answers anywhere, counts of who was asked, streaks or scores, red countdowns, guilt copy, pull-to-refresh, infinite scroll.

## Accessibility Floor

Behavioral. Contrast lives in `DESIGN.md.Colors` (all text pairs AA, lowest 7.3:1).

- **Tap targets ≥ 44px** on every interactive element (PRD NFR).
- **Reduced motion** honored as above; the final state never depends on animation.
- **Screen readers:** after Yes, an `aria-live="polite"` region announces "You're in! Burger tonight". After No: "Okay. You said no." Decorative shapes, confetti, and the jumping icon are `aria-hidden`.
- **Avatars** have the person's name as their label (emoji alone is not a name). Activity icons have a text label ("Burger").
- **Color is never the only signal:** errors = coral + "!" icon + text, with `aria-invalid` and `role="alert"`; selected chips/cells use `aria-pressed` or `aria-checked`; "not confirmed yet" is text, not only the dashed style; Deadline is text.
- **Focus:** visible focus ring everywhere; after an HTMX swap, focus moves to the new state's heading (Yes, No, error).
- **Forms:** every input has a real label; the 280 counter is announced only near the limit [ASSUMPTION].
- **Zoom:** layout survives 200% text zoom at 360px with no sideways scroll.

## Key Flows

### Flow 1 — Soroush wants a burger tonight (UJ-1)

Soroush, Friday evening, at home, logged in.

1. Opens the app. Home: nothing waiting that fits.
2. Taps **+ New plan**.
3. Picks 🍔, types "Burger tonight", "Burgeria da Gino, Via Roma 14", Exact time Fri 21 Nov 20:00, Cost Tag $$, Deadline 3 h, All members.
4. Taps **Publish**. Inline error: "The deadline must end before the plan starts." with "Try 30 min." Everything else stays.
5. Picks **30 min**, taps **Publish**. Invitees get a notification. He lands on the Inviter view: "Answers close in 30 min", empty Yes List.
6. Sara and Reza say Yes; their rows pop in.
7. **Climax:** Ali's row pops in: "Ali · is in · just now". Soroush sees the Yes List grow and knows who is coming.
8. Deadline passes. He gets the result notification; the plan stays in My Plans. Sara writes "Meet at the door at 8?" in Notes.

Edge: nobody says Yes → after the Deadline he sees "Nobody is free tonight 🌙" and can still go alone. Draft path: **Save as Draft** → the plan shows in My Plans with a Draft tag, only he sees it; nobody is notified until he publishes.

### Flow 2 — Ali passes from the bus (UJ-2)

Ali, tired, on the bus after university. iPhone, PWA installed, notifications on.

1. Notification: 🍔 Burger tonight, Burgeria da Gino, 20:00, Deadline.
2. iPhone has no notification buttons, so he taps it. The Invitation page opens directly (unanswered state).
3. He sees the facts and the Going row: Sara, Reza.
4. Taps **I'll pass**. No reason field, no confirm.
5. **Climax:** calm screen: "Okay. You said no." / "Only you can see this." A few seconds, no chat, no guilt.
6. Taps **Back to Home**. Nobody is ever shown his No (Silent No).

Android variant: he taps **I'll pass** right on the notification and is done without opening the app [ASSUMPTION: notification buttons use the same labels]. Failure: network fails → inline "Couldn't send. Try again." [ASSUMPTION]; his Answer is not saved until it succeeds.

### Flow 3 — Ali says Count me in (UJ-1 / UJ-2, Yes path)

Ali, Sunday morning, at home. Leila's "Sushi Sunday 🍣" is waiting.

1. Opens the app. Home shows **Waiting for your answer** on top with the Sushi card ("1 going", "5 h left").
2. Taps the card. Invitation page: Soroush is going.
3. Taps **Count me in**. Android: short buzz.
4. **Climax:** 🍣 jumps out of the phone, lands in the middle, Soroush pops in, then Ali with the amber glow: "You're in!".
5. Notes appear. He writes "See you there 🍣" and taps Send.
6. Back on Home, the plan is now in My Plans with "You're in".

Later, Leila changes the time → Ali gets a notification, and the page shows the Reconfirm prompt with **Still in / Not anymore** (PRD actions Still OK / Not anymore). Still in keeps him on the Yes List. Not anymore removes him silently.

### Flow 4 — Ali joins Burger Gang and picks his avatar (UJ-3)

Ali, on his phone, gets a WhatsApp message from Soroush with the Group Link.

1. Opens the link in the browser. Landing shows "Burger Gang 🍔" and "Soroush" (nothing else).
2. Signs up (name, email, password).
3. **Pick your avatar:** taps 🐙 and Coral. The preview and the "Ali is in" chip update. Taps **Continue**.
4. Joins the Group. [ASSUMPTION: then a short step guides "Add to Home Screen" on iPhone, and he logs in once inside the home-screen app — iPhone keeps separate cookies (architecture onboarding convention).]
5. Allows notifications.
6. **Climax:** he is inside Burger Gang and sees the other Members' faces: 🦊 Soroush, 🐸 Sara, 🐻 Reza.

Edge: Ali blocks notifications → he can still see and answer in the app; when his first Invitation arrives he sees the banner once ("🔔 Turn on notifications so you don't miss plans").

## Responsive & Platform

| Context | Behavior |
|---|---|
| Phone, 360px+ | The design target. Single column, 20px gutter, no sideways scroll. |
| Wider screens (tablet, desktop) | [ASSUMPTION: same single column, centered, max ~480px, black around it.] |
| PWA | Installable from the browser; standalone display; service worker for Web Push. Theme and background color `#000000` [ASSUMPTION]. Respect safe-area insets (notch, home bar). |
| iPhone (Safari / PWA) | Push only after Add to Home Screen. **No notification buttons**: tapping a notification opens the Invitation page. **No vibration.** Log in once inside the home-screen app. |
| Android (Chrome / PWA) | Notification buttons answer directly (signed token, AD-9). Vibration on Yes. |

## Inspiration & Anti-patterns

- **Lifted from How We Feel** ([imports/inspiration-howwefeel-mobbin-grid.png](imports/inspiration-howwefeel-mobbin-grid.png), [imports/inspiration-howwefeel-onboarding.png](imports/inspiration-howwefeel-onboarding.png)): pure black canvas, white high-contrast text, large serif headlines, white pill buttons, colorful gradient shapes as playful characters, lots of empty space. Inspiration only; never copy its brand or shapes.
- **Lifted from Duolingo:** the energy of the Yes celebration (a moment that jumps out of the screen + vibration).
- **Lifted from direction Tavolo** (exploration): only the activity icon popping out of the phone after Yes.
- **Rejected — typical AI-generated app look.** The app must feel new and personal.
- **Rejected — design that makes people "addicted" to Yes** (streaks, scores, presence points; PRD Non-Goals, SM-C1).
- **Rejected — sad or punished No.** No stays calm and neutral.
- **Rejected — "Change answer".** Answers are final in v1 (FR-8).
- **Rejected for v1 — photo avatars.** Emoji face + color now; real photos in v1.1 with photo storage.

## Future (not v1)

- **Mood status (v1.1 candidate, PRD §6.2 "Later").** Each Member can set a short mood (e.g. "down for anything ✨", "chill night 🛋️"). It shows next to each Member on the Group page, so an Inviter can pick someone in a good mood and invite just them through Choose people. Before building: decide who sees a mood and whether it expires at midnight (PRD change via the PM). In v1, inviting one person already works through Choose people.
- **Real profile photos** replace chosen avatars in v1.1, together with photo storage.

## Open Questions / Handoff

**Cross-team data needs (for John / Winston — not yet in PRD or architecture):**

1. **Invitation activity icon field** (e.g. `Invitation.activity_icon`). Needed by the icon picker, Home cards, plan rows, the Invitation page, and the celebration. Decide: the final icon list, required or optional, and a default.
2. **User avatar fields** (e.g. `User.avatar` = one of 12 faces, `User.avatar_color` = sun / mint / violet / coral / cream). The shape comes from the color. Set once at sign-up in v1 [ASSUMPTION: no edit screen in v1].

**UX open items:**

3. ~~Entry points to the Group page and to Create a Group; how the Group is chosen in New plan.~~ **Resolved:** small Groups icon in Home's top corner → My Groups (list + Create a Group) → Group page (Members + Share Group Link). New plan starts with "For: Burger Gang 🍔 ▾", defaulting to the last-used Group.
4. Final Deadline chip list (mock: 10 min / 30 min / 1 h / 3 h; PRD Open Question 1).
5. Activity theming beyond the icon (the earlier idea of the whole page turning "burger"); v1 spine uses the icon + celebration only.
6. Sound: where a User turns it on, and which sound.
7. Vibration pattern (Android).
8. How many avatars fit around the celebration hub when the Yes List is large.
9. ~~Count me in vs I'll pass size.~~ **Resolved:** same size (58px, full width, same type); only the amber fill marks Yes.
10. ~~Missing mocks.~~ **Resolved:** all surfaces now have mocks (gallery linked in Foundation).
11. Offline behavior beyond the PWA shell.
12. Yes List polling interval (Inviter view).
