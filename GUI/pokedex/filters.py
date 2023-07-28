from kivy.uix.dropdown import DropDown
from kivy.uix.spinner import Spinner


class TypeFilter(Spinner):
    from utils import TYPE_DICT

    types = []
    for pokemon_type in TYPE_DICT.keys():
        types.append(pokemon_type)
    types.append("Любой")
    types.append("Нет")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.values = TypeFilter.types


class GoFilters(DropDown):

    def apply(self):
        type_1 = self.ids['type_1'].text
        type_2 = self.ids['type_2'].text
        from utils import go_strongest_type
        result = go_strongest_type(pokemon_type=type_1)
        manager = None
        for child in self.parent.children:
            if child != self:
                manager = child
        manager.current_screen.grid.update_data(data=result)


filters = {'Pokemon Go': GoFilters}

