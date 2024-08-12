from datetime import datetime
from typing import List

from app.models import CharityDonation


def allocate_donation_between_funds(
        target: CharityDonation,
        sources: List[CharityDonation]
) -> List[CharityDonation]:
    """Распределяет сделанные пожертвования по благ. проектам."""
    update_sources = []
    for source in sources:
        amount = source.full_amount - source.invested_amount
        invested_amount = min(amount, target.full_amount)
        source.invested_amount += invested_amount
        target.invested_amount += invested_amount

        for obj in [source, target]:
            if obj.full_amount == obj.invested_amount:
                obj.fully_invested = True
                obj.close_date = datetime.now()

        update_sources.append(source)

        if target.full_amount == target.invested_amount:
            break

    return update_sources
