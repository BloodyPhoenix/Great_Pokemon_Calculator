from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from databases import check_data
from utils import games


class GameSelection(Screen):
    rows = len(games)

    def add_buttons(self):
        for game in games:
            self.ids.grid.add_widget(Button(text=game, font_size=20, on_release=self.proceed))

    def proceed(self, button):
        game = button.text
        data = check_data(game)
        if data:
            from . import Pokedex
            self.manager.add_widget(Pokedex(game=f'{game}', name=f'{game} pokedex'))
            self.manager.current = f'{game} pokedex'
        else:
            from . import NoData
            self.manager.add_widget(NoData(game=game, name=f'{game} no data'))
            self.manager.current = f'{game} no data'

    def go_back(self):
        self.manager.current = 'main screen'
