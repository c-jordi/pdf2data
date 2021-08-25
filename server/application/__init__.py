__version__ = '0.1.0'


def init_database():
    """
    Create a database
    """
    from sqlalchemy import create_engine
    from sqlalchemy_utils import database_exists, create_database

    engine = create_engine("sqlite:///db.sqlite")
    if not database_exists(engine.url):
        create_database(engine.url)

