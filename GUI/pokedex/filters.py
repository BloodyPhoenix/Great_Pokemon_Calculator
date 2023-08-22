from kivy.uix.checkbox import CheckBox
from kivy.uix.dropdown import DropDown
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from utils import search_by_name_go


class TypeFilter(Spinner):
    """
    Раскрывающийся список с типами покемонов
    """
    from utils import TYPE_DICT

    types = []
    for pokemon_type in TYPE_DICT.keys():
        types.append(pokemon_type)
    types.append("Любой")
    types.append("Нет")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.values = TypeFilter.types


class TypeExcluder(GridLayout):
    """
    Область меню, отвечающая за спецификацию фильтрации по типу - исключение первого типа или второго
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text="Только первый", size_hint_y=None, height=44))
        self.first_selector = CheckBox(size_hint_y=None, height=44)
        self.add_widget(self.first_selector)
        self.add_widget(Label(text="Только второй", size_hint_y=None, height=44))
        self.second_selector = CheckBox(size_hint_y=None, height=44)
        self.add_widget(self.second_selector)
        self.first_selector.bind(active=self.active)
        self.second_selector.bind(active=self.active)

    def active(self, checkbox, value):
        """
        Метод, отвечающий за то, чтобы нельзя было выбрать исключение и первого, и второго типов, но можно было не
        исключать ни один
        """
        if value:
            if checkbox == self.first_selector:
                self.second_selector.active = False
            else:
                self.first_selector.active = False


class GoFilters(DropDown):
    """
    Базовый класс фильтров для Pokemon Go
    """

    def filter(self):
        """Метод, обрабатывающий все выбранные пользователем опции и передающий их в качестве аргументов функции-фильтру
        Получает новые данные от функции-фильтра и посылает их в функцию родительского окна, ответственную за
        обновление сетки покедекса
        """
        type_1 = self.ids['type_1'].text
        type_2 = self.ids['type_2'].text
        if type_1 == 'Выберите тип':
            type_1 = "Любой"
        if type_2 == 'Выберите тип':
            type_2 = "Любой"
        params = {'pokemon_type_1': type_1, 'pokemon_type_2': type_2, 'all_types': True, 'only_first': False,
                  'only_second': False, 'monotype': False, 'both_types': False, 'exclude_no_moves': False,
                  'no_legends': False, 'no_mythics': False, 'no_megas': False, 'ordering': 'pokedex', 'desc': True}
        from utils import get_pokemon_go
        if type_2 == "Нет":
            params['all_types'] = False
            params['monotype'] = True
        if self.ids['excluder'].first_selector.active:
            params['only_first'] = True
            params['only_second'] = False
        if self.ids['excluder'].second_selector.active:
            params['only_first'] = False
            params['only_second'] = True
        if type_1 == 'Любой' and type_2 == "Любой":
            params['all_types'] = False
        if type_1 != 'Любой' and type_2 != "Любой" and type_1 != 'Нет' and type_2 != "Нет":
            params['both_types'] = True
        if self.ids['asc_or_desc'].text == "По возрастанию":
            params['desc'] = False
        else:
            params['desc'] = True
        if self.ids['sorting'].text == 'По номеру':
            params['ordering'] = 'pokedex'
        if self.ids['sorting'].text == "По названию":
            params['ordering'] = 'name'
        if self.ids['sorting'].text == "По СР":
            params['ordering'] = 'CP'
        if self.ids['no_stab'].active:
            params['exclude_no_moves'] = True
        result = get_pokemon_go(**params)
        manager = None
        for child in self.parent.children:
            if child != self:
                manager = child
        manager.current_screen.update_data(new_data=result)


filters = {'Pokemon Go': {'name_filter': search_by_name_go, 'property_filer': GoFilters}}
