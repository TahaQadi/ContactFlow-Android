#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if ! java -version 2>&1 | grep -Eq 'version "17([.]|")|openjdk 17'; then
  echo "ContactFlow Android builds require OpenJDK 17." >&2
  exit 1
fi

SDK_ROOT="${ANDROID_SDK_ROOT:-${ANDROID_HOME:-$HOME/.android-sdk}}"
if [[ ! -d "$SDK_ROOT/platforms/android-36" ]]; then
  echo "Android SDK Platform 36 was not found at $SDK_ROOT/platforms/android-36." >&2
  echo "Install Android SDK Platform 36 and matching build tools, then set ANDROID_HOME and ANDROID_SDK_ROOT." >&2
  exit 1
fi

export ANDROID_HOME="$SDK_ROOT"
export ANDROID_SDK_ROOT="$SDK_ROOT"
# The saved path may be stale. Keep Gradle from ever resolving signing material
# inside the repository, even when building the debug variant.
export SIGNING_STORE_FILE="$HOME/.android/contactflow-release.jks"
python3 scripts/check_beta_baseline.py
./gradlew --no-daemon --max-workers=1 \
  -Dorg.gradle.jvmargs="-Xmx2g -Dfile.encoding=UTF-8" \
  :app:testFossDebugUnitTest :app:assembleFossDebug :app:lintFossDebug
