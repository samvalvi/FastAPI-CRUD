from sqlalchemy import create_engine, MetaData
from dotenv import load_dotenv
import os

load_dotenv()

password = os.getenv('MYSQL_ROOT_PASSWORD')
mysql_db = os.getenv('MYSQL_DATABASE')
user = os.getenv('MYSQL_ROOT_USER')

engine = create_engine(f'mysql+pymysql://{user}:{password}@localhost:3306/{mysql_db}')

meta = MetaData()

conn = engine.connect()
