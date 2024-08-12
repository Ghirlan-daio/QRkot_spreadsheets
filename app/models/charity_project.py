from sqlalchemy import Column, String, Text

from app.models.base import CharityDonation


class CharityProject(CharityDonation):
    """Модель проектов."""
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        base_repr = super(CharityProject, self).__repr__()
        return f"{base_repr}, name={self.name}, description={self.description}"
