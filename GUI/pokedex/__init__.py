from .game_selection import GameSelection
from .pokedex import NoData, Pokedex, DataCollectorScreen
from .pokemon_pages import GoPokemonPage


pokemon_pages = {'Pokemon Go': GoPokemonPage}

__all__ = ['GameSelection', 'NoData', 'Pokedex', 'DataCollectorScreen', 'pokemon_pages']