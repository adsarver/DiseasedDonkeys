from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from dbtypes import *
import dbtypes
from gen_db import gendb
from ddsql import dbsql

Base = dbtypes.Base

username = "root"
password = "root"
host = "localhost"
port = "3306"
database = "CS440"

connection_url = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"

print("HELLO")
engine = create_engine(connection_url, echo=True)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
sql = dbsql(session, engine)
gendb().generate(session, engine) # Generate database if empty
# Print the names of all tables in the database
def print_all_tables(engine):
    # To load metdata and existing database schema
    metadata = MetaData()
    metadata.reflect(bind=engine)
    
    tables = metadata.tables.keys()
    
    print("List of tables:")
    for table in tables:
        print(table)

# Print all tables in the in-memory database
print_all_tables(engine)
session.close()
