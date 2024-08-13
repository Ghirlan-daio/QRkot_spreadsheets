from sqlalchemy import Column, String, Text

from app.models.base import CharityDonation


class CharityProject(CharityDonation):
    """Модель проектов."""
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return (f"{super().__repr__()}, name={self.name}, "
                f"description={self.description}")
