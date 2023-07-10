import os

from dotenv import load_dotenv, find_dotenv
from sqlalchemy import URL
from sqlalchemy.engine import create_engine as _create_engine


def create_engine():
    postgres_url = URL.create(
        "postgresql+psycopg2",
        username=os.getenv("POSTGRES_USER"),
        host=os.getenv('POSTGRES_HOST'),
        database=os.getenv("POSTGRES_DB"),
        port=int(os.getenv("POSTGRES_PORT") or 0),
        password=os.getenv("POSTGRES_PASSWORD"))
    return _create_engine(postgres_url, echo=False, pool_pre_ping=True)
