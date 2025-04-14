from sqlalchemy import create_engine, URL, MetaData
from sqlalchemy.orm import sessionmaker
from dbtypes import *
import dbtypes
from gen_db import gendb
from ddsql import dbsql

Base = dbtypes.Base

url = URL.create(
    "mysql+mysqlconnector",
    username="root",
    password="root",  # plain (unescaped) text
    host="localhost",
    database="CS440",
)

engine = create_engine(url)
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

temp = sql.query_all(dbtypes.Status)[0]
temp.status = "fart"
sql.update_entry(temp)

session.close()
