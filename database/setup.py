from sqlalchemy.engine import create_engine, Engine
from sqlalchemy import inspect
from database.schema import *
from sqlalchemy.engine import URL
from dotenv import load_dotenv
import os

load_dotenv()

class DB_setup():
    """ Configuration setup for database """

    REQUIRED = ['DB_HOST', 'DB_PORT', 'DB_USER', 'DB_PASSWORD', 'DB_NAME', 'DB_SCHEMA', 'DB_SSLREQUIRED']

    def __init__(self):
        self.cfg = self.load_db_config()
        self.url = self.create_url()
        self.engine:Engine = self.init_engine()
        self.inspector = self.init_inspector()

    def load_db_config(self):
        """ Load required env variables and cross verify them """
        for cfg in self.REQUIRED:
            if os.getenv(cfg) is None or os.getenv(cfg).strip() == "" :
                raise ValueError(f'Required config {cfg} is not available')

        return {
            "HOST" : os.getenv('DB_HOST'),
            "PORT" : os.getenv('DB_PORT'),
            "USERNAME" : os.getenv('DB_USER'),
            "PASSWORD": os.getenv('DB_PASSWORD'),
            "DATABASE" : os.getenv('DB_NAME'),
            "SCHEMA" : os.getenv('DB_SCHEMA'),
            "SSL" : os.getenv('DB_SSLREQUIRED')
        }

    def create_url(self):
        """ Setup url configs """
        url = URL.create(
            "postgresql+psycopg2",
            username=self.cfg["USERNAME"],
            password=self.cfg["PASSWORD"],
            host=self.cfg["HOST"],
            database=self.cfg["DATABASE"],
            port=self.cfg["PORT"],
        )
        return url

    def init_engine(self) -> Engine:
        """ Create engine """
        engine = create_engine(url=self.url)
        return engine

    def init_inspector(self):
        """ Create inspector """
        self.inspector = inspect(self.engine)

    def test_connection(engine:Engine):
        """ Establish connection with database """
        try:
            with engine.connect() as conn:
                print(f"Engine started successfully!!")
                
        except Exception as e:
            print(f"Unable to connect to database. {e}")

    def create_tables(self):
        """ Create tables from schema """
        Base.metadata.create_all(self.engine)