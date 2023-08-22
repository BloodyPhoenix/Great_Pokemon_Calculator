from kivy.uix.screenmanager import Screen


class MainScreen(Screen):
    """
    Класс главного экрана
    """
    def pokedex(self):
        """
        Переключает экран на выбор игры
        """
        self.manager.current = 'pokedex game selection'
