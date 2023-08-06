from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.operators import and_


def get_pokemon(pokemon_type_1: str, pokemon_type_2: str, all_types=True, only_first=False, only_second=False,
                   monotype=False, both_types=False, exclude_no_moves=False, no_legends=False,
                   no_mythics=False, no_megas=False, ordering='pokedex', desc=True):
    from databases import create_engine, GoPokemon, FastMove, ChargeMove
    types_selection = (GoPokemon.type_1 is not None)
    if exclude_no_moves:
        exclude_moves = (GoPokemon.fast_moves.any(FastMove.type == pokemon_type_1) &
                         GoPokemon.charge_moves.any(ChargeMove.type == pokemon_type_1))
    else:
        exclude_moves = (GoPokemon.fast_moves is not None)
    options = []
    if all_types:
        types_selection = (GoPokemon.type_1 == pokemon_type_1) | (GoPokemon.type_2 == pokemon_type_1)
    if only_first:
        types_selection = (GoPokemon.type_1 == pokemon_type_1)
    if only_second:
        types_selection = (GoPokemon.type_2 == pokemon_type_2)
    if monotype:
        types_selection = (GoPokemon.type_1 == pokemon_type_1) & (GoPokemon.type_2 == None)
    if both_types:
        types_selection = (GoPokemon.type_1 == pokemon_type_1) & (GoPokemon.type_2 == pokemon_type_2)
    if no_legends:
        options.append((GoPokemon.legendary, False))
    if no_mythics:
        options.append((GoPokemon.mythic, False))
    if no_megas:
        options.append((GoPokemon.mega, False))
    if ordering == 'pokedex':
        ordering = GoPokemon.pokedex_number
    if ordering == 'CP':
        ordering = GoPokemon.max_cp_50
    if ordering == 'name':
        ordering = GoPokemon.species_name
    engine = create_engine()
    local_session = sessionmaker(autoflush=False, autocommit=False, bind=engine)
    session = local_session()
    if options:
        result = session.query(GoPokemon).where(
                types_selection & exclude_moves & and_(*(option[0] == option[1] for option in options))
            )
    else:
        result = session.query(GoPokemon).where(types_selection & exclude_moves)
    if desc:
        return result.order_by(ordering.desc())
    else:
        return result.order_by(ordering.asc())
