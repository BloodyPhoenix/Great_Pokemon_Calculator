"""
Модуль, отвечающий за расчёт взаимодействия типов покемонов - их слабостей, сопротивлений, иммунитетов и так далее.
"""


class PokemonType:
    def __init__(self, name: str, weaknesses: list, resists: list, immunite: list, effectiveness: list,
                 not_effectiveness: list, no_damage: list):
        self.name = name
        self.weaknesses = weaknesses
        self.resists = resists
        self.immunite = immunite
        self.effectiveness = effectiveness
        self.not_effectiveness = not_effectiveness
        self.no_damage = no_damage


normal = PokemonType(name='normal', weaknesses=['fighting', ], resists=[], immunite=['ghost',], effectiveness=[],
                     not_effectiveness=['rock', 'steel'], no_damage=['ghost'])

fighting = PokemonType(name='fighting', weaknesses=['flying', 'psychic', 'fairy'], resists=['rock', 'bug', 'dark'],
                       immunite=[], effectiveness=['normal', 'rock', 'steel', 'ice', 'dark'],
                       not_effectiveness=['flying', 'poison', 'bug', 'psychic', 'fairy'], no_damage=['ghost'])

flying = PokemonType(name='flying', weaknesses=['rock', 'electric', 'ice', ],
                     resists=['fighting', 'bug', 'grass'], immunite=['ground',],
                     effectiveness=['fighting', 'bug', 'grass', ], not_effectiveness=['rock', 'steel', 'electric'],
                     no_damage=[])

poison = PokemonType(name='poison', weaknesses=['ground', 'psychic'], resists=['bug', 'grass', 'fairy', 'fighting'],
                     immunite=[], effectiveness=['grass', 'fairy'],
                     not_effectiveness=['poison', 'ground', 'rock', 'ghost'], no_damage=['steel', ])

ground = PokemonType(name='ground', weaknesses=['water', 'grass', 'ice'], resists=['poison', 'rock'],
                     immunite=['electric', ], effectiveness=['poison', 'rock', 'steel', 'fire', 'electric'],
                     not_effectiveness=['bug', 'grass'], no_damage=['flying', ])

rock = PokemonType(name='rock', weaknesses=['fighting', 'ground', 'steel', 'water', 'grass'],
                   resists=['normal', 'flying', 'poison', 'fire'], immunite=[],
                   effectiveness=['flying', 'bug', 'fire', 'ice'], not_effectiveness=['fighting', 'ground', 'steel'],
                   no_damage=[])

bug = PokemonType(name='bug', weaknesses=['flying', 'rock', 'fire'], resists=['fighting', 'ground', 'grass'],
                  immunite=[], effectiveness=['grass', 'psychic', 'dark'],
                  not_effectiveness=['fighting', 'flying', 'poison', 'ghost', 'steel', 'fire', 'fairy'],
                  no_damage=[])

ghost = PokemonType(name='ghost', weaknesses=['ghost', 'dark'], resists=['poison', 'bug'],
                    immunite=['normal', 'fighting'], effectiveness=['ghost', 'psychic'],
                    not_effectiveness=['dark', ], no_damage=['normal', ])

steel = PokemonType(name='steel', weaknesses=['fighting', 'ground', 'fire'],
                    resists=['normal', 'flying', 'rock', 'bug', 'steel', 'grass', 'psychic', 'ice', 'dragon', 'fairy'],
                    immunite=['poison', ], effectiveness=['rock', 'ice', 'fairy'],
                    not_effectiveness=['steel', 'fire', 'water', 'elecrtic'], no_damage=[])

fire = PokemonType(name='fire', weaknesses=['ground', 'rock', 'water'],
                   resists=['bug', 'steel', 'fire', 'grass', 'ice', 'fairy'], immunite=[],
                   effectiveness=['bug', 'steel', 'grass', 'ice'], not_effectiveness=['rock', 'fire', 'water', 'dragon'],
                   no_damage=[])

grass = PokemonType(name='grass', weaknesses=['flying', 'fire', 'bug', 'ice'],
                    resists=['ground', 'water', 'grass', 'electric'], immunite=[],
                    effectiveness=['ground', 'rock', 'water'],
                    not_effectiveness=['flying', 'poison', 'bug', 'steel', 'fire', 'grass', 'dragon'],
                    no_damage=[])

water = PokemonType(name='water', weaknesses=['grass', 'electric'], resists=['steel', 'fire', 'water', 'ice'],
                    immunite=[], effectiveness=['fire', 'rock', 'ground'],
                    not_effectiveness=['water', 'grass', 'dragon'], no_damage=[])

electric = PokemonType(name='electric', weaknesses=['ground',], resists=['flying', 'steel', 'elecric'],
                       immunite=[], effectiveness=['flying', 'water'], not_effectiveness=['grass', 'electric', 'dragon'],
                       no_damage=['ground', ])

psychic = PokemonType(name='psychic', weaknesses=['bug', 'ghost', 'dark'], resists=['fighting', 'psychic'],
                      immunite=[], effectiveness=['fighting', 'poison'],
                      not_effectiveness=['steel', 'psychic'], no_damage=['dark',])

ice = PokemonType(name='ice', weaknesses=['fighting', 'rock', 'steel', 'fire'], resists=['ice',], immunite=[],
                  effectiveness=['flying', 'ground', 'grass', 'dragon'],
                  not_effectiveness=['steel', 'fire', 'water', 'ice'], no_damage=[])

dragon = PokemonType(name='dragon', weaknesses=['ice', 'dragon', 'fairy'],
                     resists=['fire', 'water', 'electric', 'grass'], immunite=[], effectiveness=['dragon', ],
                     not_effectiveness=['steel', ], no_damage=['fairy',])

dark = PokemonType(name='dark', weaknesses=['fighting', 'bug', 'fairy'], resists=['ghost', 'dark'],
                   immunite=['psychic', ], effectiveness=['ghost', 'psychic'],
                   not_effectiveness=['fighting', 'dark', 'fairy'], no_damage=[])

fairy = PokemonType(name='fairy', weaknesses=['poison', 'steel'], resists=['fighting', 'bug', 'dark'],
                    immunite=['dragon',], effectiveness=['fighting', 'dragon', 'dark'],
                    not_effectiveness=['poison', 'steel', 'fire'], no_damage=[])

type_chart = {
    'normal': normal, 'fighting': fighting, 'flying': flying, 'poison': poison, 'ground': ground, 'rock': rock,
    'bug': bug, 'ghost': ghost, 'steel': steel, 'fire': fire, 'water': water, 'grass': grass, 'electric': electric,
    'psychic': psychic, 'ice': ice, 'dragon': dragon, 'dark': dark, 'fairy': fairy
}


def calculate_resists(type_1: str, type_2: str):
    """
    Высчитывает слабости, сопротивления и иммунитеты покемона на основе его типов, переданных в параметрах.
    Возвращает словарь. В данный момент не делает различия между одинарными и двойными сопротивлениями и слабостями.
    :return:
    """
    if len(type_2) == 0:
        type_1 = type_chart[type_1]
        properties = {'resists': [type_1.resists], 'immunite': [type_1.immunite], 'weaknesses': [type_1.weaknesses]}
        return properties
    type_1 = type_chart[type_1]
    type_2 = type_chart[type_2]
    properties = {'resists': [], 'immunite': [], 'weaknesses': []}
    for resist in type_1.resists:
        if resist not in type_2.weaknesses and resist not in type_2.immunite:
            properties['resists'].append(resist)
    for resist in type_2.resists:
        if resist not in type_1.weaknesses and resist not in type_1.immunite:
            properties['resists'].append(resist)
    for weakness in type_1.weaknesses:
        if weakness not in type_2.resists or weakness not in type_2.immunite:
            properties['weaknesses'].append(weakness)
    for weakness in type_2.weaknesses:
        if weakness not in type_1.resists or weakness not in type_1.immunite:
            properties['weaknesses'].append(weakness)
    for immunite in type_1.immunite:
        properties['immunite'].append(immunite)
    for immunite in type_2.immunite:
        properties['immunite'].append(immunite)
    return properties
