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

connection_url = f"mysql+mysql://{username}:{password}@{host}:{port}/{database}"

engine = create_engine(connection_url, echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
sql = dbsql(session, engine)

user = dbtypes.User(email='test@test.com', 
                    firstname='testfirst', 
                    lastname='testlast'
                    )
sql.create_entry(user)

special = dbtypes.Specializaion(specialization='Electrician')
sql.create_entry(special)

campus = dbtypes.Campus(name='testcampus', 
                        address='123 test way'
                        )
sql.create_entry(campus)

worker = dbtypes.Worker(email='test@test.com', 
                        firstname='testfirst', 
                        lastname='testlast', 
                        specialization=special, 
                        primary_campus=campus
                        )
sql.create_entry(worker)

status = dbtypes.Status(status='teststatus')
sql.create_entry(status)

room = dbtypes.Room(building_id=1, 
                    building='test', 
                    name='test')
sql.create_entry(room)

req = dbtypes.Request(status = status, 
                      user = user, 
                      reqtime=datetime.now(), 
                      assignee=worker, 
                      room=room)
sql.create_entry(req)

session.close()
