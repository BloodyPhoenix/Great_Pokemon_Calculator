from kivy.uix.screenmanager import Screen


class PokemonGoStatsAddition(Screen):
    """Класс для добавления параметров атаки, защиты, ХП и СР для покемонов в Pokemon Go"""
    def __init__(self, data, **kwargs):
        super().__init__(**kwargs)
        self.data = data

    def to_main(self):
        pass

    def pokedex(self):
        pass

    def game_selection(self):
        pass

    def proceed(self):
        pass

    def go_back(self):
        pass