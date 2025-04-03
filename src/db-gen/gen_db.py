import random
from datetime import datetime
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
        with open("src/db-gen/names.txt") as file:
            self.NAMES = file.readlines(-1)
            
            
    def gen_worker(self, speclist:list):
        first, last = random.randint(0, len(self.NAMES) - 1), random.randint(0, len(self.NAMES) - 1)
        firstname, lastname = self.NAMES[first], self.NAMES[last]
        email = firstname[0] + lastname[0:3] + str(first) + "@email.com"
        campus = list(self.BUILDINGS.keys())[random.randint(0,2)]
        special = speclist[random.randint(0,len(speclist) - 1)]
        
        return dbtypes.Worker(email, firstname, lastname, special, campus)

    def gen_user(self):
        first, last = random.randint(0, len(self.NAMES)), random.randint(0, len(self.NAMES))
        firstname, lastname = self.NAMES[first], self.NAMES[last]
        email = firstname[0] + lastname[0:3] + str(first) + "@email.com"
        
        return dbtypes.User(email, firstname, lastname)

    def gen_request(self, userlist:dbtypes.User, workerlist:dbtypes.Worker, roomlist:dbtypes.Room):
        status = dbtypes.Status(self.STATUS[random.randint(0, 2)])
        user = userlist[random.randint(0,len(userlist) - 1)]
        worker = workerlist[random.randint(0,len(workerlist) - 1)]
        room = roomlist[random.randint(0,len(roomlist) - 1)]
        return dbtypes.Request(status, user, datetime.now(), worker, room=room) # TODO: Change time
    
    def gen_rooms(self, buildings):
        rooms = {}
        for building in buildings:
            for roomnum in range(100, 411):
                if roomnum > 110 and roomnum > 210 and roomnum > 310 and roomnum > 410:
                    continue
                
                rooms[building.name] = dbtypes.Room(building, roomnum)
            
        return rooms
    
    def init_campuses(self):
        campuses = []
        buildings = []
        
        for campus in self.BUILDINGS.keys():
            address = str(random.randint(1, 2000)) + " " + self.ADDRESS
            campus = dbtypes.Campus(campus, address)
            campuses.append(campus)
            
            for name in self.BUILDINGS[campus.name]:
                building = dbtypes.Building(campus, address, name)
                buildings.append(building)

        return {"campus":campuses, "building": buildings}
    
    def init_statuses(self):
        return [dbtypes.Status(name) for name in self.STATUS]
    
    def init_specials(self):
        return [dbtypes.Specializaion(name) for name in self.SPECIALIZATIONS]
            
    def generate(self):
        status = self.init_statuses()
        special = self.init_specials()
        campus_map = self.init_campuses()
        rooms = self.gen_rooms(campus_map["building"])
        users = []
        workers = []
        requests = []
                
        for i in range(20):
            users.append(self.gen_user())
            workers.append(self.gen_worker(special))
            
        for i in range(50):
            requests.append(self.gen_request(users, workers, list(rooms.values())))
        
        
        print(status[0])
        print(special[0])
        print(campus_map["campus"][0])
        print(campus_map["building"][0])
        print(list(rooms.values())[0])
        print(users[0])
        print(workers[0])
        print(requests[0])

db = gendb()
db.generate()