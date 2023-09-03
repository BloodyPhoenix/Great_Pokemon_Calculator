from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen


class PokemonStartAddition(Screen):

    def __init__(self, game, **kwargs):
        super().__init__(**kwargs)
        from .image_selector import ImageSelector
        from GUI.pokedex.pokemon_addition_pages import SecondTypeSelector
        from utils import TypeSelector
        self.game = game
        self.image_pass = ''
        self.image_selector = ImageSelector(self.ids['image_button'], parent_window=self)
        self.main_properties_grid.add_widget(Label(font_size=24, text="Первый тип"))
        self.first_type_selector = TypeSelector()
        self.main_properties_grid.add_widget(self.first_type_selector)
        self.main_properties_grid.add_widget(Label(font_size=24, text="Второй тип"))
        self.second_type_selector = SecondTypeSelector()
        self.main_properties_grid.add_widget(self.second_type_selector)

    def proceed(self):
        """
        Метод, который проверяет корректность введённых значений, и если они не корректны, выдаёт окно ошибки.
        Если ошибок нет, переводит на следующее окно
        :return:
        """
        mistake = ''
        if len(self.image_pass) == 0:
            mistake += "Не выбран файл изображения!\n"
        if len(self.ids['number'].text) == 0:
            mistake += "Не введён номер покемона!\n"
        elif not self.ids['number'].text.isdigit():
            mistake += "В поле номера введено не число!\n"
        if len(self.ids['species_name'].text) == 0:
            mistake += "Не указано название вида!\n"
        if len(self.ids['form_name'].text) == 0:
            mistake += "Не указано название формы!\n"
        if self.first_type_selector.text not in self.first_type_selector.values:
            mistake += "Не выбран первый тип!\n"
        if self.second_type_selector.text not in self.second_type_selector.values:
            mistake += "Не выбран второй тип!\n"
        if len(mistake) > 0:
            popup = Popup(title="Ошибка ввода данных", content=Label(text=mistake, font_size=24), size_hint=(None, None),
                          size=(500, 500))
            popup.open()
        number = self.ids['number'].text
        data = {
            'image_pass': self.image_pass,
            'number': f'#{number}',
            'species_name': self.ids['species_name'].text,
            'form_name': self.ids['form_name'].text,
            'type_1': self.first_type_selector.text,
            'type_2': self.second_type_selector.text
        }

    def game_selection(self):
        self.manager.current = 'pokedex game selection'

    def pokedex(self):
        self.manager.current = 'Pokemon Go pokedex'

    def main_menu(self):
        self.manager.current = 'main screen'






