from typing import Union
import dbtypes
from sqlalchemy.sql import text
from sqlalchemy import Engine
from sqlalchemy.orm import Session

class dbsql():
    def __init__(self, session:Session, engine:Engine):
        self.session = session
        self.engine = engine
    
    # Accepts class type and string input
    def query_all(self, cls: Union[dbtypes.Mixin, str]):
        attrs = dict()
        keys = ""
        colkeys = ""
        
        for k in cls.__mapper__.columns.keys():
            attrs[k] = getattr(cls, k)
            keys = keys + k + ", "
            colkeys = colkeys + ":" + k + ", "
            
        with self.engine.connect() as con:
            statement = text(""f"SELECT * FROM {cls.__tablename__ if type(cls) is not str else cls}""")
            rs = con.execute(statement)
            
            if rs is None:
                return []

            found = list()
            for tup in rs:
                temp = cls()
                
                for i in range(len(list(attrs.keys()))):
                    key = list(attrs.keys())[i]
                    setattr(temp, key, tup[i])
                
                found.append(temp)
                
            return found
        
    # Get all from cls where case
    def query_where(self, cls: Union[dbtypes.Mixin, str], where: str):
        attrs = dict()
        
        for k in cls.__mapper__.columns.keys():
            attrs[k] = getattr(cls, k)
            
        with self.engine.connect() as con:
            statement = text(""f"SELECT * FROM {cls.__tablename__ if type(cls) is not str else cls} WHERE {where}""")
            rs = con.execute(statement)
            
            if rs is None:
                return []

            found = list()
            for tup in rs:
                temp = cls()
                
                for i in range(len(list(attrs.keys()))):
                    key = list(attrs.keys())[i]
                    setattr(temp, key, tup[i])
                
                found.append(temp)
            return found
        
    def create_entry(self, data: dbtypes.Mixin):
        attrs = dict()
        keys = ""
        colkeys = ""
        for k in data.__mapper__.columns.keys():
            attrs[k] = getattr(data, k)
            keys = keys + k + ", "
            colkeys = colkeys + ":" + k + ", "
        
        with self.engine.connect() as con:
            statement = text(""f"INSERT INTO {data.__tablename__}({keys[:-2]}) VALUES({colkeys[:-2]})""")
            con.execute(statement, attrs)
            con.commit()
                
    def update_entry(self, data: dbtypes.Mixin):
        attrs = dict()
        values = ""
        for k in data.__mapper__.columns.keys():
            val = getattr(data, k)
            attrs[k] = getattr(data, k)
            values = values + k + "=" + " :" + k + ", "
            
        with self.engine.connect() as con:
                statement = text(""f"UPDATE {data.__tablename__} SET {values[:-2]} WHERE ID={data.id}""")
                print(statement)
                con.execute(statement, attrs)
                con.commit()
                
    def delete_entry(self, data: dbtypes.Mixin):
        with self.engine.connect() as con:
            statement = text(""f"DELETE FROM {data.__tablename__} WHERE id=\'{data.id}\'""")
            con.execute(statement)
            con.commit()

            
    def create_tables(self):        
        for clas in self.classes:
            with self.engine.connect() as con:
                statement = text(""f"CREATE TABLE {clas.__tablename__} (""")
                # con.execute(statement)
                # con.commit()