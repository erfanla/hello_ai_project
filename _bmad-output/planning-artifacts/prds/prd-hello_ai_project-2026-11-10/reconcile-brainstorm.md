# Reconcile: brainstorm + PRD log vs prd.md / addendum.md

Inputs checked: brainstorm `.memlog.md` (B), PRD interview `.memlog.md` (P), `prd.md`, `addendum.md`. Items the PRD log later changed (in-app chat became Notes, guest answers became "everyone signs up") are not flagged.

## High importance

1. **No limits on notifications (max invites per day, quiet hours).** Nothing in the PRD covers this, and it is not in §6.2 either.
   - B53: "Flip: limits like max invites per day and quiet hours, so every notification feels worth opening"
   - PRD FR-12 says notifications "must feel worth opening" but gives no rule that makes this happen. SM-C1 (notifications turned off) is the risk this idea protects against.
   - **Where:** add a rule under FR-12 (for example a quiet-hours window and a daily cap per Inviter), or list it in §6.2 "Next" and say why.

2. **"Very simple UI" is missing as a requirement.** The brainstorm named this as a top reason the app could fail. The PRD has no NFR for it.
   - B51: "Fail: too many features make the UI confusing; everything we discussed must feel very easy"
   - B52: "UI must be extremely simple; all features reachable in a very easy way (simple-first design)"
   - **Where:** §4 Cross-cutting NFRs, for example "Simple first: every main action (create, answer, see Yes List) takes at most N taps from the home screen".

3. **Privacy outside one Invitation: no yes/no history and the "busy tonight" cover.** The PRD only says a User doesn't see Invitations they are not on. It never says that Group Members can't see a person's answer history or which plan they joined. The "busy tonight" cover is missing, and it is not in §6.2 either.
   - B55: "Fail (drama): someone says no to a friend in private chat, but the app shows they said yes to another plan"
   - B58: "answers are visible only to people inside that same invite; nobody else in the group can see your yes/no history"
   - B65: "'Busy tonight' cover: people outside the invite only see a neutral 'busy tonight' label, never which plan you joined"
   - B92: "privacy is the core, not an extra"
   - **Where:** make the Privacy NFR in §4 stronger: no answer history, no profile that shows which Invitations you said yes to. Add the "busy tonight" cover to §6.2 (Next or Later).

4. **The soft result screen has no "repost for another day" button.** FR-10 keeps the soft message but drops the one-tap repost. The repost is not in §6.2 either.
   - B33: "show 'Nobody is free tonight' plus a one-tap button to repost the same invite for another day"
   - **Where:** FR-10 (one more line), or §6.2 Next.

5. **The rule for later AI ("private, quiet coach") is missing.** §6.2 lists "AI activity and timing suggestions" but not the rule the brainstorm set for them.
   - B35: "privately suggests similar ones ... others don't know it came from the app"
   - B92: "AI fits as a private, quiet coach (suggestions only the user sees), never public"
   - **Where:** §6.2 Later, AI line: add "private to the user, never shown to others".

## Medium / low importance

6. **The core users (introverts) and the "avoid conflict" goal are missing from Target User.**
   - B91: "Heart of the app: it helps introverts, and helps avoid conflicts between friends"
   - B92 tagline: "Ask without fear."
   - **Where:** §2 (one line about who the app is for) and §1 Vision (the tagline could be used next to "Nobody gets hurt").

7. **Metric ideas from the PRD log are missing from §7.**
   - P27: "Track how many invited friends finish joining (metric candidate)". Sign-up friction is a known risk, and FR-1 sets a target of under 1 minute.
   - P29: "4) notes used after yes to coordinate". No metric checks FR-11 directly.
   - **Where:** §7, as a secondary metric or a counter-metric (Group Link join completion rate; share of meetups that used Notes).

8. **The addendum contradicts PRD decisions.** These are research takeaways, but they read like advice and say the opposite of what was decided.
   - Addendum A, Takeaway 1: "Friends can answer from a link with no install or account". This goes against P26: "Everyone must sign up. No answering as a guest."
   - Addendum A, Takeaway 2: "leave out chat". The PRD log (P21) chose Notes in v1.
   - **Where:** in addendum §A, mark both as "considered, not chosen" and point to the decision.

9. **1-to-1 (personal) invitation is not mentioned.**
   - B60: "personal invitation (1-to-1) besides group invitation"
   - A Guest List with one Member probably covers this, but the PRD doesn't say so.
   - **Where:** add one line under FR-5 ("a Guest List of one Member = a personal Invitation"), or list it in §6.2.

10. **Learning / portfolio goal.** The brainstorm set the project goal as growing toward AI agentic engineering, with a stack and features that impress a hiring manager (B9, B40). The PRD §0 only says "first real project".
    - **Where:** §0, one sentence. This is optional, because the PRD log (P9) calls it a "learning project".
