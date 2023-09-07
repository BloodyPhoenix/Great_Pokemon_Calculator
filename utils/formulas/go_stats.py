from math import sqrt


def round_stats(stat):
    """
    Функция для математического округления параметра покемона
    """
    return int(stat + (0.5 if stat > 0 else -0.5))


GO_CP_MULTIPLIER_40 = 0.792803968
GO_CP_MULTIPLIER_50 = 0.84529999


def count_stat_lvl_40(base_stat: int, iv=15):
    return round_stats((base_stat + iv) * GO_CP_MULTIPLIER_40)


def count_stat_lvl_50(base_stat: int, iv=15):
    return round_stats((base_stat + iv) * GO_CP_MULTIPLIER_50)


def count_cp_lvl_40(hp: list, attack: list, defence: list):
    return (attack[0] + attack[1]) * sqrt(defence[0] + defence[1]) * sqrt(hp[0] + hp[1]) * (
            GO_CP_MULTIPLIER_40 ** 2) / 10

def count_cp_lvl_50(hp: list, attack: list, defence: list):
    return (attack[0] + attack[1]) * sqrt(defence[0] + defence[1]) * sqrt(hp[0] + hp[1]) * (
            GO_CP_MULTIPLIER_50 ** 2) / 10
