package org.fossify.phone.helpers

import org.junit.Assert.assertEquals
import org.junit.Test

class ContactQuickActionsTest {
    @Test
    fun contactWithoutANumberOnlyOffersDetails() {
        assertEquals(
            listOf(ContactQuickAction.DETAILS),
            contactQuickActions(hasPhoneNumber = false, hasMessageNumber = false)
        )
    }

    @Test
    fun contactWithNumberOffersCallAndDetailsWhenMessagingNumberIsUnavailable() {
        assertEquals(
            listOf(ContactQuickAction.CALL, ContactQuickAction.DETAILS),
            contactQuickActions(hasPhoneNumber = true, hasMessageNumber = false)
        )
    }

    @Test
    fun contactWithMessagingNumberOffersCallMessageAndDetailsInOrder() {
        assertEquals(
            listOf(
                ContactQuickAction.CALL,
                ContactQuickAction.MESSAGE,
                ContactQuickAction.DETAILS
            ),
            contactQuickActions(hasPhoneNumber = true, hasMessageNumber = true)
        )
    }
}
