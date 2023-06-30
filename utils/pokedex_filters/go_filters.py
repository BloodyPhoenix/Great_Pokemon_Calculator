from sqlalchemy import select
from sqlalchemy.orm import sessionmaker


def strongest_type(amount: int, pokemon_type: str, exclude_no_moves=False, no_legends=False, no_mythics=False,
                   no_megas=False):
    from databases import create_engine, GoPokemon, FastMove, ChargeMove
    engine = create_engine()
    local_session = sessionmaker(autoflush=False, autocommit=False, bind=engine)
    session = local_session()
    if exclude_no_moves:
        print('pokemon with no moves excluded')
        if no_legends:
            if no_mythics:
                if no_megas:
                    pass
                else:
                    pass
            else:
                if no_megas:
                    pass
                else:
                    pass
        else:
            if no_mythics:
                if no_megas:
                    pass
                else:
                    pass
            else:
                if no_megas:
                    pass
                else:
                    return session.query(GoPokemon).where((
                        (GoPokemon.type_1 == pokemon_type)|(GoPokemon.type_2 == pokemon_type))&
                        (GoPokemon.fast_moves.any(FastMove.type == pokemon_type))&
                        (GoPokemon.charge_moves.any(ChargeMove.type == pokemon_type))
                                                          ).order_by(
                            GoPokemon.max_cp_50.desc()).limit(amount)

    else:
        print('pokemon with no moves not excluded')
        if no_legends:
            print('legends excluded')
            if no_mythics:
                print('mythics excluded')
                if no_megas:
                    pass
                else:
                    pass
            else:
                print('mythics not excluded')
                if no_megas:
                    pass
                else:
                    pass
        else:
            print('legends not excluded')
            if no_mythics:
                print('mythics excluded')
                if no_megas:
                    pass
                else:
                    pass
            else:
                print ('mythics not excluded')
                if no_megas:
                    print('megas excluded')
                    pass
                else:
                    print('megas not excluded')
                    return session.query(GoPokemon).where(
                        (GoPokemon.type_1 == pokemon_type)|(GoPokemon.type_2 == pokemon_type)
                    ).order_by(GoPokemon.max_cp_50.desc()).limit(amount)
