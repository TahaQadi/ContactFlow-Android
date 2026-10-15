#!/usr/bin/env python3
"""Fast, source-level guardrails for the ContactFlow Android beta baseline."""

from pathlib import Path
import sys
import tomllib
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
ANDROID = "{http://schemas.android.com/apk/res/android}"


class BaselineError(Exception):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise BaselineError(message)


def main() -> int:
    versions_path = ROOT / "gradle/libs.versions.toml"
    with versions_path.open("rb") as source:
        versions = tomllib.load(source)["versions"]

    require(
        versions.get("app-build-minimumSDK") == "26",
        "minimum Android API must remain 26",
    )
    require(
        versions.get("app-build-targetSDK") == "36",
        "target Android API must remain 36",
    )

    gradle_properties = (ROOT / "gradle.properties").read_text()
    require(
        "APPLICATION_ID=com.contactflow.phone" in gradle_properties,
        "ContactFlow application ID changed; update the beta identity review",
    )

    manifest = ET.parse(ROOT / "app/src/main/AndroidManifest.xml").getroot()
    declared_permissions = {
        element.get(ANDROID + "name")
        for element in manifest.findall("uses-permission")
    }
    required_permissions = {
        "android.permission.READ_CONTACTS",
        "android.permission.WRITE_CONTACTS",
        "android.permission.READ_CALL_LOG",
        "android.permission.WRITE_CALL_LOG",
        "android.permission.CALL_PHONE",
        "android.permission.ANSWER_PHONE_CALLS",
        "android.permission.MANAGE_OWN_CALLS",
    }
    require(
        required_permissions <= declared_permissions,
        "a permission required by the inherited contacts/call flows is missing",
    )
    require(
        "android.permission.CALL_PRIVILEGED" not in declared_permissions,
        "do not request system-only CALL_PRIVILEGED",
    )
    require(
        "android.telecom.action.CONFIGURE_PHONE_ACCOUNT" not in declared_permissions,
        "intent action must not be declared as a permission",
    )
    require(
        "android.permission.RECORD_AUDIO" not in declared_permissions,
        "the app does not record or capture audio",
    )
    require(
        "android.permission.READ_SYNC_SETTINGS" not in declared_permissions,
        "do not inspect account sync settings; Android owns contact sync",
    )
    require(
        "android.permission.INTERNET" not in declared_permissions,
        "ContactFlow must not add network access without an explicit product decision",
    )

    app = manifest.find("application")
    require(app is not None, "manifest application element is missing")
    exported_components = {
        element.get(ANDROID + "name"): element
        for element in app.iter()
        if element.tag in {"activity", "activity-alias", "service", "receiver"}
        and element.get(ANDROID + "exported") == "true"
    }
    required_exported = {
        ".activities.MainActivity",
        ".activities.SettingsActivity",
        ".activities.DialpadActivity",
        ".activities.DialerActivity",
        ".services.CallService",
        ".services.SimpleCallScreeningService",
    }
    require(
        required_exported <= exported_components.keys(),
        "an expected exported system/intent entry point is missing",
    )
    require(
        exported_components[".services.CallService"].get(ANDROID + "permission")
        == "android.permission.BIND_INCALL_SERVICE",
        "CallService must remain protected by BIND_INCALL_SERVICE",
    )
    require(
        exported_components[".services.SimpleCallScreeningService"].get(
            ANDROID + "permission"
        )
        == "android.permission.BIND_SCREENING_SERVICE",
        "screening service must remain protected by BIND_SCREENING_SERVICE",
    )

    source_root = ROOT / "app/src/main/kotlin/org/fossify/phone"
    sources = "\n".join(
        path.read_text(errors="replace")
        for path in source_root.rglob("*.kt")
    )
    required_source_contracts = {
        "Android contact lookup": "ContactsHelper",
        "Android contact creation": "ContactsContract.Contacts.CONTENT_URI",
        "Android contact edit handoff": "Intent.ACTION_INSERT_OR_EDIT",
        "contact deletion confirmation": "ConfirmationDialog",
        "contact deletion write-permission gate": "PERMISSION_WRITE_CONTACTS",
        "contact quick-action call safeguard": "startCallWithConfirmationCheck(contact)",
        "contact quick-action messaging handoff": "launchSendSMSIntent(messageNumber.orEmpty())",
        "quick-action accessibility label": "quick_actions_for_contact",
        "quick-action swipe entry point": "horizontalSwipe && !actModeCallback.isSelectable",
        "Telecom outgoing call path": "telecomManager.placeCall",
        "default-phone role request": "launchSetDefaultDialerIntent",
        "Telecom call service": "CallManager.onCallAdded(call)",
        "call-log permission denial state": "could_not_access_the_call_history",
    }
    for label, marker in required_source_contracts.items():
        require(marker in sources, f"missing source contract: {label}")

    print(
        "ContactFlow baseline checks passed "
        "(API 26/36 config, app identity, key permissions, exported services, "
        "and inherited contact/call source contracts)."
    )
    print("This check does not build, install, or interact with the Android app.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (BaselineError, OSError, ET.ParseError, KeyError) as error:
        print(f"ContactFlow baseline check failed: {error}", file=sys.stderr)
        raise SystemExit(1)
