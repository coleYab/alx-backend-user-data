#!/usr/bin/env python3
"""
users for our auth system
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    """ User class impl by orm master
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(250))
    hashed_password = Column(String(250))
    session_id = Column(String(250))
    reset_token = Column(String(250))

    def __repr__(self) -> str:
        """
        generating string representaiton for debugging
        """
        return f"User<id: {self.id}, email: {self.email}, hashed_password: {self.hashed_password}>"


