from .get_data import check_data, collect_data, get_data_from_database, get_single_pokemon_data
from .scrappers import scrappers_dict
from .engine import create_engine
from .db_models import GoPokemon, FastMove, ChargeMove, Game, table_names, Metadata
from .data_getters import pokemon_go_data_getter, single_go_data_getter
from .create_tables import create_tables

data_getters_dict = {'Pokemon Go': pokemon_go_data_getter}

single_pokemon_data_getters = {'Pokemon Go': single_go_data_getter}

__all__ = ['check_data', 'collect_data', 'scrappers_dict', 'create_engine', 'GoPokemon', 'FastMove',
           'ChargeMove', 'table_names', 'data_getters_dict', 'single_pokemon_data_getters', 'get_data_from_database',
           'get_single_pokemon_data', 'Game', 'Metadata', 'create_tables']