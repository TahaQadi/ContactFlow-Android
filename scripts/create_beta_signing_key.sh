#!/usr/bin/env bash
set -euo pipefail

for name in SIGNING_KEY_ALIAS SIGNING_KEY_PASSWORD SIGNING_STORE_PASSWORD; do
  if [[ -z "${!name:-}" ]]; then
    printf 'Missing required protected setting: %s\n' "$name" >&2
    exit 2
  fi
done

KEYSTORE_FILE="$HOME/.android/contactflow-release.jks"
if [[ -e "$KEYSTORE_FILE" ]]; then
  echo "A release keystore already exists; refusing to replace it." >&2
  exit 3
fi

umask 077
mkdir -p "$(dirname "$KEYSTORE_FILE")"
chmod 700 "$(dirname "$KEYSTORE_FILE")"

keytool -genkeypair \
  -noprompt \
  -storetype JKS \
  -keystore "$KEYSTORE_FILE" \
  -alias "$SIGNING_KEY_ALIAS" \
  -keyalg RSA \
  -keysize 2048 \
  -validity 10000 \
  -dname "CN=ContactFlow Private Beta,OU=ContactFlow" \
  -storepass:env SIGNING_STORE_PASSWORD \
  -keypass:env SIGNING_KEY_PASSWORD

chmod 600 "$KEYSTORE_FILE"
keytool -list \
  -storetype JKS \
  -keystore "$KEYSTORE_FILE" \
  -alias "$SIGNING_KEY_ALIAS" \
  -storepass:env SIGNING_STORE_PASSWORD >/dev/null

echo "Created and verified the ContactFlow release keystore outside the repository."
