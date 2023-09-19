from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen


class StatsAdditionLayout(BoxLayout):
    """Слой для добавления параметров"""
    pass


class PokemonGoStatsAddition(Screen):
    """Класс для добавления параметров атаки, защиты, ХП и СР для покемонов в Pokemon Go"""

    def __init__(self, data, first_step_grid, **kwargs):
        super().__init__(**kwargs)
        self.data = data
        self.first_step_grid = first_step_grid
        self.main_layout.add_widget(self.first_step_grid)
        self.stats = StatsAdditionLayout()
        self.main_layout.add_widget(self.stats)

    def to_main(self):
        pass

    def pokedex(self):
        pass

    def game_selection(self):
        pass

    def go_back(self):
        pass

    def proceed(self):
        """
        Метод, который проверяет корректность введённых значений, и если они не корректны, выдаёт окно ошибки.
        Если ошибок нет, переводит на следующее окно
        """
        mistake = ''
        if len(self.base_hp.text) < 1:
            mistake += "Не введено базовое значение НР\n"
        elif self.base_hp.text.isalpha():
            mistake += "В поле \"Базовое НР\" введено не число\n"
        if len(self.base_attack.text) < 1:
            mistake += "Не введено базовое значение атаки\n"
        elif self.base_attack.text.isalpha():
            mistake += "В поле \"Базовая атака\" введено не число\n"
        if len(self.base_defence.text) < 1:
            mistake += "Не введено базовое значение защиты\n"
        elif self.base_defence.text.isalpha():
            mistake += "В поле \"Базовая защита\" введено не число\n"
        if len(mistake) > 0:
            popup = Popup(title="Ошибка ввода данных", content=Label(text=mistake, font_size=24),
                          size_hint=(None, None),
                          size=(500, 500))
            popup.open()
        else:
            pass
