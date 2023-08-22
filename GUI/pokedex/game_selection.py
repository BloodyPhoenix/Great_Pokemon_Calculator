from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from databases import check_data
from utils import games


class GameSelection(Screen):
    """
    Класс, ответственный за отрисовку экрана выбора игры
    """
    rows = len(games)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_buttons()

    def add_buttons(self):
        """
        Метод, ответственный за добавление кнопок с играми. Вызывается при генерировании экрана
        """
        for game in games:
            self.ids.grid.add_widget(Button(text=game, font_size=20, on_release=self.proceed))

    def proceed(self, button):
        """Метод, ответственный за переход на страничку покедекса.
        Проверяет, есть ли данные по выбранной игре, если есть, создаёт страничку покедекса и переключает на неё.
        Если нет, создаёт экран с уведомлением об отсутствующих данных и переключает на него"""
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
        """
        Возвращение на главный экран
        """
        self.manager.current = 'main screen'
