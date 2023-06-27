from typing import Optional, List

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Float, Table, Column, ForeignKey


class Base(DeclarativeBase):
    pass


FastMoveDetail = Table(
    'FastMoveDetail',
    Base.metadata,
    Column('pokemon_id', ForeignKey('GO_pokemon.id'), primary_key=True),
    Column('move_id', ForeignKey('GO_moves_fast.id'), primary_key=True)
)


ChargeMoveDetail = Table(
    'ChargeMoveDetail',
    Base.metadata,
    Column('pokemon_id', ForeignKey('GO_pokemon.id'), primary_key=True),
    Column('move_id', ForeignKey('GO_moves_charge.id'), primary_key=True)
)


class FastMove(Base):
    __tablename__ = 'GO_moves_fast'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    type: Mapped[str] = mapped_column(String(20))
    damage_pve: Mapped[int] = mapped_column(Integer)
    damage_pvp: Mapped[int] = mapped_column(Integer)
    energy_pve: Mapped[int] = mapped_column(Integer)
    speed_pve: Mapped[float] = mapped_column(Float)
    energy_pvp: Mapped[int] = mapped_column(Integer)
    speed_pvp: Mapped[float] = mapped_column(Float)
    pokemon: Mapped[List['Pokemon']] = relationship(secondary=FastMoveDetail, back_populates='fast_moves')


class ChargeMove(Base):
    __tablename__ = 'GO_moves_charge'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    type: Mapped[str] = mapped_column(String(20))
    damage_pve: Mapped[int] = mapped_column(Integer)
    damage_pvp: Mapped[int] = mapped_column(Integer)
    speed: Mapped[float] = mapped_column(Float)
    charges_pve: Mapped[int] = mapped_column(Integer)
    energy_pvp: Mapped[int] = mapped_column(Integer)
    pokemon: Mapped[List['Pokemon']] = relationship(secondary=ChargeMoveDetail, back_populates='charge_moves')


class Pokemon(Base):
    __tablename__ = 'GO_pokemon'
    id: Mapped[int] = mapped_column(primary_key=True)
    picture_link: Mapped[str] = mapped_column(String(150))
    pokedex_number: Mapped[str] = mapped_column(String(5))
    species_name: Mapped[str] = mapped_column(String(30))
    type_1: Mapped[str] = mapped_column(String(20))
    type_2: Mapped[Optional[str]] = mapped_column(String(20))
    base_hp: Mapped[int] = mapped_column(Integer)
    max_hp_40: Mapped[int] = mapped_column(Integer)
    max_hp_50: Mapped[int] = mapped_column(Integer)
    base_attack: Mapped[int] = mapped_column(Integer)
    max_attack_40: Mapped[int] = mapped_column(Integer)
    max_attack_50: Mapped[int] = mapped_column(Integer)
    base_defence: Mapped[int] = mapped_column(Integer)
    max_defence_40: Mapped[int] = mapped_column(Integer)
    max_defence_50: Mapped[int] = mapped_column(Integer)
    max_cp_40: Mapped[int] = mapped_column(Integer)
    max_cp_50: Mapped[int] = mapped_column(Integer)
    fast_moves: Mapped[List[FastMove]] = relationship(secondary=FastMoveDetail, back_populates="pokemon")
    charge_moves: Mapped[List[ChargeMove]] = relationship(secondary=ChargeMoveDetail, back_populates="pokemon")




