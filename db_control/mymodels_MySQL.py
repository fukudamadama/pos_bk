from sqlalchemy import String, Integer, JSON, TIMESTAMP, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
# from datetime import datetime

class Base(DeclarativeBase):
    pass

class HairQuality(Base):
    __tablename__ = 'hair_quality'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nickname: Mapped[str] = mapped_column(String(255))
    age: Mapped[int] = mapped_column(Integer)
    gender: Mapped[str] = mapped_column(String(20))
    density: Mapped[str] = mapped_column(String(50))
    hair_loss: Mapped[str] = mapped_column(String(50))
    scalp: Mapped[dict] = mapped_column(JSON)
    thickness: Mapped[str] = mapped_column(String(50))
    texture: Mapped[dict] = mapped_column(JSON)
    firmness: Mapped[str] = mapped_column(String(20))
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, server_default=func.now())
    updated_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP, server_default=func.now(), onupdate=func.now()
    )

class Customers(Base):
    __tablename__ = 'customers'
    customer_id: Mapped[str] = mapped_column(String(10), primary_key=True)
    customer_name: Mapped[str] = mapped_column(String(100))
    age: Mapped[int] = mapped_column(Integer)
    gender: Mapped[str] = mapped_column(String(10))