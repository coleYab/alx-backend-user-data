#!/usr/bin/env python3
"""
a simple implementation of auth
"""
from bcrypt import hashpw, gensalt, checkpw
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4

from db import DB
from user import User


def _generate_uuid() -> str:
    """ _generate_uuid: generate a unique identifiers
    """
    return str(uuid4())


def _hash_password(password: str) -> str:
    """
    _hash_password: hashes password with bcrypt
    """
    passwd = password.encode('utf-8')
    return hashpw(passwd, gensalt())


class Auth:
    """ Auth class to interact with the authentication database
    """

    def __init__(self):
        """ constructor """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        register_user: registers a new user to the service
        """
        if not isinstance(email, str):
            raise TypeError("email has to be a string")
        if not isinstance(password, str):
            raise TypeError("password has to be a string")
        hashed_password = _hash_password(password)

        try:
            u = self._db.find_user_by(email=email)
            if u is not None:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            pass

        return self._db.add_user(email, str(hashed_password))

    def valid_login(self, email: str, password: str) -> bool:
        """ valid_login: validtes login for the user
        """
        user = None
        try:
            user = self._db.find_user_by(email=email)
            encoded_pwd = user.hashed_password[2:-1].encode('utf-8')
            return checkpw(password.encode('utf-8'), encoded_pwd)
        except Exception as e:
            return False

        return False

    def destroy_session(self, user_id: int) -> None:
        """
        removes an authorized user session
        """
        if user_id is None or not isinstance(user_id, int):
            return

        self._db.update_user(user_id, session_id=None)

    def get_user_from_session_id(self, session_id: str) -> str:
        """
        retriving a user from given session id
        """
        if session_id is None:
            return None

        try:
            return self._db.find_user_by(session_id=session_id)
        except Exception as e:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """
        get_reset_password_token: this will return password token
        """
        user = self._db.find_user_by(email=email)
        if user is None:
            return ValueError("User don't found")

        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """
        update_password: updates user password pointed by this reset_token
        """
        user = self._db.find_user_by(reset_token=reset_token)
        if user is None:
            raise ValueError("User doesn't found")

        pwd = _hash_password(password)
        self._db.update_user(
                                user.id, hashed_password=pwd,
                                reset_token=None
                                )

    def create_session(self, email: str) -> str:
        """
        create a session for a user and returns the session id
        """
        try:
            session_id = _generate_uuid()
            user = self._db.find_user_by(email=email)
            assert user is not None
            self._db.update_user(user.id, session_id=session_id)
        except Exception as e:
            return None

        return session_id
