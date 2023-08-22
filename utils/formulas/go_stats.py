def round_stats(stat):
    """
    Функция для математического округления параметра покемона
    """
    return int(stat + (0.5 if stat > 0 else -0.5))