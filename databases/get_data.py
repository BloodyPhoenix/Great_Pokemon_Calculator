from kivy.uix.screenmanager import Screen
from sqlalchemy.orm import sessionmaker


def check_data(game):
    from databases import create_engine, table_names, GoBase
    engine = create_engine()
    GoBase.metadata.create_all(engine)
    local_session = sessionmaker(autoflush=False, autocommit=False, bind=engine)
    db = local_session()
    if db.query(table_names[f'{game}']).first():
        return True
    return False


def collect_data(game, prev_screen):
    from databases import scrappers_dict
    from GUI import DataCollectorScreen
    scrapper = scrappers_dict[game]
    proceed_screen = DataCollectorScreen(game=prev_screen.game, name='proceed screen')
    prev_screen.manager.switch_to(proceed_screen)
    proceed_screen.start_collection(scrapper)


def get_data_from_database(game):
    from databases import data_getters
    getter = data_getters[game]
    return getter()


def get_single_pokemon_data(game, pokemon):
    from databases import pokemon_data_getters
    getter = pokemon_data_getters[game]
    return getter(pokemon)

