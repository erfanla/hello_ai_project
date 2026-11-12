---
title: 'Adversarial review — Architecture Spine v1'
reviewed: ARCHITECTURE-SPINE.md (draft, 2026-11-11)
context: prd.md (final, 2026-11-11)
lens: two units that each follow every AD to the letter, but still build things that do not fit together
date: 2026-11-11
---

# Adversarial review — Architecture Spine v1

## Verdict

**Needs a small revision before stories.** The layers, the computed Status (AD-4), and the single visibility module (AD-2) are good. But AD-3, AD-5 and AD-7 leave four gaps. Two stories can follow every rule and still (a) send a "result" push for a cancelled plan, (b) let an Inviter edit a cancelled plan or a Draft through the wrong path, (c) break the answer state machine when two requests arrive at the same time, and (d) show that a hidden Invitation exists by returning 403 instead of 404. Each gap needs one more line in an AD. None of them needs a new component.

Ranking: **Critical** = breaks a PRD core rule ("Nobody gets hurt", Silent No, privacy) or sends a wrong push to real friends. **High** = likely to happen in the 4-week test. **Medium** = data-shape clash that will cost a rewrite between stories. **Low** = edge case, fix if cheap.

## Holes

### H1 — Critical — The sweep sends a "Deadline result" for Cancelled (and maybe Draft) Invitations

- **Unit A (Cancel story, FR-13):** `invitations.cancel()` sets `cancelled_at` and pushes "Soroush cancelled" to the Yes List. This follows AD-3 and AD-4.
- **Unit B (Deadline sweep story, FR-10):** follows AD-7 word for word: `deadline_at <= now AND result_notified_at IS NULL`. That query does not check `cancelled_at` or `published_at`.
- **Clash:** a plan cancelled at 19:30 with a 20:00 Deadline gets a "result" push at 20:00, after the "cancelled" push. If the Draft story saves `deadline_at` when the Draft is saved (AD-4 does not say when it is set), a Draft that was never published also gets a result push. This conflicts with FR-15 ("nobody is notified until it is published").
- **Fix:** AD-7: the sweep selects only Invitations where `status(inv, now) == Closed` (so not Cancelled and not Draft). AD-4: a Draft stores `deadline_minutes`, and `deadline_at` is set only by `publish()` as `published_at + deadline_minutes`.

### H2 — High — No "which action is allowed in which Status" table, so edit, reconfirm, cancel and Notes disagree

- **Unit A (Edit place/time story, FR-14):** AD-5 says only "until 'when' starts", so the story checks `now < when_start` and nothing else.
- **Unit B (Cancel story):** sets `cancelled_at`. **Unit C (Draft story, FR-15):** needs to edit everything (what, Cost Tag, Guest List) on a Draft and reuses the edit function, or writes a second edit path.
- **Clash:** the Inviter can edit a **Cancelled** plan. That moves `YES → YES_PENDING` and sends a "place/time changed" push for a dead plan. A Draft edit through the FR-14 function sends a push before the plan is published, or the Draft story builds its own unchecked edit function. An edit can also move "when" to before `deadline_at`, which breaks FR-4 ("Deadline must be before when starts"). Reconfirming a Cancelled plan is not forbidden either.
- **Fix:** add one guard table to AD-3 (action × Status → allowed?): answer = Open only; edit place/time = Open/Closed and `now < when_start` and new `when_start > deadline_at`; reconfirm = Open/Closed and not after `when_start`; cancel = Open/Closed; add Note = Open/Closed/Cancelled; full Draft edit = Draft only (a different function, no push). Every service function checks this one table.

### H3 — High — Two answers at the same time break the AD-5 state machine (last write wins)

- **Unit A (Answer from notification action, FR-8):** reads the entry, sees `NONE`, writes `YES`.
- **Unit B (Answer from the one-screen Yes/No page, FR-8):** the same User taps No on the page a second later. That request also read `NONE` before A committed, and writes `NO`.
- **Clash:** both requests follow AD-5 ("NONE → NO is allowed"), but the result is `YES → NO`, which AD-5 forbids. The User was on the Yes List (maybe already in Notes) and then silently disappears. The same race happens between "Still OK" and an Inviter edit. A "Still OK" tap from an old page (made for edit #1) also confirms edit #2, which the User has never seen. SQLite tests will not show this race; Neon will.
- **Fix:** AD-5: every answer change is a conditional update (`UPDATE … WHERE id=? AND answer=<expected from-state>`) and checks the row count; 0 rows → `InvalidState`. A reconfirm form carries the Invitation's `place_time_changed_at` and is refused if it is out of date.

### H4 — High — The error convention returns 403, which shows that a hidden Invitation exists (privacy leak)

- **Unit A (Answer / Notes service, AD-3):** "checks permission". A User who is not on the Guest List calls `POST /invitations/42/answer`, and the service raises `NotAllowed`.
- **Unit B (Error handler, Consistency Conventions):** `NotAllowed → 403`.
- **Clash:** AD-2 says not-invited Members get "not found", but AD-3 and the error convention let each write function choose. A 403 on `/invitations/42` and a 404 on `/invitations/43` tell a curious friend which IDs are plans they were left out of. That hurts, and it breaks FR-5. The IDs are small integers, so guessing them is easy.
- **Fix:** AD-2: every service function (read **and** write) first loads the Invitation through `visibility.get_visible_invitation(user, id)`, which raises `NotFound`. `NotAllowed` is used only for Users who can already see the Invitation (for example, a No-answerer posting a Note).

### H5 — Medium — When are Guest List rows created, and who is "all Members"?

- **Unit A (Draft / Guest List story, FR-5/FR-15):** creates `GuestListEntry` rows when the Draft is saved, following AD-5 ("one row per invited Member").
- **Unit B (Open Invitations story, FR-6):** for the default "all Members", reads Membership live, so a friend who joins the Group through the Group Link after publishing also sees the plan. **Unit C (Answer):** needs a row, but finds none for that friend.
- **Clash:** the friend sees the plan but gets an error when answering. Or the friend joined between Draft and publish and gets no row and no push. Two stories, two different meanings of "the Guest List".
- **Fix:** AD-5: `GuestListEntry` rows are created only in `publish()`, from the chosen Members (or all Members at that moment). The Guest List is fixed after that, and AD-2 reads only rows, never Membership, for Invitation visibility.

### H6 — Medium — Sending a push inside the transaction, and two writers of `result_notified_at`

- **Unit A (any AD-3 service):** "check, apply, ask notifications to send, **in one transaction**". The push is sent, then the commit fails (a conflict from H3, or Neon drops the connection), so friends get a push about a change that never happened.
- **Unit B (Sweep, AD-7):** "sends the result, then sets `result_notified_at`" from `app/jobs/`. But AD-3 says only `invitations.py` writes Invitation rows, and the Jobs layer "contains no rules". Two owners for one column. If the process restarts between send and set, the push is sent twice.
- **Fix:** AD-3/AD-7: services send pushes only **after** the commit succeeds (collect the messages, then send after commit). The sweep calls `invitations.close_and_notify(inv_id, now)`, which first commits `result_notified_at` (it claims the job) and then sends. This gives at-most-once: for friends, one missing push is better than two.

### H7 — Medium — The "Updated" mark (FR-16) has no data to compare, and no owner for `PLAN_SEEN`

- **Unit A (Edit story):** updates `where`/`when` in place. AD-5 forbids extra columns per edit, so it stores no change time.
- **Unit B (My Plans story):** needs "place or time changed since last seen". It has `cancelled_at` and `Note.created_at`, but nothing for edits. `PLAN_SEEN` is not in AD-3's list, so the page route, `visibility.py`, or a new service may each write it.
- **Clash:** the Updated mark never shows for edits, or the My Plans story adds its own column. A read in `visibility.py` that writes `PLAN_SEEN` also breaks "reads have no side effects".
- **Fix:** add `place_time_changed_at` to `Invitation` (also used in H3). `invitations.mark_seen(user, inv, now)` is the only writer of `PLAN_SEEN`, and the Invitation page route calls it. Changes made by the User themself do not count as "Updated".

### H8 — Low — Smaller timing gaps (fix if cheap)

- **Answer vs sweep read:** an answer with `now` just before the Deadline can commit after the sweep has read the Yes List, so the result push is missing one Yes. Fix: the sweep only takes Invitations where `deadline_at <= now - 5s`.
- **`YES_PENDING` after "when" starts:** reconfirming is no longer allowed, so the User stays "not confirmed yet" forever. Fix: AD-2 shows `YES_PENDING` as Yes after `when_start` (no row rewrite, the same idea as "NONE after the Deadline means No").
- **Cancel push audience:** FR-13 says "Yes List". AD-2 says the Yes List includes `YES_PENDING`. State in AD-7 that every Yes-List push includes `YES_PENDING`, so the cancel story and the edit story do not pick different audiences.

## Not holes (checked)

- The sweep running twice is already handled by AD-8 (single instance).
- Status getting out of date is handled by AD-4 (computed).
- Notes leaking to No-answerers is handled by AD-2 (Yes List only), as long as H4 is fixed.
