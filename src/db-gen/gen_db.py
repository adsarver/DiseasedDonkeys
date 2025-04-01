import random
import time
import src.gui.types as dbtypes

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
            NAMES = file.readlines(-1)
            
            
    def gen_workers(self, special:dbtypes.Specializaion):
        first, last = random.randint(0, len(self.NAMES)), random.randint(0, len(self.NAMES))
        firstname, lastname = self.NAMES[first], self.NAMES[last]
        email = firstname[0] + lastname[0:3] + str(first) + "@email.com"
        campus = self.BUILDINGS.keys[random.randint(0,2)]
        
        return dbtypes.Worker(email, firstname, lastname, special, campus)

    def gen_users(self):
        first, last = random.randint(0, len(self.NAMES)), random.randint(0, len(self.NAMES))
        firstname, lastname = self.NAMES[first], self.NAMES[last]
        email = firstname[0] + lastname[0:3] + str(first) + "@email.com"
        
        return dbtypes.User(email, firstname, lastname)

    def gen_requests(self, user:dbtypes.User, worker:dbtypes.Worker, room:dbtypes.Room):
        status = dbtypes.Status(self.STATUS[random.randint(0, 2)])
        
        return dbtypes.Request(status, user, time.time(), worker, room=room) # TODO: Change time
    
    def gen_rooms(self):
        room_num = random.randint(100,500)
        campus = self.BUILDINGS.keys[random.randint(0,2)]
        possible_buildings = self.BUILDINGS[campus]
        building = possible_buildings[random.randInit(0,len(possible_buildings))]
        return dbtypes.Room(building, room_num)
    
    def init_campuses(self):
        campuses = []
        buildings = []
        
        for campus in self.BUILDINGS.keys():
            address = str(random.randint(1, 2000)) + " " + self.ADDRESS
            campus = dbtypes.Campus(campus, address)
            campuses.append(campus)
            
            for name in self.BUILDINGS[campus]:
                building = dbtypes.Building(campus, address, name)
                buildings.append(building)

        return {"campuses":campuses, "buildings":buildings}
    
    def init_statuses(self):
        return [dbtypes.Status(name) for name in self.STATUS]
    
    def init_specials(self):
        return [dbtypes.Specializaion(name) for name in self.SPECIALIZATIONS]
            