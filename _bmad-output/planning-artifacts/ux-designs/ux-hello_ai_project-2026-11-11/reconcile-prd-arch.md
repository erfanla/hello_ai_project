# Reconcile: UX spines vs PRD and architecture

Date: 2026-11-11. Checked: `DESIGN.md`, `EXPERIENCE.md`, `mockups/` against the PRD (`prd.md`, final) and `ARCHITECTURE-SPINE.md` (final). Decisions in `.memlog.md` were not changed.

## Checks that passed (no change needed)

| Check | Result |
|---|---|
| No Answers shown anywhere | OK. Silent No is kept; "Banned" list covers it; mocks show only the Yes List. |
| Guest List shown to Invitees | OK. Avatar stacks and the Going row show the Yes List only. Guest List counts appear only to the Inviter (New plan). |
| "Change answer" option | OK. Banned in the spines; the mocks have none. |
| Notification types and recipients (AD-7) | OK. New Invitation → Invitees; Deadline result → Inviter; Cancelled → Yes List; place/time changed → Yes List. No "X is coming" or reminders. |
| Notes 280 characters (FR-11) | OK. Composer counter "0 / 280"; Send disabled over the limit. |
| Deadline before "when" on create (FR-4, AD-4) | OK. Inline error with fix ("Try 30 min"). |
| Yes List visible before answering (FR-9) | OK. Going row on the unanswered state. |
| Kind-to-No voice | OK. Guardrail + Do / Don't table. |

## Contradictions found and fixed (12)

| # | Where | Problem | Source | Fix |
|---|---|---|---|---|
| 1 | `EXPERIENCE.md` State Patterns (Inviter, Closed with Yes); `mockups/key-states.html` and `mockups/all-screens.html` caption c | Said Cancel plan stays only "until the plan starts". | AD-3, FR-13: Cancel is allowed while Open or Closed, with no start-time limit. | Edit stays until the plan starts; Cancel stays while Open or Closed. |
| 2 | `EXPERIENCE.md` Inviter, Open | Edit place or time had no time limit. | AD-3, FR-14: only before `when_start`. | Edit hidden once the plan starts; IA row says the same. |
| 3 | `EXPERIENCE.md` Reconfirm prompt | Could be answered at any time. | AD-5: no transitions after `when_start`. | Prompt shown only before the plan starts; after that the User stays "not confirmed yet". |
| 4 | `EXPERIENCE.md` Edit place or time | No Deadline check on edit. | AD-4: `deadline_at < when_start` checked on every place/time edit. | Rule added to the IA row (the mock already said it). |
| 5 | `EXPERIENCE.md` Plan row | "Rows leave 24 h after 'when'". | Architecture "Updated" convention: 24 h after `when_end` (or `when_start`). | Wording made exact. |
| 6 | `EXPERIENCE.md` State Patterns | No Inviter view for a Cancelled plan. | AD-3: Inviter may still add Notes when Cancelled; no Edit or Cancel. | New row "Inviter, Cancelled" (banner text marked [ASSUMPTION]). |
| 7 | `EXPERIENCE.md` Going row, Banned list | FR-7 rule "no place to comment or suggest another plan before answering" was not stated. | FR-7. | Added to Going row and Banned list. |
| 8 | `EXPERIENCE.md` Flow 4 step 2 | "Signs up (email + password)": name missing. | FR-1, AD-9, IA row (name + email + password). | "name, email, password". |
| 9 | `EXPERIENCE.md` Flow 3 | Used "Still OK" as a button label. | Chosen string is "Still in" (stands for PRD Still OK). | Uses "Still in", with the PRD action in brackets. |
| 10 | `DESIGN.md` (4 places) | Used "Answer page", a term not used in `EXPERIENCE.md`. | One name per surface: "Invitation page". | Replaced with "Invitation page" (before answering). |
| 11 | Both spines, Facts card | Row key "Answer" was not tied to the Glossary term Deadline. | PRD Glossary: Deadline. | Spec says the row shows the Deadline as time left, labeled "Answer". |
| 12 | `EXPERIENCE.md` Back link | "Goes to Home", but navigation rules say "‹ My Groups" and "‹ New plan" on some pages. | Internal conflict. | Back link goes to the parent page; `DESIGN.md` lists the three labels. |

## Dropped qualitative ideas, restored

- **Core rules** (Nobody gets hurt, Your plan stays your plan, Simple first): `EXPERIENCE.md` Foundation now explains how each rule shapes screens; `DESIGN.md` Brand & Style ties the look to them.
- **Emotional job** ("be with friends without having to talk about why"; shy and introverted people): added to Foundation.
- **Speed NFR** (answer from a notification in under 5 seconds): added under Simple first.
- **Open Invitations (FR-6)**: Home section "Waiting for your answer" is now mapped to the Glossary term.
- **2-tap rule**: navigation rule now shows each path (answer, create, My Plans).

## Needs the user (not changed: logged decisions or other teams)

1. **Avatar step at sign-up** (memlog decision "Faces v1") vs FR-1 ("sign-up asks only for what is needed", under 1 minute). Confirm it stays required, or allow skip with a default avatar.
2. **New data fields** `Invitation.activity_icon` and `User.avatar` / `avatar_color` (memlog decisions) are not in the PRD or architecture. John / Winston must add them.
3. **"Still in" label** (approved screens) vs the PRD action name "Still OK". Confirm the label, or update the PRD wording.
4. **Architecture inside conflict**: AD-5 says `YES_PENDING` Users get edit notifications; the AD-7 table says only `YES`. UX follows the PRD ("each User on the Yes List"). Winston should align AD-5 and AD-7.

## Polish done

- `DESIGN.md` section order matches the Google Labs DESIGN.md order (Brand & Style, Colors, Typography, Layout & Spacing, Elevation & Depth, Shapes, Components, Do's and Don'ts). "Do's and Don'ts" is the spec's own heading name, so it is kept.
- All `{token}` references in `DESIGN.md` resolve. All relative links to `mockups/` and `imports/` exist.
- Frontmatter `status: draft` kept in both spines.
