from utils import TypeSelector


class SecondTypeSelector(TypeSelector):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.values = TypeSelector.types
        self.values.append("Нет")