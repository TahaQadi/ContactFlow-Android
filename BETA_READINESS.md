# ContactFlow first-beta readiness

This is an internal six-month beta plan for one full-time developer, not a
public-launch commitment. The native Kotlin app is the product under test; the
legacy Expo preview does not verify Android behavior.

## Current verification record — 2026-10-15

- The Android SDK Platform 36 and Build Tools 36.0.0 are installed outside the
  repository. The source/configuration baseline check passes.
- The three JVM quick-action tests pass. Debug and signed FOSS release assembly
  complete, and both configured lint tasks pass.
- The release APK is
  `app/build/outputs/apk/foss/release/contactflow-22-foss-release.apk`.
  It reports min API 26, target/compile API 36, version 1.11.1/code 22, and
  package ID `com.contactflow.phone`. `apksigner verify` confirms its v2
  signature. Its JKS key is at `$HOME/.android/contactflow-release.jks`, mode
  0600 and outside the repository; keep an owner-controlled encrypted backup.
  APK SHA-256:
  `19fba684dbb24b61ad8fac6a40d5234b39a76f053e50289f10dbd24dac0bb4d6`.
- Release lint succeeds with 27 non-baselined warnings; the existing baseline
  suppresses 3 errors, 124 warnings, and 1 hint. Review the generated report
  before distributing a candidate.
- `adb devices` reports no attached Android device. No API 26/API 36 install,
  call-role, live-call, TalkBack, RTL, or OEM behavior has been exercised.
- Direct signed APK via private file share is the selected distribution channel.
  A dedicated release keystore was generated at
  `$HOME/.android/contactflow-release.jks` with mode 0600, outside the
  repository. Its protected alias/password secrets are configured. Keep an
  owner-controlled encrypted backup outside this workspace. A private tester
  feedback route is still unconfigured. Do not distribute the debug APK.

## Baseline inventory

Code inspection on 2026-10-15 found these inherited paths:

- **Contacts:** `ContactsHelper` loads system contacts; `ContactsFragment`
  searches names, phone numbers, email, address, notes, organization, and other
  contact fields. Create/edit/detail hand off to Android's Contacts app through
  standard contact intents. Deleting selected contacts is preceded by a
  confirmation dialog and requests write-contact permission.
- **Favorites:** the favorites tab filters starred provider records and supports
  custom ordering.
- **Dialer:** the app uses Android's dialer role/default-phone flow, accepts
  `tel:` dial intents, searches contacts from the keypad, and routes calls
  through Telecom. Calls initiated from a contact use a confirmation-check
  path.
- **Call history:** recent calls use Android's call log. The empty/denied state
  offers a call-log permission request; clearing history is confirmed.
- **Telecom:** the exported `InCallService` is protected by
  `BIND_INCALL_SERVICE`; the call-screening service is protected by
  `BIND_SCREENING_SERVICE`. Calls drive an in-call activity and notifications.
- **Quick contact actions:** tapping or horizontally swiping the contact image
  opens a Call/Message/Details menu. Calls still use the existing
  call-confirmation path, and messages are handed to Android's SMS intent
  handler. The inherited long-press selection menu continues to provide batch
  call/SMS actions. The interaction is implemented but not yet tested with
  TalkBack, large text, or on-device touch input.

These are source observations, not Android device test results. Account
ownership and Google sync remain controlled by Android's Contacts Provider and
the user's Android account settings; ContactFlow does not add an account or
cloud contact store.

## Automated baseline checks

From this directory, using Python 3.11+:

```sh
python3 scripts/check_beta_baseline.py
./scripts/build_beta_debug.sh
```

The Python check validates critical source/configuration contracts without
requiring Android tooling. The Gradle script runs focused unit tests for safe
quick-action availability, then uses one Gradle worker with a 2 GB heap, plus
OpenJDK 17 and Android SDK Platform 36/build tools for the native build and lint.
A successful build is not proof that the APK installs or that its flows work on
a device.

## Manual acceptance checklist

Record Android version, device/OEM, app version, and pass/fail notes for each
run. Do not mark a check passed based only on source inspection.

### Device coverage

- [ ] Install and launch a debug candidate on Android API 26.
- [ ] Install and launch a debug candidate on Android API 36.
- [ ] Repeat the critical contact and calling paths on one additional OEM/device,
  if available.
- [ ] Confirm app upgrade over the previous beta preserves system contacts and
  app preferences.

### Contacts and account behavior

- [ ] Deny contact access on first request: show a clear empty/denied state and
  keep non-contact dialer functionality usable.
- [ ] Grant access, then browse Google-synced and device/local contacts in
  Contacts and Favorites.
- [ ] Search by name, partial phone number, and a non-name contact field; clear
  search and verify the complete list returns.
- [ ] Create and edit a contact through Android's contact editor; verify the
  updated record is reflected after returning to ContactFlow.
- [ ] Start deletion and cancel; verify no record changes. Confirm deletion and
  verify only the selected contact is removed.
- [ ] Verify a Google-synced record still follows the selected Android account's
  sync settings and is not copied to a ContactFlow server.
- [ ] Test empty contact and no-phone-number states.

### Contact actions and accessibility

- [ ] Place a call from a contact; verify the confirmation prevents accidental
  dialing and cancel leaves the app unchanged.
- [ ] Hand a message to the user's selected SMS/messaging app; verify the
  recipient is correct and ContactFlow does not send a message itself.
- [ ] Open quick actions by tapping the contact image and by swiping it
  horizontally; verify both routes show the same options.
- [ ] Complete those actions using visible tap controls without relying on a
  long press or swipe.
- [ ] Complete those actions with TalkBack enabled and with the largest Android
  font/display settings in the supported range.
- [ ] Verify no swipe or touch gesture triggers a call before an explicit
  confirmation/tap.

### Dialer, call role, and call history

- [ ] Accept and deny the default-phone role request; verify the app explains
  what remains usable and does not claim to be the default after denial.
- [ ] Open `tel:` with a number, enter a number manually, search a contact by
  keypad letters/numbers, and test deleting/clearing dialpad input.
- [ ] Start and cancel outgoing calls; validate SIM selection on dual-SIM
  devices when available.
- [ ] Receive and answer/reject calls while unlocked and locked. Repeat with
  notifications denied and full-screen-intent access unavailable.
- [ ] Exercise mute, speaker/audio route, hold, end-call, and return-to-call
  behavior; interrupt with Home, rotation/configuration change, and a second
  incoming call where supported.
- [ ] Deny call-log access, then grant it from the in-app prompt; verify the
  denied state is understandable and recent calls load after granting.
- [ ] Delete one recent call and clear the entire call history only after
  confirming; verify cancel preserves all entries.
- [ ] Test RTL layout, process recreation, and large text for contact and call
  screens.

## Manifest permission and exported-component review

The following permissions remain declared and need runtime validation against
the beta build:

| Permission | User-facing reason / review note |
| --- | --- |
| `READ_CONTACTS`, `WRITE_CONTACTS` | Read system contacts; delete selected records after confirmation. Create/edit uses Android's contact editor. |
| `READ_CALL_LOG`, `WRITE_CALL_LOG` | Show and remove recent call-log entries. |
| `READ_PHONE_STATE`, `CALL_PHONE`, `ANSWER_PHONE_CALLS`, `MANAGE_OWN_CALLS` | Determine call/Telecom state, request calls, and operate the in-call service. Verify exact needs on API 26 and 36. |
| `WAKE_LOCK` | Keep the in-call screen/proximity behavior working during a call. |
| `FOREGROUND_SERVICE`, `POST_NOTIFICATIONS`, `USE_FULL_SCREEN_INTENT` | Call notification and locked-screen/incoming-call presentation; verify denied/restricted states. |
| `MODIFY_AUDIO_SETTINGS`, `VIBRATE` | In-call audio controls and dialpad feedback. ContactFlow has no audio capture or call-recording feature. |
| `SYSTEM_ALERT_WINDOW` | Optional floating/overlay behavior; only request it after the user opts in. Verify the app remains usable without it. |

`CALL_PRIVILEGED` was removed because it is a system-only permission and the
app's call paths use Telecom/`CALL_PHONE`. The manifest entry named
`android.telecom.action.CONFIGURE_PHONE_ACCOUNT` was also removed because it is
an intent action, not a permission, and no source code uses it.
`RECORD_AUDIO` and `READ_SYNC_SETTINGS` were removed because app and dependency
source contain no audio-capture or sync-settings use. Android remains
responsible for account sync. The merged debug APK also does not request
`INTERNET`.

Exported components are limited to the app entry/intent routes (`MainActivity`,
`SettingsActivity`, `DialpadActivity`, `DialerActivity`, launcher aliases) and
the system-bound `CallService` and `SimpleCallScreeningService`. The Telecom
services require their platform bind permissions; internal activities and the
call-action receiver are not exported. Recheck the merged manifest for each
release build.

## Private-beta tester handout draft

**Distribution channel:** direct signed APK via private file share. Do not send
the debug APK. The release package must use application ID
`com.contactflow.phone` and the owner's private release signing key.

**Candidate:** version 1.11.1 (code 22), package `com.contactflow.phone`,
intended for Android API 26 through API 36. These are the configured minimum
and target; device install and call-flow checks are still required before
telling testers that this range is verified.

**Installation:** download the signed candidate only from the selected private
channel, open the APK, and allow installs from that source only if Android asks.
After installation, launch ContactFlow and grant Contacts, call, and call-log
access only when needed for the feature being tested. Set ContactFlow as the
default Phone app only for default-dialer tests; Android Settings can restore the
previous default afterward. To uninstall, use Android Settings > Apps >
ContactFlow. Device contacts and account sync stay in Android's Contacts
Provider.

**Permission summary:** Contacts and call-log access support those views and
edits; phone/Telecom access supports calling and the default-phone role.
Notifications and overlay/full-screen call presentation are system-controlled
and optional. ContactFlow does not request audio capture, sync-settings access,
or Internet permission.

**Privacy:** ContactFlow has no separate account or cloud contact store. The
merged debug APK requests no `INTERNET` permission and the app does not add call
recording or contact upload behavior. It accesses contacts and call history
through Android permissions. The overlay and full-screen call presentation are
optional system features.

**Feedback:** no private feedback destination is configured yet. Before
recruiting testers, provide a private form/email route and ask testers not to
include phone numbers, contact names, call-log screenshots, or other personal
contact data in reports.

## Private-beta release gates

- [x] Select direct signed APK via private file share as the release channel.
- [ ] Configure a private tester feedback route. Do not use a public issue
  tracker for personal contact/call details.
- [ ] API 26 and API 36 build/install checks and at least one available OEM
  check are recorded.
- [ ] No unresolved contact data-loss issue or release-blocking crash remains.
- [ ] The swipe quick-action menu, tap alternative, and inherited long-press
  actions pass TalkBack/large-text checks before signing.
- [ ] Every remaining declared permission has a justified runtime use, and the
  merged release manifest is re-audited.
- [x] A signed release package is produced using signing material stored outside
  the repository. Use `scripts/create_beta_signing_key.sh` once, then
  `scripts/build_beta_release.sh`; signing passwords are stored as Replit
  Secrets, never in source control or chat.
- [ ] The tester handout names the chosen distribution channel, install steps,
  supported Android versions, permission summary, known issues, uninstall
  guidance, and a private feedback route.
- [ ] A short tester feedback cycle is reviewed and release blockers are fixed
  before the go/no-go decision.

Direct APK distribution is selected and a signed release candidate has been
built. Device verification, accessibility checks, and the private feedback
route remain open; do not describe it as beta-ready until the remaining gates
are completed.
