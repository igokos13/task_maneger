from pathlib import Path

from dotenv import load_dotenv
from psycopg import Connection
from db import get_connection

PROJECT_DIR_PATH = Path(__file__).resolve().parent

def create_tables(Connection) -> None:
    query = (PROJECT_DIR_PATH / 'shema.sql').read_text(encoding='utf-8')
    Connection.execute(query)
                       
def fill_tables(Connection) ->None:
    query = (PROJECT_DIR_PATH / 'seed.sql').read_text(encoding='utf-8')
    Connection.execute(query)
    
if __name__ =='__main__':
    with get_connection() as conn:
        create_tables(conn)
        fill_tables(conn)
    print('Таблицы созданны и заполненны данными')
    
