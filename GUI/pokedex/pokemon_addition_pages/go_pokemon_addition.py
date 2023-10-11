from kivy.properties import BooleanProperty
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.screenmanager import Screen

from GUI.custom_widgets import SelectableGrid, RowLayout, SelectableRecycleBoxLayout


class StatsAdditionLayout(BoxLayout):
    """Слой для добавления параметров"""
    pass


class PokemonGoStatsAddition(Screen):
    #TODO Возможно, следует вынести работу с first_step_data в отдельный класс и отнаследоваться от него
    """Класс для добавления параметров атаки, защиты, ХП и СР для покемонов в Pokemon Go"""

    def __init__(self, data, prev_screen, **kwargs):
        super().__init__(**kwargs)
        self.data = data
        self.prev_screen = prev_screen
        self.first_step_data.image_pass = self.data['image_pass']
        self.first_step_data.number = self.data['number']
        self.first_step_data.species_name = self.data['species_name']
        self.first_step_data.form_name = self.data['form_name']
        self.first_step_data.type_1 = self.data['type_1']
        self.first_step_data.type_2 = self.data['type_2']
        if self.data['legendary']:
            self.first_step_data.rarity = "Легендарный"
        elif self.data['mythic']:
            self.first_step_data.rarity = "Мифический"
        elif self.data['ub_paradox']:
            self.first_step_data.rarity = "УЧ/Парадокс"
        else:
            self.first_step_data.rarity = "Обычный"
        if self.data['mega']:
            self.first_step_data.rarity += ", мега"

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        if 'hp' in self.data.keys():
            self.stats.base_hp.text = self.data['hp']
        if 'attack' in self.data.keys():
            self.stats.base_attack.text = self.data['attack']
        if 'defence' in self.data.keys():
            self.stats.base_defence.text = self.data['defence']

    def to_main(self):
        self.manager.current = 'main screen'

    def pokedex(self):
        self.manager.current = 'Pokemon Go pokedex'

    def game_selection(self):
        self.manager.current = 'pokedex game selection'

    def go_back(self):
        if len(self.stats.base_hp.text) > 1 and self.stats.base_hp.text.isdigit():
            self.data['hp'] = self.stats.base_hp.text
        if len(self.stats.base_attack.text) > 1 and self.stats.base_attack.text.isdigit():
            self.data['attack'] = self.stats.base_attack.text
        if len(self.stats.base_defence.text) > 1 and self.stats.base_defence.text.isdigit():
            self.data['defence'] = self.stats.base_defence.text
        self.prev_screen.data = self.data
        self.data = self.data
        self.manager.switch_to(self.prev_screen)

    def proceed(self):
        """
        Метод, который проверяет корректность введённых значений, и если они не корректны, выдаёт окно ошибки.
        Если ошибок нет, переводит на следующее окно
        """
        mistake = ''
        if len(self.stats.base_hp.text) < 1:
            mistake += "Не введено базовое значение НР\n"
        elif self.stats.base_hp.text.isalpha():
            mistake += "В поле \"Базовое НР\" введено не число\n"
        if len(self.stats.base_attack.text) < 1:
            mistake += "Не введено базовое значение атаки\n"
        elif self.stats.base_attack.text.isalpha():
            mistake += "В поле \"Базовая атака\" введено не число\n"
        if len(self.stats.base_defence.text) < 1:
            mistake += "Не введено базовое значение защиты\n"
        elif self.stats.base_defence.text.isalpha():
            mistake += "В поле \"Базовая защита\" введено не число\n"
        if len(mistake) > 0:
            popup = Popup(title="Ошибка ввода данных", content=Label(text=mistake, font_size=24),
                          size_hint=(None, None),
                          size=(500, 500))
            popup.open()
        else:
            self.data['hp'] = self.stats.base_hp.text
            self.data['attack'] = self.stats.base_attack.text
            self.data['defence'] = self.stats.base_defence.text
            new_screen_name = 'go pokemon add moves'
            new_screen = GoAddPokemonMoves(name=new_screen_name, data=self.data, prev_screen=self)
            self.manager.add_widget(new_screen)
            self.manager.switch_to(new_screen)


class GoAddPokemonMoves(Screen):

    def __init__(self, data, prev_screen, **kwargs):
        super().__init__(**kwargs)
        self.data = data
        self.prev_screen = prev_screen
        self.fast_moves_selector = MovesGrid(moves_category='fast')
        self.moves_selectors.add_widget(self.fast_moves_selector)
        self.charge_moves_selector = MovesGrid(moves_category='charge')
        self.moves_selectors.add_widget(self.charge_moves_selector)


class SelectableMoveRecycleBoxLayout(SelectableRecycleBoxLayout):
    """Класс, позволяющий создать проматываемую сетку движений с возможностью выбора по щелчку"""
    pass


class MoveRowLayout(RowLayout):
    """Класс отдельного ряда в сетке"""
    pass


class MovesGrid(SelectableGrid):
    """
    Класс сетки движений. Получает данные из базы и заполняет ряды
    """
    def __init__(self, moves_category, **kwargs):
        super().__init__(**kwargs)
        self.moves_category = moves_category
        global data
        from databases import moves_getters_dict
        data_getter = moves_getters_dict['Pokemon Go']
        data = data_getter('any', self.moves_category)
        self.rv.scroll_type = ['bars', 'content']
        self.rv.data = [{'move_name': move.name, 'move_type': move.type
        } for move in data]

    def apply_selection(self, row):
        """
        Добавить движение в список
        """
        print(row.move_name)

