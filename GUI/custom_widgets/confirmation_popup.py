from kivy.uix.widget import Widget


class ConfirmationWidget(Widget):

    def __init__(self, label_text: str, **kwargs):
        super().__init__(**kwargs)
        self.label_text = label_text


