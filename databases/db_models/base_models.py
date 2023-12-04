from typing import List, Optional

from sqlalchemy import String, Integer, Table, Column, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from .metadata import Metadata

AvailableMoves = Table(
    'AvailableMoves',
    Metadata.metadata,
    Column('game_name', ForeignKey('Games.name'), primary_key=True),
    Column('move_id', ForeignKey('BaseMove.id'), primary_key=True)
)


AvailablePokemon = Table(
    'AvailablePokemon',
    Metadata.metadata,
    Column('game_id', ForeignKey('Games.id'), primary_key=True),
    Column('pokemon_id', ForeignKey('BasePokemon.id'), primary_key=True)
)


class Game(Metadata):
    __tablename__ = 'Games'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    generation: Mapped[int] = mapped_column(Integer)
    dlc: Mapped[Optional[str]] = mapped_column(String(50))
    region: Mapped[str] = mapped_column(String(20))
    moves: Mapped[List['BaseMove']] = relationship(secondary=AvailableMoves, back_populates='games')
    pokemon: Mapped[List['BasePokemon']] = relationship(secondary=AvailablePokemon, back_populates='games')


class BaseMove(Metadata):
    __tablename__ = 'BaseMove'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    games: Mapped[List['Game']] = relationship(secondary=AvailableMoves, back_populates='moves')


class BasePokemon(Metadata):
    __tablename__ = 'BasePokemon'
    id: Mapped[int] = mapped_column(primary_key=True)
    national_number: Mapped[int] = mapped_column(Integer)
    species_name: Mapped[str] = mapped_column(String(20))
    games: Mapped[List['Game']] = relationship(secondary=AvailablePokemon, back_populates='pokemon')



