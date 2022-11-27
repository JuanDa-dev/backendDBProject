from sqlalchemy import create_engine, MetaData
from os import getenv

# Database
DB_PORT = getenv('DB_PORT')
DB_HOST = getenv('DB_HOST')
DB_USER = getenv('DB_USER')
DB_PASSWORD = getenv('DB_PASSWORD')
DB_DATABASE = getenv('DB_DATABASE')
DATABASE_URL = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_DATABASE)
DATABASE_URL = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_DATABASE)

# Conexion
engine = create_engine(DATABASE_URL)
meta = MetaData()
conn = engine.connect()