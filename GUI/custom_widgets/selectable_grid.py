from kivy.properties import BooleanProperty
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):
    """Класс, позволяющий создать проматываемую сетку с возможностью выбора по щелчку"""
    pass


class RowLayout(BoxLayout, RecycleDataViewBehavior):
    """Класс отдельного ряда в сетке"""
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        """Обработчик изменений виджета"""
        self.index = index
        return super(RowLayout, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        """Позволяет выбрать определённую строчку"""
        if super(RowLayout, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        """Применить выбор и вызвать соответствующую функцию в основном классе сетки"""
        self.selected = is_selected
        if is_selected:
            self.parent.parent.parent.parent.apply_selection(self)


class SelectableGrid(GridLayout):
    """
    Класс сетки.
    Получает данные из базы, формирует из них прокручиваемый список с возможностью выбора конкретного элемента по щелчку
    """

    def apply_selection(self, row):
        """
        Применить выбор ряда. Метод должен быть переопределён
        """
        pass