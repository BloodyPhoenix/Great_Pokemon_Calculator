def create_tables():
    """
    Функция, которая создаёт отсутствующие таблицы в базе
    :return: None
    """
    from databases import create_engine, Metadata
    engine = create_engine()
    Metadata.metadata.create_all(engine)