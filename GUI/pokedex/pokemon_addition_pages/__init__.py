from .selectors import ImageSelector, SecondTypeSelector
from GUI.pokedex.pokemon_start_addition import PokemonStartAddition
from .go_pokemon_addition import PokemonGoStatsAddition


pokemon_adders = {'Pokemon Go': PokemonGoStatsAddition}


__all__ = ['ImageSelector', 'pokemon_adders', 'SecondTypeSelector', 'PokemonStartAddition']