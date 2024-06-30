from typing import List

from app.models import CharityDonation
from app.crud.base import CRUDBase


def allocate_donation_between_funds(
        obj: CharityDonation,
        target: CharityDonation,
        sources: List[CharityDonation]
) -> None:
    """Распределяет сделанные пожертвования по благ. проектам."""
    model = CharityDonation
    objects = [source for source in sources if isinstance(source, model)]
    amount_invest = obj.full_amount
    for object in objects:
        amount = object.full_amount - object.invested_amount
        invested_amount = min(amount, amount_invest)
        object.invested_amount += invested_amount
        target.invested_amount += invested_amount
        amount_invest -= invested_amount

        if object.full_amount == object.invested_amount:
            CRUDBase.close_obj(object)

        if not amount_invest:
            CRUDBase.close_obj(target)
            break
