from kivy.uix.checkbox import CheckBox
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen

from GUI.pokedex.pokemon_addition_pages import PokemonGoStatsAddition

pokemon_adders = {'Pokemon Go': PokemonGoStatsAddition}


class PokemonStartAddition(Screen):
    """Класс для начала создания покемона. Поскольку тут ещё нет параметров, специфичных для конкретных игр,
    используется как отправная точка для создания покемона с нуля"""

    def __init__(self, game, **kwargs):
        super().__init__(**kwargs)
        from .selectors import ImageSelector, SecondTypeSelector
        from utils import TypeSelector
        self.game = game
        self.image_pass = ''
        self.data = {}
        self.image_selector = ImageSelector(self.ids['image_button'], parent_window=self)
        self.main_properties_grid.add_widget(Label(font_size=24, text="Первый тип"))
        self.first_type_selector = TypeSelector()
        self.main_properties_grid.add_widget(self.first_type_selector)
        self.main_properties_grid.add_widget(Label(font_size=24, text="Второй тип"))
        self.second_type_selector = SecondTypeSelector()
        self.main_properties_grid.add_widget(self.second_type_selector)

    def on_pre_enter(self, *args):
        """Переопределение встроенного метода, чтобы, если происходит возвращение с предыдущих шагов, не приходилось
        заново вводить данные"""
        super().on_pre_enter(*args)
        if len(self.data) > 0:
            self.ids['image_button'].text = self.image_pass.split('/')[-1]
            self.ids['number'].text = self.data['number']
            self.ids['species_name'].text = self.data['species_name']
            self.ids['form_name'].text = self.data['form_name']
            self.first_type_selector.text = self.data['type_1']
            self.second_type_selector.text = self.data['type_2']
            self.pokemon_rarity.mega.active = self.data['mega']
            self.pokemon_rarity.legendary.active = self.data['legendary']
            self.pokemon_rarity.mythic.active = self.data['mythic']
            self.pokemon_rarity.ub_paradox.active = self.data['ub_paradox']

    def proceed(self):
        """
        Метод, который проверяет корректность введённых значений, и если они не корректны, выдаёт окно ошибки.
        Если ошибок нет, переводит на следующее окно
        """
        mistake = ''
        if len(self.image_pass) == 0:
            mistake += "Не выбран файл изображения!\n"
        if len(self.ids['number'].text) == 0:
            mistake += "Не введён номер покемона!\n"
        elif not self.ids['number'].text.isdigit():
            mistake += "В поле номера введено не число!\n"
        if len(self.ids['species_name'].text) == 0:
            mistake += "Не указано название вида!\n"
        if len(self.ids['form_name'].text) == 0:
            mistake += "Не указано название формы!\n"
        if self.first_type_selector.text not in self.first_type_selector.values:
            mistake += "Не выбран первый тип!\n"
        if self.second_type_selector.text not in self.second_type_selector.values:
            mistake += "Не выбран второй тип!\n"
        if len(mistake) > 0:
            popup = Popup(title="Ошибка ввода данных", content=Label(text=mistake, font_size=24), size_hint=(None, None),
                          size=(500, 500))
            popup.open()
        number = self.ids['number'].text
        self.data = {
            'image_pass': self.image_pass,
            'number': f'#{number}',
            'species_name': self.ids['species_name'].text,
            'form_name': self.ids['form_name'].text,
            'type_1': self.first_type_selector.text,
            'type_2': self.second_type_selector.text,
            'mega': self.pokemon_rarity.mega.active,
            'legendary': self.pokemon_rarity.legendary.active,
            'mythic': self.pokemon_rarity.mythic.active,
            'ub_paradox': self.pokemon_rarity.ub_paradox.active
        }
        screen_name = f'{self.game} add pokemon'
        new_screen = pokemon_adders[self.game]()
        self.manager.add_widget(new_screen)
        self.manager.current = screen_name

    def game_selection(self):
        self.manager.current = 'pokedex game selection'

    def pokedex(self):
        self.manager.current = 'Pokemon Go pokedex'

    def main_menu(self):
        self.manager.current = 'main screen'


class PokemonRarity(GridLayout):
    """Класс, позволяющий установить редкость покемона: мега-эволюция, легендарный, мифический, ультрачудоваище/парадокс"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text="Мега-эволюция", size_hint_y=None, height=44, size_hint_x=None))
        self.mega = CheckBox(size_hint_y=None, height=44, size_hint_x=None, width=44)
        self.add_widget(self.mega)
        self.mega.bind(active=self.active)
        self.add_widget(Label(text="Легендарный", size_hint_y=None, height=44, size_hint_x=None))
        self.legendary = CheckBox(size_hint_y=None, height=44, size_hint_x=None, width=44)
        self.add_widget(self.legendary)
        self.legendary.bind(active=self.active)
        self.add_widget(Label(text="Мифический", size_hint_y=None, height=44, size_hint_x=None))
        self.mythic = CheckBox(size_hint_y=None, height=44, size_hint_x=None, width=44)
        self.add_widget(self.mythic)
        self.mythic.bind(active=self.active)
        self.add_widget(Label(text="УЧ/Парадокс", size_hint_y=None, height=44, size_hint_x=None))
        self.ub_paradox = CheckBox(size_hint_y=None, height=44, size_hint_x=None, width=44)
        self.add_widget(self.ub_paradox)
        self.ub_paradox.bind(active=self.active)

    def active(self, checkbox, value):
        """
        Метод, отвечающий за то, чтобы нельзя было выбрать сразу несколько типов редкости, но можно было не выбрать ни
        один
        """
        if value:
            if checkbox == self.mega:
                self.legendary.active = False
                self.mythic.active = False
                self.ub_paradox.active = False
            elif checkbox == self.legendary:
                self.mega.active = False
                self.mythic.active = False
                self.ub_paradox.active = False
            elif checkbox == self.mythic:
                self.mega.active = False
                self.legendary.active = False
                self.ub_paradox.active = False
            else:
                self.mega.active = False
                self.legendary.active = False
                self.mythic.active = False


class FirstStepGrid(GridLayout):
    """Класс для отображения данных, полученных на этом шаге. Поскольку данные не будут отличаться для разных игр,
    этот класс находится здесь"""

    def __init__(self, data: dict, **kwargs):
        super().__init__(**kwargs)
        self.data = data








