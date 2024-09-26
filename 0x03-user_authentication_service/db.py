#!/usr/bin/env python3
"""
Db: class for managing user and their shitty data
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """ DB class
    """

    def __init__(self) -> None:
        """ Initialize new db instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """ Memoized session object
        """
        if self.__session is None:
            DBsession = sessionmaker(bind=self._engine)
            self.__session = DBsession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        add_user: adds a new user to our db
        """
        new_user = User(email=email, hashed_password=hashed_password)
        sess = self._session
        sess.add(new_user)
        sess.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        find_user_by: this will search for user
        """
        user = None
        try:
            session = self._session
            user = session.query(User).filter_by(**kwargs).first()
        except InvalidRequestError:
            raise InvalidRequestError

        if user is None:
            raise NoResultFound

        return user

    def update_user(self, user_id: int, **kwargs: dict) -> None:
        """
        update_user: update user data
        """
        user = None
        try:
            user = self.find_user_by(id=user_id)
        except Exception as e:
            raise ValueError

        for key, val in kwargs.items():
            if key not in user.__dict__:
                raise ValueError("argument mismatch")

        session = self._session
        session.query(User).filter_by(id=user_id).update(kwargs)
        session.commit()
