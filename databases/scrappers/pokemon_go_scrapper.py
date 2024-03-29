import os
import re
import shutil
import requests
from bs4 import BeautifulSoup, NavigableString, Tag
from sqlalchemy.orm import sessionmaker
from kivy.uix.screenmanager import Screen


_POKEDEX_LINKS = ['https://serebii.net/pokemongo/gen1pokemon.shtml',
                  'https://serebii.net/pokemongo/gen2pokemon.shtml',
                  'https://serebii.net/pokemongo/gen3pokemon.shtml',
                  'https://serebii.net/pokemongo/gen4pokemon.shtml',
                  'https://serebii.net/pokemongo/gen5pokemon.shtml',
                  'https://serebii.net/pokemongo/gen6pokemon.shtml',
                  'https://serebii.net/pokemongo/gen7pokemon.shtml',
                  'https://serebii.net/pokemongo/unknownpokemon.shtml',
                  'https://serebii.net/pokemongo/gen8pokemon.shtml',
                  'https://serebii.net/pokemongo/hisuipokemon.shtml',
                  'https://serebii.net/pokemongo/gen9pokemon.shtml']


def get_move_data(move_name: str):
    """
    a func that finds info about pokemon move by it's name
    :param move_name: a name of a move we need info about
    :return: full data about that move
    """
    from databases.scrappers import open_url
    url = open_url('https://serebii.net/pokemongo/moves.shtml')
    soup = BeautifulSoup(url.read().decode('cp1252'), features="html.parser")
    moves_table = soup.find("li", {"title": "VCurrent"})
    move = moves_table.find("a", {"name": move_name.lower().replace(' ', '')})
    fast = True
    if move is None:
        moves = moves_table.find_all('td', {'class': 'fooinfo'})
        current_move = filter(lambda move: move_name in move.text, moves)
        for m in current_move:
            move = m
        fast = False
    if move is None:
        return 'skip'
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
        try:
            move_data['energy_pve'] = tags[5].find('img').attrs['alt'].split()[0]
        except AttributeError:
            move_data['energy_pve'] = 1
        move_data['damage_pvp'] = int(tags[6].text.rstrip())
        move_data['energy_pvp'] = int(tags[7].text.rstrip())
    return move_data


def get_image(pokemon_data: Tag):
    """
    A func that gets link to pokemon image
    :param pokemon_data: data where are we looking for image
    :return: a straight link to image
    """
    image = pokemon_data.find_all("img", {"src": re.compile("(pokemon)+")})
    pure_image = image[0].attrs["src"]
    pure_image = "https://serebii.net" + pure_image
    return pure_image


def check_double(line, tags):
    """
    Checks if there is double info about pokemon, which is common in serebii.net tags
    :param line: a line we are checking
    :param tags: info we really need
    :return: modifies tags
    """
    if isinstance(line, Tag):
        line = line.getText().strip()
    if len(line) > 0:
        if line.isdigit():
            if isinstance(tags[-1], str):
                tags.append(int(line))
        elif line not in tags:
            tags.append(line)


def check_content(obj, content):
    """
    function that works with serenii.net stuctures to get info out of them. A recursive func
    :param obj: tag with pokemon info
    :param content: info about pokemon we already have.
    :return: Modidies content
    """
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
    """
    reformats data from get_pokemon_data func from list to dict
    :param data: list of pokemon properties
    :return:
    """
    reformatted_data = {'image_link': data[0],
                        'number': data[1], 'species_name': data[2],
                        'form_name': data[3],
                        'type_1': data[4]
                        }
    if data[5] != 'HP':
        reformatted_data['type_2'] = data[5]
        reformatted_data['HP'] = data[7]
        reformatted_data['Attack'] = data[9]
        reformatted_data['Defence'] = data[11]
        reformatted_data['Max CP'] = data[13]
        reformatted_data['moves'] = data[16:]
    else:
        reformatted_data['type_2'] = None
        reformatted_data['HP'] = data[6]
        reformatted_data['Attack'] = data[8]
        reformatted_data['Defence'] = data[10]
        reformatted_data['Max CP'] = data[12]
        reformatted_data['moves'] = data[15:]
    return reformatted_data


def get_pokemon_data(pokemon_data: Tag, proceed_screen: Screen):
    """
    Gets and reformats data for a single pokemon.
    :param pokemon_data: dict with pokemon properties or a string that indicated that pokemon is not released yet
    :return:
    """
    image = get_image(pokemon_data)
    full_data = pokemon_data.parent.parent
    links = full_data.find_all('a', href=True)

    name = links[1]
    if name.next_sibling:
        form_name = name.text + name.next_sibling.text
    else:
        form_name = name.text
    name = name.text.rstrip()
    form_name = form_name.rstrip()
    proceed_screen.current_pokemon = name
    content = [image, ]
    types = full_data.find_all("img", {"src": re.compile("(type)+")})
    for child in full_data.children:
        check_content(child, content)
    content[2] = name
    index = 3
    for pkmn_type in types:
        content.insert(index, str(pkmn_type).split('/')[-2].split('.')[0])
        index += 1
    if 'Not Currently Available' in content:
        return 'not released'
    for info in content[4: 6]:
        if type(info) == str and len(info) > 10:
            content.remove(info)
    content.insert(3, form_name)
    try:
        data = reformat_data(content)
        return data
    except IndexError:
        return 'not released'


def save_data(data: dict):
    """
    Saves pokemon data to Postgres DB
    :param data: a dictionary of pokemon params
    :return:
    """
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
        name = str(data['form_name']).lower().replace(' ', '_') + '.png'
        with open(name, 'wb') as f:
            shutil.copyfileobj(res.raw, f)
            image_path = pictures_dir + name
    os.chdir(work_dir)
    from databases import create_engine
    engine = create_engine()
    local_session = sessionmaker(autoflush=False, autocommit=False, bind=engine)
    db = local_session()
    from databases import GoPokemon, FastMove, ChargeMove
    fast_moves = []
    charge_moves = []
    for move in data['moves']:
        if db.query(FastMove).filter(FastMove.name == move).count() != 0:
            fast_moves.append(db.query(FastMove).filter(FastMove.name == move).one())
        elif db.query(ChargeMove).filter(ChargeMove.name == move).count() != 0:
            charge_moves.append(db.query(ChargeMove).filter(ChargeMove.name == move).one())
        else:
            move_data = get_move_data(move)
            if move_data == 'skip':
                print(f'No info on move {move}')
                continue
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
    data['mythic'] = 0
    data['legendary'] = 0
    data['ub_paradox'] = 0
    if 'Mega ' in data['form_name']:
        data['mega'] = 1
    else:
        data['mega'] = 0
    GoPokemon.upsert(data, db, image_path, fast_moves, charge_moves)
    db.close()


def get_full_gen(url: str, proceed_screen: Screen):
    '''
    Connects to serebii.net page and gets data from it
    :param url: serebtt.net url
    :return: None
    '''
    from . import open_url
    url = open_url(url)
    soup = BeautifulSoup(url.read().decode('cp1252'), features="html.parser")
    table = soup.findAll("table", {"class": "pkmn"})
    for pokemon_data in table:
        data = get_pokemon_data(pokemon_data, proceed_screen)
        if data == 'not released':
            continue
        save_data(data)


def pokemon_go_scrapper(proceed_screen: Screen):
    '''
    main scrapper func
    :return: None
    '''
    for link in _POKEDEX_LINKS:
        get_full_gen(link, proceed_screen)
    from GUI import Pokedex
    proceed_screen.manager.add_widget(Pokedex(game='Pokemon_GO', name='Pokemon GO pokedex'))
    proceed_screen.manager.current = 'Pokemon GO pokedex'

