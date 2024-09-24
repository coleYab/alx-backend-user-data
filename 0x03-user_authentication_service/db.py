#!/usr/bin/env python3
"""
Db: class for managing users and their shitty data
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from typing import TypeVar

from user import Base, User


class DB:
    """ DB class
    """

    def __init__(self) -> None:
        """ Initialize new db instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def session(self) -> Session:
        """ Memoized session object
        """
        if self.__session is None:
            DBsession = sessionmaker(bind=self._engine)
            self.__session = DBsession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> TypeVar('User'):
        new_user = User(email=email, hashed_password=hashed_password)
        sess = self.session
        sess.close_on_commit = False
        sess.add(new_user)
        sess.commit()
        return new_user

