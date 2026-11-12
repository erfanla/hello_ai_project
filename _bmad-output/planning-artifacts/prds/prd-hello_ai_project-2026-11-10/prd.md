---
title: "PRD: Low-pressure friend invite app"
status: final
created: 2026-11-10
updated: 2026-11-11
---

# PRD: Low-pressure friend invite app
*Working title. The product has no name yet.*

## 0. Document Purpose

This PRD defines version 1 (v1) of a small web app that Erfan is building as his first real project, to test with about 12 friends. It is the input for architecture and for the epics and stories. Sources: the brainstorming session (`_bmad-output/brainstorming/brainstorm-first-real-project-2026-11-10/`) and the PRD interview recorded in `.memlog.md` in this folder. Technical choices and research are in `addendum.md`. Words in the Glossary (§3) are used with exactly that meaning everywhere. Guesses are tagged `[ASSUMPTION]` and listed in §9.

## 1. Vision

A web app that lets friends invite each other out without pressure. Friends answer with one tap. Saying no never needs a reason. The Inviter gets clear Answers, not a chat full of comments that change the plan.

This matters because going out should be easy, even on a bad day. Sometimes a simple Invitation, with no talking, is the easiest way to say "let's just be together." Every Invitation in this app works that way.

**Core rules** (every feature must respect them):
- **Nobody gets hurt.** Nobody is shown who said No. Nobody is asked "why?"
- **Your plan stays your plan.** Others can answer an Invitation, but they cannot change it.
- **Simple first.** Every feature must be easy to use on a phone. If a feature makes the app confusing, it waits.

## 2. Target User

### 2.1 Jobs To Be Done
- **As an Inviter:** "When I want to go out, help me find out quickly whether anyone really wants to come, without starting a group-chat debate and without the fear of hearing no."
- **As an Invitee:** "When I get asked out, let me answer in seconds, and let me say no without explaining myself."
- **Emotional:** "When I feel down, let me be with friends without having to talk about why." This matters most for shy or introverted people.

### 2.2 First Users and Non-Users (v1)
- **First users:** Erfan's friends, about 2 Groups of 6 people (about 12 Users), for a 4-week test.
- **Not for (v1):** strangers, public events, event organizers, large parties, businesses.

### 2.3 Key User Journeys

- **UJ-1. Soroush wants a burger tonight, without the group-chat wait.**
  It is Friday evening. Soroush wants a burger, but he does not want to start a long group chat. He is logged in. He opens the app and checks the **Open Invitations** in his Groups. If one fits, he answers **Yes** and he is done. If not, he creates an **Invitation**: a specific burger shop (or a place left open), a time, a **Cost Tag**, and a **Deadline** of 1 hour. Invitees get a notification and answer. **Climax:** Soroush sees the **Yes List** grow, and when the Deadline passes, he knows who is coming. **Resolution:** Soroush and the Yes List open the Invitation from **My Plans**, use **Notes** ("meet at the door at 8"), and meet at the shop. **Edge case:** nobody said Yes. Soroush sees a soft message ("Nobody is free tonight 🌙") and can still go alone.

- **UJ-2. Ali says no from the bus, and nobody asks why.**
  Ali is tired on the bus after university. His phone shows a notification: what 🍔, where 📍, when 🕗, and the Deadline. He answers **No** from the notification (on iPhone, he taps it and gets a one-screen Yes/No page). **Climax:** no reason, no chat, no guilt. It takes a few seconds. **Resolution:** nobody is shown Ali's No (**Silent No**).

- **UJ-3. Ali joins Soroush's Group.**
  Soroush creates the Group "Burger Gang 🍔" and shares its **Group Link** on WhatsApp. Ali opens the link, signs up, adds the app to his home screen, and allows notifications. **Climax:** Ali is inside the Group and sees the other Members. **Edge case:** Ali blocks notifications. He can still see and answer Invitations in the app, and gets one gentle banner (FR-12).

## 3. Glossary

- **User**: a person with an account. Every person must sign up; there are no guest Answers.
- **Group**: a set of Users who know each other (e.g. "Burger Gang"). A User can be in many Groups.
- **Member**: a User inside a Group.
- **Group Link**: a link that lets a person sign up (if needed) and join one Group.
- **Invitation**: a plan posted to one Group: what, where, when, Cost Tag, Deadline, Guest List.
- **Invitation Status**: one of **Draft** (saved, not published, only the Inviter sees it) → **Open** (published, Deadline not passed) → **Closed** (Deadline passed); or **Cancelled** (by the Inviter, from Open or Closed).
- **Open Invitation**: an Invitation with Status Open, shown to its Invitees.
- **Inviter**: the User who created an Invitation.
- **Invitee**: a Member on an Invitation's Guest List.
- **Guest List**: the Members chosen by the Inviter to receive the Invitation (default: all Members). Members not on it never see the Invitation.
- **Answer**: an Invitee's reply, **Yes** or **No**. An Answer never has a reason.
- **Deadline**: the time when answering ends, chosen by the Inviter. After it, an Invitee with no Answer counts as No.
- **Yes List**: the Invitees who answered Yes.
- **Silent No**: the rule that No Answers (and missing Answers) are never shown to anyone, including the Inviter.
- **Notes**: short text messages on one Invitation, readable and writable only by the Inviter and the Yes List.
- **My Plans**: a User's list of Invitations they created or answered Yes to.
- **Cost Tag**: the expected cost of an Invitation: Free, $, $$, or $$$.

## 4. Features

### 4.1 Accounts and Groups
**Description:** People sign up, create Groups, and invite friends with a Group Link. Realizes UJ-3.

#### FR-1: Sign up and log in
A person can create an account and log in. Realizes UJ-3.
- Sign-up asks only for what is needed to identify the User and show their name to friends.
- A new User can finish sign-up in under 1 minute (not counting home-screen install).
- **Why sign-up is required:** similar apps let friends answer from a link without an account, which is easier. This app gives that up because Silent No and notifications need to know who each person is. The risk (friends not finishing sign-up) is measured by SM-0.

#### FR-2: Create a Group
A User can create a Group with a name and becomes its first Member. Realizes UJ-3.

#### FR-3: Join with a Group Link
A Member can share a Group Link. A person who opens it can sign up (if needed) and join that Group. Realizes UJ-3.
- After joining, the new Member sees the Group and its Members.
- `[ASSUMPTION: any Member can share the Group Link, not only the creator]`

### 4.2 Invitations
**Description:** The Inviter posts a plan that others can answer but not change. Realizes UJ-1.

#### FR-4: Create an Invitation
A Member can create an Invitation in a Group with: what (text), where (a place, or "open"), when (exact time or a time window), a Cost Tag, and a Deadline. Realizes UJ-1.
- The Inviter picks the Deadline length when creating it (e.g. 10 minutes, 1 hour). `[ASSUMPTION: a short fixed list of choices]`
- The Deadline must be before "when" starts.
- If "where" or "when" is open, the Yes List agrees on it in Notes. `[ASSUMPTION: this is what "flexible" means in v1; voting on options is out of scope]`

#### FR-5: Choose the Guest List
The Inviter can choose which Members get the Invitation (default: all). Realizes UJ-1.
- Members not on the Guest List never see the Invitation or any notification about it.

#### FR-6: See Open Invitations
A User can see all Open Invitations where they are an Invitee, across their Groups, and answer from there. Realizes UJ-1.

#### FR-7: Nobody else can change an Invitation
Only the Inviter can change an Invitation, and only as FR-14 allows. Invitees can only answer. There is no place to comment or suggest another plan before answering. Realizes UJ-1.

#### FR-13: Cancel an Invitation
The Inviter can cancel their Invitation when its Status is Open or Closed. Realizes UJ-1.
- The Status becomes Cancelled. It is not deleted, so the Yes List can still read its Notes.
- Every User on the Yes List gets a notification (e.g. "Soroush cancelled: Burger tonight 🍔").
- Invitees who have not answered stop seeing it in Open Invitations, with no notification.
- The Inviter may add a reason in Notes, but it is optional.

#### FR-14: Edit place and time
The Inviter can change only the "where" and "when" of an Invitation, and only before "when" starts. Realizes UJ-1.
- Each User on the Yes List gets a notification and must reconfirm: **Still OK** (button label "Still in") or **Not anymore**. While answering is still open, Invitees who have not answered also get a notification with the new details.
- "Not anymore" removes the User from the Yes List silently, like a No.
- To change anything else (what, Cost Tag, Guest List, Deadline), the Inviter cancels and creates a new Invitation.
- `[ASSUMPTION: until a User reconfirms, they stay on the Yes List marked "not confirmed yet"]`

#### FR-15: Save as Draft
The Inviter can save an Invitation as a Draft and publish it later. Realizes UJ-1.
- Only the Inviter sees a Draft; nobody is notified until it is published.
- The Deadline starts counting when the Draft is published.

#### FR-16: My Plans
A User can see My Plans: the Invitations they created or answered Yes to, with any Status (including Closed and Cancelled). Realizes UJ-1.
- An Invitation shows an **Updated** mark if, since the User last opened it, its place or time changed, it was cancelled, or a new Note was added.
- `[ASSUMPTION: an Invitation leaves My Plans 24 hours after "when"]`

### 4.3 Answering
**Description:** Answering takes one tap and never needs a reason. Realizes UJ-2.

#### FR-8: Answer Yes or No
An Invitee can answer Yes or No with one action, from the notification (where the device allows it) or from a one-screen Yes/No page. Realizes UJ-2.
- There is no field for a reason.
- On devices without notification buttons (iPhone), tapping the notification opens the Yes/No page directly.
- In v1, an Answer is final, except when the Inviter edits the place or time (FR-14). To drop out after a Yes, a User writes in Notes.

#### FR-9: Silent No
No and missing Answers are never shown to anyone. Realizes UJ-2.
- The Inviter sees the Yes List as it grows, before and after the Deadline. `[ASSUMPTION: the Inviter sees the Yes List before the Deadline, not only after it]`
- An Invitee can see the Yes List **before** answering, so they know who is coming (e.g. to avoid a night with someone they do not want to see). They never see the full Guest List or who said No.
- **Known limit:** Silent No hides *who* said No, not *how many* were asked. In a small Guest List, people can guess. Accepted for v1.

#### FR-10: Deadline ends answering
When the Deadline passes, the Status becomes Closed, and missing Answers count as No. Realizes UJ-1.
- The Inviter is notified with the result.
- If the Yes List is empty, the Inviter sees a soft message ("Nobody is free tonight 🌙"), never "0 people".

### 4.4 Notes
**Description:** The Yes List coordinates without leaving the app. Realizes UJ-1.

#### FR-11: Notes on an Invitation
The Inviter and the Yes List can read and post Notes on an Invitation. A User can do this as soon as they are on the Yes List. Realizes UJ-1.
- A Note is at most 280 characters.
- Notes appear when the Invitation page is opened or refreshed (an automatic refresh every few seconds is allowed). They are not real-time chat.
- Nobody outside the Inviter and the Yes List can see the Notes.

**Out of scope:** live chat, typing indicators, notifications for each Note (see §6.2).

### 4.5 Notifications
**Description:** Notifications bring the Invitation to the Invitee. They must feel worth opening. Realizes UJ-2, UJ-3.

#### FR-12: Notifications
Each Invitee gets one notification per new Invitation, showing what, where, when, and the Deadline. Realizes UJ-2, UJ-3.
- The only other notifications in v1: the Deadline result (FR-10), cancelled (FR-13), and place/time changed (FR-14). No reminders and no "X is coming" messages (see §6.2).
- On iPhone, notifications only work after the app is added to the home screen. Sign-up guides the User through this.
- If a User has notifications off when their first Invitation arrives, they see one dismissible banner ("🔔 Turn on notifications so you don't miss plans"). If they dismiss it, it never comes back.

### 4.6 Cross-cutting NFRs
- **Phone first:** every screen works at 360 px width with no sideways scrolling. Buttons are at least 44 px tall. Works in a phone browser and as a home-screen app.
- **Simple:** the main actions (create, answer, open My Plans) are reachable in at most 2 taps from the app's start screen.
- **Privacy:** a User only sees Groups they belong to, and Invitations they created or are on the Guest List of. No screen shows a User's past Answers to other Members.
- **Speed:** answering from a notification takes under 5 seconds.

## 5. Non-Goals (Explicit)
- Not a chat app. No live group chat in v1.
- Not a public event platform. No strangers, no public Invitations.
- No scores, ratings, or "presence" points (they create pressure).
- No money handling: no payments, no splitting bills.
- No native iOS/Android app in v1.

## 6. MVP Scope

### 6.1 In Scope
FR-1 to FR-16: sign-up and log-in (FR-1), Groups (FR-2) and Group Links (FR-3), Invitations (FR-4) with a Guest List (FR-5), Open Invitations (FR-6), only the Inviter can change an Invitation (FR-7), one-tap Answers (FR-8), Silent No (FR-9), Deadline (FR-10), Notes (FR-11), a small set of notifications (FR-12), cancelling (FR-13), editing place/time (FR-14), Drafts (FR-15), and My Plans (FR-16).

### 6.2 Out of Scope for MVP
- **Next (v1.1):** change your Answer freely; one last-chance reminder before the Deadline; multiple options with auto-pick; control over who can see your Answer; full live chat for the Yes List; "repost for another day" button on the soft result screen; notification limits (quiet hours, max Invitations per day).
- **Later:** shared photo album; mood status and "follow"; anonymous gift ("your share is covered"); "pay me back later"; AI activity and timing suggestions (rule: a **private coach** that only the User sees, never public); place suggestions when nobody says Yes; widening an Invitation to more friends; 1-to-1 personal Invitations; "busy tonight" cover; mutual secret crush.
- **Group housekeeping (not in v1):** leaving a Group, removing Members, resetting a Group Link, deleting an account.
- **Parked, needs care:** "favourite" and "people I'd rather avoid" lists with alerts when they say Yes (maybe a premium feature). Risk: if an "avoid" list ever leaks, it hurts people, which breaks the "Nobody gets hurt" rule.
- **Parked growth ideas** (they risk adding pressure; check against SM-C1 first): "Ali is coming, want to join?" notifications; a "who's coming" notification before the Deadline; alerts when a favourite person says Yes.

## 7. Success Metrics
Measured over the 4-week test with about 12 friends in 2 Groups. The testers are friends, so the numbers may look better than with real users.

**How we measure:** SM-0 to SM-2 come from app data. SM-3 and SM-4 come from a short weekly check-in with the friends ("Which plans did you actually go to?"), because the app cannot see real meetups. `[ASSUMPTION: manual check-in chosen for v1]` App proxy, for comparison: an Invitation with Status Closed and a Yes List of 1 or more.

**Primary**
- **SM-0**: Invited friends who join a Group within 48 hours of getting the Group Link: at least 80%. Validates FR-1, FR-3.
- **SM-1**: Invitations published: at least 8 per Group (16 total). Validates FR-4.
- **SM-2**: Invitees who answer before the Deadline: at least 70%. Validates FR-8, FR-12.
- **SM-3**: Invitations that end in a real meetup: at least 50%. Validates FR-10, FR-11.
- **SM-4** ⭐: Users who go to a meetup and later answer Yes to another Invitation: at least 60% (counted per person). Validates the product as a whole.

**Secondary**
- **SM-5**: Invitations with at least one Note from the Yes List. No target. It shows if Notes are useful. Validates FR-11.

**Counter-metrics (do not optimize)**
- **SM-C1**: Users who turn off notifications: warning if more than 40%. Counterbalances SM-2.
- **SM-C2**: Users who ignore 3 Invitations in a row: warning if more than 25%. `[ASSUMPTION: threshold proposed during the PRD interview, to confirm]` Counterbalances SM-1 and SM-2.

## 8. Open Questions
1. Which Deadline choices exist (10 min, 30 min, 1 hour, 3 hours…)?
2. How does sign-up work (email link, password, Google)? Decide with the architect. It must stay under 1 minute.
3. Do the friends really feel this problem? Not yet asked. `[ASSUMPTION: they do]` A short message to both Groups before building is cheap.

## 9. Assumptions Index
- §4.1 FR-3: any Member can share the Group Link.
- §4.2 FR-4: Deadline length comes from a short fixed list.
- §4.2 FR-4: "flexible" in v1 means "where/when open, agreed in Notes".
- §4.2 FR-14: until reconfirming, a User stays on the Yes List marked "not confirmed yet".
- §4.2 FR-16: Invitations leave My Plans 24 hours after "when".
- §4.3 FR-9: the Inviter sees the Yes List before the Deadline, not only after it.
- §7 SM-3, SM-4: measured by a manual weekly check-in.
- §7 SM-C2: the 25% threshold.
- §8 Q3: the friends really feel this problem (not yet checked).
