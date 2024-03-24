from kivy.graphics import Rectangle
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.spinner import Spinner

from utils import TypeSelector


class StatisticsType(Spinner):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.values.append("Количество от всех покемонов")
        self.values.append("Количество от покемонов с тем же первым типом")
        self.values.append("Количество от покемонов с тем же вторым типом")
        self.values.append("График распределения по СР")


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


class StatisticsScreen(Screen):

    def show(self):
        statistics_type = self.statistics_type.text
        first_type = self.first_type.text
        second_type = self.second_type.text
        error_message = ''
        if statistics_type == 'Выберите тип графика':
            error_message += "Не выбран тип графика!\n"
        if first_type == "Выберите первый тип":
            error_message += "Не выбран первый тип покемонов!\n"
        if second_type == 'Выберите второй тип':
            error_message += "Не выбран второй тип покемонов!\n"
        if len(error_message) > 0:
            error_window = Popup(title="Ошибка ввода данных", content=Label(text=error_message, font_size=24),
                          size_hint=(None, None),
                          size=(500, 500))
            error_window.open()
        else:
            self.get_data(statistics_type, first_type, second_type)

    def get_data(self, statistics_type: str, first_type: str, second_type: str):
        from databases import create_engine, GoPokemon
        from sqlalchemy.orm.session import sessionmaker
        import pandas
        from kivy_garden.matplotlib.backend_kivyagg import FigureCanvas
        from matplotlib import pyplot
        engine = create_engine()
        local_session = sessionmaker(autoflush=False, autocommit=False, bind=engine)
        session = local_session()
        if statistics_type == "Количество от всех покемонов":
            compare_data = session.query(GoPokemon)
        elif statistics_type == "Количество от покемонов с тем же первым типом":
            compare_data = session.query(GoPokemon).where(GoPokemon.type_1 == first_type)
        elif statistics_type == "Количество от покемонов с тем же вторым типом":
            compare_data = session.query(GoPokemon).where(GoPokemon.type_2 == second_type)
        else:
            if second_type == "Монотип":
                second_type = None
            if second_type == "Не учитывать":
                compare_data = session.query(GoPokemon).where(GoPokemon.type_1 == first_type)
            else:
                compare_data = session.query(GoPokemon).where(GoPokemon.type_1 == first_type,
                                                              GoPokemon.type_2 == second_type)
        dataframe = pandas.read_sql(compare_data.statement, session.bind)
        if statistics_type == "Количество от всех покемонов":
            if second_type == "Монотип":
                second_type = None
            if second_type == "Не учитывать":
                compare_data = session.query(GoPokemon).where(GoPokemon.type_1 == first_type)
            else:
                compare_data = session.query(GoPokemon).where(GoPokemon.type_1 == first_type,
                                                              GoPokemon.type_2 == second_type)
            data_1 = len(pandas.read_sql(compare_data.statement, session.bind))
            data_2 = len(dataframe) - data_1
            fig, ax = pyplot.subplots()
            ax.pie([data_1,data_2], labels=[f'{first_type} {second_type}', 'others'], explode=[0.25, 0.25])
        elif statistics_type == "Количество от покемонов с тем же первым типом":
            second_types = dataframe["type_2"].unique()
            values = []
            print(second_types)
            for second_type in second_types:
                values.append(len(dataframe[dataframe["type_2"] == second_type]))
            fig, ax = pyplot.subplots()
            ax.pie(values, labels=second_types)
        elif statistics_type == "Количество от покемонов с тем же вторым типом":
            first_types = dataframe["type_1"].unique()
            values = []
            print(first_types)
            for first_type in first_types:
                values.append(len(dataframe[dataframe["type_1"] == first_type]))
            fig, ax = pyplot.subplots()
            ax.pie(values, labels=first_types)
        if statistics_type == "График распределения по СР":
            dataframe['max_cp_40'] = dataframe['max_cp_40'].astype('int64')
            graph = dataframe['max_cp_40']
            pyplot.hist(graph)
            pyplot.xlabel("CP")
            pyplot.ylabel('Pokemon')
            pyplot.grid(True, color='lightgray')
        new_widget = FigureCanvas(pyplot.gcf())
        popup = Popup(
            title="", content=new_widget,
            size_hint=(None, None),
            size=(500, 500)
        )
        popup.open()



