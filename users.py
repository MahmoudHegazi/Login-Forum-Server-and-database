import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable=False)


class Info(Base):
    __tablename__ = 'info'

    user = Column(Integer, nullable=False, primary_key=True)
    password = Column(String(50), nullable=False, primary_key=True)    
    email = Column(String(70))
    birthdate = Column(String(12))
    user_id = Column(Integer, ForeignKey('users.id'))
    users = relationship(Users)

#We added this serialize function to be able to send JSON objects in a serializable format
    @property
    def serialize(self):
       
       return {
           'name'         : self.name,
           'user'         : self.user,
           'id'         : self.id,
           'password'         : self.password,
           'email'         : self.email,
           'birthdate'         : self.birthdate,
       }

engine = create_engine('sqlite:///users.db') 

Base.metadata.create_all(engine)    
    
