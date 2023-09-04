from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

from databases import get_single_pokemon_data
from utils.formulas import round_stats


class FastMoveInfo(DropDown):

    def __init__(self, damage_pve, damage_pvp, energy_pve, energy_pvp, speed_pve, speed_pvp, **kwargs):
        super().__init__(**kwargs)
        self.damage_pve = str(round(damage_pve / speed_pve, 2))
        self.damage_pvp = str(round(damage_pvp / speed_pvp, 2))
        self.energy_pve = str(round(energy_pve / speed_pve, 2))
        self.energy_pvp = str(round(energy_pvp / speed_pve, 2))


class ChargeMoveInfo(DropDown):
    def __init__(self, damage_pve, damage_pvp, energy, charges, speed, **kwargs):
        super().__init__(**kwargs)
        self.damage_pve = str(damage_pve)
        self.energy = str(energy)
        self.damage_pvp = str(damage_pvp)
        self.charges = str(charges)
        self.speed = str(speed)


class MovePreview(Button):
    def __init__(self, move, charge=True, **kwargs):
        super().__init__(**kwargs)
        self.move = move
        self.name = self.move.name
        self.move_type = self.move.type
        self.text = f'Название: {self.name}            Тип: {self.move_type}'
        if charge:
            self.full_info = ChargeMoveInfo(self.move.damage_pve, self.move.damage_pvp, self.move.speed,
                                            self.move.charges_pve, self.move.energy_pvp)
        else:
            self.full_info = FastMoveInfo(self.move.damage_pve, self.move.damage_pvp, self.move.energy_pve,
                                          self.move.energy_pvp, self.move.speed_pve, self.move.speed_pvp)


class MovesSection(GridLayout):
    def __init__(self, fast_moves_amount, charge_moves_amount, **kwargs):
        super().__init__(**kwargs)
        self.fast_moves_amount = fast_moves_amount
        self.charge_moves_amount = charge_moves_amount


class BaseData(GridLayout):
    def __init__(self, pokemon_image, pokemon_number, pokemon_species, pokemon_form, pokemon_type_1, pokemon_type_2,
                 rarity, **kwargs):
        super().__init__(**kwargs)
        self.pokemon_image = pokemon_image
        self.pokemon_number = pokemon_number
        self.pokemon_species = pokemon_species
        self.pokemon_form = pokemon_form
        self.pokemon_type_2 = pokemon_type_2
        if len(self.pokemon_type_2) > 0:
            self.pokemon_type_1 = f'Первый тип: {pokemon_type_1}'
        else:
            self.pokemon_type_1 = f'Тип: {pokemon_type_1}'
        self.pokemon_rarity = rarity


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


class MovesInfo:
    pass


class ResistsGrid(GridLayout):
    def __init__(self, data, **kwargs):
        super().__init__(**kwargs)
        self.resists = ''
        resists_counter = 0
        string = []
        for resist in data['resists']:
            string.append(resist)
            resists_counter += 1
            if resists_counter % 3 == 0:
                string = ', '.join(string)
                self.resists += string + '\n'
                string = []
        self.weaknesses = ''
        string = []
        weaknesses_counter = 0
        for weaknesses in data['weaknesses']:
            string.append(weaknesses)
            weaknesses_counter += 1
            if weaknesses_counter % 3 == 0:
                string = ', '.join(string)
                self.weaknesses += string + '\n'
                string = []
        self.immunite = ', '.join(data['immunite'])


class GoDataGrid(GridLayout):

    def __init__(self, form, **kwargs):
        super().__init__(**kwargs)
        from utils import calculate_resists
        data = get_single_pokemon_data('Pokemon Go', form)
        fast_moves_amount = len(data.fast_moves)
        charge_moves_amount = len(data.charge_moves)
        type_1 = data.type_1
        type_2 = self.get_type_2(data)
        rarity = "Редокость: "
        if data.mega:
            rarity += "мега-эволюция"
        elif data.legendary:
            rarity += "легендарный"
        elif data.mythic:
            rarity += "мифический"
        elif data.ub_paradox:
            rarity += "УЧ/Парадокс"
        else:
            rarity += "обычный"
        base_data = BaseData(
            pokemon_image=data.picture_link,
            pokemon_number=data.pokedex_number,
            pokemon_species=data.species_name,
            pokemon_form=data.form_name,
            pokemon_type_1=type_1,
            pokemon_type_2=type_2,
            rarity=rarity
        )
        self.scroll_box.add_widget(base_data)
        resists_data = calculate_resists(type_1, type_2.split()[-1])
        resists_grid = ResistsGrid(resists_data)
        self.scroll_box.add_widget(resists_grid)
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
            move_preview = MovePreview(move, charge=False)
            moves_section.fast_moves_section.add_widget(move_preview)
        for move in data.charge_moves:
            move_preview = MovePreview(move, charge=True)
            moves_section.charge_moves_section.add_widget(move_preview)
        self.scroll_box.add_widget(moves_section)

    @staticmethod
    def get_type_2(pokemon):
        if pokemon.type_2:
            return f"Второй тип: {pokemon.type_2}"
        return ''


class PokemonEditScreen(Screen):
    pass
