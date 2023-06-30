from .pokedex_filters import strongest_type as go_strongest_type


TYPE_DICT = {"normal": "нормальный", "fighting": "боевой", "flying": "летающий", "poison": "ядовитый",
              "ground": "земляной", "rock": "каменный", "bug": "насекомый", "ghost": "призрачный", "steel": "стальной",
              "fire": "огненный", "water": "водный", "grass": "травяной", "electric": "электрический",
              "psychic": "психический", "ice": "ледяной", "dragon": "драконий", "dark": "тёмный", "fairy": "волшебный"}

GO_CP_MULTIPLIER_40 = 0.792803968
GO_CP_MULTIPLIER_50 = 0.84529999

games = ['Pokemon HOME', 'Pokemon Go', 'Pokemon Red&Blue', 'Pokemon Yellow', 'Pokemon Gold&Silver',
         'Pokemon Scarlet&Violet', 'TYPE_DICT', 'GO_CP_MULTIPLIER_40', 'GO_CP_MULTIPLIER_5']

__all__ = ['games', 'TYPE_DICT', 'GO_CP_MULTIPLIER_50', 'GO_CP_MULTIPLIER_40', 'go_strongest_type']