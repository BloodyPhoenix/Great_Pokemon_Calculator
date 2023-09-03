from kivy.uix.spinner import Spinner


class TypeSelector(Spinner):
    """Раскрывающийся список с возможными типами покемонов и атак"""

    from .type_dict import TYPE_DICT
    types = []
    for pokemon_type in TYPE_DICT.keys():
        types.append(pokemon_type)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.values = TypeSelector.types
