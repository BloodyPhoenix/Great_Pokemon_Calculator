from sqlalchemy.orm import sessionmaker


def pokemon_go_data_getter():
    """Функция, предоставляющая общие данные о покедмонах для покедекса Pokemon Go"""
    from databases import create_engine, GoPokemon
    engine = create_engine()
    local_session = sessionmaker(autoflush=False, autocommit=False, bind=engine)
    db = local_session()
    result = db.query(GoPokemon.picture_link, GoPokemon.pokedex_number, GoPokemon.form_name, GoPokemon.type_1,
             GoPokemon.type_2, GoPokemon.max_cp_40, GoPokemon.max_cp_50).order_by(GoPokemon.pokedex_number.asc())
    return result


def single_go_data_getter(pokemon: str):
    """Функция, предоставляющая данные об обном покемоне в Pokemon Go для отрисовки его индивидуальной странички"""
    from databases import create_engine, GoPokemon
    engine = create_engine()
    local_session = sessionmaker(autoflush=False, autocommit=False, bind=engine)
    db = local_session()
    result = db.query(GoPokemon).where(GoPokemon.form_name == pokemon).one()
    return result


def go_moves_data_getter(move_type: str, move_category: str):
    from databases import create_engine
    if move_category == 'fast':
        from databases import FastMove as moves_db
    else:
        from databases import ChargeMove as moves_db
    engine = create_engine()
    local_seccion = sessionmaker(autoflush=True, autocommit=False, bind=engine)
    db = local_seccion()
    if move_type == 'any':
        result = db.query(moves_db)
    else:
        result = db.query(moves_db).where(moves_db.type == move_type)
    return result
