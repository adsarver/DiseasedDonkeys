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


session.close()
