from kivy.uix.screenmanager import Screen


class FirstStepData(Screen):
    """Класс, обрабатывающий данные, полученные на первом шаге создания покемона.
    Родительский класс для второго шага создания покемона для всех игр"""

    def __init__(self, data, prev_screen, **kwargs):
        super().__init__(**kwargs)
        self.data = data
        self.prev_screen = prev_screen
        self.first_step_data.image_pass = self.data['image_pass']
        self.first_step_data.number = self.data['number']
        self.first_step_data.species_name = self.data['species_name']
        self.first_step_data.form_name = self.data['form_name']
        self.first_step_data.type_1 = self.data['type_1']
        self.first_step_data.type_2 = self.data['type_2']
        if self.data['legendary']:
            self.first_step_data.rarity = "Легендарный"
        elif self.data['mythic']:
            self.first_step_data.rarity = "Мифический"
        elif self.data['ub_paradox']:
            self.first_step_data.rarity = "УЧ/Парадокс"
        else:
            self.first_step_data.rarity = "Обычный"
        if self.data['mega']:
            self.first_step_data.rarity += ", мега"