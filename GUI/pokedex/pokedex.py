from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from GUI.custom_widgets import SelectableRecycleBoxLayout, RowLayout, SelectableGrid
from databases import collect_data, get_data_from_database
from kivy.uix.screenmanager import Screen
from GUI.pokedex.pokemon_pages import DATA_GRIDS
from databases import get_single_pokemon_data


class PokemonPage(Screen):
    """
    Базовый класс индивидуальной странички покемона.
    Ищет в словаре DATA_GRIDS виджет, соответствующий заданной игре, и генерирует его, передавая требующиеся
    данные о покемоне.
    """
    def __init__(self, game, form, **kwargs):
        super().__init__(**kwargs)
        self.game = game
        self.data = get_single_pokemon_data(game, form)
        widget = DATA_GRIDS[self.game]
        self.add_widget(widget(form))

    def to_main(self):
        """
        Возвращает пользователя на главный экран
        """
        self.manager.current = 'main screen'

    def game_selection(self):
        """
        Возвращает пользователя на экран выбора игры
        """
        self.manager.current = 'pokedex game selection'

    def pokedex(self):
        """
        Возвращает пользователя на экран покедекса
        """
        self.manager.current = 'Pokemon Go pokedex'


class PokedexRecycleBoxLayout(SelectableRecycleBoxLayout):
    """Класс, позволяющий создать проматываемую сетку покедекса с возможностью выбора по щелчку"""
    pass


class PokedexRowLayout(RowLayout):
    """Класс отдельного ряда в покедексе"""
    pass


class PokedexGrid(SelectableGrid):
    """
    Класс сетки покедекса.
    Получает данные из базы, формирует из них прокручиваемый список с возможностью выбора конкретного элемента по щелчку
    """
    def __init__(self, game, incoming_data, **kwargs):
        super().__init__(**kwargs)
        self.game = game
        global data
        if incoming_data is None:
            data = get_data_from_database(game)
        else:
            data = incoming_data
        self.rv.scroll_type = ['bars', 'content']
        self.rv.data = [{
            'image': pokemon.picture_link,
            'pokedex_number': pokemon.pokedex_number,
            'form_name': pokemon.form_name,
            'type_1': pokemon.type_1,
            'type_2': self.get_type_2(pokemon),
            'cp_40': self.round_stats(pokemon.max_cp_40),
            'cp_50': self.round_stats(pokemon.max_cp_50),
            'root_widget': self
        } for pokemon in data]

    @staticmethod
    def round_stats(stat):
        """
        Округляет стат покемона
        Нужно заменить соответствующей функцией модуля utils
        """
        return str(int(stat + (0.5 if stat > 0 else -0.5)))

    @staticmethod
    def get_type_2(pokemon):
        """
        Возвращает пустую строку, если второй тип у покемона отсутствует. Необходима для корректной обработки и
        графического представления данных. Возможно, стоит вынести в utils.
        """
        if pokemon.type_2:
            return pokemon.type_2
        return ''

    def apply_selection(self, row):
        """
        Создать и открыть страничку конкретного покемона
        """
        form = row.form.text
        page_name = self.game + " " + form
        page = PokemonPage(self.game, form, name=page_name)
        self.parent.manager.add_widget(page)
        self.parent.manager.current = page_name


class Pokedex(Screen):
    """
    Базовый экран покедекса.
    Ищет в словаре фильтров те, что соответствуют заданной игре, и добавляет в качестве виджетов
    Создаёт секцию покедекса, передавая в неё данные о нужной игре.
    Создаёт базовые кнопки навигации
    """

    def __init__(self, game, **kwargs):
        super().__init__(**kwargs)
        from .filters import filters
        self.game = game
        self.filters = filters[game]['property_filer']()
        self.name_filter = filters[game]['name_filter']
        self.grid = PokedexGrid(game, incoming_data=None)
        self.add_widget(self.grid)

    def update(self):
        screen_name = f'{self.game} choose update'
        new_screen = SelectUpdateMethod(name=screen_name, game=self.game)
        self.manager.add_widget(new_screen)
        self.manager.current = screen_name

    def to_main(self):
        """
        Возвращение на главный экран
        """
        self.manager.current = 'main screen'

    def game_selection(self):
        """
        Возвращение в меню выбора игры
        """
        self.manager.current = 'pokedex game selection'

    def update_data(self, new_data):
        """
        Обновление сетки покедекса после применения фильтров.
        НИЧЕГО НЕ ДЕЛАЕТ С БАЗОЙ
        Сетку покедекса приходится пересоздавать из-за специфической ошибки, возникающей, если после применения фильтра
        выбрать покемона, затем вернуться в покедекс и применить другой фильтр.
        """
        self.remove_widget(self.grid)
        delattr(self, 'grid')
        self.grid = PokedexGrid(self.game, incoming_data=new_data)
        self.add_widget(self.grid)

    def filter_by_name(self):
        """
        Применение фильтра по названию. Вызывает ранее найденную функцию фильтрации и обновляет сетку полученными данными
        """
        new_data = self.name_filter(self.pokemon_name.text)
        self.update_data(new_data)


class DataCollectorScreen(Screen):
    """
    Экран ожидания при получении данных скраппингом. В текущем однопоточном режиме работы приложения не открывается
    """
    def __init__(self, game, **kwargs):
        super().__init__(**kwargs)
        self.game = game
        self.current_pokemon = 'Подключение к сайту'

    def on_enter(self, *args):
        super().on_enter(*args)
        from databases import scrappers_dict
        scrapper = scrappers_dict[self.game]
        self.start_collection(scrapper)

    def start_collection(self, scrapper):
        Clock.schedule_interval(callback=self.set_pokemon, timeout=0.5)
        scrapper(self)
        Clock.unschedule(self.set_pokemon)

    def set_pokemon(self):
        self.ids.current_pokemon.text = self.current_pokemon


class NoData(Screen):
    """
    Экран, который возникает, если нет данных по какой-то игре. Методы аналогичны классу Pokedex, но их не столько,
    чтобы усложнять иерархию наследования
    """
    # TODO Переписать kv-шник для этого экрана! Разнести кнопку ручного добавления на две и связать с методами
    def __init__(self, game, **kwargs):
        super().__init__(**kwargs)
        self.game = game

    def to_main(self):
        self.manager.current = 'main screen'

    def game_selection(self):
        self.manager.current = 'pokedex game selection'

    def collect_data(self):
        """Метод для автоматического обновления данных"""
        try:
            collect_data(self.game, self)
        except KeyError:
            popup = Popup(title="Не найдена функция",
                          content=Label(text='Не найдена функция сбора данных для этой игры'),
                          size_hint=(None, None), size=(400, 400)
                          )
            popup.open()

    def add_pokemon(self):
        """Переводит на экран ручного добавления покемона"""
        pass

    def add_move(self):
        """Переводит на экран ручного добавления движения"""
        pass


class SelectUpdateMethod(Screen):
    """
    Экран, на котором выбирается метод обновления. Методы частично пересекаются с главным экраном покедекса и
    экраном, сообщающим об отсутствии данных по этой игре
    """
    def __init__(self, game, **kwargs):
        super().__init__(**kwargs)
        self.game = game

    def to_main(self):
        self.manager.current = 'main screen'

    def game_selection(self):
        self.manager.current = 'pokedex game selection'

    def pokedex(self):
        self.manager.current = f'{self.game} pokedex'

    def add_pokemon(self):
        """Переводит на экран ручного добавления покемона"""
        from .pokemon_addition_pages import PokemonStartAddition
        screen_name = 'Pokemon Adder'
        addition_screen = PokemonStartAddition(name=screen_name, game=self.game)
        self.manager.add_widget(addition_screen)
        self.manager.current = screen_name

    def add_move(self):
        """Переводит на экран ручного добавления движения"""
        pass

    def collect_data(self):
        """Метод для автоматического обновления данных"""
        try:
            collect_data(self.game, self)
        except KeyError:
            popup = Popup(title="Не найдена функция",
                          content=Label(text='Не найдена функция сбора данных для этой игры'),
                          size_hint=(None, None), size=(400, 400)
                          )
            popup.open()


