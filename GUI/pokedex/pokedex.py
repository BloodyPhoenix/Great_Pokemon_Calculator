from kivy.properties import ObjectProperty, BooleanProperty
from kivy.uix.behaviors import ButtonBehavior, FocusBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.dropdown import DropDown
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.screenmanager import Screen
from databases import collect_data, get_data_from_database, get_single_pokemon_data


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):
    pass


class RowLayout(BoxLayout, RecycleDataViewBehavior):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(RowLayout, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(RowLayout, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            self.parent.parent.parent.parent.open_pokemon_page(self.form.text)


class PokedexGrid(GridLayout):

    def __init__(self, game, **kwargs):
        super().__init__(**kwargs)
        self.game = game
        global data
        data = get_data_from_database(game)
        self.rv.scroll_type = ['bars', 'content']
        self.rv.data = [{
            'image': pokemon.picture_link,
            'pokedex_number': pokemon.pokedex_number,
            'form_name': pokemon.form_name,
            'type_1': pokemon.type_1,
            'type_2': self.get_type_2(pokemon),
            'root_widget': self
        } for pokemon in data]

    @staticmethod
    def get_type_2(pokemon):
        if pokemon.type_2:
            return pokemon.type_2
        return ''

    def update_data(self, data):
        self.rv.data = [{
            'image': pokemon.picture_link,
            'pokedex_number': pokemon.pokedex_number,
            'form_name': pokemon.form_name,
            'type_1': pokemon.type_1,
            'type_2': self.get_type_2(pokemon),
            'root_widget': self
        } for pokemon in data]

    def open_pokemon_page(self, form):
        from . import pokemon_pages
        page_name = self.game + " " + form
        page = pokemon_pages[self.game]
        page = page(form, name=page_name)
        self.parent.manager.add_widget(page)
        self.parent.manager.current = page_name


class Pokedex(Screen):

    def __init__(self, game, **kwargs):
        super().__init__(**kwargs)
        from .filters import filters
        self.game = game
        self.filters = filters[game]()
        self.grid = PokedexGrid(game)
        self.add_widget(self.grid)

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
