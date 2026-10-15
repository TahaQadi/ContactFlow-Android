#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

if ! java -version 2>&1 | grep -Eq 'version "17([.]|")|openjdk 17'; then
  echo "ContactFlow Android builds require OpenJDK 17." >&2
  exit 1
fi

SDK_ROOT="${ANDROID_SDK_ROOT:-${ANDROID_HOME:-$HOME/.android-sdk}}"
if [[ ! -d "$SDK_ROOT/platforms/android-36" ]]; then
  echo "Android SDK Platform 36 was not found. Install it and set ANDROID_HOME and ANDROID_SDK_ROOT." >&2
  exit 1
fi
export ANDROID_HOME="$SDK_ROOT"
export ANDROID_SDK_ROOT="$SDK_ROOT"

for name in SIGNING_KEY_ALIAS SIGNING_KEY_PASSWORD SIGNING_STORE_PASSWORD; do
  if [[ -z "${!name:-}" ]]; then
    printf 'Missing required protected setting: %s\n' "$name" >&2
    exit 2
  fi
done

KEYSTORE_FILE="$HOME/.android/contactflow-release.jks"
if [[ ! -f "$KEYSTORE_FILE" ]]; then
  echo "Release keystore is missing. Run bash scripts/create_beta_signing_key.sh once." >&2
  exit 3
fi

# Override any stale or unsafe saved path; signing material must stay outside
# the repository.
export SIGNING_STORE_FILE="$KEYSTORE_FILE"

python3 scripts/check_beta_baseline.py
./gradlew --no-daemon --max-workers=1 \
  -Dorg.gradle.jvmargs="-Xmx2g -Dfile.encoding=UTF-8" \
  :app:testFossDebugUnitTest :app:assembleFossRelease :app:lintFossRelease

echo "Signed FOSS release APK built at app/build/outputs/apk/foss/release/."
