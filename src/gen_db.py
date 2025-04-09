import random
from datetime import datetime

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
        campuses = self.session.query(dbtypes.Campus).all()
        speclist = self.session.query(dbtypes.Specializaion).all()
        
        for _ in range(amount):
            first, last = random.randint(0, len(self.NAMES) - 1), random.randint(0, len(self.NAMES) - 1)
            firstname, lastname = self.NAMES[first], self.NAMES[last]
            email = firstname[0] + lastname[0:3] + str(first) + "@email.com"
            campus = campuses[random.randint(0,2)]
            special = speclist[random.randint(0,len(speclist) - 1)]
            
            worker = dbtypes.Worker(email=email, firstname=firstname, lastname=lastname, specialization=special, primary_campus=campus)
            self.session.add(worker)
        self.session.commit()

    def gen_user(self, amount=20):
        print("Generating users...")
        for _ in range(amount):
            first, last = random.randint(0, len(self.NAMES)), random.randint(0, len(self.NAMES))
            firstname, lastname = self.NAMES[first], self.NAMES[last]
            email = firstname[0] + lastname[0:3] + str(first) + "@email.com"
            
            user = dbtypes.User(email=email, firstname=firstname, lastname=lastname)
            self.session.add(user)
        self.session.commit()

    def gen_request(self, amount=50):
        print("Generating requests...")
        for _ in range(amount):
            users = self.session.query(dbtypes.User).all()
            workers = self.session.query(dbtypes.Worker).all()
            rooms = self.session.query(dbtypes.Room).all()
            statuses = self.session.query(dbtypes.Status).all()
            
            status = statuses[random.randint(0, 2)]
            user = users[random.randint(0,len(users) - 1)]
            worker = workers[random.randint(0,len(workers) - 1)]
            room = rooms[random.randint(0,len(rooms) - 1)]
            
            req = dbtypes.Request(status = status, user = user, reqtime=datetime.now(), assignee=worker, room=room)
            self.session.add(req)
        self.session.commit()
        
    
    def gen_rooms(self):
        print("Generating rooms...")
        buildings = self.session.query(dbtypes.Building).all()
        for building in buildings:
            for floor in range(100, 500, 100):
                for roomnum in range(floor, floor + 11):
                    room = dbtypes.Room(building_id=building.id, building=building, name=roomnum)
                    self.session.add(room)
        self.session.commit()            
    
    def init_campuses(self):   
        print("Generating campuses...")     
        for campus in self.BUILDINGS.keys():
            address = str(random.randint(1, 2000)) + " " + self.ADDRESS
            campus = dbtypes.Campus(name=campus, address=address)
            self.session.add(campus)
        self.session.commit()
    
    def init_buildings(self):
        print("Generating buildings...")
        campuses = self.session.query(dbtypes.Campus).all()
        for campus in campuses:            
            for name in self.BUILDINGS[campus.name]:
                address = str(random.randint(1, 2000)) + " " + self.ADDRESS
                building = dbtypes.Building(campus_id=campus.id, campus=campus, address=address, name=name)
                self.session.add(building)
        self.session.commit()
    
    def init_statuses(self):
        print("Generating statuses...")
        for name in self.STATUS:
            status = dbtypes.Status(status=name)
            self.session.add(status)
        self.session.commit()
    
    def init_specials(self):
        print("Generating specializations...")
        for name in self.SPECIALIZATIONS:
            spec = dbtypes.Specializaion(specialization=name)
            self.session.add(spec)
        self.session.commit() 
               
    def generate(self, session):
        self.session = session
        if len(self.session.query(dbtypes.Status).all()) == 0: self.init_statuses()
        if len(self.session.query(dbtypes.Specializaion).all()) == 0: self.init_specials()
        if len(self.session.query(dbtypes.Campus).all()) == 0: self.init_campuses()
        if len(self.session.query(dbtypes.Building).all()) == 0: self.init_buildings()
        if len(self.session.query(dbtypes.Room).all()) == 0: self.gen_rooms()   
        if len(self.session.query(dbtypes.User).all()) == 0: self.gen_user()
        if len(self.session.query(dbtypes.Worker).all()) == 0: self.gen_worker()
        if len(self.session.query(dbtypes.Request).all()) == 0: self.gen_request()

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
gendb().generate(session)
        