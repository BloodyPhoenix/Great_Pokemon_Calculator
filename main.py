from os import walk
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from GUI import MainScreen,GameSelection
from kivy.lang import Builder
from dotenv import load_dotenv


load_dotenv('utils/settings/postgres_config.env')

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
    # GPCApp().run()
    from utils import go_strongest_type
    for pokemon in go_strongest_type(20, 'fairy', exclude_no_moves=True):
        print(pokemon, end='\n')
        print(pokemon.max_cp_40)

