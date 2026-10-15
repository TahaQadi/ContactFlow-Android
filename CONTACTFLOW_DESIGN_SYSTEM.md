# ContactFlow design system: contacts and dialer

**Status:** Core tokens, contact rows, and dialpad styling are implemented.
Validate on Android hardware before treating the visual treatment as final;
additional interaction recommendations remain design guidance until separately
implemented.

**Scope:** Native Android Contacts and Dialer screens, implemented with the
existing Views/XML stack. This is a design specification only; it does not
change the app UI or add dependencies.

## Decision

For the first beta, retain Android Views/XML, ViewBinding, Fossify Commons, and
the Material Components for Android dependency already supplied through
`org.fossify:commons`. Define ContactFlow's own semantic tokens and component
rules on top of that foundation. Do not introduce a Compose UI migration for
these screens as part of the beta.

The current app has a View-based screen and list structure, a customized
`AppTheme.Base`, and a light/dark resource split. Material Components resolves
to 1.14.0 in the current build. Compose Material 3 appears in the resolved
dependency graph, but the app's own layouts and screen code do not use Compose;
do not rely on that transitive presence as an intentional UI framework.

## Design principles

1. **Fast to scan and operate one-handed.** Names, numbers, keypad, and primary
   call actions should be immediately legible and reachable.
2. **Contact actions are explicit.** A gesture may reveal shortcuts, but must
   not be the only way to call, message, or open a contact.
3. **Use Android conventions.** Preserve system back behavior, status/navigation
   bar contrast, text scaling, TalkBack semantics, keyboard support, and
   platform contact/account behavior.
4. **Private by default.** Do not use contact photos or account data as
   decorative material; avoid unnecessary contact-data disclosure in
   notifications and previews.
5. **Color reinforces meaning.** Call outcomes and errors also have text or
   icon cues; color is never the only signal.
6. **Drupe is an interaction reference, not a visual template.** Use original
   ContactFlow styling and wording.

## Foundation tokens

All values are starting points. Validate them on-device in light and dark
themes, with Android font scaling, and with TalkBack before calling them final.
The foreground/background pairs below are selected to provide at least 4.5:1
contrast for the listed text use.

### Color

| Token | Light | Dark | Use |
|---|---|---|---|
| `cf_primary` | `#2A4CA1` | `#B6C8FF` | Main brand action, selected controls |
| `cf_on_primary` | `#FFFFFF` | `#1A326F` | Text/icons on primary |
| `cf_primary_container` | `#E5EBFF` | `#354B82` | Selected rows/chips or quiet emphasis |
| `cf_on_primary_container` | `#172F74` | `#E0E7FF` | Content on primary container |
| `cf_secondary` | `#006B63` | `#7BD9CE` | Supporting highlights, not the main call button |
| `cf_on_secondary` | `#FFFFFF` | `#003B36` | Content on secondary |
| `cf_background` | `#F7F7FB` | `#11131A` | App window background |
| `cf_surface` | `#FFFFFF` | `#191C24` | Toolbar, search, cards, keypad surface |
| `cf_surface_container` | `#EFF1F7` | `#222630` | Grouped surfaces and key backgrounds |
| `cf_on_surface` | `#191B23` | `#E4E6EF` | Primary text and icons |
| `cf_on_surface_variant` | `#444A57` | `#BDC2D0` | Supporting text and secondary icons |
| `cf_outline` | `#737B8C` | `#8991A3` | Borders, dividers, inactive outlines |
| `cf_error` | `#BA1A1A` | `#FFB4AB` | Errors and missed-call emphasis |
| `cf_on_error` | `#FFFFFF` | `#690005` | Content on error surfaces |
| `cf_call_action` | `#176B4A` | `#62D6A3` | Main call button and positive call action |
| `cf_on_call_action` | `#FFFFFF` | `#003A28` | Content on call action |

Legacy Views app bars use the contrast-safe `cf_primary_bar` / `cf_on_primary_bar`
pair: blue with white text in light mode, and a darker blue with light text in
night mode. This keeps Material Components toolbar text legible while the
semantic `cf_primary` token remains bright in dark mode.

Use a fixed ContactFlow palette by default so brand colors do not change
unexpectedly with wallpaper. System dynamic color can be considered later as an
explicit user option, not as the default for the first beta.

Map these names to Android semantic color resources, with corresponding
night-qualified values. Do not put light-mode hex values directly in layouts.
Existing call-history colors may remain distinct by direction, but pair them
with their existing labels/icons and audit their contrast in both themes.

### Spacing, shape, and elevation

| Token family | Values | Use |
|---|---|---|
| Spacing | 4, 8, 12, 16, 20, 24, 32 dp | Insets, row gaps, and screen sections |
| Shape | 8, 12, 16, 24 dp; full pill | Small controls, fields, cards, dialogs, chips |
| Elevation | 0, 1, 3, 6 dp | Prefer flat surfaces; reserve elevation for floating/raised actions |
| Minimum touch target | 48 × 48 dp | Every actionable icon, key, chip, and row action |

Use 16 dp as the standard horizontal screen inset. Do not add decorative cards
around every contact row; use spacing and subtle dividers to keep long lists
compact.

### Type

Use the Android sans-serif system family and scalable `sp` sizes. Avoid fixed
`dp` for text; the existing dialpad text dimensions should be checked during UI
implementation to ensure user font scaling works.

| Role | Size / weight | Use |
|---|---|---|
| Screen title | 24 sp / medium | Contacts and Dialer headings |
| Section title | 18 sp / medium | Favorites and grouped sections |
| Contact name / key number | 16–32 sp / medium | Row name; dialed number scales with content |
| Body | 16 sp / regular | Contact details and primary explanatory copy |
| Supporting | 14 sp / regular | Phone number, account/source, helper text |
| Compact label | 12 sp / medium | Keypad letter labels and low-priority metadata |

Do not truncate contact names unnecessarily. Supporting text may ellipsize to
one line. At large font sizes, allow the dialed number area and list rows to
grow rather than clipping text.

## Shared component contract

| Component | Specification |
|---|---|
| App bar | Surface-colored, 56 dp minimum, clear title, 48 dp action targets. Search and overflow actions have spoken labels. |
| Search field | At least 48 dp tall, leading search icon, visible focus state, explicit clear action, and a helpful empty-query hint. Keep text contrast and cursor visible in both themes. |
| Contact avatar | 40–48 dp circle. Use the contact photo when available; otherwise initials on a deterministic, accessible-color background. Never encode contact category by avatar color alone. |
| Contact row | 64–72 dp minimum height; avatar, one-line name, one supporting line, and a clear tap target. Support pressed, selected, and action-revealed states. |
| Icon button | 48 dp minimum target, 24 dp visual icon, ripple/pressed state, and an action-specific content description. |
| Divider | 1 dp or spacing-only separation. Use `cf_outline` at restrained opacity; never use a divider as the only grouping cue. |
| Empty/error state | Short title, one sentence of explanation, and one primary next action. Distinguish no contacts, no search matches, permission denied, and load failure. |

## Contacts screen

### Structure

1. **Top area:** Contacts title, search affordance, and overflow/settings action.
2. **Optional quick section:** Favorites as a compact horizontal row or a
   clearly separated section; keep it out of the way when empty.
3. **List:** Contact rows grouped and sorted consistently with the selected
   account/filter settings.
4. **Fast scroller:** Retain the alphabetical fast-scroll behavior, but ensure
   it does not overlap row actions and has an accessible alternative.
5. **Create contact:** Keep a clearly labeled add action reachable without
   obscuring the last list rows.

### Row behavior and states

- Tapping the row preserves the existing user setting: call the contact with
  confirmation or open contact details. Do not silently change this preference.
- Keep the existing selection/action-mode routes for calling and messaging.
- Do not make a whole-row swipe place a call or hide the existing call/message
  actions behind a new gesture.
- Selected/action-mode rows use `cf_primary_container` with
  `cf_on_primary_container`; selection must also have a non-color indicator.
- Favorites use a labeled/accessible favorite state, not only a different
  avatar color.
- Sort/filter changes preserve a clear indication of the active setting.

### Contacts states

| State | Presentation |
|---|---|
| Loading | Keep the app bar stable; use a restrained progress indicator or brief placeholders. |
| Empty device contacts | Explain that contacts come from Android's contacts store; offer Create Contact and, if relevant, permission/account settings. |
| Permission denied | Explain which feature needs access and provide a direct retry/settings action; do not show a blank list. |
| No search matches | Show the query context, a clear-search action, and no misleading “no contacts” copy. |
| Load error | State that the list could not be loaded and offer Retry. Preserve filter/search input. |
| Read-only contact | Keep details available; communicate unavailable edit/delete actions without implying a failed save. |

## Dialer screen

### Structure

1. **Top bar:** Dialer title and existing overflow/menu actions.
2. **Number and match area:** Number is centered or visually anchored above the
   keypad, uses LTR number layout, and can expand to multiple lines if needed.
   Show matching contacts above the keypad without covering entered digits.
3. **Editing actions:** Backspace/clear stays adjacent to the number and has a
   48 dp target. Long-press behavior may clear the full number, but a visible
   clear action remains available.
4. **Keypad:** Three-column numeric grid with consistent key dimensions and
   spacing. Digits are primary; letter groups are secondary and remain legible.
5. **Call action:** One centered, high-contrast green call button with the
   accessible label “Call [number]” where possible. SIM choice or call
   confirmation states must remain distinguishable from the normal state.

### Key states and feedback

- Each digit key has default, pressed, and disabled states; pressed feedback
  combines ripple with a brief state change and optional system haptic.
- Keep digits at least 28 sp visually in the normal layout, but allow scaling
  and responsive shrinking/growing rather than clipping on compact devices.
- Keypad cells and the primary call action meet the 48 dp minimum target.
- The `0` key's `+` behavior and special-key long presses are discoverable and
  announced to accessibility services.
- Search suggestions are selectable independently from the call action. A
  suggestion tap opens the contact; a distinct call control initiates a call.
- When the number field is blank, preserve the existing behavior of loading the
  most recent number into the field. Keep the existing localized call label;
  do not imply that the first tap places the call.
- Maintain visible focus for hardware keyboard/D-pad navigation and preserve
  the existing LTR formatting of phone-number entry in RTL locales.

## Accessibility and quality gates

- Minimum 48 dp touch targets; verify on the smallest supported device width.
- Text scales with system font settings; validate at 100%, 130%, and 200%.
- TalkBack announces contact name, relevant number, favorite/selected state,
  and each action without duplicate or unlabeled controls.
- Color contrast: 4.5:1 for normal text and 3:1 for large text and meaningful
  non-text controls; do not rely on color alone for call history, selection, or
  errors.
- Test light/dark theme, RTL layout, keyboard navigation, permission-denied,
  empty, loading, and populated states.
- Check keypad layout with short and long numbers, matched contacts, and
  compact-height devices; verify call actions remain visible above system
  navigation insets.

## Resource and implementation mapping

This specification maps naturally to the current native project:

- Semantic colors: `app/src/main/res/values/colors.xml` and
  `app/src/main/res/values-night/colors.xml`
- Spacing and component dimensions: `app/src/main/res/values/dimens.xml`
- Typography and component styles: `app/src/main/res/values/styles.xml`
- Existing contact list host: `fragment_letters_layout.xml`
- Contact row override: `item_contact_without_number.xml` (preserves the
  Fossify Commons binding IDs and adds the primary number as supporting text)
- Existing keypad and dialer host: `dialpad.xml` and `activity_dialpad.xml`
- Existing Material Components dependency: transitive from
  `org.fossify:commons`; do not add a duplicate UI kit for this spec.

When implementing, update shared resources and reusable styles first, then
apply them to the contacts row and dialer keypad. Keep colors and dimensions out
of per-screen hardcoded values where a shared token is appropriate.

## Explicit non-goals

- No Compose migration for the first beta.
- No copying Drupe screens, visual identity, or proprietary assets.
- No contact-data upload or custom cloud contact store.
- No hidden-only gestures for essential actions.
- No new UI library dependency unless an implementation need is demonstrated.
