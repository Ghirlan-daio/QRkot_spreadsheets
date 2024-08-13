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
        return (f"{super().__repr__()}, user_id={self.user_id}, "
                f"comment={self.comment}")
