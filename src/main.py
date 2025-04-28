from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dbtypes import *
import dbtypes
from ddsql import dbsql
from datetime import datetime
Base = dbtypes.Base

username = "root"
password = "root"
host = "localhost"
port = "3306"
database = "CS440"

connection_url = f"mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}"

engine = create_engine(connection_url, echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
sql = dbsql(session, engine)
dbtypes.sql = sql

user = dbtypes.User(email='test@test.com', 
                    firstname='testfirst', 
                    lastname='testlast'
                    ).create()

special = dbtypes.Specialization(specialization='Electrician').create()

campus = dbtypes.Campus(name='testcampus', 
                        address='123 test way'
                        ).create()

building = dbtypes.Building(name='testbuilding', 
                        address='123 test way',
                        campus_id=campus.id
                        ).create()

worker = dbtypes.Worker(email='test@test.com', 
                        firstname='testfirst', 
                        lastname='testlast', 
                        specialization=special, 
                        campus=campus
                        ).create()

status = dbtypes.Status(status='teststatusssss').create()

room = dbtypes.Room(building=building, 
                    name='test').create()

req = dbtypes.Request(status=status, 
                      user=user, 
                      reqtime=datetime.now(), 
                      worker=worker, 
                      room=room).create()

print(req.user)
print(room.building)
session.close()
