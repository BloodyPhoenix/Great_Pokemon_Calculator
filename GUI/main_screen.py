from kivy.uix.screenmanager import Screen


class MainScreen(Screen):

    def pokedex(self):
        self.manager.current = 'pokedex game selection'
