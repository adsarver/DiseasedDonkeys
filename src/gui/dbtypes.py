from datetime import datetime

class Specializaion:
    def __init__(self, specialization:str, description:str=None):
        self.id = -1
        self.specialization = specialization.rstrip()
        if description is not None: self.description = description.rstrip()
        else: self.description = "None"
        
    def __str__(self):
        string =   "| Specialization\n"
        string += f"| \tID: {self.id}\n"
        string += f"| \tSpecialization: {self.specialization}\n"
        string += f"| \tDescription: {self.description}\n"
        return string

class Status:
    def __init__(self, status:str, description:str=None):
        self.id = -1
        self.status = status
        if description is not None: self.description = description.rstrip()
        else: self.description = "None"
        
    def __str__(self):
        string =   "| Status\n"
        string += f"| \tID: {self.id}\n"
        string += f"| \tStatus: {self.status}\n"
        string += f"| \tDescription: {self.description}\n"
        return string
        
class Campus:
    def __init__(self, name:str, address:str, code=None):
        self.id = -1
        self.name = name.rstrip()
        self.address = address.rstrip()
        self.code = code
        
    def __str__(self):
        string =   "| Campus\n"
        string += f"| \tID: {self.id}\n"
        string += f"| \tName: {self.name}\n"
        string += f"| \tCode: {self.code}\n"
        string += f"| \tAddress: {self.address}\n"
        return string
        
class Building:
    def __init__(self, campus:Campus, address:str, name:str=None):
        self.id = -1
        self.campus = campus
        self.address = address.rstrip()
        self.name = name.rstrip()
        
    def __str__(self):
        string =   "| Building\n"
        string += f"| \tID: {self.id}\n"
        string += f"| \tName: {self.name}\n"
        string += f"| \tCampus: {self.campus.name}\n"
        string += f"| \tAddress: {self.address}\n"
        return string

class Room:
    def __init__(self, building:Building, name:str=None, type:str=None):
        self.id = -1
        self.building = building
        self.name = name.rstrip()
        self.type = type.rstrip()
        
    def __str__(self):
        string =   "| Room\n"
        string += f"| \tID: {self.id}\n"
        string += f"| \tName: {self.name}\n"
        string += f"| \tBuilding: {self.building.name}\n"
        string += f"| \tType: {self.type}\n"
        return string

class User:
    def __init__(self, email:str, firstname:str=None, lastname:str=None):
        self.id = -1
        self.email = email.rstrip()
        self.firstname = firstname.rstrip()
        self.lastname = lastname.rstrip()
        
    def getname(self):
        return f"{self.lastname.capitalize()}, {self.firstname.capitalize()}"
    
    def __str__(self):
        string =   "| User\n"
        string += f"| \tID: {self.id}\n"
        string += f"| \tName: {self.lastname.capitalize()}, {self.firstname.capitalize()}\n"
        string += f"| \tEmail: {self.email}\n"
        return string
        
class Worker:
    def __init__(self, email:str, firstname:str=None, lastname:str=None, specialization:Specializaion=None, campus:Campus=None):
        self.id = -1
        self.email = email.rstrip()
        self.firstname = firstname.rstrip()
        self.lastname = lastname.rstrip()
        self.specialization = specialization
        self.primary_campus = campus
        
    def getname(self):
        return f"{self.lastname.capitalize()}, {self.firstname.capitalize()}"
        
    def __str__(self):
        string =   "| Worker\n"
        string += f"| \tID: {self.id}\n"
        string += f"| \tName: {self.lastname.capitalize()}, {self.firstname.capitalize()}\n"
        string += f"| \tEmail: {self.email}\n"
        string += f"| \tSpecialization: {self.specialization.specialization}\n"
        string += f"| \tPrimary Campus: {self.primary_campus}\n"
        return string
        
class Request:
    def __init__(self, status:Status, user:User, reqtime:datetime, assignee:Worker=None, description:str=None, comptime:datetime=None, room:Room=None):
        self.id = -1
        self.status = status
        self.user = user
        self.reqtime = reqtime
        self.assignee = assignee
        self.description = description.rstrip()
        self.comptime = comptime
        self.room = room
        
    def __str__(self):
        reqtime = self.reqtime.strftime("%A %d/%m/%Y at %H:%M:%S")
        string =   "| Request\n"
        string += f"| \tID: {self.id}\n"
        string += f"| \tStatus: {self.status.status}\n"
        string += f"| \tRequester: {self.user.getname()}\n"
        string += f"| \tAssignee: {self.assignee.getname()}\n"
        string += f"| \tRoom: {self.room.name}\n"
        string += f"| \tDescription: {self.description}\n"
        string += f"| \tRequested on: {reqtime}\n"
        if self.comptime is None: 
            string += f"| \tCompleted on: {self.status.status}\n"
        if self.comptime is not None: 
            comptime = self.comptime.strftime("%A %d/%m/%Y at %H:%M:%S")
            string += f"| \tCompleted on: {comptime}\n"
        return string
        