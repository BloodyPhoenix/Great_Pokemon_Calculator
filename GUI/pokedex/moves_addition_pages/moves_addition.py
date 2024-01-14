from kivy.uix.screenmanager import Screen
from kivy.uix.spinner import Spinner

from utils import TypeSelector


class ChooseMoveType(Spinner):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.values = ['fast', 'charge']


class ChooseMoveTypeElement(TypeSelector):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.values = TypeSelector.types


class MovesAddition(Screen):
    pass
