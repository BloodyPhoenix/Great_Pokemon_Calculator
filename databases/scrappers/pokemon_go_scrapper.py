import os
import re
import shutil
from math import sqrt

import requests
from bs4 import BeautifulSoup, NavigableString, Tag
from sqlalchemy import exists
from sqlalchemy.orm import sessionmaker
from utils import GO_CP_MULTIPLIER_40, GO_CP_MULTIPLIER_50


def pokemon_go_scrapper():
    pass


def get_move_data(move_name: str):
    from databases.scrappers import open_url
    url = open_url('https://serebii.net/pokemongo/moves.shtml')
    soup = BeautifulSoup(url.read(), features="html.parser")
    moves_table = soup.find("li", {"title": "VCurrent"})
    move = moves_table.find("a", {"name": move_name.lower().replace(' ', '')})
    fast = True
    if move is None:
        moves = moves_table.find_all('td', {'class': 'fooinfo'})
        current_move = filter(lambda move: move_name in move.text, moves)
        for m in current_move:
            move = m
        fast = False
    move = move.parent
    if fast:
        move = move.parent
    move_data = dict()
    move_data['name'] = move_name
    move_data['move_type'] = str(move.find_all("img", {"src": re.compile("(type)+")})).split('/')[-2].split('.')[0]
    tags = move.find_all('td')
    if fast:
        move_data['damage_pve'] = int(tags[2].text.rstrip())
        move_data['energy_pve'] = int(tags[3].text.rstrip())
        move_data['speed_pve'] = float(tags[4].text.split()[0])
        move_data['damage_pvp'] = int(tags[5].text.rstrip())
        move_data['energy_pvp'] = int(tags[6].text.rstrip())
        move_data['speed_pvp'] = float(tags[7].text.split()[0])
    else:
        move_data['damage_pve'] = int(tags[2].text.rstrip())
        move_data['speed'] = float(tags[4].text.split()[0])
        move_data['energy_pve'] = tags[5].find('img').attrs['alt'].split()[0]
        move_data['damage_pvp'] = int(tags[6].text.rstrip())
        move_data['energy_pvp'] = int(tags[7].text.rstrip())
    return move_data


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
        name = name.text + name.next_sibling.text
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


def save_data(data: dict):
    work_dir = os.path.abspath(os.curdir)
    base_dir = work_dir.split('/')
    while base_dir[-1] != 'ВПК':
        base_dir.pop(-1)
    pictures_dir = ''
    for directory in base_dir:
        pictures_dir += directory
        pictures_dir += '/'
    pictures_dir += 'databases/pictures/go_pokemon/'
    if not os.path.exists(pictures_dir):
        os.makedirs(pictures_dir)
    os.chdir(pictures_dir)
    image_path = None
    res = requests.get(data['image_link'], stream=True)
    if res.status_code == 200:
        name = data['species_name'] + '.png'
        with open(name, 'wb') as f:
            shutil.copyfileobj(res.raw, f)
            image_path = pictures_dir + name
    os.chdir(work_dir)
    from databases import create_engine
    engine = create_engine()
    local_session = sessionmaker(autoflush=False, autocommit=False, bind=engine)
    db = local_session()
    from databases import GoBase, GoPokemon, FastMove, ChargeMove
    GoBase.metadata.create_all(engine)
    fast_moves = []
    charge_moves = []
    for move in data['moves']:
        if db.query(FastMove).filter(FastMove.name == move).count() != 0:
            fast_moves.append(db.query(FastMove).filter(FastMove.name == move).one())
        elif db.query(ChargeMove).filter(ChargeMove.name == move).count() != 0:
            charge_moves.append(db.query(ChargeMove).filter(ChargeMove.name == move).one())
        else:
            move_data = get_move_data(move)
            if 'speed_pve' in move_data:
                fast_move = FastMove(
                    name=move,
                    type=move_data['move_type'],
                    damage_pve=move_data['damage_pve'],
                    damage_pvp=move_data['damage_pvp'],
                    energy_pve=move_data['energy_pve'],
                    energy_pvp=move_data['energy_pvp'],
                    speed_pve=move_data['speed_pve'],
                    speed_pvp=move_data['speed_pvp']
                )
                db.add(fast_move)
                db.flush()
                fast_moves.append(fast_move)
            else:
                charge_move = ChargeMove(
                    name=move,
                    type=move_data['move_type'],
                    damage_pve=move_data['damage_pve'],
                    damage_pvp=move_data['damage_pvp'],
                    charges_pve=move_data['energy_pve'],
                    energy_pvp=move_data['energy_pvp'],
                    speed=move_data['speed'],
                )
                db.add(charge_move)
                db.flush()
                charge_moves.append(charge_move)
    pokemon = GoPokemon(
        picture_link=image_path,
        pokedex_number=data['number'],
        species_name=data['species_name'],
        type_1=data['type_1'],
        type_2=data['type_2'],
        base_hp=data['HP'],
        max_hp_40=(data['HP'] + 15) * GO_CP_MULTIPLIER_40,
        max_hp_50=(data['HP'] + 15) * GO_CP_MULTIPLIER_50,
        base_attack=data['Attack'],
        max_attack_40=(data['Attack'] + 15) * GO_CP_MULTIPLIER_40,
        max_attack_50=(data['Attack'] + 15) * GO_CP_MULTIPLIER_50,
        base_defence=data['Defense'],
        max_defence_40=(data['Defense'] + 15) * GO_CP_MULTIPLIER_40,
        max_defence_50=(data['Defense'] + 15) * GO_CP_MULTIPLIER_50,
        max_cp_40=(data['Attack'] + 15) * sqrt(data['Defense'] + 15) * sqrt(data['HP'] + 15) * (
                GO_CP_MULTIPLIER_40 ** 2) / 10,
        max_cp_50=(data['Attack'] + 15) * sqrt(data['Defense'] + 15) * sqrt(data['HP'] + 15) * (
                GO_CP_MULTIPLIER_50 ** 2) / 10,
    )
    for move in fast_moves:
        pokemon.fast_moves.append(move)
    for move in charge_moves:
        pokemon.charge_moves.append(move)
    db.add(pokemon)
    db.commit()
    db.close()


def get_full_gen(url):
    from reconnector import open_url
    url = open_url(url)
    soup = BeautifulSoup(url.read(), features="html.parser")
    table = soup.findAll("table", {"class": "pkmn"})
    index = 0
    for pokemon_data in table:
        data = get_pokemon_data(pokemon_data)
        save_data(data)
        index += 1
        if index == 1:
            break


if __name__ == '__main__':
    from databases import create_engine
    engine = create_engine()
    local_session = sessionmaker(autoflush=False, autocommit=False, bind=engine)
    db = local_session()
    from databases import GoBase, GoPokemon, FastMove, ChargeMove
    print(db.query(GoPokemon).filter(GoPokemon.species_name=='Bulbasaur').one())
