from os import walk
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from GUI import MainScreen,GameSelection
from kivy.lang import Builder


for path, _, files in walk('./GUI/kv/'):
    for kv in files:
        Builder.load_file(path+'/'+kv)


class GPCApp(App):

    def build(self):
        manager = ScreenManager()
        manager.add_widget(MainScreen(name='main screen'))
        manager.add_widget(GameSelection(name='pokedex game selection'))
        pokedex_game_selection = manager.get_screen('pokedex game selection')
        pokedex_game_selection.add_buttons()
        manager.current = 'pokedex game selection'
        return manager


if __name__ == '__main__':
    GPCApp().run()

