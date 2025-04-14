import random
from datetime import datetime
from ddsql import *
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker
import dbtypes

class gendb():
    def __init__(self):
        self.ADDRESS = "Straight ST"
        self.NAMES = []
        self.BUILDINGS = {
            "Downtown":[
                "Armstrong",
                "Brookes",
                "Mountainlair",
                "Clark",
                "White",
                "LSB",
                "Hodges",
                "Library"
                ],
            "HSC":[
                "Ruby"
                ],
            "Evansdale":[
                "ESB",
                "AERB",
                "MRB",
                "ERB",
                "NRCCE",
            ]
        }
        self.SPECIALIZATIONS = [
            "Electrician",
            "HVAC",
            "Groundskeeper",
            "Plumber",
            "Welder"
        ]
        self.STATUS = [
            "OPEN",
            "INPROGRESS",
            "COMPLETE"
        ]
        with open("names.txt") as file:
            self.NAMES = file.readlines(-1)   
    
    def gen_worker(self, amount = 20):
        print("Generating workers...")
        campuses = self.dbsql.query_all(dbtypes.Campus)
        speclist = self.dbsql.query_all(dbtypes.Specializaion)
        
        for _ in range(amount):
            first, last = random.randint(0, len(self.NAMES) - 1), random.randint(0, len(self.NAMES) - 1)
            firstname, lastname = self.NAMES[first], self.NAMES[last]
            email = firstname[0] + lastname[0:3] + str(first) + "@email.com"
            campus = campuses[random.randint(0,2)]
            special = speclist[random.randint(0,len(speclist) - 1)]
            
            worker = dbtypes.Worker(email=email, firstname=firstname, lastname=lastname, specialization=special, primary_campus=campus)
            self.dbsql.create_entry(worker)


    def gen_user(self, amount=20):
        print("Generating users...")
        for _ in range(amount):
            first, last = random.randint(0, len(self.NAMES)), random.randint(0, len(self.NAMES))
            firstname, lastname = self.NAMES[first], self.NAMES[last]
            email = firstname[0] + lastname[0:3] + str(first) + "@email.com"
            
            user = dbtypes.User(email=email, firstname=firstname, lastname=lastname)
            self.dbsql.create_entry(user)


    def gen_request(self, amount=50):
        print("Generating requests...")
        for _ in range(amount):
            users = self.dbsql.query_all(dbtypes.User)
            workers = self.dbsql.query_all(dbtypes.Worker)
            rooms = self.dbsql.query_all(dbtypes.Room)
            statuses = self.dbsql.query_all(dbtypes.Status)
            
            status = statuses[random.randint(0, 2)]
            user = users[random.randint(0,len(users) - 1)]
            worker = workers[random.randint(0,len(workers) - 1)]
            room = rooms[random.randint(0,len(rooms) - 1)]
            
            req = dbtypes.Request(status = status, user = user, reqtime=datetime.now(), assignee=worker, room=room)
            self.dbsql.create_entry(req)

        
    
    def gen_rooms(self):
        print("Generating rooms...")
        buildings = self.dbsql.query_all(dbtypes.Building)
        for building in buildings:
            for floor in range(100, 500, 100):
                for roomnum in range(floor, floor + 11):
                    room = dbtypes.Room(building_id=building.id, building=building, name=roomnum)
                    self.dbsql.create_entry(room)
            
    
    def init_campuses(self):   
        print("Generating campuses...")     
        for campus in self.BUILDINGS.keys():
            address = str(random.randint(1, 2000)) + " " + self.ADDRESS
            campus = dbtypes.Campus(name=campus, address=address)
            self.dbsql.create_entry(campus)

    
    def init_buildings(self):
        print("Generating buildings...")
        campuses = self.dbsql.query_all(dbtypes.Campus)
        for campus in campuses:

            for name in self.BUILDINGS[campus.name]:
                address = str(random.randint(1, 2000)) + " " + self.ADDRESS
                building = dbtypes.Building(campus_id=campus.id, campus=campus, address=address, name=name)
                self.dbsql.create_entry(building)

    
    def init_statuses(self):
        print("Generating statuses...")
        for name in self.STATUS:
            status = dbtypes.Status(status=name)
            self.dbsql.create_entry(status)

    
    def init_specials(self):
        print("Generating specializations...")
        for name in self.SPECIALIZATIONS:
            spec = dbtypes.Specializaion(specialization=name)
            self.dbsql.create_entry(spec)
         
        
    def generate(self, session, engine):
        self.dbsql = dbsql(session, engine)
        self.dbsql.create_tables()
        if len(self.dbsql.query_all(dbtypes.Status)) == 0: self.init_statuses()
        if len(self.dbsql.query_all(dbtypes.Specializaion)) == 0: self.init_specials()
        if len(self.dbsql.query_all(dbtypes.Campus)) == 0: self.init_campuses()
        if len(self.dbsql.query_all(dbtypes.Building)) == 0: self.init_buildings()
        if len(self.dbsql.query_all(dbtypes.Room)) == 0: self.gen_rooms()   
        if len(self.dbsql.query_all(dbtypes.User)) == 0: self.gen_user()
        if len(self.dbsql.query_all(dbtypes.Worker)) == 0: self.gen_worker()
        if len(self.dbsql.query_all(dbtypes.Request)) == 0: self.gen_request()
        temp = self.dbsql.query_all(dbtypes.Status)[0]
        temp.status = "fart"
        self.dbsql.update_entry(temp)

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
gendb().generate(session, engine)
        