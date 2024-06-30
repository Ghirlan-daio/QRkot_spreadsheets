from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base import CharityDonation


class Donation(CharityDonation):
    """Модель пожертвований."""
    user_id = Column(
        Integer,
        ForeignKey("user.id"),
        name="fk_donation_user_id_user"
    )
    comment = Column(Text)

    def __repr__(self):
        return super(Donation, self).__repr__()
