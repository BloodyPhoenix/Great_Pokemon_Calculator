import os
import re
import shutil

import requests
from bs4 import BeautifulSoup, NavigableString, Tag


def pokemon_go_scrapper():
    pass


def get_image(pokemon_data: Tag):
    image = pokemon_data.find_all("img", {"src": re.compile("(pokemon)+")})
    pure_image = image[0].attrs["src"]
    pure_image = "https://serebii.net" + pure_image
    return pure_image


def check_double(line, tags):
    if isinstance(line, Tag):
        line = line.getText().strip()
    if len(line) > 0:
        if line.isdigit():
            if isinstance(tags[-1], str):
                tags.append(int(line))
        elif line not in tags:
            tags.append(line)


def check_content(obj, content):
    if isinstance(obj, NavigableString):
        line = str(obj).strip()
        check_double(line, content)
    elif isinstance(obj, Tag):
        children = obj.findChildren()
        if len(children) > 0:
            for child in children:
                check_content(child, content)
        else:
            check_double(obj, content)


def reformat_data(data: list):
    reformatted_data = {'image_link': data[0],
                        'number': data[1], 'species_name': data[2],
                        'type_1': data[3]
                        }
    if data[4] != 'HP':
        reformatted_data['type_2'] = data[4]
        reformatted_data['HP'] = data[6]
        reformatted_data['Attack'] = data[8]
        reformatted_data['Defense'] = data[10]
        reformatted_data['Max CP'] = data[12]
        reformatted_data['moves'] = data[15:]
    else:
        reformatted_data['type_2'] = None
        reformatted_data['HP'] = data[5]
        reformatted_data['Attack'] = data[7]
        reformatted_data['Defense'] = data[9]
        reformatted_data['Max CP'] = data[11]
        reformatted_data['moves'] = data[14:]
    return reformatted_data


def get_pokemon_data(pokemon_data: Tag):
    image = get_image(pokemon_data)
    full_data = pokemon_data.parent.parent
    links = full_data.find_all('a', href=True)

    name = links[1]
    if name.next_sibling:
        name = name.text+name.next_sibling.text
    else:
        name = name.text
    name = name.rstrip()
    content = [image, ]
    types = full_data.find_all("img", {"src": re.compile("(type)+")})
    for child in full_data.children:
        check_content(child, content)
    content[2] = name
    index = 3
    for pkmn_type in types:
        content.insert(index, str(pkmn_type).split('/')[-2].split('.')[0])
        index += 1
    return reformat_data(content)


def save_data(data: list):
    # work_dir = os.path.abspath(os.curdir).split('/')
    # while work_dir[-1] != 'ВПК':
    #     work_dir.pop(-1)
    # pictures_dir = ''
    # for directory in work_dir:
    #     pictures_dir += directory
    #     pictures_dir += '/'
    # pictures_dir += 'databases/pictures/go_pokemon/'
    # if not os.path.exists(pictures_dir):
    #     os.makedirs(pictures_dir)
    # os.chdir(pictures_dir)
    # res = requests.get(data[0], stream=True)
    # if res.status_code == 200:
    #     name = data[1]+' '+data[2]+'.png'
    #     with open(name, 'wb') as f:
    #         shutil.copyfileobj(res.raw, f)
    from databases import create_engine
    engine = create_engine()
    print(engine.url.database)
    from databases import GoBase
    # GoBase.metadata.create_all(engine)
    with engine.connect() as conn:
        print('Connection successful', conn)




def get_full_gen(url):
    from reconnector import open_url
    url = open_url(url)
    soup = BeautifulSoup(url.read(), features="html.parser")
    table = soup.findAll("table", {"class": "pkmn"})
    index = 0
    for pokemon_data in table:
        data = get_pokemon_data(pokemon_data)
        print(data)
        index += 1
        if index == 4:
            break


if __name__ == '__main__':
    get_full_gen('https://serebii.net/pokemongo/gen1pokemon.shtml')
