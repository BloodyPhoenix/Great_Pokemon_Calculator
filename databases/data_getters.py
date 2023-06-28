from sqlalchemy.orm import sessionmaker


def pokemon_go_data_getter():
    from databases import create_engine, GoPokemon
    engine = create_engine()
    local_session = sessionmaker(autoflush=False, autocommit=False, bind=engine)
    db = local_session()
    result = db.query(GoPokemon.picture_link, GoPokemon.pokedex_number, GoPokemon.species_name, GoPokemon.type_1,
             GoPokemon.type_2).all()
    return result