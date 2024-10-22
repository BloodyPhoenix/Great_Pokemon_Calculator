from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.spinner import Spinner
from sqlalchemy.orm import sessionmaker

from GUI.custom_widgets import ConfirmationWidget
from utils import TypeSelector


class ChooseMoveType(Spinner):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.values = ['fast', 'charge']


class ChooseMoveTypeElement(TypeSelector):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.values = TypeSelector.types


class MovesAdditionStart(Screen):

    def __init__(self, pokemon_data=None, **kwargs, ):
        super().__init__(**kwargs)
        self.pokemon_data = pokemon_data
        self.rewrite = False

    def to_main(self):
        pass

    def go_back(self):
        pass

    def proceed(self):
        name = self.move_name.text
        type_fc = self.move_type.text
        type_element = self.move_element.text
        move_power_pwe = self.move_power_pwe.text
        move_power_pwp = self.move_power_pwp.text
        error_message = ''
        if len(name) < 1:
            error_message += "Не указано название движения!\n"
        if type_fc == 'Выберите тип движения':
            error_message += "Не указан тип движения \"быстрое/заряжаемое\"!\n"
        if type_element == 'Выберите элемент':
            error_message += "Не указан тип движения \"элемент\"!\n"
        if len(move_power_pwe) < 0:
            error_message += "Не введена сила движения в PvE!"
        elif move_power_pwe.isalpha():
            error_message += "В поле \"сила движения в PvE\" введено не число!"
        if len(move_power_pwp) < 0:
            error_message += "Не введена сила движения в PvP!"
        elif move_power_pwp.isalpha():
            error_message += "В поле \"сила движения в PvP\" введено не число!"
        if len(error_message) > 0:
            popup = Popup(title="Ошибка ввода данных", content=Label(text=error_message, font_size=24),
                          size_hint=(None, None),
                          size=(500, 500))
            popup.open()
        else:
            move_data = {
                'name': name,
                'type': type_element,
                'damage_pve': move_power_pwe,
                'damage_pvp': move_power_pwp
            }
            screen_name = 'Move Adder Second'
            if type_fc == 'fast':
                new_screen = MoveAdditionFast(move_data, name=screen_name)
            else:
                new_screen = MoveAdditionFast(move_data, name=screen_name)
            self.manager.add_widget(new_screen)
            self.manager.current = screen_name


class MoveAdditionFast(Screen):

    def __init__(self, move_data, **kw):
        super().__init__(**kw)
        self.move_data = move_data

    def check_data(self):
        """
        Проверяет, что все данные введены верно. Если это не так, возвращает False
        :return: bool
        """
        speed_pve = self.speed_pve.text
        speed_pvp = self.speed_pvp.text
        energy_pve = self.energy_pve.text
        energy_pvp = self.energy_pvp.text
        error_message = ''
        if len(speed_pve) < 0:
            error_message += 'Не заполнено поле \"Скорость в pve\"!\n'
        elif speed_pve.isalpha():
            error_message += "В поле \"Скорость в pve\" введено не число!\n"
        if len(speed_pvp) < 0:
            error_message += 'Не заполнено поле \"Скорость в pvp\"!\n'
        elif speed_pvp.isalpha():
            error_message += "В поле \"Скорость в pvp\" введено не число!\n"
        if len(energy_pve) < 0:
            error_message += 'Не заполнено поле \"Энергия в pve\"!'
        elif energy_pve.isalpha():
            error_message += "В поле \"Энергия в pve\" введено не число!\n"
        if len(energy_pvp) < 0:
            error_message += 'Не заполнено поле \"Энергия в pvp\"!\n'
        elif energy_pvp.isalpha():
            error_message += "В поле \"Энергия в pvp\" введено не число!\n"
        if len(error_message) > 0:
            popup = Popup(title="Ошибка ввода данных", content=Label(text=error_message, font_size=24),
                          size_hint=(None, None),
                          size=(500, 500))
            popup.open()
        else:
            self.move_data['energy_pve'] = energy_pve
            self.move_data['energe_pvp'] = energy_pvp
            self.move_data['speed_pve'] = speed_pve
            self.move_data['speed_pvp'] = speed_pvp
            return True

    def proceed(self):
        if self.check_data():
            from databases import FastMove, create_engine
            engine = create_engine()
            local_session = sessionmaker(autoflush=False, autocommit=False, bind=engine)
            session = local_session()
            current_move = session.query(FastMove).filter(FastMove.name == self.move_data['name']).first()
            if current_move:
                confirmed = False
                popup_content = ConfirmationWidget(label_text="Такое движение уже есть в базе\nПерезаписать?")
                popup = Popup(title="Повторное движение в базе",
                              content=popup_content,
                              size_hint=(None, None),
                              size=(500, 500))
                popup_content.cancel.bind(on_release=popup.dismiss)
                popup_content.confirm_action.bind(on_release=self.rewrite)
                popup.open()
                print(confirmed)
            FastMove.upsert(session=session, data=self.move_data)

    def rewrite(self, button):
        pass


    def to_main(self):
        self.manager.current = 'main screen'

    def go_back(self):
        pass


class MovesAdditionCharge(Screen):

    def __init__(self, move_data, **kw):
        super().__init__(**kw)
        self.move_data = move_data
