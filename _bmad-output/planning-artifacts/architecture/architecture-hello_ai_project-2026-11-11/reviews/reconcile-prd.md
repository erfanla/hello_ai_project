---
type: review
review: input-reconciliation
target: ../ARCHITECTURE-SPINE.md
inputs:
  - ../../../prds/prd-hello_ai_project-2026-11-10/prd.md
  - ../../../prds/prd-hello_ai_project-2026-11-10/addendum.md
  - ../.memlog.md
created: '2026-11-11'
---

# Input reconciliation: PRD vs Architecture Spine

Goal: find PRD rules that the spine contradicts, or where the spine is silent and two stories built separately could end up doing different things. Pure UI detail is left out.

Severity: **High** = two stories will almost surely differ, or a core rule (Silent No, privacy, timing) can break. **Medium** = likely rework. **Low** = small; a one-line note in the spine is enough.

## Summary

| # | Gap | PRD source | Severity |
| --- | --- | --- | --- |
| G1 | The Draft has no Deadline length, and "when" is not modelled, so "Deadline before when" has no single check | FR-4, FR-14, FR-15, FR-16 | High |
| G2 | Answering from a notification button breaks the CSRF rule; on iPhone the home-screen app has its own login cookies; the Group Link token is lost during install | FR-1, FR-3, FR-8, FR-12, UJ-2, UJ-3, NFR Speed | High |
| G3 | The deadline sweep does not say which Invitations it skips or who gets the result | FR-10, FR-12, FR-13, FR-15 | High |
| G4 | YES_PENDING has no end state, and its Notes access and Cancel notification are not stated | FR-11, FR-13, FR-14, FR-16 | Medium |
| G5 | The "Updated" mark and "leaves My Plans 24h after when" need change timestamps and a "when end" that the model does not have | FR-16 | Medium |
| G6 | The notifications-off banner needs saved "dismissed" state, and "notifications off" is not defined | FR-12, SM-C1 | Medium |
| G7 | The Group Link landing page is public, but the spine does not say what it may show | NFR Privacy, FR-3 | Low |
| G8 | Metrics SM-0 and SM-C1 need data the model does not keep | §7 | Low |

---

## G1 — Draft, Deadline length, and "when" are not modelled (High)

**PRD:** FR-4: the Inviter picks a Deadline *length* from a short fixed list; "when" is an exact time **or a time window**; "where" may be "open"; **the Deadline must be before "when" starts**. FR-15: the Deadline starts counting **at publish**. FR-14: the Inviter can later change "when".

**Spine:** AD-4 stores `deadline_at` and `published_at` only. There is no field for the Deadline length, and no fields for "when" (start, optional end) or "where open".

**Divergence risk:**
- The "create Draft" story may save `deadline_at = now + length` (wrong: the clock should start at publish). The "publish" story may then reuse it. Or the Draft story saves nothing, and the publish story has no length to use.
- "Deadline before when" can be checked at create, at publish (a late publish can push the Deadline past "when"), and at edit (FR-14 can move "when" before the Deadline). Each story may check it differently, or not at all.
- A time window vs an exact time changes what "before when starts" means and what "24h after when" (FR-16) means.

**Proposed fix (one rule):** Store `deadline_minutes` (enum from the fixed list) on the Draft; set `deadline_at = published_at + deadline_minutes` only in `publish()`. Model `when_start` (required) and `when_end` (nullable); `where` nullable = "open". One function in `invitations.py`, `check_deadline_before_when(deadline_at, when_start)`, is called by create, publish, and edit place/time; a failure raises `InvalidState`. Decide whether an edit may move `when_start` before an active Deadline (suggest: no). Also answer PRD open question 1 (the list of lengths) or record it as a config list.

## G2 — Answering from a notification, iPhone install, and the session (High)

**PRD:** FR-8: answer with one action **from the notification** where the device allows it (Android/desktop buttons), otherwise tap → one-screen Yes/No page. NFR Speed: under 5 seconds. FR-12/UJ-3: on iPhone, push works only after "Add to Home Screen", and sign-up guides the User through it. FR-1: sign-up under 1 minute. FR-3: a person opens the Group Link, signs up, joins.

**Spine:** AD-9: session cookie, `SameSite=Lax`; "Forms & CSRF": every change carries a CSRF token checked by one middleware. Nothing about the service worker, notification actions, or install flow.

**Divergence risk / contradiction:**
- A notification action button runs in the service worker. It has no page form, so it has no CSRF token. If the CSRF middleware applies, Android one-tap answers fail. The push story and the CSRF story will each make their own choice (skip CSRF? put a token in the push payload? open a page instead?).
- On iPhone, the home-screen app has **its own cookie storage**, separate from Safari. A friend who signs up in Safari from the WhatsApp link must log in again inside the installed app. The push subscription must be made inside the installed app. This affects the "under 1 minute" goal and the order of the sign-up steps.
- If the friend installs the app before joining, the Group Link token in the Safari URL is lost (the home-screen app opens at `start_url`).
- Session lifetime is not set. If the cookie expires, a notification tap leads to a login page, which breaks the 5-second goal.

**Proposed fix:** Add an AD for "answer from notification": the push payload carries a signed, short-lived, single-purpose answer token (Invitation id + User id + expiry), and one endpoint accepts it instead of CSRF, still calling the same `invitations.answer()` service. iPhone taps open `/invitations/{id}/answer` (one URL convention for all stories). Set a long session lifetime (e.g. 90 days, sliding). Define the onboarding order: Group Link → sign-up + join (in the browser) → install guide → log in again in the home-screen app if needed → ask for push permission. Join before install, so the token is not lost.

## G3 — Deadline sweep scope and result recipients (High)

**PRD:** FR-10: at the Deadline, "**the Inviter** is notified with the result"; an empty Yes List gives a soft message ("Nobody is free tonight 🌙"), never "0 people". FR-12: the result is one of only four notification types. FR-13: an Invitation can be Cancelled while Open. FR-15: a Draft has no running Deadline.

**Spine:** AD-7: the sweep finds Invitations with `deadline_at <= now` and empty `result_notified_at`, then "sends the result". It does not exclude Cancelled Invitations (or Drafts, if G1 sets `deadline_at` early) and does not say who receives it.

**Divergence risk:** A sweep story that follows AD-7 word for word will send a result for an Invitation cancelled before its Deadline. One story may send the result to the Yes List too, which adds a notification the PRD does not allow (§6.2 parks "who's coming" messages). The empty-result text may be written in two places (push text and page text) with different wording.

**Proposed fix:** Add to AD-7: the sweep selects only Invitations where `status(inv, now) == Closed` (so Cancelled and Draft are skipped by the AD-4 function, not a second check). The result goes **only to the Inviter**. The result text, including the empty case, comes from one function in services, used by both the push and the page. Also state that on cancel, `result_notified_at` is not needed (skip by status).

## G4 — YES_PENDING lifecycle and rights (Medium)

**PRD:** FR-14 assumption: until reconfirming, the User stays on the Yes List marked "not confirmed yet". FR-11: Notes for the Inviter and the Yes List. FR-13: on cancel, **every User on the Yes List** gets a notification.

**Spine:** AD-5 allows reconfirm "until when starts", but does not say what YES_PENDING becomes after that. AD-2 says the Yes List includes YES_PENDING, but does not say if YES_PENDING users may read/post Notes or get the cancel / second-edit notification.

**Divergence risk:** The Notes story may check `answer == YES` and lock pending users out of Notes; the cancel story may notify only `YES`. After "when" starts, one page may show "not confirmed yet" forever while another treats it as No.

**Proposed fix:** One helper `is_on_yes_list(entry)` = `answer in (YES, YES_PENDING)` in `visibility.py`, used for Notes access and for all Yes List notifications (cancel, edit). State: after `when_start`, YES_PENDING is shown as on the Yes List (not rewritten), the same way AD-5 treats NONE after the Deadline. A second edit leaves YES_PENDING as YES_PENDING and notifies again.

## G5 — "Updated" mark and My Plans removal (Medium)

**PRD:** FR-16: "Updated" if, since the User last opened it, place/time changed, it was cancelled, or a new Note was added. Assumption: an Invitation leaves My Plans 24h after "when".

**Spine:** `PLAN_SEEN` stores when a User last opened it. Nothing says what it is compared with. There is no "when" field (G1).

**Divergence risk:** The edit story may not save a change time; the Notes story compares with `Note.created_at`; the cancel story uses `cancelled_at`. My Plans may compute "updated" in three ways, or miss one. The "user's own Note" or "user's own edit" may wrongly mark it as Updated. "24h after when" is unclear for a time window (start or end?).

**Proposed fix:** Add `last_changed_at` on `Invitation`, set by `invitations.py` in edit place/time, cancel, and add Note (one owner, AD-3). Updated = `last_changed_at > plan_seen.seen_at` and the change was not made by this User (or simply: the actor's own action also updates their `plan_seen`). My Plans hides an Invitation when `now > coalesce(when_end, when_start) + 24h`.

## G6 — Notifications-off banner (Medium)

**PRD:** FR-12: if a User has notifications off when their **first** Invitation arrives, they see **one** dismissible banner; if dismissed, it **never comes back**.

**Spine:** Silent. No User field; "notifications off" is not defined.

**Divergence risk:** One story may keep the dismissal in `localStorage` (comes back on a new phone, a new browser, or after the iPhone install, since the home-screen app has its own storage). Another may use the server. "Off" can mean "browser permission is not granted" (client-side check) or "no `PushSubscription` row" (server-side) — these differ, e.g. after a 410 deletes the subscription.

**Proposed fix:** Add `push_banner_dismissed_at` to `User` (server-side, survives devices). Define "notifications off" as "this User has no `PushSubscription` row". Show the banner only if the User has at least one Invitation as Invitee, has no subscription, and has not dismissed it.

## G7 — Public Group Link landing page (Low)

**PRD:** NFR Privacy: a User sees only Groups they belong to. FR-3: Members are seen **after** joining.

**Spine:** AD-9 makes the Group Link landing page public, but does not say what it may show.

**Proposed fix:** The landing page shows only the Group name and "Join / Sign up". Never the Member list or Invitations before joining. An invalid token returns "not found".

## G8 — Data for success metrics (Low)

**PRD:** SM-0: friends who join within 48h of getting the Group Link. SM-C1: Users who turn off notifications (warning > 40%). SM-2: answers before the Deadline.

**Spine:** AD-7 "binds" SM-C1 but deletes expired subscriptions with no record. `Membership` has no join time.

**Proposed fix:** Add `Membership.joined_at` and `User.created_at`. Do not hard-delete the information for SM-C1: log the event, or keep `PushSubscription.removed_at`. SM-2 already works from `answered_at` vs `deadline_at`.

---

## Checked and consistent (no action)

- **Silent No (FR-9):** AD-2 returns only YES / YES_PENDING; tests required. Consistent.
- **Yes List visible before answering (FR-9):** AD-2 lets Invitees read the Yes List; nothing requires an Answer first. Consistent (G4 covers YES_PENDING).
- **Members not on the Guest List never see it (FR-5):** AD-2 "not found, never forbidden"; AD-3 sends notifications from the same service. Consistent, provided notification recipients are taken from the Guest List via `visibility.py` (worth one test).
- **280-char Notes (FR-11):** not in the spine; a single field check in `invitations.add_note()` under AD-3 is enough. Suggest a model column limit too, so SQLite and PostgreSQL agree.
- **Notification limits:** deferred to v1.1 in both PRD and spine.
- **Notes not real-time:** HTMX polling allowed in both.
- **Answer is final except after edit (FR-8):** AD-5 matches.
- **Simple first / phone NFRs:** left to UX; no divergence at spine level.
