import time

class Status:
    def __init__(self, status:str, description:str=None):
        self.id = -1
        self.status = status
        self.description = description
        
class Campus:
    def __init__(self, name:str, address:str, code=None):
        self.id = -1
        self.name = name
        self.address = address
        self.code = code
        
class Building:
    def __init__(self, campus:Campus, address:str, name:str=None):
        self.id = -1
        self.campus = campus
        self.address = address
        self.name = name

class Room:
    def __init__(self, building:Building, name:str=None, type:str=None):
        self.id = -1
        self.building = building
        self.name = name
        self.type = type

class User:
    def __init__(self, email:str, firstname:str=None, lastname:str=None):
        self.id = -1
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        
class Worker:
    def __init__(self, email:str, firstname:str=None, lastname:str=None, specialization:str=None, campus:Campus=None):
        self.id = -1
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.specialization = specialization
        self.primary_campus = campus
        
class Request:
    def __init__(self, status:Status, user:User, reqtime:time, assignee:Worker=None, description:str=None, comptime:time=None, room:Room=None):
        self.id = -1
        self.status = status
        self.user = user
        self.reqtime = reqtime
        self.assignee = assignee
        self.description = description
        self.comptime = comptime
        self.room = room
        