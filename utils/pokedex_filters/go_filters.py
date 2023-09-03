from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.operators import and_


def get_pokemon(pokemon_type_1: str, pokemon_type_2: str, all_types=True, only_first=False, only_second=False,
                   monotype=False, both_types=False, exclude_no_moves=False, cp_limit=False, no_legends=False,
                   no_mythics=False, no_megas=False, ordering='pokedex', desc=True):
    """
    Фильтр, возвращающий список покемонов по заданному критерию. В первой части функции формирует требования к типу или
    типам покемона на основе заданных условий. Далее формирует требования к возможным атакам, потом - к статусу покемона
    (обычный, легендарный, мифический, любой), и, наконец, к сортировке. После этого составляет запрос к базе.
    :param pokemon_type_1: первый тип покемона
    :param pokemon_type_2: второй тип покемона
    :param all_types: если True, учитывается совпадение и по первому, и по второму типу с искомым
    :param only_first: если True, учитывается совпадение только по первому типу с искомым
    :param only_second: если True, учитывается совпадение только по второму типу с искомым
    :param monotype: если True, ищет только покемонов, у которых один тип
    :param both_types: если True, ищет покемонов, у которых строго заданное сочетание типов. Например, сочетание
    flying|dragon вернёт только линеку Ноиверна, но не Драгонайта или Саламенса, так как у тех сочетание dragon/flying
    :param exclude_no_moves: не учитывает покемонов, у которых нет атак, соответствующих первому заданному типу
    :param cp_limit: позволяет установить ограничение по СР для поиска покемонов в соответствии с лимитами лиг
    :param no_legends: если True, исключает из поиска легендарных покемонов
    :param no_mythics: если True, исключает из поиска мифических покемонов
    :param no_megas: если True, исключает из поиска мегаэволюции
    :param ordering: указывает, по какому критерию сортировать покемонов - по номеру покедекса, названию или боевой силе
    :param desc: если True, возвращает покемонов в порядке убывания по критерию, заданному переменной ordering;
    В противном случае возвращает в порядке возрастания по тому же критерию
    :return: результат поиска
    """
    from databases import create_engine, GoPokemon, FastMove, ChargeMove
    types_selection = (GoPokemon.type_1 is not None)
    options = []
    if all_types:
        types_selection = (GoPokemon.type_1 == pokemon_type_1) | (GoPokemon.type_2 == pokemon_type_1)
    if only_first:
        types_selection = (GoPokemon.type_1 == pokemon_type_1)
    if only_second:
        types_selection = (GoPokemon.type_2 == pokemon_type_2)
    if monotype:
        types_selection = (GoPokemon.type_1 == pokemon_type_1) & (GoPokemon.type_2 == None)
    if both_types:
        types_selection = (GoPokemon.type_1 == pokemon_type_1) & (GoPokemon.type_2 == pokemon_type_2)
    if exclude_no_moves:
        exclude_moves = (GoPokemon.fast_moves.any(FastMove.type == pokemon_type_1) &
                         GoPokemon.charge_moves.any(ChargeMove.type == pokemon_type_1))
    else:
        exclude_moves = (GoPokemon.fast_moves is not None)
    if cp_limit:
        max_cp = GoPokemon.max_cp_40 <= cp_limit
    else:
        max_cp = GoPokemon.max_cp_40 > 0
    if no_legends:
        options.append((GoPokemon.legendary, False))
    if no_mythics:
        options.append((GoPokemon.mythic, False))
    if no_megas:
        options.append((GoPokemon.mega, False))
    if ordering == 'pokedex':
        ordering = GoPokemon.pokedex_number
    if ordering == 'CP':
        ordering = GoPokemon.max_cp_50
    if ordering == 'name':
        ordering = GoPokemon.species_name
    engine = create_engine()
    local_session = sessionmaker(autoflush=False, autocommit=False, bind=engine)
    session = local_session()
    if options:
        result = session.query(GoPokemon).where(
                types_selection & exclude_moves & and_(*(option[0] == option[1] for option in options))
            ).filter(max_cp)
    else:
        result = session.query(GoPokemon).where(types_selection & exclude_moves).filter(max_cp)
    if desc:
        return result.order_by(ordering.desc())
    else:
        return result.order_by(ordering.asc())


def search_by_name(pokemon_name: str):
    """
    Возвращает покемона или покемонов, у которых начало названия совпадает с переданной строкой.
    """
    from databases import create_engine, GoPokemon
    engine = create_engine()
    local_session = sessionmaker(autoflush=False, autocommit=False, bind=engine)
    session = local_session()
    return session.query(GoPokemon).where(GoPokemon.species_name.like(f'{pokemon_name}%'))