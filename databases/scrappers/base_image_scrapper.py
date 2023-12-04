import os
import shutil
from urllib.request import urlopen, Request

import requests
from bs4 import BeautifulSoup


def create_link(pokemon_name: str):
    """
    Создаёт ссыку на страничку покемона в Бульбапедии
    :param pokemon_name: имя покемона
    :return: ссылка на страничку в Бульбапедии
    """
    pokemon_link = f'https://bulbapedia.bulbagarden.net/wiki/{pokemon_name}'
    return pokemon_link


def get_image_link(pokemon_name):
    """
    Получает ссылку на файл с изображением покемона
    :param pokemon_name: название покемона
    :return: ссылка на изображение
    """
    link = create_link(pokemon_name)
    url = Request(url=link, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(urlopen(url).read().decode('utf-8'), features="html.parser")
    image_page_link = soup.find('a', {'class': 'image', 'title': {pokemon_name}})
    base_url = 'https://bulbapedia.bulbagarden.net'
    image_page = Request(url=base_url + image_page_link.attrs['href'], headers={'User-Agent': 'Mozilla/5.0'})
    image_page_soup = BeautifulSoup(urlopen(image_page).read().decode('utf-8'), features="html.parser")
    image = image_page_soup.find('a', {'class': 'internal'})
    return 'https:' + image.attrs['href']


def save_image(pokemon_name):
    """
    Сохраняет файл с картинкой покемона на диск, возвращает ссылку на файл на диске
    :param pokemon_name: имя покемона
    :return: ссылка на файл
    """
    link = get_image_link(pokemon_name)
    work_dir = os.path.abspath(os.curdir)
    base_dir = work_dir.split('/')
    pictures_dir = ''
    while base_dir[-1] != 'ВПК':
        base_dir.pop(-1)
    for directory in base_dir:
        pictures_dir += directory
        pictures_dir += '/'
    pictures_dir += 'databases/pictures/base_pokemon/'
    pictures_dir = os.path.normpath(pictures_dir)
    if not os.path.exists(pictures_dir):
        os.makedirs(pictures_dir)
    os.chdir(pictures_dir)
    image_path = None
    res = requests.get(link, stream=True)
    if res.status_code == 200:
        name = pokemon_name.lower().replace(' ', '_') + '.png'
        with open(name, 'wb') as f:
            shutil.copyfileobj(res.raw, f)
            image_path = pictures_dir + '/' + name
            image_path = os.path.normpath(image_path)
    os.chdir(work_dir)
    return image_path


if __name__ == "__main__":
    print(save_image('Noibat'))
