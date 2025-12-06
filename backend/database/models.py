from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column

class Base(DeclarativeBase):
    pass

# Таблица пищевых добавок
class FoodAdditives(Base):
    __tablename__ = 'additives'

    id: Mapped[int] = mapped_column()
    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()

# Таблица уровеней опасности пищевых добавок
class Categories(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column()
    category: Mapped[str] = mapped_column()

# Таблица уровеней опасности пищевых добавок
class Dangerlvls(Base):
    __tablename__ = 'dangerlvls'

    id: Mapped[int] = mapped_column()
    danger: Mapped[str] = mapped_column()

# Таблица происхождения пищевых добавок
class Origins(Base):
    __tablename__ = 'origins'

    id: Mapped[int] = mapped_column()
    origin: Mapped[str] = mapped_column()

# Индексная таблица происхождений Х добавок
class AdditiveOrigins(Base):
    __tablename__ = 'additive_origins'
    
    id: Mapped[int] = mapped_column()
    additive_id: Mapped[int] = mapped_column().foreign_keys(FoodAdditives.id)
    origin_id: Mapped[int] = mapped_column().foreign_keys(Origins.id)

# Индексная таблица опасности Х добавок
class AdditiveDangerlvl(Base):
    __tablename__ = 'additive_dangerlvls'
    
    id: Mapped[int] = mapped_column()
    additive_id: Mapped[int] = mapped_column().foreign_keys(FoodAdditives.id)
    danger_id: Mapped[int] = mapped_column().foreign_keys(Dangerlvls.id)

# Индексная таблица категории Х добавок
class AdditiveCategories(Base):
    __tablename__ = 'additive_categories'
    
    id: Mapped[int] = mapped_column()
    additive_id: Mapped[int] = mapped_column().foreign_keys(FoodAdditives.id)
    category_id: Mapped[int] = mapped_column().foreign_keys(Categories.id)