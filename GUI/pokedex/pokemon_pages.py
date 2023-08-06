from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen

from databases import get_single_pokemon_data


def round_stats(stat):
    return int(stat + (0.5 if stat > 0 else -0.5))


class FastMoveGrid(GridLayout):
    def __init__(self, name, move_type, power_pve, speed_pve, energy_pve, power_pvp, speed_pvp, energy_pvp, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.move_type = move_type
        self.power_pve = str(power_pve)
        self.speed_pve = str(speed_pve)
        self.energy_pve = str(energy_pve)
        self.power_pvp = str(power_pvp)
        self.speed_pvp = str(speed_pvp)
        self.energy_pvp = str(energy_pve)


class ChargeMovesGrid(GridLayout):
    pass


class MovesSection(GridLayout):
    pass


class GoPokemonPage(Screen):

    def __init__(self, form, **kwargs):
        super().__init__(**kwargs)
        data = get_single_pokemon_data('Pokemon Go', form)
        self.pokemon_image = data.picture_link
        self.pokemon_number = f'Номер: {data.pokedex_number}'
        self.pokemon_species = f'Название вида: {data.species_name}'
        self.pokemon_form = f'Название формы: {data.form_name}'
        self.pokemon_type_1 = f'Тип один: {data.type_1}'
        self.pokemon_type_2 = self.get_type_2(data)
        self.base_hp = str(data.base_hp)
        self.base_attack = str(data.base_attack)
        self.base_defence = str(data.base_defence)
        self.hp_lvl_40 = str(round_stats(data.max_hp_40))
        self.attack_lvl_40 = str(round_stats(data.max_attack_40))
        self.defence_lvl_40 = str(round_stats(data.max_defence_40))
        self.cp_lvl_40 = str(round_stats(data.max_cp_40))
        self.hp_lvl_50 = str(round_stats(data.max_hp_50))
        self.attack_lvl_50 = str(round_stats(data.max_attack_50))
        self.defence_lvl_50 = str(round_stats(data.max_defence_50))
        self.cp_lvl_50 = str(round_stats(data.max_cp_50))
        self.moves_section.fast_moves_amount = len(data.fast_moves)
        self.moves_section.charge_moves_amount = len(data.charge_moves)
        self.charge_moves_amount = len(data.charge_moves)
        for move in data.fast_moves:
            move_grid = FastMoveGrid(name=move.name, move_type=move.type, power_pve=move.damage_pve,
                                     speed_pve=move.speed_pve, energy_pve=move.energy_pve, power_pvp=move.damage_pvp,
                                     speed_pvp=move.speed_pvp, energy_pvp=move.energy_pvp)
            self.moves_section.fast_moves_section.add_widget(move_grid)

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


class PokemonEditScreen(Screen):
    pass
