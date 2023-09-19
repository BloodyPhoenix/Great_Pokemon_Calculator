from kivy.uix.checkbox import CheckBox
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen


class PokemonStartAddition(Screen):
    """Класс для начала создания покемона. Поскольку тут ещё нет параметров, специфичных для конкретных игр,
    используется как отправная точка для создания покемона с нуля"""

    def __init__(self, game, **kwargs):
        super().__init__(**kwargs)
        from .pokemon_addition_pages import ImageSelector, SecondTypeSelector
        from utils import TypeSelector
        self.game = game
        self.image_pass = '/home/maria/PycharmProjects/ВПК/new_images/alomomola.png'
        #TODO очиститьсловарь после завершения разработки этого функционала
        self.data = {'image_pass': '/home/maria/PycharmProjects/ВПК/new_images/alomomola.png',
            'number': '#1',
            'species_name': 'Alomomola',
            'form_name': 'Alomomola',
            'type_1': 'water',
            'type_2': 'Нет',
            'mega': True,
            'legendary': False,
            'mythic': False,
            'ub_paradox': False
        }
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
            self.ids['number'].text = self.data['number'][1:]
            self.ids['species_name'].text = self.data['species_name']
            self.ids['form_name'].text = self.data['form_name']
            self.first_type_selector.text = self.data['type_1']
            self.second_type_selector.text = self.data['type_2']
            self.mega.active = self.data['mega']
            self.pokemon_rarity.legendary.active = self.data['legendary']
            self.pokemon_rarity.mythic.active = self.data['mythic']
            self.pokemon_rarity.ub_paradox.active = self.data['ub_paradox']
            if all(not active for active in (self.data['legendary'], self.data['mythic'], self.data['ub_paradox'])):
                self.pokemon_rarity.common.active = True

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
        else:
            number = self.ids['number'].text
            self.data = {
                'image_pass': self.image_pass,
                'number': f'#{number}',
                'species_name': self.ids['species_name'].text,
                'form_name': self.ids['form_name'].text,
                'type_1': self.first_type_selector.text,
                'type_2': self.second_type_selector.text,
                'mega': self.mega.active,
                'legendary': self.pokemon_rarity.legendary.active,
                'mythic': self.pokemon_rarity.mythic.active,
                'ub_paradox': self.pokemon_rarity.ub_paradox.active
                }
            from .pokemon_addition_pages import pokemon_adders
            screen_name = f'{self.game} add pokemon'
            new_screen = pokemon_adders[self.game](name=screen_name, prev_screen=self, data=self.data)
            self.manager.add_widget(new_screen)
            self.manager.current = screen_name

    def game_selection(self):
        self.manager.current = 'pokedex game selection'

    def pokedex(self):
        self.manager.current = f'{self.game} pokedex'

    def main_menu(self):
        self.manager.current = 'main screen'


class PokemonRarity(GridLayout):
    """Класс, позволяющий установить редкость покемона: мега-эволюция, легендарный, мифический,
    ультрачудоваище/парадокс"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text="Обычный", size_hint_y=None, height=44, size_hint_x=None))
        self.common = CheckBox(size_hint_y=None, height=44, size_hint_x=None, width=44, group='rarity')
        self.add_widget(self.common)
        self.add_widget(Label(text="Легендарный", size_hint_y=None, height=44, size_hint_x=None))
        self.legendary = CheckBox(size_hint_y=None, height=44, size_hint_x=None, width=44, group='rarity')
        self.add_widget(self.legendary)
        self.add_widget(Label(text="Мифический", size_hint_y=None, height=44, size_hint_x=None))
        self.mythic = CheckBox(size_hint_y=None, height=44, size_hint_x=None, width=44, group='rarity')
        self.add_widget(self.mythic)
        self.add_widget(Label(text="УЧ/Парадокс", size_hint_y=None, height=44, size_hint_x=None))
        self.ub_paradox = CheckBox(size_hint_y=None, height=44, size_hint_x=None, width=44, group='rarity')
        self.add_widget(self.ub_paradox)


class FirstStepGrid(GridLayout):
    """Класс для отображения данных, полученных на этом шаге. Поскольку данные не будут отличаться для разных игр,
    этот класс находится здесь"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.image_pass = data['image_pass']
        # self.number = f"номер: {data['number']}"
        # self.species_name = f"Вид: {data['species_name']}"
        # self.form_name = f"Форма: {data['form_name']}"
        # self.type_1 = f"Тип 1: {data['type_1']}"
        # self.type_2 = f"Тип 2: {data['type_2']}"
        # self.rarity = "Редкость: "
        # if data['ub_paradox']:
        #     self.rarity += "УЧ/Парадокс"
        # elif data['legendary']:
        #     self.rarity += "легендарный"
        # elif data['mythic']:
        #     self.rarity += "мифический"
        # else:
        #     self.rarity += "обычный"
        # if data['mega']:
        #     self.rarity += " мега-эволюция"









