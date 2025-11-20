from django.db import transaction
from django.db.models import F
from django.utils import timezone

from stores.models import StoreInventory

from .models import Loan


class LoanUnavailableError(Exception):
    """Raised when a book cannot be borrowed due to availability constraints."""


def create_membership_loan(member, inventory: StoreInventory, due_date):
    """
    Create a loan for the given member and store inventory item.

    This function ensures availability is respected and updates related records
    atomically. It assumes all business validations (membership currency, etc.)
    have already been performed by the caller.
    """
    with transaction.atomic():
        locked_inventory = (
            StoreInventory.objects.select_for_update()
            .select_related("book", "store")
            .get(pk=inventory.pk)
        )
        if locked_inventory.available_copies <= 0:
            raise LoanUnavailableError("Book is currently unavailable.")

        loan = Loan.objects.create(
            member=member,
            book=locked_inventory.book,
            store=locked_inventory.store,
            store_inventory=locked_inventory,
            due_date=due_date,
            loan_date=timezone.localdate(),
        )

        locked_inventory.available_copies -= 1
        locked_inventory.save(update_fields=["available_copies"])

    return loan


def return_loan(loan: Loan):
    """
    Mark the provided loan as returned, update inventory and status.
    """
    with transaction.atomic():
        if loan.status == Loan.STATUS_RETURNED:
            return loan

        loan.return_date = timezone.localdate()
        loan.status = Loan.STATUS_RETURNED
        loan.save(update_fields=["return_date", "status"])

        if loan.store_inventory_id:
            StoreInventory.objects.filter(pk=loan.store_inventory_id).update(
                available_copies=F("available_copies") + 1
            )

    # Refresh from db to get updated available_copies value.
    loan.refresh_from_db(fields=["status", "return_date"])
    if loan.store_inventory_id:
        loan.store_inventory.refresh_from_db(fields=["available_copies"])
    return loan

