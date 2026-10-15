# ContactFlow native Android source

This folder is the native Android source of truth for ContactFlow. It is based
on Fossify Phone, imported from upstream commit
`991b352abadc01b33a1f23f7e14f5b30070aba48`.

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
tools. In this Replit workspace the SDK is installed at
`$HOME/.android-sdk`; set `ANDROID_HOME` and `ANDROID_SDK_ROOT` when building:

```sh
ANDROID_HOME="$HOME/.android-sdk" \
ANDROID_SDK_ROOT="$HOME/.android-sdk" \
  ./gradlew :app:assembleFossDebug
```

The debug APK is written under `app/build/outputs/apk/foss/debug/`.

This workspace's Replit preview is still the old Expo UI prototype; it is a
visual reference only and does not run or verify this Kotlin app. The native app
must be built and tested on Android before device behavior is considered
verified.
