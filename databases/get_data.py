from kivy.uix.screenmanager import Screen
from sqlalchemy.orm import sessionmaker


def check_data(game):
    """
    Функция, проверяющая, есть ли в принципе данные о покемонах в указанной игре.
    Нужно переделать так, чтобы она искала базы через словарь по ключу games
    """
    from databases import create_engine, table_names, GoBase
    engine = create_engine()
    GoBase.metadata.create_all(engine)
    local_session = sessionmaker(autoflush=False, autocommit=False, bind=engine)
    db = local_session()
    try:
        if db.query(table_names[f'{game}']).first():
            return True
    except KeyError:
        return False
    return False


def collect_data(game, prev_screen):
    """
    Функция, отвечающая за обновление базы данных в автоматическом режиме.
    Ищет нужный скраппер по словарю и запускает его. В многопоточном режиме ещё и должна переключать на экран ожидания
    """
    from GUI import DataCollectorScreen
    proceed_screen = DataCollectorScreen(game=prev_screen.game, name='proceed screen')
    prev_screen.manager.switch_to(proceed_screen)


def get_data_from_database(game):
    """
    Импортирует из текущего модуля словарь функций, получающих данные по всем покемонам.
    Ищет в нём функцию, ответственную за данные по конкретной игре
    Вызывает функцию и возвращает результат её работы
    """
    from databases import data_getters_dict
    getter = data_getters_dict[game]
    return getter()


def get_single_pokemon_data(game, pokemon):
    """
    Импортирует из текущего модуля словарь функций, получающих данные по одному покемону.
    Ищет в нём функцию, ответственную за данные по конкретной игре
    Вызывает функцию и возвращает результат её работы
    """
    from databases import single_pokemon_data_getters
    getter = single_pokemon_data_getters[game]
    return getter(pokemon)

