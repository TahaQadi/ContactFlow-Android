# ContactFlow native Android source

This folder is the native Android source of truth for ContactFlow in the
Replit workspace. The hosted GitHub fork, `ContactFlow-Android`, is the
canonical shared repository and release history. The Replit working copy does
not automatically sync to GitHub. It is based on Fossify Phone, imported from
upstream commit `991b352abadc01b33a1f23f7e14f5b30070aba48`.

## Identity and upstream code

- Display name: `ContactFlow`
- Android application ID: `com.contactflow.phone`
- Kotlin/Android namespace: `org.fossify.phone` (kept to avoid an unrelated
  package-wide source rename)
- Upstream: https://github.com/FossifyOrg/Phone
- License: GNU GPL-3.0; keep the upstream `LICENSE` and copyright notices.

The application ID is intentionally separate from the Kotlin namespace. This
lets ContactFlow install as a distinct app while keeping Fossify's existing
relative manifest class names and source packages valid.

## Building

Use OpenJDK 17 and Android SDK Platform 36 with the matching Android build
tools. Point `ANDROID_HOME` and `ANDROID_SDK_ROOT` at the SDK installation. For
a fresh machine, install Google's Android CLI from the
[official download page](https://developer.android.com/tools/agents/android-cli/download),
accept its SDK license prompts, and install the required packages:

```sh
android --sdk="$HOME/.android-sdk" sdk install \
  platforms/android-36 build-tools/36.0.0 platform-tools
```

Keep the SDK and license files outside the repository. In this workspace,
`$HOME/.android-sdk` is the SDK root. Set both Android SDK environment variables
to that path when building.

For a direct debug build:

```sh
ANDROID_HOME="$HOME/.android-sdk" \
ANDROID_SDK_ROOT="$HOME/.android-sdk" \
  ./gradlew :app:assembleFossDebug
The debug APK is written under `app/build/outputs/apk/foss/debug/`. Run the
source-level beta baseline check (Python 3.11+) and the full debug smoke build
from this directory:

```sh
python3 scripts/check_beta_baseline.py
bash scripts/build_beta_debug.sh
```

The baseline check validates source/configuration contracts; neither build
command replaces device testing. See [BETA_READINESS.md](BETA_READINESS.md) for
the contact/call acceptance checklist, permission review, and remaining gates.

For the selected direct private-APK beta, use the protected `SIGNING_KEY_ALIAS`,
`SIGNING_KEY_PASSWORD`, and `SIGNING_STORE_PASSWORD` environment secrets. Create
the release key once with `bash scripts/create_beta_signing_key.sh`, then run
`bash scripts/build_beta_release.sh`. The key is stored at
`$HOME/.android/contactflow-release.jks`, outside the repository. Back it up
securely and preserve both passwords; losing the key prevents signed updates.
Keep an owner-controlled backup outside this workspace before recruiting
testers; this workspace copy is not a substitute for a backup. The release
script overrides `SIGNING_STORE_FILE` to this external path and the Gradle
configuration rejects signing keys located inside the repository.

## Replit-to-GitHub updates

Treat Replit as the working copy and `ContactFlow-Android` as the canonical
shared Git history. Do not assume changes made in either place have synced.
This workspace currently has no GitHub remote configured; confirm the official
`ContactFlow-Android` repository and its access before syncing.
Before syncing, confirm the Replit change is committed and the native baseline
check passes. Transfer changes through a reviewed GitHub branch/pull request;
do not overwrite the GitHub default branch or copy files blindly. If GitHub has
newer changes, fetch and merge/rebase them into the Replit working branch first,
resolve conflicts, rerun the checks, then submit the reviewed update. Keep
signing files, credentials, and generated APKs out of both repositories.

## UI direction

See [CONTACTFLOW_DESIGN_SYSTEM.md](CONTACTFLOW_DESIGN_SYSTEM.md) for the
proposed native contacts and dialer tokens, components, states, and accessibility
requirements.

This workspace's Replit preview is still the old Expo UI prototype; it is a
visual reference only and does not run or verify this Kotlin app. The native app
must be built and tested on Android before device behavior is considered
verified.
