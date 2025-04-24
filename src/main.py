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
                    )
user = sql.create_entry(user)

special = dbtypes.Specialization(specialization='Electrician').create()
# special = sql.create_entry(special)

campus = dbtypes.Campus(name='testcampus', 
                        address='123 test way'
                        ).create()
# campus = sql.create_entry(campus)

building = dbtypes.Building(name='testbuilding', 
                        address='123 test way',
                        campus_id=campus.id
                        ).create()
# building = sql.create_entry(building)

worker = dbtypes.Worker(email='test@test.com', 
                        firstname='testfirst', 
                        lastname='testlast', 
                        specialization_id=special.id, 
                        campus_id=campus.id
                        ).create()
# worker = sql.create_entry(worker)

status = dbtypes.Status(status='teststatusssss').create()
# status = sql.create_entry(status)

room = dbtypes.Room(building_id=building.id, 
                    name='test').create()
# room = sql.create_entry(room)

req = dbtypes.Request(status_id=status.id, 
                      user_id=user.id, 
                      reqtime=datetime.now(), 
                      worker_id=worker.id, 
                      room_id=room.id).create()
# req = sql.create_entry(req)
print(req)
session.close()
