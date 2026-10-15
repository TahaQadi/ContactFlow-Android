package org.fossify.phone.helpers

internal enum class ContactQuickAction {
    CALL,
    MESSAGE,
    DETAILS
}

internal fun contactQuickActions(
    hasPhoneNumber: Boolean,
    hasMessageNumber: Boolean
): List<ContactQuickAction> {
    return buildList {
        if (hasPhoneNumber) {
            add(ContactQuickAction.CALL)
            if (hasMessageNumber) {
                add(ContactQuickAction.MESSAGE)
            }
        }
        add(ContactQuickAction.DETAILS)
    }
}
