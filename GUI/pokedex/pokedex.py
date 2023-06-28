from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from databases import collect_data


class Pokedex(Screen):

    def __init__(self, game, **kwargs):
        super().__init__(**kwargs)
        self.game = game

    def update(self):
        try:
            collect_data(self.game, self)
        except KeyError:
            popup = Popup(title="Не найдена функция",
                          content=Label(text='Не найдена функция сбора данных для этой игры'),
                          size_hint=(None, None), size=(400, 400)
                          )
            popup.open()


    def to_main(self):
        self.manager.current = 'main screen'

    def game_selection(self):
        self.manager.current = 'pokedex game selection'


class DataCollectorScreen(Screen):
    def __init__(self, game, **kwargs):
        super().__init__(**kwargs)
        self.game = game

    def set_pokemon(self, pokemon: str):
        self.ids.current_pokemon.text = pokemon

    def start_collection(self, scrapper):
        scrapper(self)


class NoData(Screen):
    def __init__(self, game, **kwargs):
        super().__init__(**kwargs)
        self.game = game

    def to_main(self):
        self.manager.current = 'main screen'

    def game_selection(self):
        self.manager.current = 'pokedex game selection'

    def collect_data(self):
        try:
            collect_data(self.game, self)
        except KeyError:
            popup = Popup(title="Не найдена функция",
                          content=Label(text='Не найдена функция сбора данных для этой игры'),
                          size_hint=(None, None), size=(400, 400)
                          )
            popup.open()

    def input_data(self):
        pass
