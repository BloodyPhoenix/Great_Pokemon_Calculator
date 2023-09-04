import os
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from utils import TypeSelector


class SecondTypeSelector(TypeSelector):
    """Класс для выбора второго типа при ручном создании покемона"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.values = TypeSelector.types
        self.values.append("Нет")


class ImageSelector(Popup):
    """Класс для загрузки изображения при ручном создании покемона. Загрузка производится строго из директории
    new_images корневой папки приложения"""

    def __init__(self, button: Button, parent_window, **kwargs):
        super().__init__(**kwargs)
        self.button = button
        self.parent_window = parent_window
        work_dir = os.path.abspath(os.curdir)
        base_dir = work_dir.split('/')
        while base_dir[-1] != 'ВПК':
            base_dir.pop(-1)
        pictures_dir = ''
        for directory in base_dir:
            pictures_dir += directory
            pictures_dir += '/'
        pictures_dir += 'new_images/'
        if not os.path.exists(pictures_dir):
            os.makedirs(pictures_dir)
        self.pictures_dir = pictures_dir

    def image_selected(self, filename):
        self.ids['selected_image'].source = filename[0]

    def accept(self):
        path = self.ids['selected_image'].source
        self.button.text = path.split('/')[-1]
        self.parent_window.image_pass = path
        self.dismiss()
