from kivy.event import EventDispatcher


class ConfirmationDispatcher(EventDispatcher):

    def __init__(self, *args, **kwargs):
        self.register_event_type('confirm')
        super(ConfirmationDispatcher, self).__init__(**kwargs)

    def confirm_action(self, value):
        self.dispatch('confirm', value)

    def confirm(self, *args):
        print('yay!', args)