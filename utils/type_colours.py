type_colours = {
    'dark': 'dimgrey',
    'normal': 'lightgrey',
    'grass': 'limegreen',
    'water': 'blue',
    'fire': 'red',
    'electric': 'yellow',
    'ice': 'aquamarine',
    'steel': 'silver',
    'rock': 'darkgoldenrod',
    'ground': 'gold',
    'bug': 'greenyellow',
    'fighting': 'firebrick',
    'flying': 'azure',
    'poison': 'purple',
    'ghost': 'midnightblue',
    'psychic': 'fuchsia',
    'fairy': 'deeppink',
    'dragon': 'indigo'
}


def get_colours(types: list, deter_type: str):
    colours = []
    for one_type in types:
        if one_type not in type_colours:
            colours.append(type_colours[deter_type])
        else:
            colours.append(type_colours[one_type])
    return colours
