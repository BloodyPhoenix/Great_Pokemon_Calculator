from .pokemon_go_scrapper import pokemon_go_scrapper
from .reconnector import open_url

scrappers_dict = {'Pokemon Go': pokemon_go_scrapper}

__all__ = ['scrappers_dict', 'open_url']
