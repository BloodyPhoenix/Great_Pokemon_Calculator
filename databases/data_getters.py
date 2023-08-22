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
