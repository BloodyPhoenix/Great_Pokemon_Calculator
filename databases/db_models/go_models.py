from math import sqrt
from typing import Optional, List

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, InstrumentedAttribute
from sqlalchemy import Integer, String, Float, Table, Column, ForeignKey, Boolean


class Base(DeclarativeBase):
    pass


FastMoveDetail = Table(
    'FastMoveDetail',
    Base.metadata,
    Column('pokemon_form_name', ForeignKey('GO_pokemon.form_name'), primary_key=True),
    Column('move_id', ForeignKey('GO_moves_fast.id'), primary_key=True)
)

ChargeMoveDetail = Table(
    'ChargeMoveDetail',
    Base.metadata,
    Column('pokemon_form_name', ForeignKey('GO_pokemon.form_name'), primary_key=True),
    Column('move_id', ForeignKey('GO_moves_charge.id'), primary_key=True)
)


# MyPokemonChargeMoves = Table(
#     'MyPokemonChargeMoves',
#     Base.metadata,
#     Column('pokemon_form_name', ForeignKey('GO_my_pokemon.name'), primary_key=True),
#     Column('move_id', ForeignKey('GO_moves_charge.id'), primary_key=True)
# )


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

    def __str__(self):
        return f"""
move name: {self.name}
type: {self.type}
"""


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

    def __str__(self):
        return f"""
move name: {self.name}
type: {self.type}
"""


class Pokemon(Base):
    __tablename__ = 'GO_pokemon'
    picture_link: Mapped[str] = mapped_column(String(150))
    pokedex_number: Mapped[str] = mapped_column(String(5))
    species_name: Mapped[str] = mapped_column(String(30))
    form_name: Mapped[str] = mapped_column(String(50), primary_key=True)
    type_1: Mapped[str] = mapped_column(String(20))
    type_2: Mapped[Optional[str]] = mapped_column(String(20))
    legendary: Mapped[bool] = mapped_column(Boolean, default=False)
    mythic: Mapped[bool] = mapped_column(Boolean, default=False)
    mega: Mapped[bool] = mapped_column(Boolean, default=False)
    ub_paradox: Mapped[bool] = mapped_column(Boolean, default=False)
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

    @classmethod
    def upsert(cls, data, session, image_path, fast_moves, charge_moves):
        #TODO Написать логику для изменения статуса (мега, легенда, мифик, УЧ/парадокс)
        from utils import count_cp_lvl_40, count_cp_lvl_50, count_stat_lvl_50, count_stat_lvl_40
        current_pokemon = session.query(cls).filter(cls.form_name == data['form_name']).first()
        if current_pokemon is None:
            pokemon = cls(
                picture_link=image_path,
                pokedex_number=data['number'],
                species_name=data['species_name'],
                form_name=data['form_name'],
                type_1=data['type_1'],
                type_2=data['type_2'],
                base_hp=data['HP'],
                max_hp_40=count_stat_lvl_40(data['HP']),
                max_hp_50=count_stat_lvl_50(data['HP']),
                base_attack=data['Attack'],
                max_attack_40=count_stat_lvl_40(data['Attack']),
                max_attack_50=count_stat_lvl_50(data['Attack']),
                base_defence=data['Defence'],
                max_defence_40=count_stat_lvl_40(data['Defence']),
                max_defence_50=count_stat_lvl_50(data['Defence']),
                max_cp_40=count_cp_lvl_40(attack=[data['Attack'], 15], defence=[data['Defence'], 15], hp=[data['HP'], 15]),
                max_cp_50=count_cp_lvl_50(attack=[data['Attack'], 15], defence=[data['Defence'], 15], hp=[data['HP'], 15])
            )
            for move in fast_moves:
                pokemon.fast_moves.append(move)
            for move in charge_moves:
                pokemon.charge_moves.append(move)
            session.add(pokemon)
            session.commit()
        else:
            current_pokemon.picture_link = image_path
            current_pokemon.pokedex_number = data['number'],
            current_pokemon.species_name = data['species_name'],
            current_pokemon.form_name = data['form_name'],
            current_pokemon.type_1 = data['type_1'],
            current_pokemon.type_2 = data['type_2'],
            current_pokemon.base_hp = data['HP'],
            current_pokemon.max_hp_40 = count_stat_lvl_40(data['HP']),
            current_pokemon.max_hp_50 = count_stat_lvl_50(data['HP']),
            current_pokemon.base_attack = data['Attack'],
            current_pokemon.max_attack_40 = count_stat_lvl_40(data['Attack']),
            current_pokemon.max_attack_50 = count_stat_lvl_50(data['Attack']),
            current_pokemon.base_defence = data['Defence'],
            current_pokemon.max_defence_40 = count_stat_lvl_40(data['Defence']),
            current_pokemon.max_defence_50 = count_stat_lvl_50(data['Defence']),
            current_pokemon.max_cp_40 = count_cp_lvl_40(attack=[data['Attack'], 15], defence=[data['Defence'], 15],
                                        hp=[data['HP'], 15]),
            current_pokemon.max_cp_50 = count_cp_lvl_50(attack=[data['Attack'], 15], defence=[data['Defence'], 15], hp=[data['HP'], 15])
            session.commit()
            for move in fast_moves:
                if move not in current_pokemon.fast_moves:
                    current_pokemon.fast_moves.append(move)
                    session.commit()
            for move in current_pokemon.fast_moves:
                if move not in fast_moves:
                    current_pokemon.fast_moves.remove(move)
                    session.add(move)
                    session.commit()
            for move in charge_moves:
                if move not in current_pokemon.charge_moves:
                    current_pokemon.charge_moves.append(move)
                    session.commit()
            for move in current_pokemon.charge_moves:
                if move not in charge_moves:
                    current_pokemon.charge_moves.remove(move)
                    session.add(move)
                    session.commit()

    def __str__(self):
        return f'''
pokedex_number: {self.pokedex_number}
species name: {self.species_name}
type 1: {self.type_1}
type 2: {self.type_2}
image link: {self.picture_link}'''

    # class MyPokemon(Base):
    #     __tablename__ = 'GO_my_pokemon'
    #     picture_link: Mapped[str] = mapped_column(String(150))
    #     pokedex_number: Mapped[str] = mapped_column(String(5))
    #     species_name: Mapped[str] = mapped_column(String(30))
    #     form_name: Mapped[str] = mapped_column(String(50), primary_key=True)
    #     name: Mapped[str] = mapped_column(String(50))
    #     type_1: Mapped[str] = mapped_column(String(20))
    #     type_2: Mapped[Optional[str]] = mapped_column(String(20))
    #     legendary: Mapped[bool] = mapped_column(Boolean, default=False)
    #     mythic: Mapped[bool] = mapped_column(Boolean, default=False)
    #     mega: Mapped[bool] = mapped_column(Boolean, default=False)
    #     iv_hp: Mapped[int] = mapped_column(Integer)
    #     iv_attack: Mapped[int] = mapped_column(Integer)
    #     iv_defence: Mapped[int] = mapped_column(Integer)
    #     base_hp: Mapped[int] = mapped_column(Integer)
    #     max_hp_40: Mapped[int] = mapped_column(Integer)
    #     max_hp_50: Mapped[int] = mapped_column(Integer)
    #     base_attack: Mapped[int] = mapped_column(Integer)
    #     max_attack_40: Mapped[int] = mapped_column(Integer)
    #     max_attack_50: Mapped[int] = mapped_column(Integer)
    #     base_defence: Mapped[int] = mapped_column(Integer)
    #     max_defence_40: Mapped[int] = mapped_column(Integer)
    #     max_defence_50: Mapped[int] = mapped_column(Integer)
    #     max_cp_40: Mapped[int] = mapped_column(Integer)
    #     max_cp_50: Mapped[int] = mapped_column(Integer)
    #     fast_move_name: Mapped[int] = mapped_column(ForeignKey('GO_moves_fast.id'))
    #     fast_move: Mapped[FastMove] = relationship(back_populates="my_pokemon")

    def __str__(self):
        return f'''
    pokedex_number: {self.pokedex_number}
    species name: {self.species_name}
    type 1: {self.type_1}
    type 2: {self.type_2}
    image link: {self.picture_link}'''
