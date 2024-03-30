from collections import defaultdict

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.spinner import Spinner

from utils import TypeSelector, get_colours


def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{p:.2f}%  ({v:d})'.format(p=pct,v=val)
    return my_autopct


class StatisticsType(Spinner):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.values.append("Количество от всех покемонов")
        self.values.append("Количество от покемонов с тем же первым типом")
        self.values.append("Количество от покемонов с тем же вторым типом")
        self.values.append("График распределения по СР")
        self.values.append("График распределения по атаке")
        self.values.append("График распределения по защите")
        self.values.append("График распределения по жизням")


class ChooseFirstType(TypeSelector):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.values = TypeSelector.types
        self.values.append("Не учитывать")


class ChooseSecondType(TypeSelector):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.values = TypeSelector.types
        self.values.append("Не учитывать")
        self.values.append("Монотип")


class StatisticsLayout(BoxLayout):

    def update(self, new_widget):
        self.clear_widgets()
        self.add_widget(new_widget)


class StatisticsScreen(Screen):

    def game_selection(self):
        self.manager.current = 'pokedex game selection'

    def pokedex(self):
        self.manager.current = 'Pokemon Go pokedex'

    def to_main(self):
        self.manager.current = 'main screen'

    def show(self):
        statistics_type = self.statistics_type.text
        first_type = self.first_type.text
        second_type = self.second_type.text
        error_message = ''
        if statistics_type == 'Выберите тип графика':
            error_message += "Не выбран тип графика!\n"
        if first_type == "Выберите первый тип":
            error_message += "Не выбран первый тип покемонов!\n"
        if first_type == "Не учитывать" and statistics_type == "Количество от покемонов с тем же первым типом":
            error_message += "Невозможно посчитать количество покемонов\n от первого типа, не задав его!\n"
        if second_type == 'Выберите второй тип':
            error_message += "Не выбран второй тип покемонов!\n"
        if ((second_type == "Не учитывать" or second_type == "Монотип")
                and statistics_type == "Количество от покемонов с тем же\n вторым типом"):
            error_message += "Невозможно посчитать количество покемонов от второго типа, не задав его!\n"
        if len(error_message) > 0:
            error_window = Popup(title="Ошибка ввода данных", content=Label(text=error_message, font_size=24),
                          size_hint=(None, None),
                          size=(500, 500))
            error_window.open()
        else:
            new_widget = self.get_data(statistics_type, first_type, second_type)
            self.statistics_layout.update(new_widget)

    def get_data(self, statistics_type: str, first_type: str, second_type: str):
        if statistics_type == "Количество от всех покемонов":
            new_widget = self.cuantity_from_total(first_type, second_type)
        elif statistics_type == "Количество от покемонов с тем же первым типом":
            new_widget = self.cuantity_from_primary(first_type)
        elif statistics_type == "Количество от покемонов с тем же вторым типом":
            new_widget = self.cuantity_from_second(second_type)
        else:
            new_widget = self.stats(first_type, second_type)
        return new_widget

    def cuantity_from_total(self, first_type: str, second_type: str):
        from databases import create_engine, GoPokemon
        from sqlalchemy.orm.session import sessionmaker
        import pandas
        from kivy_garden.matplotlib.backend_kivyagg import FigureCanvas
        from matplotlib import pyplot
        engine = create_engine()
        local_session = sessionmaker(autoflush=False, autocommit=False, bind=engine)
        session = local_session()
        compare_data = session.query(GoPokemon)
        dataframe = pandas.read_sql(compare_data.statement, session.bind)
        if second_type == "Монотип":
            second_type = None
        if second_type == "Не учитывать":
            if self.ignore_type_order.active:
                types_selection = (GoPokemon.type_1 == first_type) | (GoPokemon.type_2 == first_type)
            else:
                types_selection = GoPokemon.type_1 == first_type
        elif first_type == "Не учитывать":
            if self.ignore_type_order.active:
                types_selection = (GoPokemon.type_2 == second_type) | (GoPokemon.type_1 == second_type)
            else:
                types_selection = GoPokemon.type_2 == second_type
        elif self.ignore_type_order.active:
            types_selection = (
                    ((GoPokemon.type_1 == first_type) & (GoPokemon.type_2 == second_type)) |
                    ((GoPokemon.type_1 == second_type) & (GoPokemon.type_2 == first_type))
            )
        else:
            types_selection = (GoPokemon.type_1 == first_type) & (GoPokemon.type_2 == second_type)
        compare_data = session.query(GoPokemon).where(types_selection)
        data_1 = len(pandas.read_sql(compare_data.statement, session.bind))
        data_2 = len(dataframe) - data_1
        values = [data_1, data_2]
        fig, ax = pyplot.subplots()
        ax.pie(values, labels=[f'{first_type} {second_type}', 'others'], explode=[0.25, 0.25],
               autopct=make_autopct(values))
        return FigureCanvas(pyplot.gcf())

    def cuantity_from_primary(self, first_type: str):
        from databases import create_engine, GoPokemon
        from sqlalchemy.orm.session import sessionmaker
        import pandas
        from kivy_garden.matplotlib.backend_kivyagg import FigureCanvas
        from matplotlib import pyplot
        engine = create_engine()
        local_session = sessionmaker(autoflush=False, autocommit=False, bind=engine)
        session = local_session()
        if self.ignore_type_order.active:
            type_selector = ((GoPokemon.type_1 == first_type) | (GoPokemon.type_2 == first_type))
            compare_data = session.query(GoPokemon).where(type_selector)
        else:
            compare_data = session.query(GoPokemon).where(GoPokemon.type_1 == first_type)
        dataframe = pandas.read_sql(compare_data.statement, session.bind)
        second_types = dataframe["type_2"].unique()
        values = defaultdict(int)
        for second_type in second_types:
            if second_type == first_type:
                continue
            value = len(dataframe[dataframe["type_2"] == second_type])
            values[second_type] += value
        if self.ignore_type_order.active:
            first_types = dataframe['type_1'].unique()
            for current_type in first_types:
                if current_type == first_type:
                    continue
                value = len(dataframe[dataframe["type_1"] == current_type])
                values[current_type] += value
        values['monotype'] = len(dataframe) - sum(values.values())
        values.pop(None)
        second_types = []
        numbers = []
        for key, value in values.items():
            second_types.append(key)
            numbers.append(value)
        colours = get_colours(second_types, first_type)
        fig, ax = pyplot.subplots()
        ax.pie(numbers, labels=second_types, autopct=make_autopct(numbers), pctdistance=1.5, colors=colours)
        return FigureCanvas(pyplot.gcf())

    def cuantity_from_second(self, second_type: str):
        from databases import create_engine, GoPokemon
        from sqlalchemy.orm.session import sessionmaker
        import pandas
        from kivy_garden.matplotlib.backend_kivyagg import FigureCanvas
        from matplotlib import pyplot
        engine = create_engine()
        local_session = sessionmaker(autoflush=False, autocommit=False, bind=engine)
        session = local_session()
        if self.ignore_type_order.active:
            type_selector = (GoPokemon.type_1 == second_type) | (GoPokemon.type_2 == second_type)
            compare_data = session.query(GoPokemon).where(type_selector)
        else:
            compare_data = session.query(GoPokemon).where(GoPokemon.type_2 == second_type)
        dataframe = pandas.read_sql(compare_data.statement, session.bind)
        first_types = dataframe["type_1"].unique()
        values = defaultdict(int)
        for first_type in first_types:
            if first_type == second_type:
                continue
            value = len(dataframe[dataframe["type_1"] == first_type])
            values[first_type] += value
        if self.ignore_type_order.active:
            second_types = dataframe['type_2'].unique()
            for current_type in second_types:
                if current_type == second_type:
                    continue
                value = len(dataframe[dataframe["type_2"] == current_type])
                values[current_type] += value
            values.pop(None)
        second_types = []
        numbers = []
        for key, value in values.items():
            second_types.append(key)
            numbers.append(value)
        colours = get_colours(second_types, second_type)
        fig, ax = pyplot.subplots()
        ax.pie(numbers, labels=second_types, autopct=make_autopct(numbers), pctdistance=1.5, colors=colours)
        return FigureCanvas(pyplot.gcf())

    def stats(self, first_type: str, second_type: str):
        from databases import create_engine, GoPokemon
        from sqlalchemy.orm.session import sessionmaker
        import pandas
        from kivy_garden.matplotlib.backend_kivyagg import FigureCanvas
        from matplotlib import pyplot
        engine = create_engine()
        local_session = sessionmaker(autoflush=False, autocommit=False, bind=engine)
        session = local_session()
        if second_type == "Монотип":
            second_type = None
        if first_type == "Не учитывать" and second_type == "Не учитывать":
            type_selector = None
        elif first_type == "Не учитывать":
            type_selector = (GoPokemon.type_2 == second_type)
        elif self.ignore_type_order:
            if second_type == "Не учитывать":
                type_selector = (GoPokemon.type_1 == first_type) | (GoPokemon.type_2 == first_type)
            elif first_type == "Не учитывать":
                type_selector = (GoPokemon.type_1 == second_type) | (GoPokemon.type_2 == second_type)
            else:
                type_selector = ((
                                         (GoPokemon.type_1 == first_type) & (GoPokemon.type_2 == second_type)) |
                                 ((GoPokemon.type_1 == second_type) &
                                  (GoPokemon.type_2 == first_type)))
        elif second_type == "Не учитывать":
            type_selector = (GoPokemon.type_1 == first_type)
        else:
            type_selector = (GoPokemon.type_1 == first_type) & (GoPokemon.type_2 == second_type)
        if type_selector is not None:
            compare_data = session.query(GoPokemon).where(type_selector)
        else:
            compare_data = session.query(GoPokemon)
        dataframe = pandas.read_sql(compare_data.statement, session.bind)
        statistics_type = self.statistics_type.text
        if "атак" in statistics_type:
            dataframe['max_attack_40'] = dataframe['max_attack_40'].astype('int64')
            graph = dataframe['max_attack_40']
            label = 'attack'
        elif "защит" in statistics_type:
            dataframe['max_defence_40'] = dataframe['max_defence_40'].astype('int64')
            graph = dataframe['max_defence_40']
            label = 'defence'
        elif "жизн" in statistics_type:
            dataframe['max_hp_40'] = dataframe['max_hp_40'].astype('int64')
            graph = dataframe['max_hp_40']
            label = 'HP'
        else:
            dataframe['max_cp_40'] = dataframe['max_cp_40'].astype('int64')
            graph = dataframe['max_cp_40']
            label = 'CP'
        figure = pyplot.gcf()
        if figure:
            figure.clear(keep_observers=False)
        pyplot.hist(graph)
        pyplot.xlabel(label)
        pyplot.ylabel('Pokemon')
        pyplot.grid(True, color='lightgray')
        return FigureCanvas(pyplot.gcf())





