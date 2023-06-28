from .go_models import Base as GoBase, FastMove, ChargeMove, Pokemon as GoPokemon

table_names = {
    'Pokemon Go': GoPokemon
}

__all__ = ['GoBase', 'GoPokemon', 'FastMove', 'ChargeMove', table_names]