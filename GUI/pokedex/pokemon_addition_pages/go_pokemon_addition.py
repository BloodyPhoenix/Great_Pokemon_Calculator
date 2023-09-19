from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen


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

    def to_main(self):
        self.manager.current = 'main screen'

    def pokedex(self):
        self.manager.current = 'Pokemon Go pokedex'

    def game_selection(self):
        self.manager.current = 'pokedex game selection'

    def go_back(self):
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
