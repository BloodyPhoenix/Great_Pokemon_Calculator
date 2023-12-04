from .go_models import FastMove, ChargeMove, GoPokemon
from .base_models import Game, BaseMove as BaseMove, BasePokemon
from .metadata import Metadata

table_names = {
    'Pokemon Go': GoPokemon,
    'Base Pokemon': BasePokemon,
    'Base Move': BaseMove,
    'Game': Game
}

__all__ = ['GoPokemon', 'FastMove', 'ChargeMove', 'Game', 'BaseMove', 'BasePokemon', 'Metadata',
           table_names]