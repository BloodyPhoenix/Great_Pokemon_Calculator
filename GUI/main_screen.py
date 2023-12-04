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

    def add_game(self):
        """
        Переключает на экран добавления игры
        :return: None
        """

        from .game_addition import GameAddition
        from databases import create_tables
        create_tables()
        self.manager.add_widget(GameAddition(name='create game'))
        self.manager.current = 'create game'
