from .selectors import ImageSelector, SecondTypeSelector
from GUI.pokedex.pokemon_start_addition import PokemonStartAddition
from .go_pokemon_addition import PokemonGoStatsAddition
from GUI.custom_widgets.first_step_data import FirstStepData


pokemon_adders = {'Pokemon Go': PokemonGoStatsAddition}


__all__ = ['ImageSelector', 'pokemon_adders', 'SecondTypeSelector', 'PokemonStartAddition', 'FirstStepData']