from typing import List

from app.crud.base import CRUDBase
from app.models import CharityDonation


def allocate_donation_between_funds(
        target: CharityDonation,
        sources: List[CharityDonation]
) -> None:
    """Распределяет сделанные пожертвования по благ. проектам."""
    # update_sources = []
    amount_invest = target.full_amount
    for source in sources:
        amount = source.full_amount - source.invested_amount
        invested_amount = min(amount, amount_invest)
        source.invested_amount += invested_amount 
        target.invested_amount += invested_amount
        amount_invest -= invested_amount

        if source.full_amount == source.invested_amount:
            # update_sources.append(source)
            CRUDBase.close_obj(source)

        if not amount_invest:
            CRUDBase.close_obj(target)
            break

    # return update_sources
