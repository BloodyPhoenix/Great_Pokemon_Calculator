from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

from databases import get_single_pokemon_data
from utils.formulas import round_stats


class FastMoveGrid(BoxLayout):
    def __init__(self, name, move_type, power_pve, speed_pve, energy_pve, power_pvp, speed_pvp, energy_pvp, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.move_type = move_type
        self.power_pve = str(power_pve)
        self.speed_pve = str(speed_pve)
        self.energy_pve = str(energy_pve)
        self.power_pvp = str(power_pvp)
        self.speed_pvp = str(speed_pvp)
        self.energy_pvp = str(energy_pvp)


class ChargeMovesGrid(GridLayout):
    pass


class MovesSection(AnchorLayout):
    def __init__(self, fast_moves_amount, charge_moves_amount, **kwargs):
        super().__init__(**kwargs)
        self.fast_moves_amount = fast_moves_amount
        self.charge_moves_amount = charge_moves_amount


class BaseData(GridLayout):
    def __init__(self, pokemon_image, pokemon_number, pokemon_species, pokemon_form, pokemon_type_1, pokemon_type_2,
                 **kwargs):
        super().__init__(**kwargs)
        self.pokemon_image = pokemon_image
        self.pokemon_number = pokemon_number
        self.pokemon_species = pokemon_species
        self.pokemon_form = pokemon_form
        self.pokemon_type_1 = pokemon_type_1
        self.pokemon_type_2 = pokemon_type_2


class StatsGrid(GridLayout):
    pass


class BaseStats(GridLayout):
    def __init__(self, base_hp, base_attack, base_defence, **kwargs):
        super().__init__(**kwargs)
        self.base_hp = base_hp
        self.base_attack = base_attack
        self.base_defence = base_defence


class StatsLevel40(GridLayout):
    def __init__(self, hp_lvl_40, attack_lvl_40, defence_lvl_40, cp_lvl_40, **kwargs):
        super().__init__(**kwargs)
        self.hp_lvl_40 = hp_lvl_40
        self.attack_lvl_40 = attack_lvl_40
        self.defence_lvl_40 = defence_lvl_40
        self.cp_lvl_40 = cp_lvl_40


class StatsLevel50(GridLayout):
    def __init__(self, hp_lvl_50, attack_lvl_50, defence_lvl_50, cp_lvl_50, **kwargs):
        super().__init__(**kwargs)
        self.hp_lvl_50 = hp_lvl_50
        self.attack_lvl_50 = attack_lvl_50
        self.defence_lvl_50 = defence_lvl_50
        self.cp_lvl_50 = cp_lvl_50


class GoDataGrid(GridLayout):

    def __init__(self, form, **kwargs):
        super().__init__(**kwargs)
        data = get_single_pokemon_data('Pokemon Go', form)
        fast_moves_amount = len(data.fast_moves)
        charge_moves_amount = len(data.charge_moves)
        base_data = BaseData(
            pokemon_image=data.picture_link,
            pokemon_number=data.pokedex_number,
            pokemon_species=data.species_name,
            pokemon_form=data.form_name,
            pokemon_type_1=data.type_1,
            pokemon_type_2=self.get_type_2(data)
        )
        self.scroll_box.add_widget(base_data)
        stats_grid = StatsGrid()
        stats_grid.add_widget(BaseStats(str(data.base_hp), str(data.base_attack), str(data.base_defence)))
        stats_grid.add_widget(StatsLevel40(
            str(data.max_hp_40), str(data.max_attack_40), str(data.max_defence_40), str(round_stats(data.max_hp_40)))
        )
        stats_grid.add_widget(StatsLevel50(
            str(data.max_hp_50), str(data.max_attack_50), str(data.max_defence_50), str(round_stats(data.max_hp_50)))
        )
        self.scroll_box.add_widget(stats_grid)
        self.scroll_box.add_widget(Label(text="Данные о движениях", height=100, size_hint_y=None))
        moves_section = MovesSection(fast_moves_amount=fast_moves_amount, charge_moves_amount=charge_moves_amount)
        for move in data.fast_moves:
            move_grid = FastMoveGrid(name=move.name, move_type=move.type, power_pve=move.damage_pve,
                                     speed_pve=move.speed_pve, energy_pve=move.energy_pve, power_pvp=move.damage_pvp,
                                     speed_pvp=move.speed_pvp, energy_pvp=move.energy_pvp)
            moves_section.fast_moves_section.add_widget(move_grid)
        self.scroll_box.add_widget(moves_section)

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
