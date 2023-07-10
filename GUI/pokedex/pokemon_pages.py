from kivy.uix.screenmanager import Screen

from databases import get_single_pokemon_data


def round_stats(stat):
    return int(stat + (0.5 if stat > 0 else -0.5))


class GoPokemonPage(Screen):

    def __init__(self, form, **kw):
        super().__init__(**kw)
        data = get_single_pokemon_data('Pokemon Go', form)
        self.pokemon_image = data.picture_link
        self.pokemon_number = f'Номер: {data.pokedex_number}'
        self.pokemon_species = f'Название вида: {data.species_name}'
        self.pokemon_form = f'Название формы: {data.form_name}'
        self.pokemon_type_1 = f'Тип один: {data.type_1}'
        self.pokemon_type_2 = self.get_type_2(data)
        self.base_hp = str(data.base_hp)
        self.base_attack= str(data.base_attack)
        self.base_defence = str(data.base_defence)
        self.hp_lvl_40 = str(round_stats(data.max_hp_40))
        self.attack_lvl_40 = str(round_stats(data.max_attack_40))
        self.defence_lvl_40 = str(round_stats(data.max_defence_40))
        self.cp_lvl_40 = str(round_stats(data.max_cp_40))
        self.hp_lvl_50 = str(round_stats(data.max_hp_50))
        self.attack_lvl_50 = str(round_stats(data.max_attack_50))
        self.defence_lvl_50 = str(round_stats(data.max_defence_50))
        self.cp_lvl_50 = str(round_stats(data.max_cp_50))

    @staticmethod
    def get_type_2(pokemon):
        if pokemon.type_2:
            return f"Тип два: {pokemon.type_2}"
        return ''

    def to_main(self):
        self.manager.current = 'main screen'

    def game_selection(self):
        self.manager.current = 'pokedex game selection'

    def pokedex(self):
        self.manager.current = 'Pokemon Go pokedex'
