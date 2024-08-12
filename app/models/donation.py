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
        base_repr = super(Donation, self).__repr__()
        return f"{base_repr}, user_id={self.user_id}, comment={self.comment}"
