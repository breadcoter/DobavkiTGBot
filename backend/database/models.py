from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class FoodAdditives(Base):
    __tablename__ = 'food_additives'

    id: Mapped[int] = mapped_column()
    name: Mapped[str] = mapped_column()
    danger_level: Mapped[str] = mapped_column()
    e_type: Mapped[str] = mapped_column()
    origins: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()


class AdditiveOrigins(Base):
    __tablename__ = 'origins'
    
    id: Mapped[int] = mapped_column()
    additive_id: Mapped[int] = mapped_column().foreign_keys(FoodAdditives.id)

class Origins(Base):
    __tablename__ = 'additive_origins'

    id: Mapped[int] = mapped_column()
    origin: Mapped[str] = mapped_column()