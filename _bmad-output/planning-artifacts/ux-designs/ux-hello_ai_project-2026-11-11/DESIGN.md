---
name: Low-pressure friend invite app
description: 'Notte Pura: pure black, big white serif words, one warm amber lamp for Yes. Dark only. Phone-first PWA, server-rendered (Jinja2 + HTMX 2).'
status: final
created: 2026-11-11
updated: 2026-11-11
sources:
  - _bmad-output/planning-artifacts/prds/prd-hello_ai_project-2026-11-10/prd.md
  - _bmad-output/planning-artifacts/architecture/architecture-hello_ai_project-2026-11-11/ARCHITECTURE-SPINE.md
colors:
  # Dark only. There are no light-mode tokens.
  background: '#000000'
  surface: '#141414'
  surface-raised: '#1F1F1F'
  ink: '#FFFFFF'
  ink-muted: '#A3A3A3'
  line: '#2B2B2B'
  accent: '#FFB547'
  on-accent: '#000000'
  inverse: '#FFFFFF'
  on-inverse: '#000000'
  error: '#FF7A6B'
  # Avatar gradients (135deg, from -> to). Names match the color picker labels.
  avatar-sun-from: '#FFD25E'
  avatar-sun-to: '#FF9A1F'
  avatar-mint-from: '#4FE3A5'
  avatar-mint-to: '#18B877'
  avatar-violet-from: '#7D95FF'
  avatar-violet-to: '#8A5CFF'
  avatar-coral-from: '#FF7A6B'
  avatar-coral-to: '#FF4F8B'
  avatar-cream-from: '#F7F2E8'
  avatar-cream-to: '#CFC6B4'
typography:
  display-xl:
    fontFamily: Gloock
    fontSize: 46px
    fontWeight: '400'
    lineHeight: '1'
    letterSpacing: -0.01em
  display-lg:
    fontFamily: Gloock
    fontSize: 42px
    fontWeight: '400'
    lineHeight: '1'
    letterSpacing: -0.01em
  headline:
    fontFamily: Gloock
    fontSize: 36px
    fontWeight: '400'
    lineHeight: '1.05'
    letterSpacing: -0.01em
  headline-sm:
    fontFamily: Gloock
    fontSize: 30px
    fontWeight: '400'
    lineHeight: '1.1'
    letterSpacing: -0.01em
  title:
    fontFamily: Gloock
    fontSize: 24px
    fontWeight: '400'
    lineHeight: '1.1'
    letterSpacing: -0.01em
  body-lg:
    fontFamily: Onest
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.4'
  body:
    fontFamily: Onest
    fontSize: 15px
    fontWeight: '400'
    lineHeight: '1.45'
  body-strong:
    fontFamily: Onest
    fontSize: 16px
    fontWeight: '600'
    lineHeight: '1.3'
  meta:
    fontFamily: Onest
    fontSize: 14px
    fontWeight: '400'
    lineHeight: '1.4'
  caption:
    fontFamily: Onest
    fontSize: 13px
    fontWeight: '400'
    lineHeight: '1.4'
  label-caps:
    fontFamily: Onest
    fontSize: 12px
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: 0.09em
  button:
    fontFamily: Onest
    fontSize: 17px
    fontWeight: '600'
    lineHeight: '1'
  button-lg:
    fontFamily: Onest
    fontSize: 18px
    fontWeight: '600'
    lineHeight: '1'
rounded:
  xs: 4px
  sm: 14px
  md: 16px
  lg: 18px
  xl: 24px
  full: 9999px
spacing:
  '1': 4px
  '2': 8px
  '3': 12px
  '4': 16px
  '5': 20px
  '6': 24px
  '7': 32px
  gutter-mobile: 20px
  touch-min: 44px
components:
  button-yes:
    background: '{colors.accent}'
    foreground: '{colors.on-accent}'
    typography: '{typography.button-lg}'
    radius: '{rounded.full}'
    height: 58px
  button-no:
    # Same size as button-yes (same height, same full width, same type). Only the amber fill marks Yes.
    background: '{colors.surface-raised}'
    foreground: '{colors.ink}'
    typography: '{typography.button-lg}'
    radius: '{rounded.full}'
    height: 58px
  button-publish:
    background: '{colors.accent}'
    foreground: '{colors.on-accent}'
    typography: '{typography.button-lg}'
    radius: '{rounded.full}'
    height: 58px
  button-white:
    background: '{colors.inverse}'
    foreground: '{colors.on-inverse}'
    typography: '{typography.button}'
    radius: '{rounded.full}'
    height: 52px
  button-new-plan:
    background: '{colors.inverse}'
    foreground: '{colors.on-inverse}'
    typography: '{typography.button-lg}'
    radius: '{rounded.full}'
    height: 60px
  button-ghost:
    background: 'transparent'
    foreground: '{colors.ink}'
    border: '1px solid {colors.line}'
    typography: '{typography.button}'
    radius: '{rounded.full}'
    height: 52px
  button-text:
    background: 'transparent'
    foreground: '{colors.ink-muted}'
    typography: '{typography.body}'
    height: '{spacing.touch-min}'
  back-link:
    foreground: '{colors.ink-muted}'
    typography: '{typography.body}'
    height: '{spacing.touch-min}'
  section-label:
    foreground: '{colors.ink-muted}'
    typography: '{typography.label-caps}'
    textTransform: uppercase
  count-badge:
    background: '{colors.ink}'
    foreground: '{colors.background}'
    radius: '{rounded.full}'
    size: 22px
  invitation-card:
    background: '{colors.surface}'
    border: '1px solid {colors.line}'
    radius: '{rounded.xl}'
    padding: '{spacing.4}'
    titleTypography: '{typography.title}'
  activity-tile:
    background: '{colors.surface-raised}'
    radius: '{rounded.lg}'
    size: 56px
    emojiSize: 32px
  activity-tile-small:
    background: '{colors.surface-raised}'
    radius: '{rounded.sm}'
    size: 44px
    emojiSize: 24px
  plan-row:
    divider: '1px solid {colors.line}'
    minHeight: 64px
    titleTypography: '{typography.body-strong}'
    metaTypography: '{typography.caption}'
  updated-mark:
    background: '{colors.surface-raised}'
    border: '1px solid {colors.line}'
    dot: '{colors.ink}'
    radius: '{rounded.full}'
  draft-tag:
    foreground: '{colors.ink-muted}'
    border: '1px dashed {colors.line}'
    radius: '{rounded.full}'
  your-plan-tag:
    foreground: '{colors.ink}'
    border: '1px solid {colors.line}'
    radius: '{rounded.full}'
  deadline-indicator:
    dot: '{colors.ink}'
    foreground: '{colors.ink}'
    fontWeight: '600'
  avatar:
    sizeSmall: 28px
    sizeMedium: 40px
    sizeLarge: 52px
    sizeYou: 62px
    sizePreview: 132px
    shape-sun: '50%'
    shape-mint: '50% 50% 50% 10px'
    shape-violet: '50% 50% 14px 14px'
    shape-coral: '14px'
    shape-cream: '50% 10px 50% 10px'
  avatar-stack:
    overlap: -8px
    ring: '2px solid {colors.surface}'
  facts-card:
    background: '{colors.surface}'
    border: '1px solid {colors.line}'
    radius: '{rounded.xl}'
    rowDivider: '1px solid {colors.line}'
    keyForeground: '{colors.ink-muted}'
  cost-tag:
    border: '1px solid {colors.line}'
    radius: '{rounded.full}'
    fontWeight: '600'
  going-row:
    labelTypography: '{typography.label-caps}'
    avatarSize: 52px
    nameTypography: '{typography.caption}'
  celebration-stage:
    hubBackground: '{colors.surface}'
    hubBorder: '1px solid {colors.line}'
    hubSize: 104px
    hubEmojiSize: 58px
    jumpEmojiSize: 130px
    glow: 'radial-gradient(circle, rgba(255,181,71,.24), rgba(255,181,71,0) 62%)'
    inBubbleBackground: '{colors.surface-raised}'
    youBubbleBackground: '{colors.accent}'
    youBubbleForeground: '{colors.on-accent}'
    youRing: '0 0 0 3px {colors.background}, 0 0 0 5px {colors.accent}, 0 0 34px 6px rgba(255,181,71,.5)'
  yes-list:
    rowMinHeight: 52px
    divider: '1px solid {colors.line}'
    statusForeground: '{colors.ink-muted}'
    newStatusForeground: '{colors.accent}'
    pendingAvatarOpacity: '0.5'
    pendingOutline: '1.5px dashed {colors.ink-muted}'
  live-dot:
    color: '{colors.accent}'
    size: 7px
  note-bubble:
    background: '{colors.surface}'
    border: '1px solid {colors.line}'
    radius: '4px 18px 18px 18px'
    typography: '{typography.body}'
  note-composer:
    border: '1px solid {colors.line}'
    radius: '20px'
    counterTypography: '{typography.label-caps}'
    sendButton: '{components.button-white}'
  text-input:
    background: '{colors.surface}'
    border: '1px solid {colors.line}'
    radius: '{rounded.md}'
    height: 52px
    typography: '{typography.body-lg}'
  text-input-what:
    typography: '{typography.title}'
  icon-picker:
    columns: 6
    cellBackground: '{colors.surface}'
    cellBorder: '1px solid {colors.line}'
    cellRadius: '{rounded.md}'
    selectedBorder: '2px solid {colors.inverse}'
    selectedBackground: '{colors.surface-raised}'
  chip:
    border: '1px solid {colors.line}'
    foreground: '{colors.ink}'
    radius: '{rounded.full}'
    height: '{spacing.touch-min}'
  chip-selected:
    background: '{colors.inverse}'
    foreground: '{colors.on-inverse}'
  chip-error:
    background: 'transparent'
    foreground: '{colors.error}'
    border: '2px solid {colors.error}'
  segmented-control:
    background: '{colors.surface}'
    border: '1px solid {colors.line}'
    radius: '{rounded.full}'
    selectedBackground: '{colors.inverse}'
    selectedForeground: '{colors.on-inverse}'
  radio-row:
    background: '{colors.surface}'
    border: '1px solid {colors.line}'
    selectedBorder: '1px solid {colors.inverse}'
    radius: '{rounded.md}'
    height: 56px
  inline-error:
    foreground: '{colors.error}'
    icon: 'circled "!" in {colors.error}'
    detailForeground: '{colors.ink-muted}'
  face-picker:
    columns: 4
    cellBackground: '{colors.surface}'
    cellRadius: '{rounded.lg}'
    selectedBorder: '2px solid {colors.inverse}'
  color-swatch:
    size: 52px
    selectedRing: '0 0 0 3px {colors.background}, 0 0 0 5px {colors.inverse}'
  empty-state:
    border: '1px solid {colors.line}'
    radius: '{rounded.xl}'
    titleTypography: '{typography.headline-sm}'
  calm-no-panel:
    titleTypography: '{typography.display-lg}'
    iconFilter: 'grayscale(.7), opacity .7'
  icon-button:
    # Groups icon in Home's top corner.
    background: 'transparent'
    foreground: '{colors.ink}'
    border: '1px solid {colors.line}'
    radius: '{rounded.full}'
    size: '{spacing.touch-min}'
  group-picker:
    # 'For: Burger Gang 🍔 ▾' at the top of New plan.
    background: '{colors.surface}'
    border: '1px solid {colors.line}'
    radius: '{rounded.full}'
    height: '{spacing.touch-min}'
    keyForeground: '{colors.ink-muted}'
    typography: '{typography.body-strong}'
  group-row:
    divider: '1px solid {colors.line}'
    minHeight: 72px
    titleTypography: '{typography.title}'
    metaTypography: '{typography.caption}'
  member-row:
    divider: '1px solid {colors.line}'
    minHeight: 56px
    avatarSize: 40px
    typography: '{typography.body-lg}'
  check-row:
    divider: '1px solid {colors.line}'
    minHeight: 56px
    boxSize: 24px
    boxRadius: 8px
    boxBorder: '2px solid {colors.ink-muted}'
    checkedBackground: '{colors.inverse}'
    checkedForeground: '{colors.on-inverse}'
  notification-banner:
    background: '{colors.surface}'
    border: '1px solid {colors.line}'
    radius: '{rounded.xl}'
    typography: '{typography.body}'
    actionButton: '{components.button-white}'
    dismissSize: '{spacing.touch-min}'
  reconfirm-card:
    background: '{colors.surface}'
    border: '1px solid {colors.inverse}'
    radius: '{rounded.xl}'
    titleTypography: '{typography.headline-sm}'
    stillInButton: '{components.button-white}'
    notAnymoreButton: '{components.button-no}'
  status-banner:
    # 'Cancelled' / 'Answers are closed' line on the Invitation page. Never colored.
    background: '{colors.surface-raised}'
    border: '1px solid {colors.line}'
    radius: '{rounded.md}'
    typography: '{typography.body-strong}'
---

## Brand & Style

This is a small app for friends who want to go out without pressure. Saying Yes should feel like a little party. Saying No should feel like nothing at all.

The look serves the three PRD core rules. **Nobody gets hurt:** No is never colored, never smaller, never sad, and nothing on screen shows who said No. **Your plan stays your plan:** the Invitation facts look fixed and read-only for Invitees. **Simple first:** one column, one main action per screen, lots of empty space.

The look is **Notte Pura** ("pure night"): pure black, big white words, and one warm lamp. Everything is calm and quiet, with lots of empty black space, until someone says Yes. Then the amber light comes on, the activity icon jumps out of the phone, and friends' faces pop in.

The app must **not** look like a typical AI-generated app. Personality comes from three things only: an elegant display serif for big words, playful gradient avatars (emoji faces on soft shapes), and the Yes moment. Everything else stays plain.

Dark only. There is no light mode.

Visual references: **all screens in one page: [mockups/all-screens.html](mockups/all-screens.html)**. Single files: [mockups/key-signup.html](mockups/key-signup.html), [mockups/key-grouplink.html](mockups/key-grouplink.html), [mockups/key-avatar.html](mockups/key-avatar.html), [mockups/key-home.html](mockups/key-home.html), [mockups/key-banner.html](mockups/key-banner.html), [mockups/key-groups.html](mockups/key-groups.html), [mockups/key-create.html](mockups/key-create.html), [mockups/key-choose-people.html](mockups/key-choose-people.html), [mockups/key-invitation.html](mockups/key-invitation.html), [mockups/key-edit.html](mockups/key-edit.html), [mockups/key-states.html](mockups/key-states.html). The spines (this file and `EXPERIENCE.md`) win on any conflict. Inspiration: [imports/inspiration-howwefeel-mobbin-grid.png](imports/inspiration-howwefeel-mobbin-grid.png) and [imports/inspiration-howwefeel-onboarding.png](imports/inspiration-howwefeel-onboarding.png) (black canvas, white pill button, big serif, gradient shapes as characters; inspiration only, never copy that app's brand or shapes).

## Colors

One canvas, two quiet surface steps, one hairline, one accent, one error color. All text passes WCAG AA; the lowest text pair is 7.3:1.

| Token | Hex | Job | Contrast |
|---|---|---|---|
| `background` | `#000000` | Canvas on every screen. | `ink` on it: 21.0:1 |
| `surface` | `#141414` | Cards, inputs, facts card, Notes bubbles. | `ink` on it: 18.4:1 |
| `surface-raised` | `#1F1F1F` | I'll pass button, activity tiles, small tags, "is in" bubbles, selected picker cell. | `ink` on it: 16.5:1 |
| `ink` | `#FFFFFF` | Main text, Deadline dot, Updated dot. | — |
| `ink-muted` | `#A3A3A3` | Secondary text, labels, hints, back link. | 8.3:1 on `background`, 7.3:1 on `surface` |
| `line` | `#2B2B2B` | Hairline borders and dividers. | Decorative only |
| `accent` | `#FFB547` | **Yes only:** Count me in button, Publish button, the celebration glow, the "You're in!" bubble, the "just now" Yes List status, the live dot. | `on-accent` on it: 12.0:1 |
| `on-accent` | `#000000` | Text on amber. | — |
| `inverse` / `on-inverse` | `#FFFFFF` / `#000000` | White pill buttons (New plan, Continue, Send) and every **selected** state (chips, segmented control, radio, picker cells). | 21.0:1 |
| `error` | `#FF7A6B` | Inline form errors (coral). | 7.4:1 on `background` |

Rules:

- **Amber means Yes.** It is the "go" color: Yes, Publish, celebration. Never use it for chrome, links, selection, or warnings.
- **Selection is white**, not amber. This keeps amber special.
- **No is never colored.** The No button sits on `surface-raised` with white text. No red, no grey-out, no sad tone.
- **Error is coral and never alone.** Always outline (not fill) + a circled "!" icon + text. Coral is never a fill behind text. Coral is also the start of the coral avatar gradient; because errors are always outline + icon + text, the two never look the same.
- **Time left is white**, never red or amber ("42 min left" with a white dot). No alarm colors.
- **Avatar gradients** (135deg, `from` → `to`) are the only multi-color element. Five colors: Sun, Mint, Violet, Coral, Cream. Each color comes with its own soft shape (see Shapes). They also appear as soft decorative shapes in empty states and as confetti bits in the celebration. Never use them for UI meaning.

## Typography

Two Google Fonts:

- **Gloock** (display serif) for big words: screen titles, the Invitation title, the Home greeting, card titles, the text of the "What" field. Always weight 400, slight negative tracking.
- **Onest** (clean sans) for everything else: body, times, dates, buttons, labels, numbers.

| Token | Use |
|---|---|
| `display-xl` (46px) | Invitation title on the Invitation page before answering ("Burger tonight"). |
| `display-lg` (42px) | Screen titles: Home greeting "Hi Ali", "New plan", "Pick your avatar", the calm No title. |
| `headline` (36px) | Invitation title in the Inviter view and after Yes. |
| `headline-sm` (30px) | Empty-state title ("Nothing waiting."). |
| `title` (24px) | Invitation card title on Home; text in the "What" input. |
| `body-lg` (16px) | Inputs, radio rows, calm No message. |
| `body` (15px) | Facts, Notes, Yes List rows, back link. |
| `body-strong` (16px / 600) | Plan row title in My Plans. |
| `meta` (14px) | "Soroush · Fri 21 Nov, 20:00", "2 going", inline error text. |
| `caption` (13px) | Hints, helper lines, names under avatars, plan row meta. |
| `label-caps` (12px / 600 / 0.09em, uppercase) | Section labels: WAITING FOR YOUR ANSWER, MY PLANS, GOING, YES LIST, NOTES, field labels in New plan. |
| `button` (17px / 600) | Normal pill buttons. |
| `button-lg` (18px / 600) | Count me in, Publish, New plan, Continue. |

The ramp is normalized from the mocks (they used 40–44px for screen titles; the spine uses 42px). Dates always use the format `Fri 21 Nov, 20:00` (architecture convention).

## Layout & Spacing

- Phone first. Designed at **360px** wide, single column, no sideways scroll.
- Side gutter `{spacing.gutter-mobile}` (20px).
- Scale: 4 / 8 / 12 / 16 / 20 / 24 / 32px (`{spacing.1}`–`{spacing.7}`). Related items 8–12px apart; form fields 24px apart; big groups 24–32px apart.
- Every tap target is at least `{spacing.touch-min}` (44px) tall.
- The main action sits at the **bottom** of the screen (New plan on Home, Count me in / I'll pass on the Invitation page, Publish on New plan), pushed down with empty space above it.
- Lists use hairline dividers, not boxes. Cards are used only for things you tap into (Invitation cards) or for one block of facts.

## Elevation & Depth

Depth comes from **tone**, not shadow: `background` (#000) → `surface` (#141414) → `surface-raised` (#1F1F1F), with `line` hairlines.

Shadows and glows exist only for the Yes moment and the avatar:

- The jumping activity icon gets a dark drop shadow (`0 20px 18px rgba(0,0,0,.6)`).
- The amber glow behind the celebration (`{components.celebration-stage.glow}`).
- The "You" avatar ring with amber glow (`{components.celebration-stage.youRing}`).
- The big avatar preview on Pick your avatar gets a soft colored glow from its own gradient.

Nothing else floats.

## Shapes

Soft and round, never sharp.

- `{rounded.full}` pills for every button, chip, tag, count badge, and segmented control.
- `{rounded.xl}` (24px) for cards (Invitation card, facts card, empty state).
- `{rounded.lg}` (18px) for big activity tiles and face-picker cells.
- `{rounded.md}` (16px) for inputs, radio rows, icon-picker cells.
- `{rounded.sm}` (14px) for small activity tiles in My Plans.
- `{rounded.xs}` (4px) only for the top-left "tail" corner of a Note bubble.

**Avatar shapes.** Each avatar color has its own shape: Sun = circle, Mint = round with one sharp bottom-left corner, Violet = round top with soft square bottom, Coral = soft square, Cream = leaf (two round, two soft corners). Small (28px) avatars scale the corner radii down (10px → 7px, 14px → 9px). Avatars are never initials and never photos in v1.

## Components

Names here match `EXPERIENCE.md.Component Patterns`.

- **Button: Count me in** (`button-yes`) — Full width, amber pill, 58px, black text in `button-lg`. Only on the Invitation page, before answering.
- **Button: I'll pass** (`button-no`) — **Exactly the same size as Count me in**: full width, 58px, `button-lg`. `surface-raised` pill, white text. Directly under Count me in. Only the amber fill marks Yes; size never pushes one answer. Under it, one `caption` line in `ink-muted`.
- **Button: Publish** (`button-publish`) — Same look as Count me in. The only other amber button.
- **Button: white** (`button-white`) — White pill, black text. Continue, Send. **New plan** (`button-new-plan`) is the 60px version with a "+".
- **Button: ghost** (`button-ghost`) — Transparent with hairline. Save as Draft, Edit place or time, Back to Home.
- **Button: text** (`button-text`) — Muted text only, 44px tall. Cancel plan.
- **Back link** — "‹ Home" (or "‹ My Groups", "‹ New plan") in `ink-muted`, top left, 44px tall.
- **Section label** — `label-caps` in `ink-muted`. May carry a **count badge** (white circle, black number).
- **Invitation card** (Home) — `surface` card, 24px corners. Top: activity tile (56px) + title in `title` + meta line ("Soroush · Fri 21 Nov, 20:00"). Bottom, after a hairline: avatar stack + "2 going" on the left, Deadline indicator on the right.
- **Plan row** (My Plans) — 64px row, small activity tile (44px), title in `body-strong`, meta line in `caption` ("Sara's plan · Sat 22 Nov, 10:30 · You're in"). Right side: **Updated mark** (pill with white dot) or **Draft tag** (dashed pill, muted).
- **Deadline indicator** — White dot + bold time left ("42 min left"). No color change as time runs out.
- **Avatar** — Emoji face centered on a gradient shape. Sizes: 28 (lists, stacks), 40 (header), 52 (Going row, celebration), 62 ("You" in celebration), 132 (preview).
- **Avatar stack** — Small avatars overlapping by 8px, each with a 2px `surface` ring.
- **Facts card** (Invitation page) — `surface` card with rows Where / When / Cost / Answer (the Answer row shows the Deadline as time left). Keys in `ink-muted` `caption`, 52px column. Second line (address) in `ink-muted`.
- **Cost Tag** — Outline pill with the value: Free, $, $$, $$$.
- **Going row** — `GOING` label + 52px avatars with names under them. Shows the Yes List only.
- **Celebration stage** (after Yes) — 104px round hub (`surface`, hairline) holding the activity icon (58px emoji). Avatars with "Reza is in" bubbles (`surface-raised` pills) around it; "You" last, 62px, amber ring and glow, with an amber "You're in!" bubble. Behind it: the amber radial glow. Above it during motion: the 130px activity icon and six small confetti bits in the avatar gradients and amber.
- **Yes List** (Inviter view) — Rows of 52px: small avatar, name, status on the right in `ink-muted` ("is in"). New arrival: status in amber ("is in · just now"). Not confirmed: avatar at 50% opacity with dashed outline, status in a dashed pill ("not confirmed yet"). Header has the **live dot** (amber, softly pulsing) + "Updates live".
- **Your plan tag** — Hairline pill top right in the Inviter view.
- **Note bubble** — Small avatar + name and time in `caption` muted + `surface` bubble with a 4px top-left corner.
- **Note composer** — Hairline box (20px corners), auto-growing text area, counter "0 / 280" bottom left, white **Send** pill bottom right.
- **Text input** — `surface`, 52px, 16px corners. The "What" input uses `title` (serif) for its text.
- **Icon picker** — 6-column grid of emoji cells (`surface`, 16px corners). Selected = white 2px border on `surface-raised`.
- **Chip** — Outline pill, 44px tall. Selected = white fill, black text. Error = coral 2px outline and coral text (`chip-error`). Used for Cost Tag, Deadline, "Decide later".
- **Segmented control** — Two options in a `surface` pill ("Exact time" / "Time window"). Selected = white.
- **Radio row** — `surface` row, 56px, 16px corners. Selected = white border and white filled dot. Right side shows extra info (avatar stack + count, or "›").
- **Inline error** — Coral circled "!" + coral bold line + muted detail line under it. Sits right under the field.
- **Face picker** — 4-column grid of 12 emoji faces (`surface` cells, 18px corners). Selected = white 2px border.
- **Color swatch** — 52px gradient swatch in its own avatar shape. Selected = black gap + white ring.
- **Empty state** — Hairline card with three soft gradient shapes (decorative), serif title, muted line.
- **Reconfirm prompt** (`reconfirm-card`) — `surface` card with a white hairline, on top of the Invitation page: "Plan changed" label, serif "Still OK?", what changed (old value struck through in `ink-muted`, new value in `ink`), then **Still in** (`button-white`) and **Not anymore** (`button-no`), same size, stacked. No amber. → [mockups/key-edit.html](mockups/key-edit.html)
- **Notification banner** (`notification-banner`) — `surface` card at the top of Home: 🔔 line in `body`, a small white **Turn on** pill, and a 44px ✕ to dismiss. → [mockups/key-banner.html](mockups/key-banner.html)
- **Groups icon button** (`icon-button`) — 44px round hairline button with a simple two-people line icon, top right of Home, above the greeting. Label "My Groups" for screen readers.
- **Group picker** (`group-picker`) — `surface` pill at the top of New plan: muted "For:" + Group name in `body-strong` + "▾". → [mockups/key-create.html](mockups/key-create.html)
- **Group row** (`group-row`) — My Groups list row: Group name in `title` serif, meta "7 members" in `caption`, avatar stack, "›". Hairline dividers.
- **Member row** (`member-row`) — Group page: 40px avatar + name in `body-lg`; your own row says "you" in `ink-muted`. → [mockups/key-groups.html](mockups/key-groups.html)
- **Check row** (`check-row`) — Choose people: avatar + name + 24px rounded checkbox on the right. Checked = white box with black ✓ (selection is white). → [mockups/key-choose-people.html](mockups/key-choose-people.html)
- **Status banner** (`status-banner`) — `surface-raised` strip on top of the Invitation page for "Soroush cancelled this plan." or "Answers are closed." Plain white text, an emoji, no color. → [mockups/key-states.html](mockups/key-states.html)
- **Calm No panel** — Small greyed activity tile + muted title line, serif title, muted line, ghost button. No color, no motion.

## Do's and Don'ts

| Do | Don't |
|---|---|
| Use amber only for Yes, Publish, and the celebration | Use amber for links, selection, warnings, or decoration |
| Show selection in white | Mix several accent colors for state |
| Keep No calm: dark pill, white text, no motion, same size as Yes | Make No grey, red, smaller, hidden, or sad |
| Show time left in plain white text | Turn the Deadline red or orange as time runs out |
| Show errors as coral outline + "!" icon + text | Use color alone for an error, or fill a block with coral |
| Use emoji faces on gradient shapes for people | Use initials, photos (v1), or default grey user icons |
| Use Gloock only for big words | Set body text, buttons, or numbers in the serif |
| Use tone (#000 → #141414 → #1F1F1F) and hairlines for depth | Add card shadows or glows outside the Yes moment |
| Keep lots of black space | Fill the screen with boxes, banners, or icons |
| Stay dark only | Add a light theme |
