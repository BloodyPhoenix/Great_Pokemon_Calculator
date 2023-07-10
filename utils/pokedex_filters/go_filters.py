from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.operators import and_


def strongest_type(amount: int, pokemon_type: str, all_types=True, only_first=False, only_second=False, monotype=False,
                   exclude_no_moves=False, no_legends=False, no_mythics=False, no_megas=False):
    from databases import create_engine, GoPokemon, FastMove, ChargeMove
    types_selection = None
    exclude_moves = ((GoPokemon.fast_moves.any(FastMove.type == pokemon_type)) &
                     (GoPokemon.charge_moves.any(ChargeMove.type == pokemon_type)))
    options = []
    if all_types:
        types_selection = (GoPokemon.type_1 == pokemon_type) | (GoPokemon.type_2 == pokemon_type)
    if only_first:
        types_selection = (GoPokemon.type_1 == pokemon_type)
    if only_second:
        types_selection = (GoPokemon.type_2 == pokemon_type)
    if monotype:
        types_selection = (GoPokemon.type_1 == pokemon_type) & (GoPokemon.type_2 == None)
    if no_legends:
        options.append((GoPokemon.legendary, False))
    if no_mythics:
        options.append((GoPokemon.mythic, False))
    if no_megas:
        options.append((GoPokemon.mega, False))
    engine = create_engine()
    local_session = sessionmaker(autoflush=False, autocommit=False, bind=engine)
    session = local_session()
    if options:
        if exclude_no_moves:
            session.query(GoPokemon).where(
                types_selection & exclude_moves & and_(*(option[0] == option[1] for option in options))
            ).order_by(
                GoPokemon.max_cp_50.desc()).limit(amount)
        else:
            return session.query(GoPokemon).where(and_(*(option[0] == option[1] for option in options))).order_by(
                GoPokemon.max_cp_50.desc()).limit(amount)
    else:
        if exclude_no_moves:
            return session.query(GoPokemon).where(
                types_selection & exclude_moves).order_by(GoPokemon.max_cp_50.desc()).limit(amount)
        else:
            return session.query(GoPokemon).where(types_selection).order_by(
                GoPokemon.max_cp_50.desc()).limit(amount)
