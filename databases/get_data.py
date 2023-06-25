def check_data(game):
    return None


def collect_data(game):
    from databases import scrappers_dict
    scrappers_dict[game]()
