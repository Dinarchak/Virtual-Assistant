from sqlalchemy.orm import (
    DeclarativeBase,
    mapped_column,
    relationship,
    Mapped
)

from sqlalchemy import ForeignKey, String, create_engine

# from sqlalchemy import create_engine
# from settings import config


from typing import (
    List
)

from datetime import datetime

class Base(DeclarativeBase):
    pass

class ProcessType(Base):
    __tablename__ = 'processtype'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))

    processes: Mapped[List['Process']] = relationship(back_populates='type', cascade="all, delete")

class Process(Base):
    __tablename__ = 'process'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))

    type_id: Mapped[int] = mapped_column(ForeignKey('processtype.id'))
    type: Mapped['ProcessType'] = relationship(back_populates='processes')

    life_periods: Mapped[List['LifePeriod']] = relationship(back_populates='process', cascade="all, delete")

class LifePeriod(Base):
    __tablename__ = 'lifeperiod'
    id: Mapped[int] = mapped_column(primary_key=True)
    start: Mapped[datetime] = mapped_column()
    end: Mapped[datetime] = mapped_column()
    delta: Mapped[int] = mapped_column(default=0)

    process_id: Mapped[int] = mapped_column(ForeignKey('process.id'))
    process: Mapped['Process'] = relationship(back_populates='life_periods')

# engine = create_engine(config['db_url'])
# Base.metadata.create_all(engine)
