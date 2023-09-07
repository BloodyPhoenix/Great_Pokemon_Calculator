from .pokedex_filters import get_pokemon as get_pokemon_go, search_by_name as search_by_name_go
from .formulas import go_stats
from .type_chart import calculate_resists, type_chart
from .type_selector import TypeSelector
from .type_dict import TYPE_DICT
from .formulas import count_cp_lvl_40, count_stat_lvl_50, count_cp_lvl_50, count_stat_lvl_40

games = ['Pokemon HOME', 'Pokemon Go', 'Pokemon Red&Blue', 'Pokemon Yellow', 'Pokemon Gold&Silver',
         'Pokemon Scarlet&Violet']

__all__ = ['games', 'TYPE_DICT', 'count_stat_lvl_50', 'count_cp_lvl_50', 'count_cp_lvl_40', 'count_stat_lvl_40',
           'get_pokemon_go', 'go_stats', 'search_by_name_go', 'calculate_resists', 'type_chart', 'TYPE_DICT',
           'TypeSelector']