from sqlalchemy import Column, Integer, ForeignKey, DateTime, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Mixin:
    def __repr__(self):
        package = self.__class__.__module__
        class_ = self.__class__.__name__
        attrs = sorted((k, getattr(self, k)) for k in self.__mapper__.columns.keys())
        sattrs = ', '.join(f'{key}={value!r}' for key, value in attrs)
        return f'{package}.{class_}({sattrs})'
    
    def __str__(self):
        class_ = self.__class__.__name__
        attrs = dict()
        for k in self.__mapper__.columns.keys():
            attrs[k] = getattr(self, k)

        Text = f"| {class_}:\n"
        for key, value in attrs.items():
            if key == "firstname":
                Text += f"| \tName: {attrs['lastname'].capitalize().rstrip()}, {value.capitalize().rstrip()}\n"
                continue
            elif key == "lastname":
                continue
            elif key == "status" and value is None:
                Text += f"| \tCompleted on: {attrs['status']}\n"
                continue
            elif key == "comptime" and value is not None: 
                comptime = value.strftime("%A %d/%m/%Y at %H:%M:%S")
                Text += f"| \tCompleted on: {comptime}\n"
                continue
            
            Text += f"| \t{key.capitalize()}: {value}\n"
        
        return Text
            
        

class Specialization(Mixin, Base):
    __tablename__ = "specialization"
    id = Column(Integer, primary_key=True)
    specialization = Column(Text)
    description = Column(Text, nullable=True)
    workers = relationship("Worker", backref="specialization")
    __table_args__ = tuple(UniqueConstraint("specialization"))

class Status(Mixin, Base):
    __tablename__ = "status"
    id = Column(Integer, primary_key=True)
    status = Column(Text)
    description = Column(Text, nullable=True)
    requests = relationship("Request", backref="status")
    __table_args__ = tuple(UniqueConstraint("status"))
        
class Campus(Mixin, Base):
    __tablename__ = "campus"
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    address = Column(Text)
    code = Column(Text, nullable=True)
    buildings = relationship("Building", backref="campus")
    workers = relationship("Worker", backref="primary_campus")
    __table_args__ = tuple(UniqueConstraint("name"))
        
class Building(Mixin, Base):
    __tablename__ = "building"
    id = Column(Integer, primary_key=True)
    campus_id = Column(Integer, ForeignKey('campus.id'))
    name = Column(Text, nullable=True)
    address = Column(Text)
    rooms = relationship("Room", backref="building")
    __table_args__ = tuple(UniqueConstraint("name"))

class Room(Mixin, Base):
    __tablename__ = "room"
    id = Column(Integer, primary_key=True)
    building_id = Column(Integer, ForeignKey('building.id'))
    name = Column(Text, nullable=True)
    type = Column(Text, nullable=True)
    requests = relationship("Request", backref="room")
    __table_args__ = tuple(UniqueConstraint("building_id", "name"))
    
class User(Mixin, Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    email = Column(Text)
    firstname = Column(Text, nullable=True)
    lastname = Column(Text, nullable=True)
    requests = relationship("Request", backref="user")
        
class Worker(Mixin, Base):
    __tablename__ = "worker"
    id = Column(Integer, primary_key=True)
    email = Column(Text)
    firstname = Column(Text, nullable=True)
    lastname = Column(Text, nullable=True)
    specialization_id = Column(Integer, ForeignKey('specialization.id'), nullable=True)
    campus_id = Column(Integer, ForeignKey('campus.id'), nullable=True)
    assignments = relationship("Request", backref="worker")
        
class Request(Mixin, Base):
    __tablename__ = "request"
    id = Column(Integer, primary_key=True)
    status_id = Column(Integer, ForeignKey('status.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    reqtime = Column(DateTime)
    worker_id = Column(Integer, ForeignKey("worker.id"))
    description = Column(Text, nullable=True)
    comptime = Column(DateTime, nullable=True)
    room_id = Column(Integer, ForeignKey("room.id"))