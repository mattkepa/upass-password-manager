import psycopg2
from config import db_config
from utils import console


def connect_db():
    """
    Connects to database and returns connection object
    """
    conn = None
    try:
        params = db_config()
        conn = psycopg2.connect(**params)
    except (Exception, psycopg2.DatabaseError) as error:
        console.print(error, style='red')

    return conn